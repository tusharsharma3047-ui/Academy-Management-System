import tkinter as tk
from tkinter import ttk, messagebox

from fees import (
    add_fee,
    update_fee,
    get_pending_fees,
    get_fees_by_student,
    get_students_for_dropdown
)

class FeesUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Fees Management")
        self.root.geometry("900x600")

        self.selected_fee_id = None

        self.create_widgets()
        self.load_students()

    def create_widgets(self):

        form = tk.Frame(self.root)
        form.pack(pady=10)

        tk.Label(form, text="Student").grid(row=0, column=0)

        self.student_var = tk.StringVar()

        self.student_combo = ttk.Combobox(
            form,
            textvariable=self.student_var,
            width=30,
            state="readonly"
        )
        self.student_combo.grid(row=0, column=1)

        tk.Label(form,text="Fee Month").grid(row=3,column=0)

        self.month_entry=tk.Entry(form)

        self.month_entry.grid(row=3,column=1)

        tk.Label(form, text="Amount").grid(row=0, column=2)

        self.amount_entry = tk.Entry(form)
        self.amount_entry.grid(row=0, column=3)

        tk.Label(form, text="Payment Mode").grid(row=1, column=0)

        self.mode_var = tk.StringVar(value="Cash")

        ttk.Combobox(
            form,
            textvariable=self.mode_var,
            values=["Cash","UPI","Card","Bank Transfer"],
            state="readonly"
        ).grid(row=1, column=1)

        tk.Label(form, text="Remarks").grid(row=1, column=2)

        self.remarks_entry = tk.Entry(form)
        self.remarks_entry.grid(row=1, column=3)

        tk.Button(form,text="Add Payment",command=self.add_payment)\
            .grid(row=2,column=0,pady=10)

        tk.Button(form,text="Update Payment",command=self.update_payment)\
            .grid(row=2,column=2)

        tk.Button(form,text="Load Fees",command=self.load_fees)\
            .grid(row=2,column=1)

        self.pending_label = tk.Label(
            self.root,
            text="Pending Fees: ₹0",
            font=("Arial",12,"bold")
        )

        self.pending_label.pack(pady=5)

        table_frame = tk.Frame(self.root)
        table_frame.pack(fill="both",expand=True)

        x_scroll = tk.Scrollbar(table_frame,orient="horizontal")
        y_scroll = tk.Scrollbar(table_frame,orient="vertical")

        x_scroll.pack(side="bottom",fill="x")
        y_scroll.pack(side="right",fill="y")

        self.tree = ttk.Treeview(
            table_frame,
            columns=(
                "Fee ID",
                "Student ID",
                "Name",
                "Fee Month",
                "Amount",
                "Payment Date",
                "Payment Mode",
                "Remarks"
            ),
            show="headings",
            xscrollcommand=x_scroll.set,
            yscrollcommand=y_scroll.set
        )

        x_scroll.config(command=self.tree.xview)
        y_scroll.config(command=self.tree.yview)

        self.tree.pack(fill="both",expand=True)

        cols = (
            "Fee ID",
            "Student ID",
            "Name",
            "Fee Month",
            "Amount",
            "Payment Date",
            "Payment Mode",
            "Remarks"
        )

        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=120, anchor="center")

        self.tree.bind("<<TreeviewSelect>>", self.fill_form)

    # ---------- Load Students ----------
    def load_students(self):

        students = get_students_for_dropdown()

        self.student_map = {}

        values = []

        for sid,name in students:
            text = f"{sid} - {name}"
            values.append(text)
            self.student_map[text] = sid

        self.student_combo["values"] = values

    # ---------- Add ----------
    def add_payment(self):

        try:

            selected = self.student_combo.get()

            if not selected:
                messagebox.showwarning("Select","Select student")
                return

            student_id = self.student_map[selected]

            amount = int(self.amount_entry.get())

            add_fee(
                student_id,
                self.month_entry.get(),
                amount,
                self.mode_var.get(),
                self.remarks_entry.get()
            )

            self.load_fees()

            messagebox.showinfo("Success","Fee added")

        except Exception as e:
            messagebox.showerror("Error",str(e))

    # ---------- Update ----------
    
        # ---------- Update ----------
    def update_payment(self):

        if not self.selected_fee_id:
            messagebox.showwarning(
                "Select",
                "Select fee record first"
            )
            return

        try:

            fee_month = self.month_entry.get().strip()
            amount_text = self.amount_entry.get().strip()

            if not fee_month:
                messagebox.showwarning(
                    "Input",
                    "Enter fee month"
                )
                return

            if not amount_text:
                messagebox.showwarning(
                    "Input",
                    "Enter amount"
                )
                return

            amount = int(amount_text)

            update_fee(
                self.selected_fee_id,
                fee_month,
                amount,
                self.mode_var.get(),
                self.remarks_entry.get().strip()
            )

            self.load_fees()

            messagebox.showinfo(
                "Updated",
                "Fee updated successfully"
            )

        except ValueError:
            messagebox.showerror(
                "Error",
                "Amount must be a valid number"
            )

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )

            
    # ---------- Load ----------
    def load_fees(self):

        selected = self.student_combo.get()

        if not selected:
            return

        student_id = self.student_map[selected]

        for row in self.tree.get_children():
            self.tree.delete(row)

        for row in get_fees_by_student(student_id):
            self.tree.insert("", "end", values=row)

        pending = get_pending_fees(student_id)

        self.pending_label.config(text=f"Pending Fees: ₹{pending}")

    # ---------- Fill Form ----------
    def fill_form(self, event):

        selected = self.tree.focus()

        if not selected:
            return

        values = self.tree.item(selected)["values"]

        self.selected_fee_id = values[0]

        self.month_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.remarks_entry.delete(0, tk.END)

        self.month_entry.insert(0, values[3])
        self.amount_entry.insert(0, values[4])
        self.mode_var.set(values[6])
        self.remarks_entry.insert(0, values[7])