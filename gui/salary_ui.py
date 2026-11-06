import tkinter as tk
from tkinter import ttk, messagebox

from salary import (
    pay_salary,
    get_salary_by_faculty,
    get_faculty_dropdown,
    update_salary
)

class SalaryUI:

    def __init__(self, root):

        self.root = root
        self.root.title("Salary Management")
        self.root.geometry("900x600")

        self.create_widgets()
        self.load_faculty()

    def create_widgets(self):

        form = tk.Frame(self.root)
        form.pack(pady=10)

        tk.Label(form, text="Faculty ID").grid(row=0, column=0)

        self.faculty_var = tk.StringVar()

        self.faculty_combo = ttk.Combobox(
            form,
            textvariable=self.faculty_var,
            width=30,
            state="readonly"
        )

        self.faculty_combo.grid(row=0,column=1)

        tk.Label(form, text="Salary Month (YYYY-MM)").grid(row=1, column=0)

        self.salary_month_entry = tk.Entry(form)
        self.salary_month_entry.grid(row=1, column=1, padx=5)

        tk.Label(form,text="Amount").grid(row=2,column=0)

        self.amount_entry = tk.Entry(form)
        self.amount_entry.grid(row=2,column=1)

        tk.Button(form, text="Pay Salary", command=self.pay_salary)\
            .grid(row=4, column=0, pady=10)

        tk.Button(form, text="Update Salary", command=self.update_salary)\
            .grid(row=4, column=2, pady=10)

        tk.Button(form, text="Load Salary", command=self.load_salary)\
            .grid(row=4, column=1, pady=10)

        table_frame = tk.Frame(self.root)
        table_frame.pack(fill="both",expand=True)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("ID","FacultyID","Name","Month","Amount","Date"),
            show="headings"
        )

        self.tree.pack(fill="both",expand=True)

        cols=("ID","FacultyID","Name","Month","Amount","Date")

        for c in cols:
            self.tree.heading(c,text=c)
            self.tree.column(c,width=120,anchor="center")
        
        self.tree.bind("<<TreeviewSelect>>", self.fill_form)

    def load_faculty(self):
        faculty = get_faculty_dropdown()
        self.faculty_map = {}
        values=[]

        for fid,name in faculty:
            text=f"{fid} - {name}"
            values.append(text)
            self.faculty_map[text]=fid

        self.faculty_combo["values"]=values

    def pay_salary(self):

        try:
        
            selected = self.faculty_combo.get()
    
            if not selected:
                messagebox.showwarning("Input Error", "Select Faculty")
                return
    
            faculty_id = self.faculty_map[selected]
    
            month = self.salary_month_entry.get().strip()
            amount_text = self.amount_entry.get().strip()
    
            if not month or not amount_text:
                messagebox.showwarning("Input Error", "Month and Amount required")
                return
    
            if not amount_text.isdigit():
                messagebox.showerror("Error", "Amount must be a number")
                return
    
            amount = int(amount_text)
    
            pay_salary(faculty_id, month, amount)
    
            self.load_salary()
    
            messagebox.showinfo("Success", "Salary paid successfully")
    
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_salary(self):

        selected = self.faculty_combo.get()

        if not selected:
            messagebox.showwarning("Input", "Select faculty first")
            return

        faculty_id = self.faculty_map[selected]

        for row in self.tree.get_children():
            self.tree.delete(row)

        for row in get_salary_by_faculty(faculty_id):
            self.tree.insert("", "end", values=row)

    def update_salary(self):

        selected = self.tree.focus()

        if not selected:
            messagebox.showwarning("Select", "Select salary record first")
            return

        values = self.tree.item(selected)["values"]

        salary_id = values[0]

        try:
            update_salary(
                salary_id,
                int(self.amount_entry.get())
            )

            self.load_salary()

            messagebox.showinfo("Updated", "Salary updated successfully")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    

    def fill_form(self, event):

        selected = self.tree.focus()
        values = self.tree.item(selected)["values"]

        if not values:
            return

        
        self.salary_month_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)

        self.salary_month_entry.insert(0, values[3])
        self.amount_entry.insert(0, values[4])