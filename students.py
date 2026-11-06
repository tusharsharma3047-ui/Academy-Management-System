from database import create_connection

def is_valid_phone(phone):
    return phone.isdigit() and len(phone) == 10


def add_student(name, batch, phone, fee):
    if not name.strip():
        raise ValueError("Name cannot be empty")
    if not batch.strip():
        raise ValueError("Batch cannot be empty")
    if not phone.isdigit() or len(phone) != 10:
        raise ValueError("Invalid phone number")
    if fee <= 0:
        raise ValueError("Total fee must be positive")

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO students (name, batch, phone, status, fee)
        VALUES (?, ?, ?, ?, ?)
    """, (name, batch, phone, "Active", fee))

    conn.commit()
    conn.close()


def get_all_students():
    conn= create_connection()
    cursor= conn.cursor()

    cursor.execute("SELECT * FROM students")
    rows= cursor.fetchall()

    conn.close()
    return rows



def update_student(student_id, name, batch, phone, status, fee):
    if not phone.isdigit() or len(phone) != 10:
        raise ValueError("Invalid phone number")

    if status not in ("Active", "Inactive"):
        raise ValueError("Invalid status")
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE students
        SET name = ?, batch = ?, phone = ?, status = ?, monthly_fee = ?
        WHERE student_id = ?
    """, (name, batch, phone, status, fee, student_id))

    conn.commit()
    conn.close()



def deactivate_student(student_id):
    conn= create_connection()
    cursor= conn.cursor()

    cursor.execute("""UPDATE students
        SET status = 'Inactive'
        WHERE student_id = ?""", (student_id,))
    
    if cursor.rowcount == 0:
        conn.close()
        raise ValueError("Student not found")

    conn.commit()
    conn.close()





# if __name__=="__main__":                                  
#     add_student("Saket", "Advanced", "9876544410")
#     add_student("Sanket", "Beginner", "9876511410")


#     update_student(1, "Prisha Sharma", "Intermediate", "9876543210", "Active")

#     delete_student(3)

#     students = get_all_students()
#     for s in students:
#         print(s)
