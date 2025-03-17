import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import sqlite3
import os

class SQLiteManager:
    def __init__(self, root):
        self.root = root
        self.root.title("SQLite Database Manager")
        self.root.geometry("900x700")
        
        # Set the gray background and yellow text as default
        self.root.configure(background="#404040")
        self.style = ttk.Style()
        self.style.configure(".", background="#404040", foreground="#FFFF00")
        self.style.configure("TFrame", background="#404040")
        self.style.configure("TLabelframe", background="#404040")
        self.style.configure("TLabelframe.Label", background="#404040", foreground="#FFFF00")
        self.style.configure("TLabel", background="#404040", foreground="#FFFF00")
        self.style.configure("TButton", background="#606060", foreground="#FFFF00")
        self.style.configure("Treeview", background="#505050", foreground="#FFFF00", fieldbackground="#505050")
        self.style.configure("Treeview.Heading", background="#606060", foreground="#FFFF00")
        
        self.current_db = None
        self.table_name = "users"  # Default table name
        self.editing_id = None  # To track which record is being edited
        
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
        
        # Edit/Add record frame
        self.edit_frame = ttk.LabelFrame(self.main_frame, text="Add/Edit Record", padding="10")
        self.edit_frame.pack(fill=tk.X, pady=5)
        
        # Entry fields for record
        ttk.Label(self.edit_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.name_entry = ttk.Entry(self.edit_frame, width=20)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.edit_frame, text="Email:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.email_entry = ttk.Entry(self.edit_frame, width=30)
        self.email_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # Notes field (multiline)
        ttk.Label(self.edit_frame, text="Notes:").grid(row=1, column=0, padx=5, pady=5, sticky="nw")
        self.notes_text = scrolledtext.ScrolledText(self.edit_frame, width=50, height=4, wrap=tk.WORD)
        self.notes_text.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky="ew")
        
        # Custom background and foreground for ScrolledText (not affected by ttk.Style)
        self.notes_text.config(background="#505050", foreground="#FFFF00")
        
        # Add/Save/Cancel buttons
        self.button_container = ttk.Frame(self.edit_frame)
        self.button_container.grid(row=2, column=0, columnspan=4, pady=5)
        
        self.add_btn = ttk.Button(self.button_container, text="Add Record", command=self.add_record)
        self.add_btn.pack(side=tk.LEFT, padx=5)
        
        self.save_btn = ttk.Button(self.button_container, text="Save Changes", command=self.save_changes)
        self.save_btn.pack(side=tk.LEFT, padx=5)
        
        self.cancel_btn = ttk.Button(self.button_container, text="Cancel Edit", command=self.cancel_edit)
        self.cancel_btn.pack(side=tk.LEFT, padx=5)
        
        # Records frame
        self.records_frame = ttk.LabelFrame(self.main_frame, text="Records", padding="10")
        self.records_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Treeview for displaying records
        self.tree = ttk.Treeview(self.records_frame, columns=("ID", "Name", "Email", "Notes"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Notes", text="Notes")
        self.tree.column("ID", width=50, anchor=tk.CENTER)
        self.tree.column("Name", width=150)
        self.tree.column("Email", width=200)
        self.tree.column("Notes", width=350)
        
        # Add scrollbar to treeview
        scrollbar = ttk.Scrollbar(self.records_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree and scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Double-click to edit
        self.tree.bind("<Double-1>", self.on_record_double_click)
        
        # Button frame
        self.action_frame = ttk.Frame(self.main_frame, padding="10")
        self.action_frame.pack(fill=tk.X, pady=5)
        
        # Button to refresh records
        self.refresh_btn = ttk.Button(self.action_frame, text="Refresh Records", command=self.load_records)
        self.refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Button to edit selected record
        self.edit_btn = ttk.Button(self.action_frame, text="Edit Selected", command=self.edit_record)
        self.edit_btn.pack(side=tk.LEFT, padx=5)
        
        # Button to delete selected record
        self.delete_btn = ttk.Button(self.action_frame, text="Delete Selected", command=self.delete_record)
        self.delete_btn.pack(side=tk.LEFT, padx=5)
        
        # Initialize UI state
        self.update_ui_state(False)
        self.update_edit_mode(False)
    
    def update_ui_state(self, db_connected):
        """Update UI elements based on database connection state"""
        state = "normal" if db_connected else "disabled"
        self.add_btn["state"] = state
        self.refresh_btn["state"] = state
        self.delete_btn["state"] = state
        self.edit_btn["state"] = state
        self.name_entry["state"] = state
        self.email_entry["state"] = state
        self.notes_text["state"] = state if state == "normal" else tk.DISABLED
    
    def update_edit_mode(self, editing):
        """Update UI based on whether we're editing or adding"""
        if editing:
            self.add_btn["state"] = "disabled"
            self.save_btn["state"] = "normal"
            self.cancel_btn["state"] = "normal"
            self.edit_frame["text"] = "Edit Record"
        else:
            self.add_btn["state"] = "normal" if self.current_db else "disabled"
            self.save_btn["state"] = "disabled"
            self.cancel_btn["state"] = "disabled"
            self.edit_frame["text"] = "Add Record"
            self.editing_id = None
            # Clear fields
            self.name_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
            self.notes_text.delete(1.0, tk.END)
    
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
                
                # Create a table with a notes column
                cursor.execute(f'''
                CREATE TABLE {self.table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT,
                    notes TEXT
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
                            email TEXT,
                            notes TEXT
                        )
                        ''')
                        conn.commit()
                    else:
                        conn.close()
                        return
                else:
                    # Check if notes column exists and add it if it doesn't
                    cursor.execute(f"PRAGMA table_info({self.table_name})")
                    columns = [info[1] for info in cursor.fetchall()]
                    
                    if "notes" not in columns:
                        cursor.execute(f"ALTER TABLE {self.table_name} ADD COLUMN notes TEXT")
                        conn.commit()
                        messagebox.showinfo("Database Updated", "Added 'notes' column to existing table.")
                
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
            
            cursor.execute(f"SELECT id, name, email, notes FROM {self.table_name}")
            rows = cursor.fetchall()
            
            for row in rows:
                # Truncate notes for display if too long
                display_row = list(row)
                if display_row[3] and len(display_row[3]) > 30:
                    display_row[3] = display_row[3][:27] + "..."
                self.tree.insert("", tk.END, values=display_row)
            
            conn.close()
            
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to load records: {e}")
    
    def add_record(self):
        """Add a new record to the database"""
        if not self.current_db:
            return
        
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        notes = self.notes_text.get(1.0, tk.END).strip()
        
        if not name:
            messagebox.showwarning("Input Error", "Name field is required")
            return
        
        try:
            conn = sqlite3.connect(self.current_db)
            cursor = conn.cursor()
            
            cursor.execute(f"INSERT INTO {self.table_name} (name, email, notes) VALUES (?, ?, ?)", 
                          (name, email, notes))
            conn.commit()
            
            # Clear entry fields
            self.name_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
            self.notes_text.delete(1.0, tk.END)
            
            # Refresh the records
            self.load_records()
            
            conn.close()
            
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to add record: {e}")
    
    def on_record_double_click(self, event):
        """Handle double-click on a record"""
        self.edit_record()
    
    def edit_record(self):
        """Load the selected record for editing"""
        if not self.current_db:
            return
            
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showinfo("Info", "Please select a record to edit")
            return
            
        # Get the ID of the selected item
        item_values = self.tree.item(selected_item[0], 'values')
        item_id = item_values[0]
            
        try:
            conn = sqlite3.connect(self.current_db)
            cursor = conn.cursor()
            
            cursor.execute(f"SELECT id, name, email, notes FROM {self.table_name} WHERE id = ?", (item_id,))
            record = cursor.fetchone()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to add record: {e}")