import customtkinter as ctk
from tkinter import messagebox
from tkinter import messagebox
import Create_deposit_slip_GUI
import Create_withdrawal_slip_GUI
import Lookup_Bankbook_GUI
import Prepare_monthly_report_GUI

from utils.db_utils import DatabaseConnection
from BUS.BankbookBUS import BankbookBUS

class BankbookGUI(ctk.CTk):
    def __init__(self, user_id, username, password):
        super().__init__()
        
        self.title("BankBook Management ")
        self.geometry("800x600")

        # Configure grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Set appearance
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Account information
        self.account_detail_label = ctk.CTkLabel(self.left_frame, text="Account Information :", font=ctk.CTkFont(size=18, weight="bold"))
        self.account_detail_label.pack(pady=20)
        print("concac")


        self.user_id = user_id  # Store the user ID
        self.username = username  # Store the username
        self.password = password  # Store the password
        self.db = DatabaseConnection()  # Initialize the database connection utility
        self.bankbook_bus = BankbookBUS()  # Initialize the business layer
        
        self.account_label = ctk.CTkLabel(self.left_frame, text=f"Tài khoản : {self.username}")
        self.account_label.pack(pady=5)

        self.id_account_label = ctk.CTkLabel(self.left_frame, text=f"ID : {self.user_id}")
        self.id_account_label.pack(pady=5)

        # Navigation buttons with hover effects
        button_style = {
            "corner_radius": 10,
            "font": ctk.CTkFont(size=14, family="Segoe UI"),
            "hover": True,
            "fg_color": ("#1E3A8A", "#2B4F8C"),
            "text_color": ("#FFFFFF", "#FFFFFF"),
            "height": 40
        }

        self.create_bankbook_button = ctk.CTkButton(self.left_frame, 
                                                   text="Mở sổ tiết kiệm", 
                                                   command=self.create_bankbook,
                                                   **button_style)
        self.create_bankbook_button.pack(pady=10, padx=10, fill="x")

        self.create_deposit_slip_button = ctk.CTkButton(self.left_frame, 
                                                       text="Lập phiếu gửi tiền", 
                                                       command=self.create_deposit_slip,
                                                       **button_style)
        self.create_deposit_slip_button.pack(pady=10, padx=10, fill="x")

        self.create_withdrawal_slip_button = ctk.CTkButton(self.left_frame, 
                                                          text="Lập phiếu rút tiền", 
                                                          command=self.create_withdrawal_slip,
                                                          **button_style)
        self.create_withdrawal_slip_button.pack(pady=10, padx=10, fill="x")

        self.lookup_bankbook_button = ctk.CTkButton(self.left_frame, 
                                                   text="Tra cứu sổ", 
                                                   command=self.lookup_bankbook,
                                                   **button_style)
        self.lookup_bankbook_button.pack(pady=10, padx=10, fill="x")

        self.prepare_monthly_report_button = ctk.CTkButton(self.left_frame, 
                                                          text="Lập báo cáo tháng", 
                                                          command=self.prepare_monthly_report,
                                                          **button_style)
        self.prepare_monthly_report_button.pack(pady=10, padx=10, fill="x")

        self.change_rules_button = ctk.CTkButton(self.left_frame, 
                                                text="Thay đổi quy định", 
                                                command=self.change_rules,
                                                **button_style)
        self.change_rules_button.pack(pady=10, padx=10, fill="x")

        # Right frame for content with gradient background
        self.right_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=("#FFFFFF", "#1E3A8A"))
        self.right_frame.grid(row=0, column=1, sticky="nsew")

        # Display default screen
        self.create_bankbook()

    def clear_right_frame(self):
        """Clear all widgets in the right frame"""
        for widget in self.right_frame.winfo_children():
            widget.destroy()

    def create_bankbook(self):
        """Display the form for creating a new savings account"""
        self.clear_right_frame()


        # Title
        title_label = ctk.CTkLabel(self.right_frame, text="Mở Sổ Tiết Kiệm", font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=20)

        # Main form with card-like appearance
        form_frame = ctk.CTkFrame(self.right_frame, corner_radius=15, fg_color=("#F0F8FF", "#2B4F8C"))
        form_frame.pack(pady=20, padx=20, fill="x")

        # Entry style configuration
        entry_style = {
            "corner_radius": 8,
            "border_width": 1,
            "font": ctk.CTkFont(size=14, family="Segoe UI"),
            "fg_color": ("#FFFFFF", "#1E3A8A"),
            "border_color": ("#1E3A8A", "#FFFFFF"),
            "height": 35
        }

        # Label style configuration
        label_style = {
            "font": ctk.CTkFont(size=14, family="Segoe UI"),
            "text_color": ("#1E3A8A", "#FFFFFF")
        }

        # Account number and type
        row1_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        row1_frame.pack(fill="x", padx=20, pady=10)
        
        maso_label = ctk.CTkLabel(row1_frame, text="Mã số:", **label_style)
        maso_label.pack(side="left", padx=5)
        self.maso_entry = ctk.CTkEntry(row1_frame)  # Store as instance variable
        self.maso_entry.pack(side="left", expand=True, fill="x", padx=5)
        
        loaitk_label = ctk.CTkLabel(row1_frame, text="Loại tiết kiệm:", **label_style)
        loaitk_label.pack(side="left", padx=5)
        loaitk_entry = ctk.CTkEntry(row1_frame)
        loaitk_entry.pack(side="left", expand=True, fill="x", padx=5)

        # Customer information
        row2_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        row2_frame.pack(fill="x", padx=20, pady=10)
        
        khachhang_label = ctk.CTkLabel(row2_frame, text="Khách hàng:", **label_style)
        khachhang_label.pack(side="left", padx=5)
        self.khachhang_entry = ctk.CTkEntry(row2_frame)  # Store as instance variable
        self.khachhang_entry.pack(side="left", expand=True, fill="x", padx=5)
        
        cmnd_label = ctk.CTkLabel(row2_frame, text="CMND:", **label_style)
        cmnd_label.pack(side="left", padx=5)
        self.cmnd_entry = ctk.CTkEntry(row2_frame)  # Store as instance variable
        self.cmnd_entry.pack(side="left", expand=True, fill="x", padx=5)

        # Address
        row3_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        row3_frame.pack(fill="x", padx=20, pady=10)
        
        diachi_label = ctk.CTkLabel(row3_frame, text="Địa chỉ:", **label_style)
        diachi_label.pack(side="left", padx=5)
        self.diachi_entry = ctk.CTkEntry(row3_frame)  # Store as instance variable
        self.diachi_entry.pack(side="left", expand=True, fill="x", padx=5)

        # Row 4
        row4_frame = ctk.CTkFrame(form_frame)
        row4_frame.pack(fill="x", padx=10, pady=5)
        
        sotiengoi_label = ctk.CTkLabel(row4_frame, text="Số tiền gởi:")
        sotiengoi_label.pack(side="left", padx=5)
        sotiengoi_entry = ctk.CTkEntry(row4_frame)
        sotiengoi_entry.pack(side="left", expand=True, fill="x", padx=5)

        # Buttons frame
        button_frame = ctk.CTkFrame(self.right_frame)
        button_frame.pack(pady=20)
        
        save_button = ctk.CTkButton(button_frame, text="Lưu", command=self.insert_new_record)
        save_button = ctk.CTkButton(button_frame, text="Lưu", command=self.insert_new_record)
        save_button.pack(side="left", padx=10)
        
        cancel_button = ctk.CTkButton(button_frame, text="Huỷ", command=self.clear_bankbook_fields)  # Link to clear fields
        cancel_button = ctk.CTkButton(button_frame, text="Huỷ", command=self.clear_bankbook_fields)  # Link to clear fields
        cancel_button.pack(side="left", padx=10)

    def create_deposit_slip(self):
        """Display deposit slip creation screen"""
        self.clear_right_frame()
        Create_deposit_slip_GUI.Create_deposit_slip_GUI(self.right_frame)

    def create_withdrawal_slip(self):
        """Display withdrawal slip creation screen"""
        self.clear_right_frame()
        Create_withdrawal_slip_GUI.Create_withdrawal_slip_GUI(self.right_frame)
    
    def lookup_bankbook(self):
        """Display account lookup screen"""
        self.clear_right_frame()
        # self.geometry("1200x800")  # Resize window for lookup screen
        Lookup_Bankbook_GUI.Lookup_Bankbook_GUI(self.right_frame)
    
    def prepare_monthly_report(self):
        """Display monthly report generation screen"""
        self.clear_right_frame()
        Prepare_monthly_report_GUI.Prepare_monthly_report_GUI(self.right_frame)
        Prepare_monthly_report_GUI.Prepare_monthly_report_GUI(self.right_frame)
    
    def change_rules(self):
        """Display rules change screen"""
        self.clear_right_frame()
        # Change_rules_GUI.Change_rules_GUI(self.right_frame)
    
    def insert_new_record(self):
        try:
            # Gather data from form fields
            maso = self.maso_entry.get()
            loaitk = self.loaitk_entry.get()
            khachhang = self.khachhang_entry.get()
            cmnd = self.cmnd_entry.get()
            diachi = self.diachi_entry.get()
            ngaymo = self.ngaymo_entry.get()
            sotiengui = self.sotiengui_entry.get()

            # Validate required fields
            if not (maso and loaitk and khachhang and cmnd and diachi and ngaymo and sotiengui):
                print("All fields are required.")
                return

            # Call the business layer to insert the record
            result = self.bankbook_bus.insert_new_record(
                maso, loaitk, khachhang, cmnd, diachi, ngaymo, sotiengui
            )

            if result:
                print("New bankbook record inserted successfully.")
            else:
                print("Failed to insert bankbook record.")
        except Exception as e:
            print(f"Error inserting data: {e}")

    def clear_bankbook_fields(self):
            print("Clear button clicked")  # Debugging statement
            try:
                self.maso_entry.delete(0, "end")
                self.loaitk_entry.delete(0, "end")
                self.khachhang_entry.delete(0, "end")
                self.cmnd_entry.delete(0, "end")
                self.diachi_entry.delete(0, "end")
                self.ngaymo_entry.delete(0, "end")
                self.sotiengui_entry.delete(0, "end")
                print("Fields cleared successfully")  # Debugging statement
            except Exception as e:
                print(f"Error clearing fields: {e}")  # Debugging statement

# if __name__ == "__main__":
#     app = BankbookGUI()
#     app.mainloop()