# import modules 
from tkinter import *
from tkinter import ttk
import datetime as dt
from mydb import *
from tkinter import messagebox

# object for database
data = Database(db='test.db')

# global variables
count = 0
selected_rowid = 0

# functions
def saveRecord():
    global data
    # Modified to include category
    data.insertRecordWithCategory(
        item_name=item_name.get(),
        item_price=item_amt.get(),
        purchase_date=transaction_date.get(),
        category=item_category.get(),
    )

def setDate():
    date = dt.datetime.now()
    dopvar.set(f'{date:%d %B %Y}')

def clearEntries():
    item_name.delete(0, 'end')
    item_amt.delete(0, 'end')
    transaction_date.delete(0, 'end')
    item_category.delete(0, 'end')  # Clear category entry

def fetch_records():
    f = data.fetchRecord('select rowid, * from expense_record')
    global count
    for rec in f:
        # Modified to include category
        tv.insert(parent='', index='0', iid=count, values=(rec[0], rec[1], rec[2], rec[3], rec[4]))
        count += 1
    tv.after(400, refreshData)

def select_record(event):
    global selected_rowid
    selected = tv.focus()    
    val = tv.item(selected, 'values')
  
    try:
        selected_rowid = val[0]
        d = val[3]
        namevar.set(val[1])
        amtvar.set(val[2])
        dopvar.set(str(d))
        categoryvar.set(val[4])  # Set category field
    except Exception as ep:
        pass

def update_record():
    global selected_rowid

    selected = tv.focus()
    try:
        data.updateRecord(
            namevar.get(),
            amtvar.get(),
            dopvar.get(),
            selected_rowid
        )
        data.updateCategory(
            selected_rowid,
            categoryvar.get()  # Update category
        )
        tv.item(selected, text="", values=(namevar.get(), amtvar.get(), dopvar.get(), categoryvar.get()))
    except Exception as ep:
        messagebox.showerror('Error', ep)

    item_name.delete(0, END)
    item_amt.delete(0, END)
    transaction_date.delete(0, END)
    item_category.delete(0, END)
    tv.after(400, refreshData)

def totalBalance():
    f = data.fetchRecord(query="Select sum(item_price) from expense_record")
    for i in f:
        for j in i:
            messagebox.showinfo('Current Balance: ', f"Total Expense: ' {j} \nBalance Remaining: {5000 - j}")

def refreshData():
    for item in tv.get_children():
        tv.delete(item)
    fetch_records()

def deleteRow():
    global selected_rowid
    data.removeRecord(selected_rowid)
    refreshData()

# create tkinter object
ws = Tk()
ws.title('Daily Expenses')
ws.geometry("800x600")
ws.configure(bg="#f5f5f5")  # Light background

# variables
f = ('Verdana', 12)
namevar = StringVar()
amtvar = IntVar()
dopvar = StringVar()
categoryvar = StringVar()  # Added variable for category

# Frame widget for entries and buttons
entry_frame = Frame(ws, bg="#ffffff", bd=2, relief=RIDGE)
entry_frame.pack(side=TOP, fill=X, padx=10, pady=10)

# Frame widget for Treeview
tree_frame = Frame(ws, bg="#ffffff", bd=2, relief=RIDGE)
tree_frame.pack(side=TOP, fill=BOTH, expand=True, padx=10, pady=10)

# Labels and entry widgets
Label(entry_frame, text='ITEM NAME', font=f, bg="#ffffff", anchor=W).grid(row=0, column=0, sticky=W, padx=5, pady=5)
Label(entry_frame, text='ITEM PRICE', font=f, bg="#ffffff", anchor=W).grid(row=1, column=0, sticky=W, padx=5, pady=5)
Label(entry_frame, text='PURCHASE DATE', font=f, bg="#ffffff", anchor=W).grid(row=2, column=0, sticky=W, padx=5, pady=5)
Label(entry_frame, text='CATEGORY', font=f, bg="#ffffff", anchor=W).grid(row=3, column=0, sticky=W, padx=5, pady=5)

item_name = Entry(entry_frame, font=f, textvariable=namevar, bd=1, relief=SOLID)
item_amt = Entry(entry_frame, font=f, textvariable=amtvar, bd=1, relief=SOLID)
transaction_date = Entry(entry_frame, font=f, textvariable=dopvar, bd=1, relief=SOLID)
item_category = Entry(entry_frame, font=f, textvariable=categoryvar, bd=1, relief=SOLID)

item_name.grid(row=0, column=1, sticky=EW, padx=5, pady=5)
item_amt.grid(row=1, column=1, sticky=EW, padx=5, pady=5)
transaction_date.grid(row=2, column=1, sticky=EW, padx=5, pady=5)
item_category.grid(row=3, column=1, sticky=EW, padx=5, pady=5)

# Buttons
button_frame = Frame(entry_frame, bg="#ffffff")
button_frame.grid(row=4, column=0, columnspan=2, pady=10)

Button(button_frame, text='Save Record', font=f, bg="#28a745", fg="#ffffff", command=saveRecord, width=12).grid(row=0, column=0, padx=5)
Button(button_frame, text='Clear Entry', font=f, bg="#ffc107", fg="#000000", command=clearEntries, width=12).grid(row=0, column=1, padx=5)
Button(button_frame, text='Current Date', font=f, bg="#17a2b8", fg="#ffffff", command=setDate, width=12).grid(row=0, column=2, padx=5)
Button(button_frame, text='Update', font=f, bg="#007bff", fg="#ffffff", command=update_record, width=12).grid(row=0, column=3, padx=5)
Button(button_frame, text='Delete', font=f, bg="#dc3545", fg="#ffffff", command=deleteRow, width=12).grid(row=0, column=4, padx=5)
Button(button_frame, text='Exit', font=f, bg="#343a40", fg="#ffffff", command=ws.destroy, width=12).grid(row=0, column=5, padx=5)

# Add the Total Balance Button
Button(button_frame, text='Total Balance', font=f, bg="#28a745", fg="#ffffff", command=totalBalance, width=12).grid(row=0, column=6, padx=5)


# Treeview widget
tv = ttk.Treeview(tree_frame, columns=(1, 2, 3, 4, 5), show='headings', height=15)
tv.pack(side=LEFT, fill=BOTH, expand=True)

# add heading to treeview
tv.column(1, anchor=CENTER, stretch=NO, width=70)
tv.column(2, anchor=W, width=150)
tv.column(3, anchor=CENTER, width=100)
tv.column(4, anchor=CENTER, width=150)
tv.column(5, anchor=W, width=150)

tv.heading(1, text="Serial no")
tv.heading(2, text="Item Name")
tv.heading(3, text="Item Price")
tv.heading(4, text="Purchase Date")
tv.heading(5, text="Category")

# binding treeview
tv.bind("<ButtonRelease-1>", select_record)

# Scrollbars
scroll_y = Scrollbar(tree_frame, orient=VERTICAL, command=tv.yview)
scroll_y.pack(side=RIGHT, fill=Y)
tv.configure(yscrollcommand=scroll_y.set)

# calling function 
fetch_records()

# infinite loop
ws.mainloop()
