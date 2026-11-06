import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

from attendance import (
    get_daily_student_attendance,
    save_student_attendance
)

from faculty_attendance import (
    get_daily_faculty_attendance,
    save_faculty_attendance
)


class AttendanceUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance Management")
        self.root.geometry("900x600")

        self.build_ui()

    def build_ui(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True)

        self.student_tab = tk.Frame(notebook)
        self.faculty_tab = tk.Frame(notebook)

        notebook.add(self.student_tab, text="Student Attendance")
        notebook.add(self.faculty_tab, text="Faculty Attendance")

        self.build_student_tab()
        self.build_faculty_tab()

    # ================= STUDENT TAB =================

    def build_student_tab(self):
        top = tk.Frame(self.student_tab)
        top.pack(pady=10)

        tk.Label(top, text="Date (YYYY-MM-DD)").pack(side="left")
        self.student_date = tk.Entry(top)
        self.student_date.pack(side="left", padx=5)
        self.student_date.insert(0, date.today().isoformat())

        tk.Button(top, text="Load", command=self.load_student_attendance).pack(side="left", padx=5)
        tk.Button(top, text="Save Attendance", command=self.save_student).pack(side="left", padx=5)

        self.student_table = ttk.Treeview(
            self.student_tab,
            columns=("ID", "Name", "Status"),
            show="headings"
        )

        for col in ("ID", "Name", "Status"):
            self.student_table.heading(col, text=col)
            self.student_table.column(col, width=200, anchor="center")

        self.student_table.pack(fill="both", expand=True, pady=10)
        self.student_table.bind("<Double-1>", self.toggle_student_status)

    def load_student_attendance(self):
        self.student_table.delete(*self.student_table.get_children())
        data = get_daily_student_attendance(self.student_date.get())

        for row in data:
            self.student_table.insert("", "end", values=row)

    def toggle_student_status(self, event):
        item = self.student_table.focus()
        values = list(self.student_table.item(item, "values"))
        values[2] = "Present" if values[2] == "Absent" else "Absent"
        self.student_table.item(item, values=values)

    def save_student(self):
        att_date = self.student_date.get()

        for row in self.student_table.get_children():
            student_id, _, status = self.student_table.item(row, "values")
            save_student_attendance(student_id, att_date, status)

        messagebox.showinfo("Saved", "Student attendance saved")

    # ================= FACULTY TAB =================

    def build_faculty_tab(self):
        top = tk.Frame(self.faculty_tab)
        top.pack(pady=10)

        tk.Label(top, text="Date (YYYY-MM-DD)").pack(side="left")
        self.faculty_date = tk.Entry(top)
        self.faculty_date.pack(side="left", padx=5)
        self.faculty_date.insert(0, date.today().isoformat())

        tk.Button(top, text="Load", command=self.load_faculty_attendance).pack(side="left", padx=5)
        tk.Button(top, text="Save Attendance", command=self.save_faculty).pack(side="left", padx=5)

        self.faculty_table = ttk.Treeview(
            self.faculty_tab,
            columns=("ID", "Name", "Status"),
            show="headings"
        )

        for col in ("ID", "Name", "Status"):
            self.faculty_table.heading(col, text=col)
            self.faculty_table.column(col, width=200, anchor="center")

        self.faculty_table.pack(fill="both", expand=True, pady=10)
        self.faculty_table.bind("<Double-1>", self.toggle_faculty_status)

    def load_faculty_attendance(self):
        self.faculty_table.delete(*self.faculty_table.get_children())
        data = get_daily_faculty_attendance(self.faculty_date.get())

        for row in data:
            self.faculty_table.insert("", "end", values=row)

    def toggle_faculty_status(self, event):
        item = self.faculty_table.focus()
        values = list(self.faculty_table.item(item, "values"))
        values[2] = "Present" if values[2] == "Absent" else "Absent"
        self.faculty_table.item(item, values=values)

    def save_faculty(self):
        att_date = self.faculty_date.get()

        for row in self.faculty_table.get_children():
            faculty_id, _, status = self.faculty_table.item(row, "values")
            save_faculty_attendance(faculty_id, att_date, status)

        messagebox.showinfo("Saved", "Faculty attendance saved")