import tkinter as tk
from tkinter import ttk, messagebox

from students import (
    add_student,
    get_all_students,
    update_student,
    deactivate_student
)


class StudentUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Students Management")
        self.root.geometry("750x600")

        self.create_widgets()
        self.load_students()

    def create_widgets(self):
        # ---------- Form ----------
        form = tk.Frame(self.root)
        form.pack(pady=10)

        tk.Label(form, text="Name").grid(row=0, column=0)
        tk.Label(form, text="Batch").grid(row=0, column=2)
        tk.Label(form, text="Phone").grid(row=1, column=0)
        tk.Label(form, text="Status").grid(row=1, column=2)
        tk.Label(form, text="Fee").grid(row=2, column=0)

        self.name_entry = tk.Entry(form)
        self.batch_entry = tk.Entry(form)
        self.phone_entry = tk.Entry(form)
        self.status_var = tk.StringVar(value="Active")
        self.total_fee_entry = tk.Entry(form)

        self.name_entry.grid(row=0, column=1, padx=5)
        self.batch_entry.grid(row=0, column=3, padx=5)
        self.phone_entry.grid(row=1, column=1, padx=5)
        self.total_fee_entry.grid(row=2, column=1, padx=5)
        ttk.Combobox(
            form, textvariable=self.status_var,
            values=["Active", "Inactive"], width=17
        ).grid(row=1, column=3)

        tk.Button(form, text="Add Student", command=self.add).grid(row=3, column=1, pady=5)
        tk.Button(form, text="Update Student", command=self.update).grid(row=3, column=3, pady=5)

        # ---------- Table ----------
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, pady=10)

        x_scroll = tk.Scrollbar(table_frame, orient="horizontal")
        x_scroll.pack(side="bottom", fill="x")

        y_scroll = tk.Scrollbar(table_frame, orient="vertical")
        y_scroll.pack(side="right", fill="y")

        self.tree = ttk.Treeview(
            table_frame,
            columns=(
                "ID",
                "Name",
                "Batch",
                "Phone",
                "Status",
                "Fee",
                # "Admission Date"
            ),
            show="headings",
            xscrollcommand=x_scroll.set,
            yscrollcommand=y_scroll.set
        )

        x_scroll.config(command=self.tree.xview)
        y_scroll.config(command=self.tree.yview)

        for col in (
            "ID",
            "Name",
            "Batch",
            "Phone",
            "Status",
            "Fee",
            # "Admission Date"
            ):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")

        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.fill_form)

        # ---------- Deactivate ----------
        bottom = tk.Frame(self.root)
        bottom.pack(pady=10)

        tk.Label(bottom, text="Student ID").grid(row=0, column=0)
        self.deactivate_id = tk.Entry(bottom)
        self.deactivate_id.grid(row=0, column=1, padx=5)

        tk.Button(bottom, text="Deactivate", command=self.deactivate).grid(row=0, column=2)

    def load_students(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for student in get_all_students():
            self.tree.insert("", "end", values=student)

    def add(self):
        try:
            add_student(
                self.name_entry.get(),
                self.batch_entry.get(),
                self.phone_entry.get(),
                int(self.total_fee_entry.get())
            )
            self.load_students()
            messagebox.showinfo("Success", "Student added")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Select", "Select a student first")
            return

        student_id = self.tree.item(selected)["values"][0]

        try:
            update_student(
                student_id,
                self.name_entry.get(),
                self.batch_entry.get(),
                self.phone_entry.get(),
                self.status_var.get(),
                int(self.total_fee_entry.get())
            )
            self.load_students()
            messagebox.showinfo("Updated", "Student updated")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def deactivate(self):
        sid = self.deactivate_id.get()
        if not sid:
            messagebox.showwarning("Input", "Enter student ID")
            return

        deactivate_student(sid)
        self.load_students()
        messagebox.showinfo("Done", "Student deactivated")

    
    def fill_form(self, event):
        selected = self.tree.focus()
        values = self.tree.item(selected)["values"]

        if not values:
            return

        self.name_entry.delete(0, tk.END)
        self.batch_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.total_fee_entry.delete(0, tk.END)
        # self.admission_date_entry.delete(0, tk.END)

        self.name_entry.insert(0, values[1])
        self.batch_entry.insert(0, values[2])
        self.phone_entry.insert(0, values[3])
        self.status_var.set(values[4])
        self.total_fee_entry.insert(0, values[5])
        # self.admission_date_entry.insert(0, values[6])