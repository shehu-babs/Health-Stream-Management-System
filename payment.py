import sys

import customtkinter as ctk
from tkinter import messagebox
from operation import submit_payment, print_card

p_id = sys.argv[1]
subtracting_dis = sys.argv[2]
bill_id=sys.argv[3]
patient_name=sys.argv[4]
taxvalue = sys.argv[5]
netvalue = sys.argv[6]
subTvalue = sys.argv[7]


# Function to handle payment processing
def process_payment():
    fig1 = f'{float(taxvalue):.2f}'
    fig2 = f'{float(netvalue):.2f}'
    payment_method = payment_method_combobox.get()
    try:
        # Process payment (replace with actual payment processing logic)
        submit_payment(fig2,fig1,subtracting_dis,payment_method,bill_id)
        messagebox.showinfo("Payment Successful", f"Payment of ${subtracting_dis} by {patient_name} was successful!")

        user_response = messagebox.askyesno('Receipt', 'Do you want to print receipt?')
        if user_response:  # This will be True if "Yes" is clicked
            filename_sv = f'#000{bill_id}'
            print_card(payment_frame,filename_sv)

    except Exception as e:
        messagebox.showerror("Payment Error", f"An error occurred: {str(e)}")

# Initialize the CTk window
root = ctk.CTk()
root.title("Payment Screen")
root.geometry("400x600")
root.focus_force()

# Frame for payment details
payment_frame = ctk.CTkFrame(root, corner_radius=10)
payment_frame.pack(pady=20, padx=20, fill="both", expand=True)

# Title Label
title_label = ctk.CTkLabel(payment_frame, text="Payment Form", font=("Helvetica", 20, "bold"))
title_label.pack(pady=15)

# Payer's Name
payer_name_label = ctk.CTkLabel(payment_frame, text="Payer's Name:")
payer_name_label.pack(anchor="w", padx=20)
payer_name_entry = ctk.CTkButton(payment_frame,text=patient_name,fg_color='gray97',state='readonly',text_color='black')
payer_name_entry.pack(pady=5, padx=20, fill="x")

# Payment Amount
amount_label = ctk.CTkLabel(payment_frame, text="Bill ID:")
amount_label.pack(anchor="w", padx=20)
amount_entry = ctk.CTkButton(payment_frame, text=f'BILL#00{bill_id}',fg_color='gray97',state='readonly',text_color='black')
amount_entry.pack(pady=5, padx=20, fill="x")

amount_label = ctk.CTkLabel(payment_frame, text="Taxed Amount ($):")
amount_label.pack(anchor="w", padx=20)
amount_entry = ctk.CTkButton(payment_frame, text=f'$ {taxvalue}', fg_color='gray97',state='readonly',text_color='black')
amount_entry.pack(pady=5, padx=20, fill="x")

amount_label = ctk.CTkLabel(payment_frame, text="Total Cost ($)")
amount_label.pack(anchor="w", padx=20)
amount_entry = ctk.CTkButton(payment_frame, text=f'$ {netvalue}', fg_color='gray97',state='readonly',text_color='black')
amount_entry.pack(pady=5, padx=20, fill="x")

# Payment Amount
amount_label = ctk.CTkLabel(payment_frame, text="Payment Amount Due ($):")
amount_label.pack(anchor="w", padx=20)
amount_entry = ctk.CTkButton(payment_frame, text=f'$ {subtracting_dis}', fg_color='gray97',state='readonly',text_color='black')
amount_entry.pack(pady=5, padx=20, fill="x")





# Payment Method Dropdown
payment_method_label = ctk.CTkLabel(payment_frame, text="Payment Method:")
payment_method_label.pack(anchor="w", padx=20)
payment_method_combobox = ctk.CTkComboBox(payment_frame, values=["Credit Card", "Debit Card", "Cash", "Bank Transfer"])
payment_method_combobox.pack(pady=5, padx=20, fill="x")

# Submit Button
submit_button = ctk.CTkButton(payment_frame, text="Submit Payment", command=process_payment)
submit_button.pack(pady=20)

# Run the CTk main loop
root.mainloop()