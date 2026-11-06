import sqlite3

DB_PATH = "data/academy.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def get_faculty_dropdown():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT faculty_id, name
        FROM faculty
        WHERE status='Active'
        ORDER BY name
    """)

    rows = cursor.fetchall()
    conn.close()

    return rows


def pay_salary(faculty_id, month, amount):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO salary
        (faculty_id, salary_month, amount_paid, payment_date)
        VALUES (?, ?, ?, DATE('now'))
    """, (faculty_id, month, amount))

    conn.commit()
    conn.close()

def update_salary(salary_id, amount_paid):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE salary
        SET amount_paid = ?
        WHERE salary_id = ?
    """, (amount_paid, salary_id))

    conn.commit()
    conn.close()

def get_salary_by_faculty(faculty_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT s.salary_id, s.faculty_id, f.name,
               s.salary_month, s.amount_paid, s.payment_date
        FROM salary s
        JOIN faculty f ON s.faculty_id = f.faculty_id
        WHERE s.faculty_id=?
        ORDER BY s.salary_month DESC
    """, (faculty_id,))

    rows = cursor.fetchall()
    conn.close()

    return rows