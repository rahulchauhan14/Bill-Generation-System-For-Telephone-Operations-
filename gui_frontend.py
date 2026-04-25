import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import mysql.connector
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import os

class TelecomBillingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title(" Rahul Telecoms - Bill Generation System")
        self.root.geometry("900x700")
        self.root.configure(bg="#5D8BB6")
        
        # Database configuration
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'passwd': '84610',
            'database': 'project'
        }
        
        # Create main header
        self.create_header()
        
        # Create notebook for tabs
        self.create_tabs()
        
    def create_header(self):
        header_frame = tk.Frame(self.root, bg="#23609d", height=80)
        header_frame.pack(fill='x', padx=10, pady=10)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="Rahul Telecoms", 
                              font=('Arial', 24, 'bold'), 
                              bg="#23609d", fg='white')
        title_label.pack(pady=10)
        
        subtitle_label = tk.Label(header_frame, text="Bill Generation System - Indore Bhawarkua Branch", 
                                 font=('Arial', 12), 
                                 bg="#23609d", fg='#ecf0f1')
        subtitle_label.pack()
        
    def create_tabs(self):
        # Create notebook (tab container)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.add_tab = tk.Frame(self.notebook, bg='#ecf0f1')
        self.search_tab = tk.Frame(self.notebook, bg='#ecf0f1')
        self.view_tab = tk.Frame(self.notebook, bg='#ecf0f1')
        self.edit_tab = tk.Frame(self.notebook, bg='#ecf0f1')
        self.delete_tab = tk.Frame(self.notebook, bg='#ecf0f1')
        self.bill_tab = tk.Frame(self.notebook, bg='#ecf0f1')
        
        # Add tabs to notebook
        self.notebook.add(self.add_tab, text='Add Customer')
        self.notebook.add(self.search_tab, text='Search Customer')
        self.notebook.add(self.view_tab, text='View All Records')
        self.notebook.add(self.edit_tab, text='Edit Customer')
        self.notebook.add(self.delete_tab, text='Delete Customer')
        self.notebook.add(self.bill_tab, text='Generate Bill')
        
        # Setup each tab
        self.setup_add_tab()
        self.setup_search_tab()
        self.setup_view_tab()
        self.setup_edit_tab()
        self.setup_delete_tab()
        self.setup_bill_tab()
        
    def setup_add_tab(self):
        # Create form frame
        form_frame = tk.Frame(self.add_tab, bg='#ecf0f1')
        form_frame.pack(pady=30, padx=50)
        
        # Form fields
        fields = [
            ('Customer No:', 'cno'),
            ('Customer Name:', 'cname'),
            ('Phone No.:', 'mobile'),
            ('Address:', 'address'),
            ('Email:', 'email'),
            ('No. of Calls:', 'no_calls')
        ]
        
        self.add_entries = {}
        
        for idx, (label_text, field_name) in enumerate(fields):
            label = tk.Label(form_frame, text=label_text, font=('Arial', 12), 
                           bg='#ecf0f1', fg='#2c3e50')
            label.grid(row=idx, column=0, sticky='w', pady=10, padx=10)
            
            entry = tk.Entry(form_frame, font=('Arial', 11), width=30)
            entry.grid(row=idx, column=1, pady=10, padx=10)
            self.add_entries[field_name] = entry
        
        # Add button
        add_btn = tk.Button(form_frame, text='Add Customer', 
                           command=self.add_customer,
                           bg='#27ae60', fg='white', 
                           font=('Arial', 12, 'bold'),
                           width=20, height=2)
        add_btn.grid(row=len(fields), column=0, columnspan=2, pady=20)
        
        # Clear button
        clear_btn = tk.Button(form_frame, text='Clear Fields', 
                             command=self.clear_add_fields,
                             bg='#95a5a6', fg='white', 
                             font=('Arial', 10),
                             width=20)
        clear_btn.grid(row=len(fields)+1, column=0, columnspan=2)
        
    def setup_search_tab(self):
        # Search frame
        search_frame = tk.Frame(self.search_tab, bg='#ecf0f1')
        search_frame.pack(pady=30, padx=50)
        
        label = tk.Label(search_frame, text='Enter Customer No:', 
                        font=('Arial', 12), bg='#ecf0f1', fg='#2c3e50')
        label.grid(row=0, column=0, pady=10, padx=10)
        
        self.search_entry = tk.Entry(search_frame, font=('Arial', 11), width=20)
        self.search_entry.grid(row=0, column=1, pady=10, padx=10)
        
        search_btn = tk.Button(search_frame, text='Search', 
                              command=self.search_customer,
                              bg='#3498db', fg='white', 
                              font=('Arial', 12, 'bold'),
                              width=15)
        search_btn.grid(row=0, column=2, pady=10, padx=10)
        
        # Result frame
        result_frame = tk.Frame(self.search_tab, bg='#ecf0f1')
        result_frame.pack(pady=20, padx=50, fill='both', expand=True)
        
        self.search_result = scrolledtext.ScrolledText(result_frame, 
                                                       font=('Courier', 10),
                                                       height=15, width=70)
        self.search_result.pack(pady=10)
        
    def setup_view_tab(self):
        # Button frame
        btn_frame = tk.Frame(self.view_tab, bg='#ecf0f1')
        btn_frame.pack(pady=20)
        
        refresh_btn = tk.Button(btn_frame, text='Refresh Records', 
                               command=self.view_all_records,
                               bg='#3498db', fg='white', 
                               font=('Arial', 12, 'bold'),
                               width=20)
        refresh_btn.pack()
        
        # Treeview for displaying records
        tree_frame = tk.Frame(self.view_tab, bg='#ecf0f1')
        tree_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        # Create treeview
        self.tree = ttk.Treeview(tree_frame, 
                                columns=('cno', 'cname', 'mobile', 'address', 'email', 'no_calls'),
                                show='headings',
                                yscrollcommand=vsb.set,
                                xscrollcommand=hsb.set)
        
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)
        
        # Define headings
        headings = [('cno', 'Customer No', 100),
                   ('cname', 'Name', 150),
                   ('mobile', 'Mobile', 120),
                   ('address', 'Address', 200),
                   ('email', 'Email', 200),
                   ('no_calls', 'Calls', 80)]
        
        for col, heading, width in headings:
            self.tree.heading(col, text=heading)
            self.tree.column(col, width=width)
        
        # Pack treeview and scrollbars
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
    def setup_edit_tab(self):
        # Customer selection frame
        select_frame = tk.Frame(self.edit_tab, bg='#ecf0f1')
        select_frame.pack(pady=20, padx=50)
        
        label = tk.Label(select_frame, text='Select Customer No:', 
                        font=('Arial', 12), bg='#ecf0f1', fg='#2c3e50')
        label.grid(row=0, column=0, pady=10, padx=10)
        
        self.edit_cno_entry = tk.Entry(select_frame, font=('Arial', 11), width=20)
        self.edit_cno_entry.grid(row=0, column=1, pady=10, padx=10)
        
        load_btn = tk.Button(select_frame, text='Load Customer', 
                            command=self.load_customer_for_edit,
                            bg='#3498db', fg='white', 
                            font=('Arial', 10, 'bold'),
                            width=15)
        load_btn.grid(row=0, column=2, pady=10, padx=10)
        
        # Edit form frame
        edit_form_frame = tk.Frame(self.edit_tab, bg='#ecf0f1')
        edit_form_frame.pack(pady=10, padx=50)
        
        fields = [
            ('Customer Name:', 'cname'),
            ('Phone No.:', 'mobile'),
            ('Address:', 'address'),
            ('Email:', 'email'),
            ('No. of Calls:', 'no_calls')
        ]
        
        self.edit_entries = {}
        
        for idx, (label_text, field_name) in enumerate(fields):
            label = tk.Label(edit_form_frame, text=label_text, font=('Arial', 11), 
                           bg='#ecf0f1', fg='#2c3e50')
            label.grid(row=idx, column=0, sticky='w', pady=8, padx=10)
            
            entry = tk.Entry(edit_form_frame, font=('Arial', 11), width=30)
            entry.grid(row=idx, column=1, pady=8, padx=10)
            self.edit_entries[field_name] = entry
        
        # Update button
        update_btn = tk.Button(edit_form_frame, text='Update Customer', 
                              command=self.update_customer,
                              bg='#f39c12', fg='white', 
                              font=('Arial', 12, 'bold'),
                              width=20, height=2)
        update_btn.grid(row=len(fields), column=0, columnspan=2, pady=20)
        
    def setup_delete_tab(self):
        delete_frame = tk.Frame(self.delete_tab, bg='#ecf0f1')
        delete_frame.pack(pady=30, padx=50)
        
        label = tk.Label(delete_frame, text='Enter Customer No to Delete:', 
                        font=('Arial', 12), bg='#ecf0f1', fg='#2c3e50')
        label.grid(row=0, column=0, pady=10, padx=10)
        
        self.delete_entry = tk.Entry(delete_frame, font=('Arial', 11), width=20)
        self.delete_entry.grid(row=0, column=1, pady=10, padx=10)
        
        delete_btn = tk.Button(delete_frame, text='Delete Customer', 
                              command=self.delete_customer,
                              bg='#e74c3c', fg='white', 
                              font=('Arial', 12, 'bold'),
                              width=20)
        delete_btn.grid(row=1, column=0, columnspan=2, pady=20)
        
        # Result display
        self.delete_result = scrolledtext.ScrolledText(self.delete_tab, 
                                                       font=('Courier', 10),
                                                       height=15, width=70)
        self.delete_result.pack(pady=20, padx=50)
        
    def setup_bill_tab(self):
        bill_frame = tk.Frame(self.bill_tab, bg='#ecf0f1')
        bill_frame.pack(pady=30, padx=50)
        
        label = tk.Label(bill_frame, text='Enter Customer No:', 
                        font=('Arial', 12), bg='#ecf0f1', fg='#2c3e50')
        label.grid(row=0, column=0, pady=10, padx=10)
        
        self.bill_entry = tk.Entry(bill_frame, font=('Arial', 11), width=20)
        self.bill_entry.grid(row=0, column=1, pady=10, padx=10)
        
        generate_btn = tk.Button(bill_frame, text='Generate Bill', 
                                command=self.generate_bill,
                                bg='#16a085', fg='white', 
                                font=('Arial', 12, 'bold'),
                                width=20)
        generate_btn.grid(row=1, column=0, columnspan=2, pady=20)
        
        # Print buttons frame
        print_btns_frame = tk.Frame(bill_frame, bg='#ecf0f1')
        print_btns_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        print_txt_btn = tk.Button(print_btns_frame, text='Save as TXT', 
                                 command=self.print_bill,
                                 bg='#9b59b6', fg='white', 
                                 font=('Arial', 10, 'bold'),
                                 width=15)
        print_txt_btn.grid(row=0, column=0, padx=5)
        
        print_pdf_btn = tk.Button(print_btns_frame, text='Save as PDF', 
                                 command=self.print_bill_pdf,
                                 bg='#e74c3c', fg='white', 
                                 font=('Arial', 10, 'bold'),
                                 width=15)
        print_pdf_btn.grid(row=0, column=1, padx=5)
        
        # Bill display
        self.bill_display = scrolledtext.ScrolledText(self.bill_tab, 
                                                      font=('Courier', 11),
                                                      height=20, width=70,
                                                      bg='white')
        self.bill_display.pack(pady=20, padx=50)
        
    def get_db_connection(self):
        try:
            return mysql.connector.connect(**self.db_config)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error connecting to database: {err}")
            return None
            
    def add_customer(self):
        try:
            cno = int(self.add_entries['cno'].get())
            cname = self.add_entries['cname'].get()
            mobile = int(self.add_entries['mobile'].get())
            address = self.add_entries['address'].get()
            email = self.add_entries['email'].get()
            no_calls = int(self.add_entries['no_calls'].get())
            
            mydb = self.get_db_connection()
            if not mydb:
                return
                
            mycur = mydb.cursor()
            query = "INSERT INTO mtnl VALUES (%s, %s, %s, %s, %s, %s)"
            mycur.execute(query, (cno, cname, mobile, address, email, no_calls))
            mydb.commit()
            mydb.close()
            
            messagebox.showinfo("Success", "Customer record added successfully!")
            self.clear_add_fields()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid data!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            
    def clear_add_fields(self):
        for entry in self.add_entries.values():
            entry.delete(0, tk.END)
            
    def search_customer(self):
        try:
            cno = int(self.search_entry.get())
            
            mydb = self.get_db_connection()
            if not mydb:
                return
                
            mycur = mydb.cursor()
            query = "SELECT * FROM mtnl WHERE cno=%s"
            mycur.execute(query, (cno,))
            myrec = mycur.fetchall()
            mydb.close()
            
            self.search_result.delete(1.0, tk.END)
            
            if myrec:
                self.search_result.insert(tk.END, "="*70 + "\n")
                self.search_result.insert(tk.END, "CUSTOMER DETAILS\n")
                self.search_result.insert(tk.END, "="*70 + "\n\n")
                
                for x in myrec:
                    self.search_result.insert(tk.END, f"Customer No:    {x[0]}\n")
                    self.search_result.insert(tk.END, f"Name:           {x[1]}\n")
                    self.search_result.insert(tk.END, f"Mobile:         {x[2]}\n")
                    self.search_result.insert(tk.END, f"Address:        {x[3]}\n")
                    self.search_result.insert(tk.END, f"Email:          {x[4]}\n")
                    self.search_result.insert(tk.END, f"No. of Calls:   {x[5]}\n")
                    
                self.search_result.insert(tk.END, "\n" + "="*70)
            else:
                self.search_result.insert(tk.END, "No customer found with this number!")
                
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid customer number!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            
    def view_all_records(self):
        try:
            mydb = self.get_db_connection()
            if not mydb:
                return
                
            mycur = mydb.cursor()
            mycur.execute("SELECT * FROM mtnl")
            records = mycur.fetchall()
            mydb.close()
            
            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Insert records
            for record in records:
                self.tree.insert('', 'end', values=record)
                
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            
    def load_customer_for_edit(self):
        try:
            cno = int(self.edit_cno_entry.get())
            
            mydb = self.get_db_connection()
            if not mydb:
                return
                
            mycur = mydb.cursor()
            query = "SELECT * FROM mtnl WHERE cno=%s"
            mycur.execute(query, (cno,))
            record = mycur.fetchone()
            mydb.close()
            
            if record:
                self.edit_entries['cname'].delete(0, tk.END)
                self.edit_entries['cname'].insert(0, record[1])
                
                self.edit_entries['mobile'].delete(0, tk.END)
                self.edit_entries['mobile'].insert(0, record[2])
                
                self.edit_entries['address'].delete(0, tk.END)
                self.edit_entries['address'].insert(0, record[3])
                
                self.edit_entries['email'].delete(0, tk.END)
                self.edit_entries['email'].insert(0, record[4])
                
                self.edit_entries['no_calls'].delete(0, tk.END)
                self.edit_entries['no_calls'].insert(0, record[5])
            else:
                messagebox.showerror("Error", "Customer not found!")
                
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid customer number!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            
    def update_customer(self):
        try:
            cno = int(self.edit_cno_entry.get())
            cname = self.edit_entries['cname'].get()
            mobile = self.edit_entries['mobile'].get()
            address = self.edit_entries['address'].get()
            email = self.edit_entries['email'].get()
            no_calls = int(self.edit_entries['no_calls'].get())
            
            mydb = self.get_db_connection()
            if not mydb:
                return
                
            mycur = mydb.cursor()
            query = """UPDATE mtnl SET cname=%s, mobile=%s, address=%s, 
                      email=%s, no_calls=%s WHERE cno=%s"""
            mycur.execute(query, (cname, mobile, address, email, no_calls, cno))
            mydb.commit()
            mydb.close()
            
            messagebox.showinfo("Success", "Customer updated successfully!")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid data!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            
    def delete_customer(self):
        try:
            cno = int(self.delete_entry.get())
            
            # Confirm deletion
            confirm = messagebox.askyesno("Confirm Delete", 
                                         f"Are you sure you want to delete customer {cno}?")
            if not confirm:
                return
            
            mydb = self.get_db_connection()
            if not mydb:
                return
                
            mycur = mydb.cursor()
            
            # Get record before deletion
            mycur.execute("SELECT * FROM mtnl WHERE cno=%s", (cno,))
            record = mycur.fetchone()
            
            if record:
                # Delete the record
                mycur.execute("DELETE FROM mtnl WHERE cno=%s", (cno,))
                mydb.commit()
                
                self.delete_result.delete(1.0, tk.END)
                self.delete_result.insert(tk.END, "="*70 + "\n")
                self.delete_result.insert(tk.END, "DELETED CUSTOMER DETAILS\n")
                self.delete_result.insert(tk.END, "="*70 + "\n\n")
                self.delete_result.insert(tk.END, f"Customer No:    {record[0]}\n")
                self.delete_result.insert(tk.END, f"Name:           {record[1]}\n")
                self.delete_result.insert(tk.END, f"Mobile:         {record[2]}\n")
                self.delete_result.insert(tk.END, f"Address:        {record[3]}\n")
                self.delete_result.insert(tk.END, f"Email:          {record[4]}\n")
                self.delete_result.insert(tk.END, f"No. of Calls:   {record[5]}\n")
                self.delete_result.insert(tk.END, "\n" + "="*70 + "\n")
                self.delete_result.insert(tk.END, "Record deleted successfully!")
                
                messagebox.showinfo("Success", "Customer deleted successfully!")
                self.delete_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Customer not found!")
                
            mydb.close()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid customer number!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            
    def generate_bill(self):
        try:
            cno = int(self.bill_entry.get())
            
            mydb = self.get_db_connection()
            if not mydb:
                return
                
            mycur = mydb.cursor()
            query = "SELECT * FROM mtnl WHERE cno=%s"
            mycur.execute(query, (cno,))
            record = mycur.fetchone()
            mydb.close()
            
            if record:
                cno, cname, mobile, address, email, no_calls = record
                
                # Calculate bill
                if no_calls <= 100:
                    amt = 200
                elif no_calls <= 150:
                    amt = 200 + 0.60 * (no_calls - 100)
                elif no_calls <= 200:
                    amt = 200 + 0.60 * 50 + 0.50 * (no_calls - 150)
                else:
                    amt = 200 + 0.60 * 50 + 0.50 * 50 + 0.40 * (no_calls - 200)
                
                tax = round(amt * 0.10, 2)
                net = round(amt + tax, 2)
                
                # Display bill
                self.bill_display.delete(1.0, tk.END)
                self.bill_display.insert(tk.END, "="*70 + "\n")
                self.bill_display.insert(tk.END, "               Rahul TELECOMS\n")
                self.bill_display.insert(tk.END, "="*70 + "\n")
                self.bill_display.insert(tk.END, "M:- 011563287                  Branch:- Bhawarkua Indore\n")
                self.bill_display.insert(tk.END, f"Date: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n")
                self.bill_display.insert(tk.END, "="*70 + "\n\n")
                self.bill_display.insert(tk.END, f"Customer No:        {cno}\n")
                self.bill_display.insert(tk.END, f"Customer Name:      {cname}\n")
                self.bill_display.insert(tk.END, "="*70 + "\n")
                self.bill_display.insert(tk.END, f"Phone No:           {mobile}\n")
                self.bill_display.insert(tk.END, f"Address:            {address}\n")
                self.bill_display.insert(tk.END, "="*70 + "\n")
                self.bill_display.insert(tk.END, f"Email:              {email}\n")
                self.bill_display.insert(tk.END, f"No. of Calls:       {no_calls}\n")
                self.bill_display.insert(tk.END, "="*70 + "\n\n")
                self.bill_display.insert(tk.END, f"Base Amount:        Rs. {amt:.2f}\n")
                self.bill_display.insert(tk.END, f"GST (10%):          Rs. {tax:.2f}\n")
                self.bill_display.insert(tk.END, "="*70 + "\n")
                self.bill_display.insert(tk.END, f"NET AMOUNT:         Rs. {net:.2f}\n")
                self.bill_display.insert(tk.END, "="*70 + "\n\n")
                self.bill_display.insert(tk.END, "           Thank you for choosing Rahul Telecoms!\n")
                self.bill_display.insert(tk.END, "="*70 + "\n")
                
            else:
                messagebox.showerror("Error", "Customer not found!")
                
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid customer number!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
    
    def print_bill(self):
        # Check if bill is generated
        bill_content = self.bill_display.get(1.0, tk.END).strip()
        
        if not bill_content or bill_content == "":
            messagebox.showwarning("Warning", "Please generate a bill first!")
            return
        
        # Ask user where to save the file
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Save Bill As",
            initialfile=f"Bill_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            initialdir="D:\\Computer science\\DBMS Project"
        )
        
        if file_path:
            try:
                # Ensure the directory exists
                import os
                directory = os.path.dirname(file_path)
                if directory and not os.path.exists(directory):
                    os.makedirs(directory)
                
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(bill_content)
                messagebox.showinfo("Success", f"Bill saved successfully to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save bill: {str(e)}")
    
    def print_bill_pdf(self):
        # Check if bill is generated
        try:
            cno = int(self.bill_entry.get())
        except ValueError:
            messagebox.showwarning("Warning", "Please generate a bill first!")
            return
        
        # Get customer data
        mydb = self.get_db_connection()
        if not mydb:
            return
            
        mycur = mydb.cursor()
        query = "SELECT * FROM mtnl WHERE cno=%s"
        mycur.execute(query, (cno,))
        record = mycur.fetchone()
        mydb.close()
        
        if not record:
            messagebox.showerror("Error", "Customer not found!")
            return
        
        cno, cname, mobile, address, email, no_calls = record
        
        # Calculate bill
        if no_calls <= 100:
            amt = 200
        elif no_calls <= 150:
            amt = 200 + 0.60 * (no_calls - 100)
        elif no_calls <= 200:
            amt = 200 + 0.60 * 50 + 0.50 * (no_calls - 150)
        else:
            amt = 200 + 0.60 * 50 + 0.50 * 50 + 0.40 * (no_calls - 200)
        
        tax = round(amt * 0.10, 2)
        net = round(amt + tax, 2)
        
        # Ask user where to save the PDF
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            title="Save Bill As PDF",
            initialfile=f"Bill_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            initialdir="D:\\Computer science\\DBMS Project"
        )
        
        if file_path:
            try:
                # Ensure the directory exists
                directory = os.path.dirname(file_path)
                if directory and not os.path.exists(directory):
                    os.makedirs(directory)
                
                # Create PDF
                c = canvas.Canvas(file_path, pagesize=letter)
                width, height = letter
                
                # Set up fonts and positions
                y = height - 50
                
                # Header
                c.setFont("Helvetica-Bold", 20)
                c.drawCentredString(width/2, y, "RAHUL TELECOMS")
                y -= 30
                
                c.setFont("Helvetica", 10)
                c.drawCentredString(width/2, y, "M:- 011563287                  Branch:- GTB Nagar")
                y -= 15
                c.drawCentredString(width/2, y, f"Date: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")
                y -= 30
                
                # Draw line
                c.line(50, y, width-50, y)
                y -= 30
                
                # Customer details
                c.setFont("Helvetica-Bold", 12)
                c.drawString(50, y, "BILL DETAILS")
                y -= 25
                
                c.setFont("Helvetica", 11)
                c.drawString(50, y, f"Customer No:")
                c.drawString(200, y, str(cno))
                y -= 20
                
                c.drawString(50, y, f"Customer Name:")
                c.drawString(200, y, str(cname))
                y -= 20
                
                c.drawString(50, y, f"Phone No:")
                c.drawString(200, y, str(mobile))
                y -= 20
                
                c.drawString(50, y, f"Address:")
                c.drawString(200, y, str(address))
                y -= 20
                
                c.drawString(50, y, f"Email:")
                c.drawString(200, y, str(email))
                y -= 20
                
                c.drawString(50, y, f"No. of Calls:")
                c.drawString(200, y, str(no_calls))
                y -= 35
                
                # Draw line
                c.line(50, y, width-50, y)
                y -= 30
                
                # Billing details
                c.setFont("Helvetica-Bold", 12)
                c.drawString(50, y, "BILLING SUMMARY")
                y -= 25
                
                c.setFont("Helvetica", 11)
                c.drawString(50, y, f"Base Amount:")
                c.drawRightString(width-50, y, f"Rs. {amt:.2f}")
                y -= 20
                
                c.drawString(50, y, f"GST (10%):")
                c.drawRightString(width-50, y, f"Rs. {tax:.2f}")
                y -= 25
                
                # Draw line
                c.line(50, y, width-50, y)
                y -= 25
                
                # Net amount
                c.setFont("Helvetica-Bold", 14)
                c.drawString(50, y, f"NET AMOUNT:")
                c.drawRightString(width-50, y, f"Rs. {net:.2f}")
                y -= 40
                
                # Draw line
                c.line(50, y, width-50, y)
                y -= 30
                
                # Footer
                c.setFont("Helvetica-Oblique", 10)
                c.drawCentredString(width/2, y, "Thank you for choosing Rahul Telecoms!")
                
                # Save PDF
                c.save()
                
                messagebox.showinfo("Success", f"Bill saved as PDF successfully to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to generate PDF: {str(e)}")


def main():
    root = tk.Tk()
    app = TelecomBillingGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
