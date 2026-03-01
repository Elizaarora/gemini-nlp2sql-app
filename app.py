# from dotenv import load_dotenv
# load_dotenv()  ## load all the environment variables

# import streamlit as st
# import os
# import sqlite3

# import google.generativeai as genai

# ## Configure our API key
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# # Function to Load Google Gemini Model and provide SQL query
# def get_gemini_response(question, prompt):
#     model = genai.GenerativeModel("gemini-2.5-flash")
#     response = model.generate_content([prompt[0], question])
#     return response.text

# def read_sql_query(sql,db):
#     conn=sqlite3.connect(db)
#     cur=conn.cursor()
#     cur.execute(sql)
#     rows=cur.fetchall()
#     conn.commit()
#     conn.close()
#     for row in rows:
#         print(row)
#     return rows

# ## Define Your Prompt
# prompt = [
#     """
#     You are an expert in converting plain English questions into accurate SQL queries.
#     The database table name is STUDENT and it has these columns: NAME, CLASS, SECTION, and MARKS.

#     IMPORTANT RULES:
#     - Always return the full and correct SQL query.
#     - Do not add any unnecessary filters or conditions unless they are clearly mentioned in the question.
#     - When asked for all students, select all matching records from the STUDENT table without filtering.
#     - Output must only be the SQL query itself, no extra text, no ``` and no 'sql' word.

#     EXAMPLES:
#     Q: How many entries of records are present?
#     A: SELECT COUNT(*) FROM STUDENT;

#     Q: Tell me all the students studying in Data Science class.
#     A: SELECT * FROM STUDENT WHERE CLASS = "Data Science";

#     Q: Name of all the students.
#     A: SELECT NAME FROM STUDENT;
#     """
# ]


# ## Streamlit App

# st.set_page_config(page_title="I can Retrieve Any SQL query")
# st.header("Gemini App To Retrieve SQL Data")

# question=st.text_input("Input: ",key="input")

# submit=st.button("Ask the question")

# # if submit is clicked
# if submit:
#     response=get_gemini_response(question,prompt)
#     print(response)
#     response=read_sql_query(response,"student.db")
#     st.subheader("The Response is")
#     for row in response:
#         print(row)
#         st.header(row)



from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import sqlite3
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(question, prompt):
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content([prompt[0], question])
    return response.text.strip()

def read_sql_query(sql, db):
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        col_names = [description[0] for description in cur.description] if cur.description else []
        conn.close()
        return rows, col_names
    except Exception as e:
        return None, str(e)

def format_response(rows, col_names, question):
    """Use Gemini to convert raw SQL results into natural language"""
    if rows is None:
        return "Sorry, I couldn't understand that question. Could you rephrase it?"
    if len(rows) == 0:
        return "No matching records found in the database."

    model = genai.GenerativeModel("gemini-2.5-flash")
    data_str = f"Columns: {col_names}\nData: {rows}"
    format_prompt = f"""
    The user asked: "{question}"
    The database returned this data: {data_str}
    
    Write a clear, friendly, natural language answer to the user's question using this data.
    Be concise. Don't mention SQL or database. Just answer naturally like a human would.
    If it's a count, say something like "There are X students..."
    If it's a list, present them nicely.
    """
    response = model.generate_content(format_prompt)
    return response.text.strip()

prompt = [
    """
    You are an expert in converting plain English questions into accurate SQL queries.
    The database table name is STUDENT and it has these columns: NAME, CLASS, SECTION, and MARKS.

    IMPORTANT RULES:
    - Always return ONLY the SQL query, nothing else. No backticks, no 'sql' word, no explanation.
    - For names: use exact match with = by default. Only use LIKE if the name is a very obvious minor typo (1-2 characters off) of a real name. For example "rachell" → "Rachel" is ok. But "racheajj" or "racheajj" is too different — return no results with exact match.
    - For class names: use LIKE with % only for partial matches like "data sci" → "Data Science".
    - Never guess a completely different name just because it shares some letters.

    EXAMPLES:
    Q: How many students are there?
    A: SELECT COUNT(*) FROM STUDENT;

    Q: How many students named rachell?
    A: SELECT COUNT(*) FROM STUDENT WHERE NAME = "Rachel";

    Q: How many students named racheajj?
    A: SELECT COUNT(*) FROM STUDENT WHERE NAME = "racheajj";

    Q: Show students in data sci class
    A: SELECT * FROM STUDENT WHERE CLASS LIKE "%Data Science%";

    Q: Who scored the highest?
    A: SELECT * FROM STUDENT ORDER BY MARKS DESC LIMIT 1;

    Q: Name of all students
    A: SELECT NAME FROM STUDENT;
    """
]

## Streamlit App
st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Gemini App To Retrieve SQL Data")

question = st.text_input("Input:", key="input")
submit = st.button("Ask the question")

if submit:
    if question.strip() == "":
        st.warning("Please type a question first.")
    else:
        sql = get_gemini_response(question, prompt)
        print("Generated SQL:", sql)
        rows, col_names = read_sql_query(sql, "student.db")
        answer = format_response(rows, col_names, question)
        st.subheader("Answer")
        st.write(answer)