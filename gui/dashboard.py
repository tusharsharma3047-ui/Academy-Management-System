import tkinter as tk
from tkinter import messagebox
from gui.student_ui import StudentUI
from gui.faculty_ui import FacultyUI
from gui.attendance_ui import AttendanceUI
from gui.fees_ui import FeesUI
from gui.salary_ui import SalaryUI
from gui.reports_ui import ReportsUI
from backup import backup_database, cleanup_old_backups, restore_database


from reports.reports_utils import (
    total_students,
    active_students,
    total_faculty,
    active_faculty
)


def open_students():
    StudentUI(tk.Toplevel())

def open_faculty():
    FacultyUI(tk.Toplevel())

def open_fees():
    FeesUI(tk.Toplevel())

def open_attendance():
    AttendanceUI(tk.Toplevel())

def open_salary():
    SalaryUI(tk.Toplevel())

def open_report():
    ReportsUI(tk.Toplevel())


def launch_dashboard():
    print("D1: Entered launch_dashboard")

    root = tk.Tk()

    print("D2: Tk window created")
    root.title("Academy Management System")
    root.geometry("750x600")
    root.resizable(True, True)

    tk.Label(
        root,
        text="Academy Dashboard",
        font=("Arial", 16, "bold")
    ).pack(pady=20)

    tk.Label(root, text=f"Total Students: {total_students()}").pack()
    tk.Label(root, text=f"Active Students: {active_students()}").pack()
    tk.Label(root, text=f"Total Faculty: {total_faculty()}").pack()
    tk.Label(root, text=f"Active Faculty: {active_faculty()}").pack()

    tk.Button(root, text="Students", width=25, command=open_students).pack(pady=5)
    tk.Button(root, text="Faculty", width=25, command=open_faculty).pack(pady=5)
    tk.Button(root, text="Fees", width=25, command=open_fees).pack(pady=5)
    tk.Button(root, text="Attendance", width=25, command=open_attendance).pack(pady=5)
    tk.Button(root, text="Salary", width=25, command=open_salary).pack(pady=5)
    tk.Button(root, text="Reports", width=25, command=open_report).pack(pady=5)

    tk.Button(
        root,
        text="Exit",
        width=25,
        command=root.destroy,
        bg="red",
        fg="white"
    ).pack(pady=20)

    # tk.Button(
    #     root,
    #     text="Backup Data",
    #     width=25,
    #     command=lambda: messagebox.showinfo(
    #         "Backup",
    #         f"Backup saved at:\n{backup_database()}"
    #     )
    # ).pack(pady=5)

    tk.Button(
        root,
        text="Restore Backup",
        width=25,
        command=restore_database
    ).pack(pady=5)


    # backup_database()
    # cleanup_old_backups()


    print("D3: About to start mainloop")
    try:
        root.mainloop()
    except Exception as e:
        print("MAINLOOP ERROR:", repr(e))
    finally:
        print("D4: Mainloop ended")