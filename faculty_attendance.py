from database import create_connection


def mark_faculty_attendance(faculty_id, status):
    if status not in ("Present", "Absent"):
        raise ValueError("Invalid attendance status")

    conn = create_connection()
    cursor = conn.cursor()

    # Check faculty exists and is active
    cursor.execute("""
        SELECT status FROM faculty WHERE faculty_id = ?
    """, (faculty_id,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        raise ValueError("Faculty does not exist")

    if row[0] != "Active":
        conn.close()
        raise ValueError("Cannot mark attendance for inactive faculty")

    # Prevent duplicate attendance for same day
    cursor.execute("""
        SELECT 1 FROM faculty_attendance
        WHERE faculty_id = ? AND attendance_date = DATE('now')
    """, (faculty_id,))

    if cursor.fetchone():
        conn.close()
        raise ValueError("Attendance already marked for today")

    # Insert attendance
    cursor.execute("""
        INSERT INTO faculty_attendance (faculty_id, attendance_date, status)
        VALUES (?, DATE('now'), ?)
    """, (faculty_id, status))

    conn.commit()
    conn.close()


def get_faculty_attendance(faculty_id):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT attendance_date, status
        FROM faculty_attendance
        WHERE faculty_id = ?
        ORDER BY attendance_date
    """, (faculty_id,))

    records = cursor.fetchall()
    conn.close()
    return records


def get_faculty_attendance_by_date(date):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT f.name, fa.status
        FROM faculty_attendance fa
        JOIN faculty f ON fa.faculty_id = f.faculty_id
        WHERE fa.attendance_date = ?
        ORDER BY f.name
    """, (date,))

    records = cursor.fetchall()
    conn.close()
    return records

def get_faculty_attendance_summary(faculty_id, month):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            COUNT(*) AS present_days
        FROM faculty_attendance
        WHERE faculty_id = ?
          AND status = 'Present'
          AND strftime('%Y-%m', attendance_date) = ?
    """, (faculty_id, month))

    count = cursor.fetchone()[0]
    conn.close()
    return count


def get_faculty_attendance_full(faculty_id):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT f.faculty_id, f.name, fa.attendance_date, fa.status
        FROM faculty_attendance fa
        JOIN faculty f ON fa.faculty_id = f.faculty_id
        WHERE f.faculty_id = ?
        ORDER BY fa.attendance_date
    """, (faculty_id,))

    data = cursor.fetchall()
    conn.close()
    return data

def get_daily_faculty_attendance(att_date):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            f.faculty_id,
            f.name,
            COALESCE(a.status, 'Present')
        FROM faculty f
        LEFT JOIN faculty_attendance a
          ON f.faculty_id = a.faculty_id
         AND a.attendance_date = ?
        WHERE f.status = 'Active'
        ORDER BY f.name
    """, (att_date,))

    data = cursor.fetchall()
    conn.close()
    return data

def save_faculty_attendance(faculty_id, att_date, status):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 1 FROM faculty_attendance
        WHERE faculty_id = ? AND attendance_date = ?
    """, (faculty_id, att_date))

    if cursor.fetchone():
        cursor.execute("""
            UPDATE faculty_attendance
            SET status = ?
            WHERE faculty_id = ? AND attendance_date = ?
        """, (status, faculty_id, att_date))
    else:
        cursor.execute("""
            INSERT INTO faculty_attendance(faculty_id, attendance_date, status)
            VALUES (?, ?, ?)
        """, (faculty_id, att_date, status))

    conn.commit()
    conn.close()