import customtkinter as ctk
from BankbookGUI import BankbookGUI
import sqlite3  # Import sqlite3 for database operations

class LoginGUI:
    def __init__(self):
        # Configure appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create the main window
        self.window = ctk.CTk()
        self.window.title("Login System")
        self.window.geometry("400x300")
        
        # Create frame
        self.frame = ctk.CTkFrame(master=self.window)
        self.frame.pack(pady=20, padx=40, fill="both", expand=True)
        
        # Login label
        self.label = ctk.CTkLabel(master=self.frame, text="Login System", font=("Roboto", 24))
        self.label.pack(pady=12, padx=10)
        
        # Username entry
        self.username_entry = ctk.CTkEntry(master=self.frame, placeholder_text="Username")
        self.username_entry.pack(pady=12, padx=10)
        
        # Password entry
        self.password_entry = ctk.CTkEntry(master=self.frame, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=12, padx=10)
        
        # Login button
        self.login_button = ctk.CTkButton(master=self.frame, text="Login", command=self.login_event)
        self.login_button.pack(pady=12, padx=10)


    def login_event(self):
        username = self.username_entry.get()  # Get the entered username
        password = self.password_entry.get()  # Get the entered password

        # Connect to the database
        conn = sqlite3.connect("db.db")
        cursor = conn.cursor()

        # Query the database for the entered credentials
        cursor.execute("SELECT ID, NAME, PASSWORD FROM Admin WHERE NAME = ? AND PASSWORD = ?", (username, password))
        result = cursor.fetchone()

        if result:  # If a matching record is found
            user_id, username, password = result  # Extract ID, username, and password
            print("Login successful")
            self.window.destroy()  # Close the login window
            bankbook_gui = BankbookGUI(user_id, username, password)  # Pass ID, username, and password to BankbookGUI
            bankbook_gui.mainloop()
        else:
            print("Invalid credentials")
            # Optionally, show an error message to the user
            error_label = ctk.CTkLabel(master=self.frame, text="Invalid username or password", text_color="red")
            error_label.pack(pady=5)

        # Close the database connection
        conn.close()
        
    def run(self):
        self.window.mainloop()

# Create and run the application
# if __name__ == "__main__":
#     app = LoginGUI()
#     app.run()