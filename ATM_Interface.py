import tkinter as tk
from tkinter import messagebox
import pyttsx3

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

class ATM:
    def __init__(self, master):
        self.master = master
        self.master.title("ATM MACHINE")
        self.master.geometry("400x500")
        self.master.configure(bg="#D3D3D3")  # Setting background colour to light gray

        # specifying attributes
        self.balance = 10000
        self.transaction_history = []
        self.pin = "1234"  # Set a default 4-digit PIN
        self.account_number = "9876543210"  # Dummy account number
        self.is_logged_in = False

        # ATM UI elements (initially hidden)
        self.atm_frame = tk.Frame(master, bg="#D3D3D3")

        # Row for amount entry and label
        self.amount_frame = tk.Frame(self.atm_frame, bg="#D3D3D3")
        self.amount_label = tk.Label(self.amount_frame, text="Enter amount:", font=("Arial", 12), bg="#D3D3D3")
        self.amount_label.pack(side="left", padx=5)

        self.entry = tk.Entry(self.amount_frame, font=("Arial", 15), width=15, bd=5)
        self.entry.pack(side="right", padx=5)
        self.amount_frame.pack(pady=10)

        # Label for "Select Operation" in blue color
        self.operation_label = tk.Label(self.atm_frame, text="Select Operation", font=("Arial", 15, "bold"), fg="blue", bg="#D3D3D3")
        self.operation_label.pack(pady=10)

        # creating buttons
        button_style = {"font": ("Arial", 12), "width": 20, "bg": "#4682B4", "fg": "white", "bd": 3}
        self.btn_deposit = tk.Button(self.atm_frame, text="Deposit", command=self.deposit, **button_style)
        self.btn_deposit.pack(pady=5)

        self.btn_withdraw = tk.Button(self.atm_frame, text="Withdraw", command=self.withdraw, **button_style)
        self.btn_withdraw.pack(pady=5)

        self.btn_balance = tk.Button(self.atm_frame, text="Check Balance", command=self.check_balance, **button_style)
        self.btn_balance.pack(pady=5)

        self.btn_history = tk.Button(self.atm_frame, text="Transaction History", command=self.show_history, **button_style)
        self.btn_history.pack(pady=5)

        self.btn_exit = tk.Button(self.atm_frame, text="Exit", command=self.exit_atm, **button_style)
        self.btn_exit.pack(pady=5)

        self.message_label = tk.Label(self.atm_frame, text="", font=("Arial", 15), bg="#D3D3D3")
        self.message_label.pack(pady=20)

        # PIN and Account Number entry screen 
        self.pin_label = tk.Label(master, text="Welcome to ATM\nPlease Enter Account Number and 4-digit PIN", font=("Arial", 15, "bold"), bg="#D3D3D3")
        self.pin_label.pack(pady=20)

        self.acc_label = tk.Label(master, text="Account Number", font=("Arial", 12), bg="#D3D3D3")
        self.acc_label.pack(pady=5)

        self.acc_entry = tk.Entry(master, font=("Arial", 15), width=15)  # Account number field
        self.acc_entry.pack(pady=5)

        self.pin_entry = tk.Entry(master, font=("Arial", 15), width=10, show="*")  # pin field and pin hidden with "*"
        self.pin_entry.pack(pady=10)

        self.pin_btn = tk.Button(master, text="Login", command=self.check_pin, font=("Arial", 12), width=20, bg="#4682B4", fg="white")
        self.pin_btn.pack(pady=5)

        # Call welcome message and play voice simultaneously
        self.welcome_message()

    def welcome_message(self):
        """Play welcome message first."""
        speak("Welcome to the ATM. Please enter your account number and 4 digit PIN to continue.")
        self.message_label.config(text="Welcome to the ATM")

    def check_pin(self):
        """Check if the entered PIN and Account Number are correct."""
        entered_pin = self.pin_entry.get()
        entered_account = self.acc_entry.get()
        if entered_pin == self.pin and entered_account == self.account_number:
            self.is_logged_in = True
            self.pin_label.pack_forget()
            self.acc_label.pack_forget()
            self.acc_entry.pack_forget()
            self.pin_entry.pack_forget()
            self.pin_btn.pack_forget()
            self.show_atm_interface()
            speak("PIN and Account Number correct. You are now logged in.")
        else:
            messagebox.showerror("Error", "Incorrect PIN or Account Number")
            speak("Incorrect PIN or Account Number. Please try again.")

    def show_atm_interface(self):
        """Display the ATM options after PIN verification."""
        self.atm_frame.pack()
        self.message_label.config(text="Select your operation")

    def deposit(self):
        """Perform deposit operation."""
        amount = self.get_amount()
        if amount is not None:
            self.balance += amount
            self.transaction_history.append(f"Deposited: {amount}")
            self.message_label.config(text=f"Deposited: {amount}")
            speak(f"You have successfully deposited {amount}")
        self.clear_entry()

    def withdraw(self):
        """Perform withdraw operation."""
        amount = self.get_amount()
        if amount is not None:
            if amount <= self.balance:
                self.balance -= amount
                self.transaction_history.append(f"Withdrew: {amount}")
                self.message_label.config(text=f"Withdrew: {amount}")
                speak(f"You have successfully withdrawn {amount}")
            else:
                messagebox.showerror("Error", "Insufficient balance")
                speak("Insufficient balance")
        self.clear_entry()

    def check_balance(self):
        self.message_label.config(text=f"Current Balance: {self.balance}")
        speak(f"Your current balance is {self.balance}")

    def show_history(self):
        history_str = "\n".join(self.transaction_history)
        if history_str:
            messagebox.showinfo("Transaction History", history_str)
        else:
            messagebox.showinfo("Transaction History", "No transactions yet.")
        speak("Here is your transaction history")

    def exit_atm(self):
        """Return to the PIN entry screen upon exiting instead of closing the window."""
        speak("Thank you for using the ATM. You are logged out.")
        self.atm_frame.pack_forget()  # Hide the ATM interface
        self.pin_label.pack(pady=20)  # Show PIN entry interface again
        self.acc_label.pack(pady=5)
        self.acc_entry.pack(pady=5)
        self.pin_entry.pack(pady=10)
        self.pin_btn.pack(pady=5)
        self.clear_entry()  # Clear any entered values
        self.clear_login_fields()  # Clear the PIN and Account Number fields

    def clear_login_fields(self):
        """Clear the PIN and Account Number fields."""
        self.pin_entry.delete(0, tk.END)
        self.acc_entry.delete(0, tk.END)

    def get_amount(self):
        """Get the entered amount and validate it."""
        try:
            amount = float(self.entry.get())
            if amount <= 0:
                raise ValueError("Amount should be positive")
            return amount
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")
            speak("Please enter a valid amount")
            return None

    def clear_entry(self):
        """Clear the input field."""
        self.entry.delete(0, tk.END)

# Initialize the ATM GUI
root = tk.Tk()
atm = ATM(root)
root.mainloop()
