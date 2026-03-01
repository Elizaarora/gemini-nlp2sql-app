# 🎓 NLQ — Natural Language SQL Query App

A web app that lets you query a student database using **plain English**. No SQL knowledge needed. Powered by **Google Gemini AI** — just type your question and get a friendly, human-readable answer.

---

## 🚀 Live Demo

> Type: *"Who scored the highest marks?"*
> App runs: `SELECT * FROM STUDENT ORDER BY MARKS DESC LIMIT 1;`
> You see: *"Sara scored the highest with 95 marks in the AI class, Section A."*

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| [Streamlit](https://streamlit.io/) | Web UI |
| [Google Gemini 2.5 Flash](https://aistudio.google.com/) | English → SQL + Natural language responses |
| [SQLite](https://www.sqlite.org/) | Local database |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | API key management |

---

## 📁 Project Structure

```
nlq/
│
├── app.py              # Main Streamlit application
├── sql.py              # Database setup script (run once)
├── requirements.txt    # Python dependencies
├── .env                # Your secret API key (create manually, never push to GitHub)
├── .gitignore          # Keeps venv, .env, student.db out of Git
└── student.db          # Auto-generated SQLite database
```

---

## 🗄️ Database Schema

Table: `STUDENT`

| Column | Type | Example |
|--------|------|---------|
| NAME | VARCHAR(25) | Rachel |
| CLASS | VARCHAR(25) | AI |
| SECTION | VARCHAR(25) | B |
| MARKS | INT | 71 |

### Sample Data

| NAME | CLASS | SECTION | MARKS |
|------|-------|---------|-------|
| Krish | Data Science | A | 90 |
| John | Machine Learning | B | 85 |
| Ben | DEVOPS | A | 70 |
| Rachel | AI | B | 71 |
| Sara | AI | A | 95 |

---

## ⚙️ Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/nlq.git
cd nlq
```

### 2. Create & Activate Virtual Environment

```bash
python -m venv venv
```

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Get Your Google Gemini API Key

1. Go to [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. Click **Create API Key**
3. Copy the key

### 5. Create `.env` File

In the project root, create a file named `.env`:

```
GOOGLE_API_KEY=your_actual_api_key_here
```

> ⚠️ Never share or push this file. It's already in `.gitignore`.

### 6. Create the Database (One Time Only)

```bash
python sql.py
```

### 7. Run the App

```bash
streamlit run app.py
```

Opens at `http://localhost:8501`

---

## 💬 Example Questions

```
How many students are there?
Show all students in the AI class.
Who scored the highest marks?
List all students in section A.
How many students named Rachel?
Show students in data science class.
Who scored less than 80?
```

---

## 🔍 How It Works

```
You type a question
       ↓
Gemini AI converts it to SQL
       ↓
SQL runs on student.db
       ↓
Raw results sent back to Gemini
       ↓
Gemini writes a friendly human answer
       ↓
Answer shown on screen
```

### Smart Name Matching
- Small typos are handled: `"rachell"` → matches `Rachel`
- Very different names are not guessed: `"racheajj"` → returns no results
- Class names support partial match: `"data sci"` → matches `Data Science`

---

## 📦 Requirements

```
streamlit
google-generativeai
python-dotenv
```

---

## ⚠️ Common Issues

| Problem | Fix |
|---|---|
| `quota exceeded` error | You hit Gemini free tier limit. Wait or use a different API key |
| `ModuleNotFoundError` | Make sure venv is active, run `pip install -r requirements.txt` |
| Wrong student count | You ran `sql.py` multiple times. Uncomment `DELETE FROM STUDENT` in sql.py, run it once, then comment it back |
| `.env` not loading | Make sure `.env` is in the root project folder, not inside any subfolder |

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙌 Built With

- [Google Gemini](https://deepmind.google/technologies/gemini/)
- [Streamlit](https://streamlit.io/)
