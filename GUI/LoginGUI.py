import customtkinter as ctk
from BankbookGUI import BankbookGUI

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

        #Valid credentials
        valid_username = "admin"
        valid_password = "admin"

        if username == valid_username and password == valid_password:
            print("Login successful")
            self.window.destroy()  # Close the login window
            bankbook_gui = BankbookGUI()  # Open the main application window
            bankbook_gui.mainloop()
        else:
            print("Invalid credentials")
            # Optionally, show an error message to the user
            error_label = ctk.CTkLabel(master=self.frame, text="Invalid username or password", text_color="red")
            error_label.pack(pady=5)
        
    def run(self):
        self.window.mainloop()

# Create and run the application
# if __name__ == "__main__":
#     app = LoginGUI()
#     app.run()