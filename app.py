from dotenv import load_dotenv
load_dotenv()  ## load all the environment variables

import streamlit as st
import os
import sqlite3

import google.generativeai as genai

## Configure our API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to Load Google Gemini Model and provide SQL query
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([prompt[0], question])
    return response.text

def read_sql_query(sql,db):
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows

## Define Your Prompt
prompt = [
    """
    You are an expert in converting plain English questions into accurate SQL queries.
    The database table name is STUDENT and it has these columns: NAME, CLASS, SECTION, and MARKS.

    IMPORTANT RULES:
    - Always return the full and correct SQL query.
    - Do not add any unnecessary filters or conditions unless they are clearly mentioned in the question.
    - When asked for all students, select all matching records from the STUDENT table without filtering.
    - Output must only be the SQL query itself, no extra text, no ``` and no 'sql' word.

    EXAMPLES:
    Q: How many entries of records are present?
    A: SELECT COUNT(*) FROM STUDENT;

    Q: Tell me all the students studying in Data Science class.
    A: SELECT * FROM STUDENT WHERE CLASS = "Data Science";

    Q: Name of all the students.
    A: SELECT NAME FROM STUDENT;
    """
]


## Streamlit App

st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Gemini App To Retrieve SQL Data")

question=st.text_input("Input: ",key="input")

submit=st.button("Ask the question")

# if submit is clicked
if submit:
    response=get_gemini_response(question,prompt)
    print(response)
    response=read_sql_query(response,"student.db")
    st.subheader("The Response is")
    for row in response:
        print(row)
        st.header(row)
