from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3

class Employee:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title('Employee Management System')
        self.root.configure(bg='#f0f0f0')

        # Title
        title_frame = Frame(self.root, bg='#4A90E2', bd=2, relief=RIDGE)
        title_frame.place(x=0, y=0, width=1530, height=60)
        lbl_title = Label(title_frame, text='Employee Management System',
                          font=('Poppins', 30, 'bold'),
                          fg='white', bg='#4A90E2')
        lbl_title.pack(fill=BOTH, pady=10)

        # Database setup
        self.db_connect()

        # Frame for employee form
        form_frame = Frame(self.root, bd=2, relief=RIDGE, bg='white', padx=20, pady=20)
        form_frame.place(x=10, y=80, width=500, height=700)

        # Labels and Entries
        self.setup_form(form_frame)

        # Buttons
        self.setup_buttons(form_frame)

        # Frame for displaying employee data
        data_frame = Frame(self.root, bd=2, relief=RIDGE, bg='white')
        data_frame.place(x=520, y=80, width=1000, height=700)

        # Employee Data Table
        self.setup_data_table(data_frame)

        # Fetch data to display in the table
        self.fetch_data()

    def db_connect(self):
        self.conn = sqlite3.connect("employee.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT,
                gender TEXT,
                contact TEXT,
                dob TEXT,
                address TEXT
            )
        """)
        self.conn.commit()

    def setup_form(self, frame):
        self.name_var = StringVar()
        self.email_var = StringVar()
        self.gender_var = StringVar()
        self.contact_var = StringVar()
        self.dob_var = StringVar()
        self.address_var = StringVar()

        lbl_name = Label(frame, text='Name', font=('Poppins', 15), bg='white')
        lbl_name.grid(row=0, column=0, pady=10, padx=10, sticky='w')
        txt_name = Entry(frame, textvariable=self.name_var, font=('Poppins', 15), bd=2, relief=GROOVE, width=25)
        txt_name.grid(row=0, column=1, pady=10, padx=10, sticky='w')

        lbl_email = Label(frame, text='Email', font=('Poppins', 15), bg='white')
        lbl_email.grid(row=1, column=0, pady=10, padx=10, sticky='w')
        txt_email = Entry(frame, textvariable=self.email_var, font=('Poppins', 15), bd=2, relief=GROOVE, width=25)
        txt_email.grid(row=1, column=1, pady=10, padx=10, sticky='w')

        lbl_gender = Label(frame, text='Gender', font=('Poppins', 15), bg='white')
        lbl_gender.grid(row=2, column=0, pady=10, padx=10, sticky='w')
        combo_gender = ttk.Combobox(frame, textvariable=self.gender_var, font=('Poppins', 13), state='readonly', width=23)
        combo_gender['values'] = ("Male", "Female", "Other")
        combo_gender.grid(row=2, column=1, pady=10, padx=10)

        lbl_contact = Label(frame, text='Contact No.', font=('Poppins', 15), bg='white')
        lbl_contact.grid(row=3, column=0, pady=10, padx=10, sticky='w')
        txt_contact = Entry(frame, textvariable=self.contact_var, font=('Poppins', 15), bd=2, relief=GROOVE, width=25)
        txt_contact.grid(row=3, column=1, pady=10, padx=10, sticky='w')

        lbl_dob = Label(frame, text='D.O.B', font=('Poppins', 15), bg='white')
        lbl_dob.grid(row=4, column=0, pady=10, padx=10, sticky='w')
        txt_dob = Entry(frame, textvariable=self.dob_var, font=('Poppins', 15), bd=2, relief=GROOVE, width=25)
        txt_dob.grid(row=4, column=1, pady=10, padx=10, sticky='w')

        lbl_address = Label(frame, text='Address', font=('Poppins', 15), bg='white')
        lbl_address.grid(row=5, column=0, pady=10, padx=10, sticky='w')
        self.txt_address = Text(frame, width=30, height=4, font=('Poppins', 15), bd=2, relief=GROOVE)
        self.txt_address.grid(row=5, column=1, pady=10, padx=10, sticky='w')

    def setup_buttons(self, frame):
        btn_frame = Frame(frame, bd=2, relief=RIDGE, bg='white')
        btn_frame.place(x=10, y=380, width=480, height=50)

        btn_add = Button(btn_frame, text='Add', command=self.add_employee, font=('Poppins', 12), bg='#4A90E2', fg='white', width=10)
        btn_add.grid(row=0, column=0, padx=10, pady=10)

        btn_update = Button(btn_frame, text='Update', command=self.update_employee, font=('Poppins', 12), bg='#E94E77', fg='white', width=10)
        btn_update.grid(row=0, column=1, padx=10, pady=10)

        btn_delete = Button(btn_frame, text='Delete', command=self.delete_employee, font=('Poppins', 12), bg='#D32F2F', fg='white', width=10)
        btn_delete.grid(row=0, column=2, padx=10, pady=10)

        btn_clear = Button(btn_frame, text='Clear', command=self.clear_form, font=('Poppins', 12), bg='#7B1FA2', fg='white', width=10)
        btn_clear.grid(row=0, column=3, padx=10, pady=10)

    def setup_data_table(self, frame):
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Poppins', 12, 'bold'), foreground='#333')
        style.configure("Treeview", font=('Poppins', 11), rowheight=25)
        style.map("Treeview", background=[("selected", '#E6E6E6')])

        self.tree = ttk.Treeview(frame, columns=("ID", "Name", "Email", "Gender", "Contact", "DOB", "Address"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Gender", text="Gender")
        self.tree.heading("Contact", text="Contact")
        self.tree.heading("DOB", text="DOB")
        self.tree.heading("Address", text="Address")
        self.tree.column("ID", width=50, anchor='center')
        self.tree.column("Name", width=150, anchor='w')
        self.tree.column("Email", width=200, anchor='w')
        self.tree.column("Gender", width=100, anchor='center')
        self.tree.column("Contact", width=150, anchor='center')
        self.tree.column("DOB", width=100, anchor='center')
        self.tree.column("Address", width=200, anchor='w')

        self.tree.pack(fill=BOTH, expand=1)
        self.tree.bind("<ButtonRelease-1>", self.get_cursor)

    def add_employee(self):
        if self.name_var.get() == "" or self.email_var.get() == "":
            messagebox.showerror("Error", "All fields are required!")
            return

        self.cursor.execute("""
            INSERT INTO employees (name, email, gender, contact, dob, address)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            self.name_var.get(),
            self.email_var.get(),
            self.gender_var.get(),
            self.contact_var.get(),
            self.dob_var.get(),
            self.txt_address.get('1.0', END).strip()
        ))
        self.conn.commit()
        self.fetch_data()
        self.clear_form()
        messagebox.showinfo("Success", "Employee added successfully!")

    def fetch_data(self):
        self.cursor.execute("SELECT * FROM employees")
        rows = self.cursor.fetchall()
        if len(rows) != 0:
            self.tree.delete(*self.tree.get_children())
            for row in rows:
                self.tree.insert('', END, values=row)

    def clear_form(self):
        self.name_var.set("")
        self.email_var.set("")
        self.gender_var.set("")
        self.contact_var.set("")
        self.dob_var.set("")
        self.txt_address.delete('1.0', END)

    def get_cursor(self, event):
        cursor_row = self.tree.focus()
        contents = self.tree.item(cursor_row)
        row = contents['values']
        self.name_var.set(row[1])
        self.email_var.set(row[2])
        self.gender_var.set(row[3])
        self.contact_var.set(row[4])
        self.dob_var.set(row[5])
        self.txt_address.delete('1.0', END)
        self.txt_address.insert(END, row[6])

    def update_employee(self):
        cursor_row = self.tree.focus()
        contents = self.tree.item(cursor_row)
        row = contents['values']

        self.cursor.execute("""
            UPDATE employees SET 
            name=?, email=?, gender=?, contact=?, dob=?, address=?
            WHERE id=?
        """, (
            self.name_var.get(),
            self.email_var.get(),
            self.gender_var.get(),
            self.contact_var.get(),
            self.dob_var.get(),
            self.txt_address.get('1.0', END).strip(),
            row[0]
        ))
        self.conn.commit()
        self.fetch_data()
        self.clear_form()
        messagebox.showinfo("Success", "Employee updated successfully!")

    def delete_employee(self):
        cursor_row = self.tree.focus()
        contents = self.tree.item(cursor_row)
        row = contents['values']

        self.cursor.execute("DELETE FROM employees WHERE id=?", (row[0],))
        self.conn.commit()
        self.fetch_data()
        self.clear_form()
        messagebox.showinfo("Success", "Employee deleted successfully!")

if __name__ == "__main__":
    root = Tk()
    obj = Employee(root)
    root.mainloop()
