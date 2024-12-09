import tkinter as tk
from tkinter import ttk


def get_all_items():
    # Iterate over all root items
    getting_tree_item = []
    for item in treeview.get_children():
        item_data = treeview.item(item)  # Get item data
        # print(f"Item Text: {item_data['text']}, Item Values: {item_data['values']}")
        getting_tree_item.append(item_data['values'])
    print(getting_tree_item)



# Create the main window
root = tk.Tk()
root.title("Treeview Example")

# Create Treeview widget
treeview = ttk.Treeview(root)

# Define columns
treeview['columns'] = ('Age', 'Department', 'Location')

# Format the columns
treeview.column("#0", width=150, minwidth=150, anchor="w")  # For the first column (Name)
treeview.column("Age", width=100, anchor="center")
treeview.column("Department", width=100, anchor="center")
treeview.column("Location", width=150, anchor="center")

# Define column headings
treeview.heading("#0", text="Name", anchor="w")
treeview.heading("Age", text="Age", anchor="center")
treeview.heading("Department", text="Department", anchor="center")
treeview.heading("Location", text="Location", anchor="center")

# Insert items (some with children, some without)
root_item = treeview.insert("", "end", "Company", text="Company", values=("", "", ""))
treeview.insert('', "end", "HR", text="HR", values=("30", "HR", "New York"))
treeview.insert('', "end", "IT", text="IT", values=("25", "IT", "San Francisco"))
treeview.insert('', "end", "Finance", text="Finance", values=("35", "Finance", "Chicago"))
treeview.insert('', "end", "Alice", text="Alice", values=("40", "Admin", "London"))
treeview.insert('', "end", "Bob", text="Bob", values=("25", "Dev", "Toronto"))

# Add a button to retrieve all items
button = ttk.Button(root, text="Get All Items", command=get_all_items)
button.pack(pady=10)

# Pack the Treeview
treeview.pack(expand=True, fill="both")

# Run the Tkinter event loop
root.mainloop()