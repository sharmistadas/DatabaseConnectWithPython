import sqlite3
from datetime import date

# ---------- Connect ----------
connector = sqlite3.connect("Student.db")
cursor = connector.cursor()


# ---------- Age calculation ----------
def calculate_age(dob_str):
    dob = date.fromisoformat(dob_str)  # format: YYYY-MM-DD
    today = date.today()
    # subtract 1 if birthday has not come yet this year
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))


# ---------- Table creation (8 columns) ----------
cursor.execute("DROP TABLE IF EXISTS STUDENT")
cursor.execute("""
CREATE TABLE STUDENT (
    ID         INTEGER PRIMARY KEY,
    NAME       VARCHAR(32) NOT NULL,
    PHONE      INTEGER UNIQUE,
    MAILID     VARCHAR(50) UNIQUE,
    DOB        DATE NOT NULL,
    CGPA       REAL NOT NULL,
    DEPARTMENT VARCHAR(20),
    AGE        INTEGER
)
""")
print("Table Created")

# ---------- Data insertion (14 records) ----------
students = [
    (101, "Arjun",   9876500001, "arjun@gmail.com",       "2003-01-15", 8.45, "CSE"),
    (102, "Priya",   9876500002, "priya@gmail.com",       "2004-03-22", 9.10, "ECE"),
    (103, "Ram",     7895465550, "ramdevloper@gmail.com", "2004-07-05", 9.02, "CSE"),
    (104, "Sneha",   9876500004, "sneha@gmail.com",       "2003-11-30", 8.75, "IT"),
    (105, "Kiran",   9876500005, "kiran@gmail.com",       "2004-05-18", 7.95, "MECH"),
    (106, "Divya",   9876500006, "divya@gmail.com",       "2003-09-09", 9.35, "CSE"),
    (107, "Rahul",   9876500007, "rahul@gmail.com",       "2004-12-01", 8.10, "EEE"),
    (108, "Anjali",  9876500008, "anjali@gmail.com",      "2003-06-25", 8.90, "IT"),
    (109, "Vikram",  9876500009, "vikram@gmail.com",      "2004-02-14", 7.60, "CIVIL"),
    (110, "Meena",   9876500010, "meena@gmail.com",       "2003-08-12", 9.20, "ECE"),
    (111, "Suresh",  9876500011, "suresh@gmail.com",      "2004-10-27", 8.30, "MECH"),
    (112, "Lakshmi", 9876500012, "lakshmi@gmail.com",     "2003-04-03", 9.50, "CSE"),
    (113, "Naveen",  9876500013, "naveen@gmail.com",      "2004-01-19", 8.05, "EEE"),
    (114, "Pooja",   9876500014, "pooja@gmail.com",       "2003-12-08", 8.65, "IT"),
]

# add calculated age to each record -> 8 values per row
rows = [s + (calculate_age(s[4]),) for s in students]

cursor.executemany("INSERT INTO STUDENT VALUES (?, ?, ?, ?, ?, ?, ?, ?)", rows)
connector.commit()
print("14 records inserted")


# ---------- Display ----------
def show_table():
    data = cursor.execute("SELECT * FROM STUDENT").fetchall()
    print()
    print(f"{'ID':<5}{'NAME':<10}{'PHONE':<13}{'MAILID':<24}{'DOB':<12}{'CGPA':<6}{'DEPT':<7}AGE")
    print("-" * 85)
    for r in data:
        print(f"{r[0]:<5}{r[1]:<10}{r[2]:<13}{r[3]:<24}{r[4]:<12}{r[5]:<6}{r[6]:<7}{r[7]}")
    print(f"\nTotal records: {len(data)}")


show_table()

# ---------- Age calculated directly in SQL (always up to date) ----------
print("\nAge calculated using SQL query:")
result = cursor.execute("""
SELECT ID, NAME, DOB,
       CAST((julianday('now') - julianday(DOB)) / 365.25 AS INTEGER) AS AGE
FROM STUDENT
""").fetchall()
for r in result:
    print(r)

# ---------- Refresh stored AGE column any time ----------
cursor.execute("""
UPDATE STUDENT
SET AGE = CAST((julianday('now') - julianday(DOB)) / 365.25 AS INTEGER)
""")
connector.commit()

connector.close()