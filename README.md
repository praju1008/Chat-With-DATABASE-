# Chat with SQL Database 🗨️🗄️ — Natural Language Query Tool

A Streamlit + LangChain application that lets users ask questions about their database in plain English — no SQL knowledge required. The app converts natural language into safe, schema-aware SQL queries and returns summarized, easy-to-understand results.

---

## 🔗 Live Demo & Repository

- **GitHub:** https://github.com/praju1008/Chat-With-DATABASE-
- **Live Demo:** _Add your deployed link here if hosted (e.g. Streamlit Cloud)_

---

## 📌 About the Project

Chat with SQL Database bridges the gap between non-technical users and structured data. Instead of writing SQL manually, users simply type a question in plain English (e.g. "Show me all customers who ordered last month"), and the app translates it into an accurate SQL query, executes it safely, and returns the results in a readable format.

Built with schema-aware prompting, the tool understands the structure of the connected database (MySQL/SQLite) and generates queries that respect that schema — while strictly preventing destructive operations like DELETE or DROP.

---

## ✨ Features

- 💬 **Natural Language to SQL** — Ask questions in plain English, get accurate SQL queries
- 🧠 **Schema-Aware Prompting** — LangChain understands your database structure for accurate query generation
- 🔒 **Safe, Read-Only Queries** — Built-in safeguards prevent destructive operations (no DELETE/DROP/UPDATE)
- ⚡ **Instant Results** — Queries execute directly on MySQL/SQLite and return summarized insights
- 🖥️ **Simple Streamlit UI** — Clean, no-code interface for querying data
- ⚠️ **Error Handling** — Gracefully handles invalid or ambiguous queries with helpful feedback

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend/UI | Streamlit |
| AI/LLM Framework | LangChain |
| Database | MySQL / SQLite |
| Language | Python |

---

## 📂 Project Structure

```
Chat-With-DATABASE/
├── app.py                # Main Streamlit application
├── utils/
│   ├── db_connector.py   # Database connection handling
│   ├── query_generator.py # LangChain prompt + SQL generation logic
│   └── safety_checks.py  # Read-only / non-destructive query validation
├── requirements.txt
└── README.md
```

*(Adjust the structure above to match your actual file layout if it differs.)*

---

## ⚙️ Getting Started

### Prerequisites
- Python 3.9 or later
- pip
- A MySQL or SQLite database to connect to
- An LLM API key (e.g. OpenAI) if required by your LangChain setup

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/praju1008/Chat-With-DATABASE-.git
cd Chat-With-DATABASE-
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**

Create a `.env` file in the root folder:
```
DATABASE_URL=your_database_connection_string
OPENAI_API_KEY=your_api_key_here
```

4. **Run the app**
```bash
streamlit run app.py
```

5. **Open the app**
Visit `http://localhost:8501` in your browser.

---

## 🔑 Environment Variables

| Variable | Description |
|---|---|
| `DATABASE_URL` | Connection string for your MySQL/SQLite database |
| `OPENAI_API_KEY` | API key for the LLM used by LangChain |

---
## 🚀 Future Improvements

- Support for additional databases (PostgreSQL, MongoDB)
- Query history and saved queries
- Data visualization for query results (charts/graphs)
- Multi-turn conversational context for follow-up questions
- Export results to CSV/Excel

---

## 👤 Author

**Prajwal Mathapati**
Full-Stack Web Developer | MERN Stack
📧 mathapatipraju1008@gmail.com
🔗 [LinkedIn](https://www.linkedin.com/in/prajwal-m-3263b11b0/) | [GitHub](https://github.com/praju1008)

---

## 📄 License

This project is open source and available for educational purposes.
