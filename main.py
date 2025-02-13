import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class SchoolManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("School Management System")
        self.root.geometry("1200x700")
        self.root.config(bg="#F0F0F0")
        
        self.is_dark_theme = False
        
        # Store user data
        self.students = {
            "240265": {"name": "Aagaman Koirala", "password": "aagaman"}
        }
        self.teachers = {
            "240240": {"name": "Ram Nepali", "password": "teacher123", "subject": "Math"},
            "240241": {"name": "Chris Brown", "password": "teacher123", "subject": "Python"},
            "240242": {"name": "Shyam Pandit", "password": "teacher123", "subject": "Software Design"}
        }
        
        # Store attendance data with student IDs and subjects
        self.attendance_data = {}  # Format: {date: {subject: {student_id: status}}}
        
        self.routine_data = [
            ("10:30 AM", "Python", "Python", "Python", "Python", "Python"),
            ("12:30 PM", "Math", "Math", "Math", "Math", "Math"),
            ("2:30 PM", "Software Design", "Software Design", "Software Design", "Software Design", "Software Design")
        ]
        
        # Initialize login frame
        self.login_frame = tk.Frame(root, bg="#FFFFFF", bd=2, relief="groove")
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=300)
        
        # Theme button
        self.theme_button = tk.Button(root, text="Dark Theme", font=("Arial", 12), 
                                    bg="#E0E0E0", fg="#000000", command=self.toggle_theme)
        self.theme_button.place(relx=0.95, rely=0.05, anchor="ne")
        
        self.show_main_login()

    def apply_theme_to_window(self, window):
        if self.is_dark_theme:
            window.config(bg="#2E2E2E")
            for widget in window.winfo_children():
                if isinstance(widget, tk.Frame):
                    widget.config(bg="#3E3E3E")
                elif isinstance(widget, tk.Label):
                    widget.config(bg="#3E3E3E", fg="#FFFFFF")
                elif isinstance(widget, tk.Button):
                    widget.config(bg="#505050", fg="#FFFFFF")
        else:
            window.config(bg="#F0F0F0")
            for widget in window.winfo_children():
                if isinstance(widget, tk.Frame):
                    widget.config(bg="#FFFFFF")
                elif isinstance(widget, tk.Label):
                    widget.config(bg="#FFFFFF", fg="#000000")
                elif isinstance(widget, tk.Button):
                    widget.config(bg="#E0E0E0", fg="#000000")

    def student_dashboard(self, student_id):
        dashboard = tk.Toplevel(self.root)
        dashboard.title(f"Student Dashboard - {self.students[student_id]['name']}")
        dashboard.geometry("1200x700")
        
        # Apply theme
        self.apply_theme_to_window(dashboard)

        fullscreen_btn = tk.Button(dashboard, text="Toggle Fullscreen", 
                                 command=lambda: self.toggle_fullscreen(dashboard))
        fullscreen_btn.pack(anchor="ne", padx=10, pady=10)

        notebook = ttk.Notebook(dashboard)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Routine Tab
        routine_frame = ttk.Frame(notebook)
        notebook.add(routine_frame, text="Class Routine")
        
        routine_tree = ttk.Treeview(routine_frame, 
                                  columns=("Time", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"), 
                                  show="headings")
        
        for col in routine_tree["columns"]:
            routine_tree.heading(col, text=col)
            routine_tree.column(col, width=150)

        for item in self.routine_data:
            routine_tree.insert("", "end", values=item)
        
        routine_tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Attendance Tab
        attendance_frame = ttk.Frame(notebook)
        notebook.add(attendance_frame, text="Attendance")
        
        attendance_label = tk.Label(attendance_frame, text="Attendance Record", 
                                  font=("Arial", 16, "bold"))
        attendance_label.pack(pady=20)
        
        attendance_tree = ttk.Treeview(attendance_frame, columns=("Date", "Subject", "Status"), 
                                     show="headings")
        attendance_tree.heading("Date", text="Date")
        attendance_tree.heading("Subject", text="Subject")
        attendance_tree.heading("Status", text="Status")
        
        # Show student's attendance
        for date, subjects in self.attendance_data.items():
            for subject, records in subjects.items():
                if student_id in records:
                    attendance_tree.insert("", "end", values=(date, subject, records[student_id]))
        
        attendance_tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Teacher Contacts Tab
        contacts_frame = ttk.Frame(notebook)
        notebook.add(contacts_frame, text="Teacher Contacts")
        
        contacts_label = tk.Label(contacts_frame, text="Teacher Contact Information", 
                                font=("Arial", 16, "bold"))
        contacts_label.pack(pady=20)
        
        for teacher_id, teacher_data in self.teachers.items():
            contact_frame = tk.Frame(contacts_frame, relief="solid", bd=1)
            contact_frame.pack(fill="x", padx=20, pady=5)
            
            teacher_info = f"{teacher_data['name']} - {teacher_data['subject']}"
            tk.Label(contact_frame, text=teacher_info, font=("Arial", 12, "bold")).pack(side="left", padx=10, pady=5)

    def teacher_dashboard(self, teacher_id):
        dashboard = tk.Toplevel(self.root)
        teacher_data = self.teachers[teacher_id]
        dashboard.title(f"Teacher Dashboard - {teacher_data['name']} ({teacher_data['subject']})")
        dashboard.geometry("1200x700")
        
        # Apply theme
        self.apply_theme_to_window(dashboard)

        fullscreen_btn = tk.Button(dashboard, text="Toggle Fullscreen", 
                                 command=lambda: self.toggle_fullscreen(dashboard))
        fullscreen_btn.pack(anchor="ne", padx=10, pady=10)

        notebook = ttk.Notebook(dashboard)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Manage Attendance Tab
        attendance_frame = ttk.Frame(notebook)
        notebook.add(attendance_frame, text=f"Manage {teacher_data['subject']} Attendance")
        
        # Add attendance
        tk.Label(attendance_frame, text=f"Mark {teacher_data['subject']} Attendance", 
                font=("Arial", 16, "bold")).pack(pady=20)
        
        date_frame = tk.Frame(attendance_frame)
        date_frame.pack(fill="x", padx=20, pady=5)
        
        tk.Label(date_frame, text="Date:").pack(side="left", padx=5)
        date_entry = tk.Entry(date_frame)
        date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        date_entry.pack(side="left", padx=5)
        
        # Student list for attendance
        students_frame = tk.Frame(attendance_frame)
        students_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        tk.Label(students_frame, text="Students", font=("Arial", 14, "bold")).pack(pady=10)
        
        for student_id, student_data in self.students.items():
            student_frame = tk.Frame(students_frame)
            student_frame.pack(fill="x", pady=5)
            
            tk.Label(student_frame, text=f"{student_data['name']} ({student_id})").pack(side="left", padx=5)
            
            status_var = tk.StringVar(value="Present")
            tk.Radiobutton(student_frame, text="Present", variable=status_var, 
                          value="Present").pack(side="left", padx=5)
            tk.Radiobutton(student_frame, text="Absent", variable=status_var, 
                          value="Absent").pack(side="left", padx=5)
            
            def mark_attendance(sid=student_id, status_v=status_var):
                date = date_entry.get()
                if date not in self.attendance_data:
                    self.attendance_data[date] = {}
                if teacher_data['subject'] not in self.attendance_data[date]:
                    self.attendance_data[date][teacher_data['subject']] = {}
                self.attendance_data[date][teacher_data['subject']][sid] = status_v.get()
                messagebox.showinfo("Success", f"Attendance marked for {self.students[sid]['name']}")
            
            tk.Button(student_frame, text="Mark", 
                     command=mark_attendance).pack(side="right", padx=5)

    def admin_dashboard(self):
        dashboard = tk.Toplevel(self.root)
        dashboard.title("Admin Dashboard")
        dashboard.geometry("1200x700")
        
        # Apply theme
        self.apply_theme_to_window(dashboard)

        fullscreen_btn = tk.Button(dashboard, text="Toggle Fullscreen", 
                                 command=lambda: self.toggle_fullscreen(dashboard))
        fullscreen_btn.pack(anchor="ne", padx=10, pady=10)

        notebook = ttk.Notebook(dashboard)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Manage Students Tab
        students_frame = ttk.Frame(notebook)
        notebook.add(students_frame, text="Manage Students")
        
        # Student List
        list_frame = tk.Frame(students_frame)
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        tk.Label(list_frame, text="Current Students", 
                font=("Arial", 16, "bold")).pack(pady=10)
        
        students_tree = ttk.Treeview(list_frame, columns=("ID", "Name", "Password"), 
                                   show="headings")
        students_tree.heading("ID", text="Student ID")
        students_tree.heading("Name", text="Name")
        students_tree.heading("Password", text="Password")
        
        for student_id, data in self.students.items():
            students_tree.insert("", "end", values=(student_id, data["name"], data["password"]))
        
        students_tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add Student Form
        form_frame = tk.Frame(students_frame)
        form_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(form_frame, text="Add New Student", 
                font=("Arial", 14, "bold")).pack(pady=10)
        
        tk.Label(form_frame, text="Student ID:").pack()
        student_id_entry = tk.Entry(form_frame)
        student_id_entry.pack()
        
        tk.Label(form_frame, text="Name:").pack()
        student_name_entry = tk.Entry(form_frame)
        student_name_entry.pack()
        
        tk.Label(form_frame, text="Password:").pack()
        student_password_entry = tk.Entry(form_frame)
        student_password_entry.pack()
        
        def add_student():
            student_id = student_id_entry.get()
            name = student_name_entry.get()
            password = student_password_entry.get()
            
            if not student_id or not name or not password:
                messagebox.showerror("Error", "Please fill all fields")
                return
            
            if student_id in self.students:
                messagebox.showerror("Error", "Student ID already exists")
                return
            
            self.students[student_id] = {"name": name, "password": password}
            students_tree.insert("", "end", values=(student_id, name, password))
            
            # Clear entries
            student_id_entry.delete(0, tk.END)
            student_name_entry.delete(0, tk.END)
            student_password_entry.delete(0, tk.END)
            
            messagebox.showinfo("Success", "Student added successfully!")
        
        tk.Button(form_frame, text="Add Student", 
                 command=add_student).pack(pady=10)

        # Manage Teachers Tab
        teachers_frame = ttk.Frame(notebook)
        notebook.add(teachers_frame, text="Manage Teachers")
        
        # Teacher List
        teacher_list_frame = tk.Frame(teachers_frame)
        teacher_list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        tk.Label(teacher_list_frame, text="Current Teachers", 
                font=("Arial", 16, "bold")).pack(pady=10)
        
        teachers_tree = ttk.Treeview(teacher_list_frame, columns=("ID", "Name", "Subject", "Password"), 
                                   show="headings")
        teachers_tree.heading("ID", text="Teacher ID")
        teachers_tree.heading("Name", text="Name")
        teachers_tree.heading("Subject", text="Subject")
        teachers_tree.heading("Password", text="Password")
        
        for teacher_id, data in self.teachers.items():
            teachers_tree.insert("", "end", values=(teacher_id, data["name"], data["subject"], data["password"]))
        
        teachers_tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add Teacher Form
        teacher_form_frame = tk.Frame(teachers_frame)
        teacher_form_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(teacher_form_frame, text="Add New Teacher", 
                font=("Arial", 14, "bold")).pack(pady=10)
        
        tk.Label(teacher_form_frame, text="Teacher ID:").pack()
        teacher_id_entry = tk.Entry(teacher_form_frame)
        teacher_id_entry.pack()
        
        tk.Label(teacher_form_frame, text="Name:").pack()
        teacher_name_entry = tk.Entry(teacher_form_frame)
        teacher_name_entry.pack()
        
        tk.Label(teacher_form_frame, text="Subject:").pack()
        teacher_subject_entry = tk.Entry(teacher_form_frame)
        teacher_subject_entry.pack()
        
        tk.Label(teacher_form_frame, text="Password:").pack()
        teacher_password_entry = tk.Entry(teacher_form_frame)
        teacher_password_entry.pack()
        
        def add_teacher():
            teacher_id = teacher_id_entry.get()
            name = teacher_name_entry.get()
            subject = teacher_subject_entry.get()
            password = teacher_password_entry.get()
            
            if not teacher_id or not name or not subject or not password:
                messagebox.showerror("Error", "Please fill all fields")
                return
            
            if teacher_id in self.teachers:
                messagebox.showerror("Error", "Teacher ID already exists")
                return
            
            self.teachers[teacher_id] = {
                "name": name,
                "subject": subject,
                "password": password
            }
            teachers_tree.insert("", "end", values=(teacher_id, name, subject, password))
            
            # Clear entries
            teacher_id_entry.delete(0, tk.END)
            teacher_name_entry.delete(0, tk.END)
            teacher_subject_entry.delete(0, tk.END)
            teacher_password_entry.delete(0, tk.END)
            
            messagebox.showinfo("Success", "Teacher added successfully!")
        
        tk.Button(teacher_form_frame, text="Add Teacher", 
                 command=add_teacher).pack(pady=10)

    def toggle_fullscreen(self, window):
        window.attributes('-fullscreen', not window.attributes('-fullscreen'))
        
    def toggle_theme(self):
        self.is_dark_theme = not self.is_dark_theme
        if self.is_dark_theme:
            self.root.config(bg="#2E2E2E")
            self.login_frame.config(bg="#3E3E3E")
            self.theme_button.config(text="Light Theme", bg="#505050", fg="#FFFFFF")
        else:
            self.root.config(bg="#F0F0F0")
            self.login_frame.config(bg="#FFFFFF")
            self.theme_button.config(text="Dark Theme", bg="#E0E0E0", fg="#000000")

    def student_login(self):
        for widget in self.login_frame.winfo_children():
            widget.destroy()

        tk.Label(self.login_frame, text="Student Login", font=("Arial", 20, "bold"), 
                bg=self.login_frame["bg"]).pack(pady=10)

        tk.Label(self.login_frame, text="Student ID:", font=("Arial", 14), 
                bg=self.login_frame["bg"]).pack(pady=5)
        student_id_entry = tk.Entry(self.login_frame, font=("Arial", 14))
        student_id_entry.pack(pady=5)

        tk.Label(self.login_frame, text="Password:", font=("Arial", 14), 
                bg=self.login_frame["bg"]).pack(pady=5)
        student_password_entry = tk.Entry(self.login_frame, font=("Arial", 14), show="*")
        student_password_entry.pack(pady=5)

        def submit_student_login():
            student_id = student_id_entry.get()
            student_password = student_password_entry.get()
            if (student_id in self.students and 
                self.students[student_id]["password"] == student_password):
                self.student_dashboard(student_id)
            else:
                messagebox.showerror("Error", "Invalid Student ID or Password!")

        tk.Button(self.login_frame, text="Submit", font=("Arial", 14), 
                 command=submit_student_login).pack(pady=10)
        tk.Button(self.login_frame, text="Back", font=("Arial", 14), 
                 command=self.show_main_login).pack(pady=10)

    def teacher_login(self):
        for widget in self.login_frame.winfo_children():
            widget.destroy()

        tk.Label(self.login_frame, text="Teacher Login", font=("Arial", 20, "bold"), 
                bg=self.login_frame["bg"]).pack(pady=10)

        tk.Label(self.login_frame, text="Teacher ID:", font=("Arial", 14), 
                bg=self.login_frame["bg"]).pack(pady=5)
        teacher_id_entry = tk.Entry(self.login_frame, font=("Arial", 14))
        teacher_id_entry.pack(pady=5)

        tk.Label(self.login_frame, text="Password:", font=("Arial", 14), 
                bg=self.login_frame["bg"]).pack(pady=5)
        teacher_password_entry = tk.Entry(self.login_frame, font=("Arial", 14), show="*")
        teacher_password_entry.pack(pady=5)

        def submit_teacher_login():
            teacher_id = teacher_id_entry.get()
            teacher_password = teacher_password_entry.get()
            if (teacher_id in self.teachers and 
                self.teachers[teacher_id]["password"] == teacher_password):
                self.teacher_dashboard(teacher_id)
            else:
                messagebox.showerror("Error", "Invalid Teacher ID or Password!")

        tk.Button(self.login_frame, text="Submit", font=("Arial", 14), 
                 command=submit_teacher_login).pack(pady=10)
        tk.Button(self.login_frame, text="Back", font=("Arial", 14), 
                 command=self.show_main_login).pack(pady=10)

    def admin_login(self):
        for widget in self.login_frame.winfo_children():
            widget.destroy()

        tk.Label(self.login_frame, text="Admin Login", font=("Arial", 20, "bold"), 
                bg=self.login_frame["bg"]).pack(pady=10)

        tk.Label(self.login_frame, text="Admin ID:", font=("Arial", 14), 
                bg=self.login_frame["bg"]).pack(pady=5)
        admin_id_entry = tk.Entry(self.login_frame, font=("Arial", 14))
        admin_id_entry.pack(pady=5)

        tk.Label(self.login_frame, text="Password:", font=("Arial", 14), 
                bg=self.login_frame["bg"]).pack(pady=5)
        admin_password_entry = tk.Entry(self.login_frame, font=("Arial", 14), show="*")
        admin_password_entry.pack(pady=5)

        def submit_admin_login():
            admin_id = admin_id_entry.get()
            admin_password = admin_password_entry.get()
            if admin_id == "123" and admin_password == "admin":
                self.admin_dashboard()
            else:
                messagebox.showerror("Error", "Invalid Admin ID or Password!")

        tk.Button(self.login_frame, text="Submit", font=("Arial", 14), 
                 command=submit_admin_login).pack(pady=10)
        tk.Button(self.login_frame, text="Back", font=("Arial", 14), 
                 command=self.show_main_login).pack(pady=10)

    def show_main_login(self):
        for widget in self.login_frame.winfo_children():
            widget.destroy()

        title_label = tk.Label(self.login_frame, text="Login", font=("Arial", 24, "bold"), 
                              bg="#FFFFFF", fg="#000000")
        title_label.pack(pady=20)

        student_button = tk.Button(self.login_frame, text="Student Login", font=("Arial", 14), 
                                 bg="#E0E0E0", fg="#000000", command=self.student_login)
        student_button.pack(pady=10, padx=20, fill="x")

        teacher_button = tk.Button(self.login_frame, text="Teacher Login", font=("Arial", 14), 
                                 bg="#E0E0E0", fg="#000000", command=self.teacher_login)
        teacher_button.pack(pady=10, padx=20, fill="x")

        admin_button = tk.Button(self.login_frame, text="Admin Login", font=("Arial", 14), 
                                 bg="#E0E0E0", fg="#000000", command=self.admin_login)
        admin_button.pack(pady=10, padx=20, fill="x")

if __name__ == "__main__":
    root = tk.Tk()
    app = SchoolManagementSystem(root)
    root.mainloop()
