import sqlite3

def create_connection():
    conn= sqlite3.connect("data/academy.db", timeout= 10)
    return conn

def create_students_table():
    conn= create_connection()
    cursor= conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students(
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    batch TEXT,
    phone TEXT,
    status TEXT DEFAULT 'Active',
    monthly_fee INTEGER NOT NULL,
    admission_date DATE DEFAULT CURRENT_DATE
);
    """)

    conn.commit()
    conn.close()

if __name__=="__main__":
    create_students_table()
    print("Students table created successfully in data/academy.db")