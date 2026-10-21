import sqlite3
connector = sqlite3.connect("Student.db")
cursor = connector.cursor()

#! Table Creation-------------------

# cursor.execute("""
# CREATE TABLE STUDENT (ID NUMBER(3) PRIMARY KEY,
# NAME VARCHAR(32) NOT NULL,
# PHONE NUMBER(10) UNIQUE,
# MAILID VARCHAR(50) UNIQUE,
# DOB DATE NOT NULL,
# CGPA NUMBER(4,2) NOT NULL
# );
# """)
# print ("Table Created")

#! Data Insertion------------------

cursor.execute("""
INSERT INTO STUDENT VALUES
(103, "Ram", 7895465550, 'ramdevloper@gmail.com', '05-07-2004', 9.02)
""")
connector.commit()
#! Connector.commit()

data= cursor.execute("SELECT * FROM STUDENT")
print (data)
data=cursor.execute("SELECT * FROM STUDENT").fetchall()
print(data)

