import sqlite3
DB_PATH = "data/academy.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def add_faculty(name, phone, specialization, monthly_salary):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO faculty
            (name, phone, specialization, monthly_salary, status, join_date)
            VALUES (?, ?, ?, ?, 'Active', DATE('now'))
        """, (name, phone, specialization, monthly_salary))

        conn.commit()
    finally:
        conn.close()


def get_all_faculty():
    conn= get_connection()
    cursor= conn.cursor()

    cursor.execute("""SELECT * FROM faculty""")
    data= cursor.fetchall()

    conn.close()
    return data


def update_faculty(faculty_id, name, phone, specialization, monthly_salary, status):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE faculty
            SET name=?, phone=?, specialization=?,
                monthly_salary=?, status=?
            WHERE faculty_id=?
        """, (name, phone, specialization, monthly_salary, status, faculty_id))

        conn.commit()
    finally:
        conn.close()

def deactivate_faculty(faculty_id):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE faculty
            SET status='Inactive',
                end_date = DATE('now')
            WHERE faculty_id=?
        """, (faculty_id,))

        conn.commit()
    finally:
        conn.close()


# if __name__=="__main__":
#     add_faculty("New", "1234567890", "Advanced Chess", 20000)

    # print("Faculty")
    # print(get_all_faculty())

    # pay_salary(2, "2026-02", 20000)

    # print("Salary")
    # print(get_salary_history(2))