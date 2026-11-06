import sqlite3
from datetime import datetime
import os

DB_PATH = "data/academy.db"

print("FEES DATABASE:")
print("Absolute path:", os.path.abspath(DB_PATH))       

def get_connection():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# ---------- Student list for dropdown ----------
def get_students_for_dropdown():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT student_id, name
        FROM students
        WHERE status = 'Active'
        ORDER BY name
    """)

    rows = cursor.fetchall()
    print(rows)
    conn.close()
    return rows

    
# ---------- Add Fee ----------
def add_fee(student_id, fee_month, amount_paid, payment_mode, remarks=""):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO fees
        (
            student_id,
            fee_month,
            amount_paid,
            payment_date,
            payment_mode,
            remarks
        )
        VALUES (?, ?, ?, DATE('now'), ?, ?)
    """,
    (
        student_id,
        fee_month,
        amount_paid,
        payment_mode,
        remarks
    ))

    conn.commit()
    conn.close()


# ---------- Update Fee ----------
# ---------- Update Fee ----------
def update_fee(fee_id, fee_month, amount_paid, payment_mode, remarks):

    conn = get_connection()
    cursor = conn.cursor()

    print("\n========== UPDATE FEE ==========")
    print("Database:", os.path.abspath(DB_PATH))
    print("Fee ID:", fee_id)
    print("New Month:", fee_month)
    print("New Amount:", amount_paid)

    cursor.execute("""
        UPDATE fees
        SET fee_month = ?,
            amount_paid = ?,
            payment_mode = ?,
            remarks = ?
        WHERE fee_id = ?
    """, (
        fee_month,
        amount_paid,
        payment_mode,
        remarks,
        fee_id
    ))

    print("Rows updated:", cursor.rowcount)

    conn.commit()

    # Immediately read the same record back
    cursor.execute("""
        SELECT fee_id, fee_month, amount_paid, payment_mode, remarks
        FROM fees
        WHERE fee_id = ?
    """, (fee_id,))

    updated = cursor.fetchone()

    print("Database now contains:", updated)
    print("================================\n")

    conn.close()

# ---------- Get Fees by Student ----------
def get_fees_by_student(student_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
        f.fee_id,
        f.student_id,
        s.name,
        f.fee_month,
        f.amount_paid,
        f.payment_date,
        f.payment_mode,
        f.remarks
        FROM fees f
        JOIN students s
        ON f.student_id=s.student_id
        WHERE f.student_id=?
        ORDER BY f.fee_month DESC
    """,(student_id,))

    rows = cursor.fetchall()
    conn.close()
    return rows


# ---------- Pending Fees ----------
def get_pending_fees(student_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT monthly_fee, admission_date
        FROM students
        WHERE student_id = ?
    """, (student_id,))

    row = cursor.fetchone()

    if not row:
        conn.close()
        raise ValueError("Student not found")

    monthly_fee, admission_date = row

    from datetime import datetime

    start = datetime.strptime(admission_date, "%Y-%m-%d")
    today = datetime.today()

    months = (today.year - start.year) * 12 + (today.month - start.month) + 1

    total_expected = months * monthly_fee

    cursor.execute("""
        SELECT COALESCE(SUM(amount_paid), 0)
        FROM fees
        WHERE student_id = ?
    """, (student_id,))

    total_paid = cursor.fetchone()[0]

    conn.close()

    pending = total_expected - total_paid

    return max(0, pending)