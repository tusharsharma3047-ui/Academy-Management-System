import tkinter as tk
from tkinter import ttk, messagebox

from faculty import (
    add_faculty,
    get_all_faculty,
    deactivate_faculty,
    update_faculty
)

class FacultyUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Faculty Management")
        self.root.geometry("750x600")

        self.create_widgets()
        self.load_faculty()

    def create_widgets(self):
        # ---------- Form ----------
        form = tk.Frame(self.root)
        form.pack(pady=10)

        tk.Label(form, text="Name").grid(row=0, column=0)
        tk.Label(form, text="Phone").grid(row=0, column=2)
        tk.Label(form, text="Specialization").grid(row=1, column=0)
        tk.Label(form, text="Monthly Salary").grid(row=1, column=2)
        tk.Label(form, text="Status").grid(row=2, column=0)

        self.status_var = tk.StringVar(value="Active")
        ttk.Combobox(
            form,
            textvariable=self.status_var,
            values=["Active", "Inactive"],
            width=17,
            state="readonly"
        ).grid(row=2, column=1)

        self.name_entry = tk.Entry(form)
        self.phone_entry = tk.Entry(form)
        self.spec_entry = tk.Entry(form)
        self.salary_entry = tk.Entry(form)

        self.name_entry.grid(row=0, column=1, padx=5)
        self.phone_entry.grid(row=0, column=3, padx=5)
        self.spec_entry.grid(row=1, column=1, padx=5)
        self.salary_entry.grid(row=1, column=3, padx=5)

        tk.Button(form, text="Add Faculty", command=self.add).grid(row=3, column=1, pady=5)
        tk.Button(form, text="Update Faculty", command=self.update).grid(row=3, column=3, pady=5)

        # ---------- Table ----------
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, pady=10)

        x_scroll = tk.Scrollbar(table_frame, orient="horizontal")
        x_scroll.pack(side="bottom", fill="x")

        y_scroll = tk.Scrollbar(table_frame, orient="vertical")
        y_scroll.pack(side="right", fill="y")

        self.tree = ttk.Treeview(
            table_frame,
            columns=("ID", "Name", "Phone", "Specialization", "Salary", "Status", "Join Date", "End Date"),
            show="headings",
            xscrollcommand=x_scroll.set,
            yscrollcommand=y_scroll.set
        )

        x_scroll.config(command=self.tree.xview)
        y_scroll.config(command=self.tree.yview)

        for col in ("ID", "Name", "Phone", "Specialization", "Salary", "Status", "Join Date", "End Date"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")

        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.fill_form)

        # ---------- Deactivate ----------
        bottom = tk.Frame(self.root)
        bottom.pack(pady=10)

        tk.Label(bottom, text="Faculty ID").grid(row=0, column=0)
        self.deactivate_id = tk.Entry(bottom)
        self.deactivate_id.grid(row=0, column=1, padx=5)

        tk.Button(bottom, text="Deactivate", command=self.deactivate).grid(row=0, column=2)

    def load_faculty(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for faculty in get_all_faculty():
            self.tree.insert("", "end", values=faculty)

    def add(self):
        try:
            add_faculty(
                self.name_entry.get(),
                self.phone_entry.get(),
                self.spec_entry.get(),
                int(self.salary_entry.get())
            )
            self.load_faculty()
            messagebox.showinfo("Success", "Faculty added")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Select", "Select a faculty first")
            return

        faculty_id = self.tree.item(selected)["values"][0]

        try:
            update_faculty(
                faculty_id,
                self.name_entry.get(),
                self.phone_entry.get(),
                self.spec_entry.get(),
                int(self.salary_entry.get()),
                self.status_var.get()
            )
            self.load_faculty()
            messagebox.showinfo("Updated", "Faculty updated")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def deactivate(self):
        fid = self.deactivate_id.get()
        if not fid:
            messagebox.showwarning("Input", "Enter faculty ID")
            return

        try:
            deactivate_faculty(fid)
            self.load_faculty()
            messagebox.showinfo("Done", "Faculty deactivated")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def fill_form(self, event):
        selected = self.tree.focus()
        values = self.tree.item(selected)["values"]

        if not values:
            return

        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.spec_entry.delete(0, tk.END)
        self.salary_entry.delete(0, tk.END)

        self.name_entry.insert(0, values[1])
        self.phone_entry.insert(0, values[2])
        self.spec_entry.insert(0, values[3])
        self.salary_entry.insert(0, values[4])
        self.status_var.set(values[5])