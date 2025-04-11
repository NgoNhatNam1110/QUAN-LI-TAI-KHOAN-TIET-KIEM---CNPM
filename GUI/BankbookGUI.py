import customtkinter as ctk
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

        self.user_id = user_id  # Store the user ID
        self.username = username  # Store the username
        self.password = password  # Store the password
        self.db = DatabaseConnection()  # Initialize the database connection utility
        self.bankbook_bus = BankbookBUS()  # Initialize the business layer

        self.title("BankBook Management")
        self.geometry("800x600")

        # Configure grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Left frame
        self.left_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.left_frame.grid(row=0, column=0, sticky="nsew")
        
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Account information
        self.account_detail_label = ctk.CTkLabel(self.left_frame, text="Account Information :", font=ctk.CTkFont(size=18, weight="bold"))
        self.account_detail_label.pack(pady=20)

        self.account_label = ctk.CTkLabel(self.left_frame, text=f"Tài khoản : {self.username}")
        self.account_label.pack(pady=5)

        self.id_account_label = ctk.CTkLabel(self.left_frame, text=f"ID : {self.user_id}")
        self.id_account_label.pack(pady=5)

        # Các nút chức năng
        self.create_bankbook_button = ctk.CTkButton(self.left_frame, text="Mở sổ tiết kiệm", command=self.create_bankbook)
        self.create_bankbook_button.pack(pady=10)

        self.create_deposit_slip_button= ctk.CTkButton(self.left_frame, text="Lập phiếu gởi tiền", command=self.create_deposit_slip)
        self.create_deposit_slip_button.pack(pady=10)

        self.create_withdrawal_slip_button = ctk.CTkButton(self.left_frame, text="Lập phiếu rút tiền", command=self.create_withdrawal_slip)
        self.create_withdrawal_slip_button.pack(pady=10)

        self.lookup_bankbook_button = ctk.CTkButton(self.left_frame, text="Tra cứu sổ", command=self.lookup_bankbook)
        self.lookup_bankbook_button.pack(pady=10)

        self.prepare_monthly_report_button = ctk.CTkButton(self.left_frame, text="Lập báo cáo tháng", command=self.prepare_monthly_report)
        self.prepare_monthly_report_button.pack(pady=10)

        self.change_rules_button = ctk.CTkButton(self.left_frame, text="Thay đổi qui định", command=self.change_rules)
        self.change_rules_button.pack(pady=10)

        # Right frame
        self.right_frame = ctk.CTkFrame(self, corner_radius=0)
        self.right_frame.grid(row=0, column=1, sticky="nsew")

        # Display default information
        self.create_bankbook()

    def clear_right_frame(self):
        # Clear all widgets in the right frame
        for widget in self.right_frame.winfo_children():
            widget.destroy()

    def create_bankbook(self):
        self.clear_right_frame()

        # Title
        title_label = ctk.CTkLabel(self.right_frame, text="Mở Sổ Tiết Kiệm", font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=20)

        # Create main form frame
        form_frame = ctk.CTkFrame(self.right_frame)
        form_frame.pack(pady=20, padx=20, fill="x")

        # Row 1
        row1_frame = ctk.CTkFrame(form_frame)
        row1_frame.pack(fill="x", padx=10, pady=5)
        
        maso_label = ctk.CTkLabel(row1_frame, text="Mã số:")
        maso_label.pack(side="left", padx=5)
        self.maso_entry = ctk.CTkEntry(row1_frame)  # Store as instance variable
        self.maso_entry.pack(side="left", expand=True, fill="x", padx=5)
        
        loaitk_label = ctk.CTkLabel(row1_frame, text="Loại tiết kiệm:")
        loaitk_label.pack(side="left", padx=5)
        self.selected_option = ctk.StringVar(value="3 tháng")
        options = ["3 thang", "6 thang", "vo han"]
        dropdown = ctk.CTkOptionMenu(row1_frame, variable=self.selected_option, text_color="black", fg_color="#F5F5F5", values=options)
        dropdown.pack(side="left", expand=True, fill="x", pady=5)
        # self.loaitk_entry = ctk.CTkEntry(row1_frame)  # Store as instance variable
        # self.loaitk_entry.pack(side="left", expand=True, fill="x", padx=5)

        # Row 2
        row2_frame = ctk.CTkFrame(form_frame)
        row2_frame.pack(fill="x", padx=10, pady=5)
        
        khachhang_label = ctk.CTkLabel(row2_frame, text="Khách hàng:")
        khachhang_label.pack(side="left", padx=5)
        self.khachhang_entry = ctk.CTkEntry(row2_frame)  # Store as instance variable
        self.khachhang_entry.pack(side="left", expand=True, fill="x", padx=5)
        
        cmnd_label = ctk.CTkLabel(row2_frame, text="CMND:")
        cmnd_label.pack(side="left", padx=5)
        self.cmnd_entry = ctk.CTkEntry(row2_frame)  # Store as instance variable
        self.cmnd_entry.pack(side="left", expand=True, fill="x", padx=5)

        # Row 3
        row3_frame = ctk.CTkFrame(form_frame)
        row3_frame.pack(fill="x", padx=10, pady=5)
        
        diachi_label = ctk.CTkLabel(row3_frame, text="Địa chỉ:")
        diachi_label.pack(side="left", padx=5)
        self.diachi_entry = ctk.CTkEntry(row3_frame)  # Store as instance variable
        self.diachi_entry.pack(side="left", expand=True, fill="x", padx=5)
        
        ngaymo_label = ctk.CTkLabel(row3_frame, text="Ngày mở sổ:")
        ngaymo_label.pack(side="left", padx=5)
        self.ngaymo_entry = ctk.CTkEntry(row3_frame)  # Store as instance variable
        self.ngaymo_entry.pack(side="left", expand=True, fill="x", padx=5)

        # Row 4
        row4_frame = ctk.CTkFrame(form_frame)
        row4_frame.pack(fill="x", padx=10, pady=5)
        # Row 5
        row5_frame = ctk.CTkFrame(form_frame)
        row5_frame.pack(fill="x", padx=10, pady=5)
        # Row 6
        row6_frame = ctk.CTkFrame(form_frame)
        row6_frame.pack(fill="x", padx=10, pady=5)

        sotiengui_label = ctk.CTkLabel(row4_frame, text="Số tiền gửi:")
        sotiengui_label.pack(side="left", padx=5)
        self.sotiengui_entry = ctk.CTkEntry(row4_frame)  # Store as instance variable
        self.sotiengui_entry.pack(side="left", expand=True, fill="x", padx=5)
        self.entry_var = ctk.StringVar()
        self.result_label = ctk.CTkLabel(row6_frame, text="")
        self.result_label.pack(side="left", expand= True, fill="x", padx=5)

        # Buttons frame
        button_frame = ctk.CTkFrame(self.right_frame)
        button_frame.pack(pady=20)
        
        save_button = ctk.CTkButton(button_frame, text="Lưu", command=self.insert_new_record)
        save_button.pack(side="left", padx=10)
        
        cancel_button = ctk.CTkButton(button_frame, text="Huỷ", command=self.clear_bankbook_fields)  # Link to clear fields
        cancel_button.pack(side="left", padx=10)

    def insert_new_record(self):
        try:
            # Gather data from form fields
            maso = self.maso_entry.get()
            # loaitk = self.loaitk_entry.get()
            loaitk = self.selected_option.get()
            khachhang = self.khachhang_entry.get()
            cmnd = self.cmnd_entry.get()
            diachi = self.diachi_entry.get()
            ngaymo = self.ngaymo_entry.get()
            sotiengui = self.sotiengui_entry.get()

            # Validate required fields
            if not (maso and loaitk and khachhang and cmnd and diachi and ngaymo and sotiengui):
                print("All fields are required.")
                return
            
            # check if 
            try:
                value = float(self.sotiengui_entry.get().replace(",", ""))
                if value >= 1000000:
                    self.result_label.configure(
                        text=f"Giá trị hợp lệ: {value:,.0f}",
                        text_color="green"
                    )
                else:
                    messagebox.showerror(
                        "Lỗi",
                        "Số tiền phải lớn hơn hoặc bằng 1,000,000!"
                    )
                    self.entry_var.set("")
                    self.sotiengui_entry.focus()
            except ValueError:
                messagebox.showerror(
                    "Lỗi",
                    "Vui lòng nhập một số hợp lệ!"
                )
                self.entry_var.set("")
                self.sotiengui_entry.focus()

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
            # self.loaitk_entry.delete(0, "end")
            self.khachhang_entry.delete(0, "end")
            self.cmnd_entry.delete(0, "end")
            self.diachi_entry.delete(0, "end")
            self.ngaymo_entry.delete(0, "end")
            self.sotiengui_entry.delete(0, "end")
            print("Fields cleared successfully")  # Debugging statement
        except Exception as e:
            print(f"Error clearing fields: {e}")  # Debugging statement

    def create_deposit_slip(self):
        self.clear_right_frame()
        Create_deposit_slip_GUI.Create_deposit_slip_GUI(self.right_frame)

    def create_withdrawal_slip(self):
        self.clear_right_frame()
        Create_withdrawal_slip_GUI.Create_withdrawal_slip_GUI(self.right_frame)
    
    def lookup_bankbook(self):
        self.clear_right_frame()
        Lookup_Bankbook_GUI.Lookup_Bankbook_GUI(self.right_frame)
    
    def prepare_monthly_report(self):
        self.clear_right_frame()
        Prepare_monthly_report_GUI.Prepare_monthly_report_GUI(self.right_frame)
    
    def change_rules(self):
        self.clear_right_frame()
        # Change_rules_GUI.Change_rules_GUI(self.right_frame)

# if __name__ == "__main__":
#     app = BankbookGUI()
#     app.mainloop()