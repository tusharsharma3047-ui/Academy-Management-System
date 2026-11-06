import sqlite3
def get_connection():
    conn= sqlite3.connect("data/academy.db", timeout= 10)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def mark_attendance(student_id, status):
    if status not in ("Present", "Absent"):
        raise ValueError("Invalid attendance status")

    conn = get_connection()
    cursor= conn.cursor()

    cursor.execute("""INSERT INTO attendance(student_id, attendance_date, status) VALUES(?, DATE('now'), ?)""", (student_id, status))

    conn.commit()
    conn.close()

def get_attendance_by_student(student_id):
    conn= get_connection()
    cursor= conn.cursor()

    cursor.execute("""SELECT attendance_date, status FROM attendance WHERE student_id =? ORDER BY attendance_date""", (student_id,))

    records= cursor.fetchall()
    conn.close()
    return records
    
def get_attendance_by_date(att_date):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT student_id, status
        FROM attendance
        WHERE attendance_date = ?
        ORDER BY student_id
    """, (att_date,))

    records = cursor.fetchall()
    conn.close()
    return records

def update_attendance(student_id, att_date, status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE attendance
        SET status = ?
        WHERE student_id = ? AND attendance_date = ?
    """, (status, student_id, att_date))

    conn.commit()
    conn.close()


def get_student_attendance_full(student_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT s.student_id, s.name, a.attendance_date, a.status
        FROM attendance a
        JOIN students s ON a.student_id = s.student_id
        WHERE s.student_id = ?
        ORDER BY a.attendance_date
    """, (student_id,))

    data = cursor.fetchall()
    conn.close()
    return data

def get_daily_student_attendance(att_date):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            s.student_id,
            s.name,
            COALESCE(a.status, 'Present')
        FROM students s
        LEFT JOIN attendance a
          ON s.student_id = a.student_id
         AND a.attendance_date = ?
        WHERE s.status = 'Active'
        ORDER BY s.name
    """, (att_date,))

    data = cursor.fetchall()
    conn.close()
    return data

def save_student_attendance(student_id, att_date, status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 1 FROM attendance
        WHERE student_id = ? AND attendance_date = ?
    """, (student_id, att_date))

    if cursor.fetchone():
        cursor.execute("""
            UPDATE attendance
            SET status = ?
            WHERE student_id = ? AND attendance_date = ?
        """, (status, student_id, att_date))
    else:
        cursor.execute("""
            INSERT INTO attendance(student_id, attendance_date, status)
            VALUES (?, ?, ?)
        """, (student_id, att_date, status))

    conn.commit()
    conn.close()
# if __name__ == "__main__":
    # mark_attendance(7, "Absent")
    # mark_attendance(1, "Present")  # should fail (duplicate)

    # data = get_attendance_by_date("2026-02-12")
    # for row in data:
    #     print(row)
