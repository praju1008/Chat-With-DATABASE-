import streamlit as st
from pathlib import Path
import sqlite3
from urllib.parse import quote_plus
from sqlalchemy import create_engine

from langchain_community.utilities import SQLDatabase
from langchain_groq import ChatGroq


# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Chat with SQL Database", page_icon=":robot:")
st.title("Chat with SQL Database :robot:")

# ---------- DB CHOICE ----------
LOCAL_SQLITE = "LOCAL_SQLITE"
LOCAL_MYSQL = "LOCAL_MYSQL"
SERVER_MYSQL = "SERVER_MYSQL"

db_mode_opt = ["Use Local SQLite DB", "Use Local MySQL DB", "Use Server MySQL DB"]
db_mode = st.sidebar.radio("Choose the database type", db_mode_opt)

db_uri = None
mysql_host = mysql_user = mysql_password = mysql_db_name = None

if db_mode_opt.index(db_mode) == 0:
    db_uri = LOCAL_SQLITE
elif db_mode_opt.index(db_mode) == 1:
    db_uri = LOCAL_MYSQL
    st.sidebar.subheader("Local MySQL Settings")
    mysql_host = st.sidebar.text_input("Local MySQL Host", value="localhost")
    mysql_user = st.sidebar.text_input("Local MySQL User")
    mysql_password = st.sidebar.text_input("Local MySQL Password", type="password")
    mysql_db_name = st.sidebar.text_input("Local MySQL Database Name")
else:
    db_uri = SERVER_MYSQL
    st.sidebar.subheader("Server MySQL Settings")
    mysql_host = st.sidebar.text_input("Server MySQL Host (domain or IP)")
    mysql_user = st.sidebar.text_input("Server MySQL User")
    mysql_password = st.sidebar.text_input("Server MySQL Password", type="password")
    mysql_db_name = st.sidebar.text_input("Server MySQL Database Name")

# ---------- API KEY ----------
api_key = st.sidebar.text_input("Enter your Groq API Key", type="password")
if not api_key:
    st.warning("Please enter your Groq API Key to proceed.")
    st.stop()

llm = ChatGroq(
    groq_api_key=api_key,
    model_name="llama-3.1-8b-instant",
    streaming=False,
)


# ---------- DB CONFIG ----------
@st.cache_resource(ttl="2h")
def configure_db(db_uri, mysql_host=None, mysql_user=None, mysql_password=None, mysql_db_name=None):
    if db_uri == LOCAL_SQLITE:
        dbpath = (Path(__file__).parent / "Student.db").absolute()
        if not dbpath.exists():
            raise FileNotFoundError(f"SQLite DB not found: {dbpath}")
        creator = lambda: sqlite3.connect(f"file:{dbpath}?mode=ro", uri=True)
        engine = create_engine("sqlite://", creator=creator)
        return SQLDatabase(engine)

    if db_uri in (LOCAL_MYSQL, SERVER_MYSQL):
        if not (mysql_host and mysql_user and mysql_password and mysql_db_name):
            raise ValueError("All MySQL connection details are required.")
        safe_pwd = quote_plus(mysql_password)
        engine = create_engine(
            f"mysql+mysqlconnector://{mysql_user}:{safe_pwd}@{mysql_host}/{mysql_db_name}"
        )
        return SQLDatabase(engine)

    raise ValueError(f"Unknown db_uri: {db_uri}")


try:
    db = configure_db(db_uri, mysql_host, mysql_user, mysql_password, mysql_db_name)
except Exception as e:
    st.error(f"Error connecting to database: {e}")
    st.stop()


# ---------- SQL GENERATION ----------
def generate_sql(question: str, db: SQLDatabase, llm: ChatGroq) -> str:
    dialect = db.dialect
    tables = ", ".join(db.get_usable_table_names())
    schema = db.get_table_info()

    prompt = f"""
You are an expert SQL assistant.

Database dialect: {dialect}
Available tables: {tables}

Database schema:
{schema}

Rules:
- Use ONLY columns and tables that exist in the schema.
- If the user asks something unclear or unrelated, still write a valid SQL query
  that returns some reasonable data (for example, SELECT * from a relevant table).
- Write ONE SQL query that best answers the user question.
- Do NOT return any natural-language message inside SQL.
- Return ONLY the SQL, no explanation, no backticks.

User question: {question}
"""

    resp = llm.invoke(prompt)
    sql_text = getattr(resp, "content", str(resp)).strip()
    sql_text = sql_text.replace("``````", "").strip()
    return sql_text


def is_generic_sql(sql: str) -> bool:
    """Detect obviously vague queries like plain SELECT * FROM ..."""
    s = sql.strip().lower()
    return s.startswith("select * from") and " where " not in s


# ---------- CHAT UI ----------
if "messages" not in st.session_state or st.sidebar.button("Clear Chat history"):
    st.session_state["messages"] = [
        {
            "role": "assistant",
            "content": "Ask something about your database (e.g., 'Show all records from STUDENT').",
        }
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

user_query = st.chat_input("Ask anything about the database...")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)

    response_placeholder = st.chat_message("assistant")

    with st.spinner("Generating SQL and running it..."):
        try:
            # 1) Very short / unclear input → warn only
            if len(user_query.strip()) < 3:
                full_response = (
                    "Warning: Your question is too short or unclear.\n\n"
                    "Please ask something more specific, e.g. "
                    "'Show all users' or 'Show users where email contains gmail.com'."
                )
            else:
                # 2) Generate SQL
                sql = generate_sql(user_query, db, llm)

                # 3) Always run SQL, but add note if it's generic
                result = db.run(sql)

                if is_generic_sql(sql):
                    note = (
                        "Note: Your question is quite vague, so I ran a generic query.\n"
                        "For more precise results, mention columns or conditions.\n\n"
                    )
                else:
                    note = ""

                full_response = f"{note}Generated SQL:\n{sql}\n\nResult:\n{result}"
        except Exception as e:
            full_response = f"Error: {e}"

    response_placeholder.write(full_response)
    st.session_state.messages.append(
        {"role": "assistant", "content": full_response}
    )
