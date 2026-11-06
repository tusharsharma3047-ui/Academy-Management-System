import tkinter as tk
from tkinter import ttk, messagebox

from reports.reports_utils import (
    get_students_with_pending_fees,
    get_monthly_fee_collection,
    get_student_attendance_percentage,
    get_faculty_attendance_summary,
    salary_due_report,
    get_inactive_students,
    get_inactive_faculty
)


class ReportsUI:

    def __init__(self, root):

        self.root = root
        self.root.title("Reports")
        self.root.geometry("900x600")

        notebook = ttk.Notebook(root)
        notebook.pack(fill="both", expand=True)

        self.pending_tab = tk.Frame(notebook)
        self.fees_tab = tk.Frame(notebook)
        self.attendance_tab = tk.Frame(notebook)
        self.salary_tab = tk.Frame(notebook)
        self.inactive_tab = tk.Frame(notebook)

        notebook.add(self.pending_tab, text="Pending Fees")
        notebook.add(self.fees_tab, text="Monthly Fees")
        notebook.add(self.attendance_tab, text="Attendance %")
        notebook.add(self.salary_tab, text="Salary Due")
        notebook.add(self.inactive_tab, text="Inactive")

        self.build_pending_tab()
        self.build_fees_tab()
        self.build_attendance_tab()
        self.build_salary_tab()
        self.build_inactive_tab()

    # ---------------- Pending Fees ----------------

    def build_pending_tab(self):

        btn = tk.Button(
            self.pending_tab,
            text="Load Pending Fees",
            command=self.load_pending
        )
        btn.pack(pady=10)

        self.pending_tree = ttk.Treeview(
            self.pending_tab,
            columns=("ID","Name","Batch","Pending"),
            show="headings"
        )

        for col in ("ID","Name","Batch","Pending"):
            self.pending_tree.heading(col,text=col)
            self.pending_tree.column(col,width=150,anchor="center")

        self.pending_tree.pack(fill="both",expand=True)

    def load_pending(self):

        for r in self.pending_tree.get_children():
            self.pending_tree.delete(r)

        data = get_students_with_pending_fees()

        for row in data:
            self.pending_tree.insert("", "end", values=row)

    # ---------------- Monthly Fee ----------------

    def build_fees_tab(self):

        frame = tk.Frame(self.fees_tab)
        frame.pack(pady=20)

        tk.Label(frame,text="Month (YYYY-MM)").grid(row=0,column=0)

        self.month_entry = tk.Entry(frame)
        self.month_entry.grid(row=0,column=1,padx=10)

        tk.Button(
            frame,
            text="Get Collection",
            command=self.show_collection
        ).grid(row=0,column=2)

        self.collection_label = tk.Label(
            self.fees_tab,
            text="Total Collection: ₹0",
            font=("Arial",14)
        )

        self.collection_label.pack(pady=20)

    def show_collection(self):

        month = self.month_entry.get()

        if not month:
            messagebox.showwarning("Input","Enter month")
            return

        total = get_monthly_fee_collection(month)

        self.collection_label.config(
            text=f"Total Collection: ₹{total}"
        )

    # ---------------- Attendance ----------------

    def build_attendance_tab(self):

        frame = tk.Frame(self.attendance_tab)
        frame.pack(pady=20)

        tk.Label(frame,text="Student ID").grid(row=0,column=0)

        self.student_id_entry = tk.Entry(frame)
        self.student_id_entry.grid(row=0,column=1,padx=10)

        tk.Button(
            frame,
            text="Get %",
            command=self.student_attendance
        ).grid(row=0,column=2)

        self.student_att_label = tk.Label(
            self.attendance_tab,
            text="Attendance: 0%",
            font=("Arial",14)
        )

        self.student_att_label.pack(pady=20)
        # Faculty
        tk.Label(frame,text="Faculty ID").grid(row=1,column=0)

        self.faculty_id_entry = tk.Entry(frame)
        self.faculty_id_entry.grid(row=1,column=1,padx=10)

        tk.Button(
            frame,
            text="Get Faculty %",
            command=self.faculty_attendance
        ).grid(row=1,column=2)

        self.faculty_att_label = tk.Label(
            self.attendance_tab,
            text="Faculty Attendance: 0%",
            font=("Arial",14)
        )

        self.faculty_att_label.pack(pady=10)

    def student_attendance(self):

        sid = self.student_id_entry.get()

        if not sid.isdigit():
            messagebox.showerror("Error","Invalid student ID")
            return

        percent = get_student_attendance_percentage(int(sid))

        self.student_att_label.config(
            text=f"Attendance: {percent}%"
        )

    def faculty_attendance(self):

        fid = self.faculty_id_entry.get()

        if not fid.isdigit():
            messagebox.showerror("Error","Invalid faculty ID")
            return

        percent = get_faculty_attendance_summary(int(fid))

        self.faculty_att_label.config(
            text=f"Faculty Attendance: {percent}%"
        )


    # ---------------- Salary Due ----------------

    def build_salary_tab(self):

        frame = tk.Frame(self.salary_tab)
        frame.pack(pady=10)

        tk.Label(frame,text="Month (YYYY-MM)").grid(row=0,column=0)

        self.salary_month = tk.Entry(frame)
        self.salary_month.grid(row=0,column=1,padx=10)

        tk.Button(
            frame,
            text="Load Report",
            command=self.load_salary_due
        ).grid(row=0,column=2)

        self.salary_tree = ttk.Treeview(
            self.salary_tab,
            columns=("Name","Due Salary"),
            show="headings"
        )

        self.salary_tree.heading("Name",text="Name")
        self.salary_tree.heading("Due Salary",text="Due Salary")

        self.salary_tree.column("Name",width=200,anchor="center")
        self.salary_tree.column("Due Salary",width=200,anchor="center")

        self.salary_tree.pack(fill="both",expand=True,pady=20)

    def load_salary_due(self):

        month = self.salary_month.get()

        if not month:
            messagebox.showwarning("Input","Enter month")
            return

        for r in self.salary_tree.get_children():
            self.salary_tree.delete(r)

        data = salary_due_report(month)

        for row in data:
            self.salary_tree.insert("", "end", values=row)

    # ---------------- Inactive ----------------

    def build_inactive_tab(self):

        frame = tk.Frame(self.inactive_tab)
        frame.pack(pady=10)

        tk.Button(
            frame,
            text="Inactive Students",
            command=self.load_inactive_students
        ).grid(row=0,column=0,padx=10)

        tk.Button(
            frame,
            text="Inactive Faculty",
            command=self.load_inactive_faculty
        ).grid(row=0,column=1,padx=10)

        self.inactive_tree = ttk.Treeview(
            self.inactive_tab,
            columns=("ID","Name","Extra","Phone"),
            show="headings"
        )

        for col in ("ID","Name","Extra","Phone"):
            self.inactive_tree.heading(col,text=col)
            self.inactive_tree.column(col,width=150,anchor="center")

        self.inactive_tree.pack(fill="both",expand=True,pady=20)

    def load_inactive_students(self):

        for r in self.inactive_tree.get_children():
            self.inactive_tree.delete(r)

        data = get_inactive_students()

        for row in data:
            self.inactive_tree.insert("", "end", values=row)

    def load_inactive_faculty(self):

        for r in self.inactive_tree.get_children():
            self.inactive_tree.delete(r)

        data = get_inactive_faculty()

        for row in data:
            self.inactive_tree.insert("", "end", values=row)