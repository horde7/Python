import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sqlite3
import os

class SQLiteManager:
    def __init__(self, root):
        self.root = root
        self.root.title("SQLite Database Manager")
        self.root.geometry("800x600")
        
        self.current_db = None
        self.table_name = "users"  # Default table name
        
        # Create the main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Database controls frame
        self.db_frame = ttk.LabelFrame(self.main_frame, text="Database Controls", padding="10")
        self.db_frame.pack(fill=tk.X, pady=5)
        
        # Button to create new database
        self.create_db_btn = ttk.Button(self.db_frame, text="Create New Database", command=self.create_new_database)
        self.create_db_btn.pack(side=tk.LEFT, padx=5)
        
        # Button to open existing database
        self.open_db_btn = ttk.Button(self.db_frame, text="Open Database", command=self.open_database)
        self.open_db_btn.pack(side=tk.LEFT, padx=5)
        
        # Label to show current database
        self.db_label = ttk.Label(self.db_frame, text="No database selected")
        self.db_label.pack(side=tk.LEFT, padx=20)
        
        # Add record frame
        self.add_record_frame = ttk.LabelFrame(self.main_frame, text="Add Record", padding="10")
        self.add_record_frame.pack(fill=tk.X, pady=5)
        
        # Entry fields for new record
        ttk.Label(self.add_record_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = ttk.Entry(self.add_record_frame, width=20)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.add_record_frame, text="Email:").grid(row=0, column=2, padx=5, pady=5)
        self.email_entry = ttk.Entry(self.add_record_frame, width=30)
        self.email_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # Add record button
        self.add_btn = ttk.Button(self.add_record_frame, text="Add Record", command=self.add_record)
        self.add_btn.grid(row=0, column=4, padx=5, pady=5)
        
        # Records frame
        self.records_frame = ttk.LabelFrame(self.main_frame, text="Records", padding="10")
        self.records_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Treeview for displaying records
        self.tree = ttk.Treeview(self.records_frame, columns=("ID", "Name", "Email"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Email", text="Email")
        self.tree.column("ID", width=50, anchor=tk.CENTER)
        self.tree.column("Name", width=200)
        self.tree.column("Email", width=300)
        
        # Add scrollbar to treeview
        scrollbar = ttk.Scrollbar(self.records_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree and scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Button frame
        self.button_frame = ttk.Frame(self.main_frame, padding="10")
        self.button_frame.pack(fill=tk.X, pady=5)
        
        # Button to refresh records
        self.refresh_btn = ttk.Button(self.button_frame, text="Refresh Records", command=self.load_records)
        self.refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Button to delete selected record
        self.delete_btn = ttk.Button(self.button_frame, text="Delete Selected", command=self.delete_record)
        self.delete_btn.pack(side=tk.LEFT, padx=5)
        
        # Initialize UI state
        self.update_ui_state(False)
    
    def update_ui_state(self, db_connected):
        """Update UI elements based on database connection state"""
        state = "normal" if db_connected else "disabled"
        self.add_btn["state"] = state
        self.refresh_btn["state"] = state
        self.delete_btn["state"] = state
        self.name_entry["state"] = state
        self.email_entry["state"] = state
    
    def create_new_database(self):
        """Create a new SQLite database with a users table"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".db",
            filetypes=[("SQLite Database", "*.db"), ("All Files", "*.*")],
            title="Create New Database"
        )
        
        if file_path:
            try:
                # Create a new database
                conn = sqlite3.connect(file_path)
                cursor = conn.cursor()
                
                # Create a table
                cursor.execute(f'''
                CREATE TABLE {self.table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT
                )
                ''')
                
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Success", f"Database created successfully with table '{self.table_name}'")
                
                # Open the newly created database
                self.current_db = file_path
                self.db_label["text"] = f"Database: {os.path.basename(file_path)}"
                self.update_ui_state(True)
                self.load_records()
                
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Failed to create database: {e}")
    
    def open_database(self):
        """Open an existing SQLite database"""
        file_path = filedialog.askopenfilename(
            filetypes=[("SQLite Database", "*.db"), ("All Files", "*.*")],
            title="Open Database"
        )
        
        if file_path:
            try:
                # Test connection to the database
                conn = sqlite3.connect(file_path)
                cursor = conn.cursor()
                
                # Check if the users table exists
                cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{self.table_name}'")
                if not cursor.fetchone():
                    create_table = messagebox.askyesno(
                        "Table Not Found", 
                        f"The '{self.table_name}' table was not found in this database. Create it now?"
                    )
                    
                    if create_table:
                        cursor.execute(f'''
                        CREATE TABLE {self.table_name} (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            email TEXT
                        )
                        ''')
                        conn.commit()
                    else:
                        conn.close()
                        return
                
                conn.close()
                
                # Set as current database
                self.current_db = file_path
                self.db_label["text"] = f"Database: {os.path.basename(file_path)}"
                self.update_ui_state(True)
                self.load_records()
                
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Failed to open database: {e}")
    
    def load_records(self):
        """Load records from the database and display in treeview"""
        if not self.current_db:
            return
        
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            conn = sqlite3.connect(self.current_db)
            cursor = conn.cursor()
            
            cursor.execute(f"SELECT id, name, email FROM {self.table_name}")
            rows = cursor.fetchall()
            
            for row in rows:
                self.tree.insert("", tk.END, values=row)
            
            conn.close()
            
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to load records: {e}")
    
    def add_record(self):
        """Add a new record to the database"""
        if not self.current_db:
            return
        
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        
        if not name:
            messagebox.showwarning("Input Error", "Name field is required")
            return
        
        try:
            conn = sqlite3.connect(self.current_db)
            cursor = conn.cursor()
            
            cursor.execute(f"INSERT INTO {self.table_name} (name, email) VALUES (?, ?)", (name, email))
            conn.commit()
            
            # Clear entry fields
            self.name_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
            
            # Refresh the records
            self.load_records()
            
            conn.close()
            
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to add record: {e}")
    
    def delete_record(self):
        """Delete the selected record from the database"""
        if not self.current_db:
            return
        
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showinfo("Info", "Please select a record to delete")
            return
        
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this record?")
        if not confirm:
            return
        
        try:
            # Get the ID of the selected item
            item_id = self.tree.item(selected_item[0], 'values')[0]
            
            conn = sqlite3.connect(self.current_db)
            cursor = conn.cursor()
            
            cursor.execute(f"DELETE FROM {self.table_name} WHERE id = ?", (item_id,))
            conn.commit()
            conn.close()
            
            # Refresh the records
            self.load_records()
            
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to delete record: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SQLiteManager(root)
    root.mainloop()
