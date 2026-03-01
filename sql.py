import sqlite3

# Connect to SQLite (this creates student.db if it doesn't exist)
connection = sqlite3.connect("student.db")

# Create a cursor object to insert record, create table, retrieve data
cursor = connection.cursor()

# Create the table
table_info = """
CREATE TABLE IF NOT EXISTS STUDENT (
    NAME VARCHAR(25),
    CLASS VARCHAR(25),
    SECTION VARCHAR(25),
    MARKS INT
);
"""

# Clear old data to avoid duplicates
cursor.execute("DELETE FROM STUDENT;")

cursor.execute(table_info)

# Insert some records
cursor.execute("INSERT INTO STUDENT VALUES ('Krish', 'Data Science', 'A', 90)")
cursor.execute("INSERT INTO STUDENT VALUES ('John', 'Machine Learning', 'B', 85)")
cursor.execute("INSERT INTO STUDENT VALUES ('Ben', 'DEVOPS', 'A', 70)")
cursor.execute("INSERT INTO STUDENT VALUES ('Rachel', 'AI', 'B', 71)")
cursor.execute("INSERT INTO STUDENT VALUES ('Sara', 'AI', 'A', 95)")

# display all records 
print("the inserted records are")

# Retrieve and display all records
data= cursor.execute("SELECT * FROM STUDENT")
for row in data:
    print(row)

# Commit the changes
connection.commit()

# Close the connection
connection.close()
