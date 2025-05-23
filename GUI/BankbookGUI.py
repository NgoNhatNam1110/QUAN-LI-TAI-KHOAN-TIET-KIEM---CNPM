import customtkinter as ctk
import re
from tkinter import messagebox
from datetime import datetime
from tkcalendar import Calendar
import tkinter as tk
import Change_rules_GUI
import Create_deposit_slip_GUI
import Create_withdrawal_slip_GUI
import Lookup_Bankbook_GUI
import Prepare_monthly_report_GUI
from utils.db_utils import DatabaseConnection
from BUS.BankbookBUS import BankbookBUS


class BankbookGUI(ctk.CTk):
    def __init__(self, user_id, username, password):
        super().__init__()

        # Store user information
        self.user_id = user_id
        self.username = username
        self.password = password
        self.db = DatabaseConnection()
        self.bankbook_bus = BankbookBUS()

        # Configure window
        self.title("Quản Lý Sổ Tiết Kiệm")
        # self.geometry("800x600")
        self.geometry("1200x800") 

        # Configure grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Set appearance
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Left frame for navigation with gradient background
        self.left_frame = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color=("#F0F8FF", "#1E3A8A"))
        self.left_frame.grid(row=0, column=0, sticky="nsew")
        
        # Account information section with card-like appearance
        account_card = ctk.CTkFrame(self.left_frame, corner_radius=15, fg_color=("#FFFFFF", "#2B4F8C"))
        account_card.pack(pady=20, padx=10, fill="x")
        
        self.account_detail_label = ctk.CTkLabel(account_card, 
                                                text="Thông Tin Tài Khoản", 
                                                font=ctk.CTkFont(size=18, weight="bold", family="Segoe UI"),
                                                text_color=("#1E3A8A", "#FFFFFF"))
        self.account_detail_label.pack(pady=10)

        self.account_label = ctk.CTkLabel(account_card, 
                                         text=f"Tài khoản: {self.username}",
                                         font=ctk.CTkFont(size=14, family="Segoe UI"),
                                         text_color=("#1E3A8A", "#FFFFFF"))
        self.account_label.pack(pady=5)

        self.id_account_label = ctk.CTkLabel(account_card, 
                                            text=f"ID: {self.user_id}",
                                            font=ctk.CTkFont(size=14, family="Segoe UI"),
                                            text_color=("#1E3A8A", "#FFFFFF"))
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

        # self.prepare_monthly_report_button = ctk.CTkButton(self.left_frame, 
        #                                                   text="Lập báo cáo tháng", 
        #                                                   command=self.prepare_monthly_report,
        #                                                   **button_style)
        # self.prepare_monthly_report_button.pack(pady=10, padx=10, fill="x")

        # self.change_rules_button = ctk.CTkButton(self.left_frame, 
        #                                         text="Thay đổi quy định", 
        #                                         command=self.change_rules,
        #                                         **button_style)
        # self.change_rules_button.pack(pady=10, padx=10, fill="x")

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

        # Title with gradient background
        title_frame = ctk.CTkFrame(self.right_frame, corner_radius=15, fg_color=("#1E3A8A", "#2B4F8C"))
        title_frame.pack(pady=20, padx=20, fill="x")
        
        title_label = ctk.CTkLabel(title_frame, 
                                text="Mở Sổ Tiết Kiệm", 
                                font=ctk.CTkFont(size=24, weight="bold", family="Segoe UI"),
                                text_color=("#FFFFFF", "#FFFFFF"))
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

        # Automatically generate the account number
        generated_maso = self.auto_increase_maso()
        self.maso_entry = ctk.CTkEntry(row1_frame, **entry_style)
        self.maso_entry.insert(0, generated_maso if generated_maso else "Không thể tạo mã số")
        self.maso_entry.configure(state='readonly')  # Set to readonly
        self.maso_entry.pack(side="left", expand=True, fill="x", padx=5)

        loaitk_label = ctk.CTkLabel(row1_frame, text="Loại tiết kiệm:", **label_style)
        loaitk_label.pack(side="left", padx=5)
        self.selected_option = ctk.StringVar(value="3 tháng")
        options = self.bankbook_bus.GetInterestOptions()
        dropdown = ctk.CTkOptionMenu(row1_frame, 
                                    variable=self.selected_option, 
                                    values=options,
                                    corner_radius=8,
                                    font=ctk.CTkFont(size=14, family="Segoe UI"),
                                    fg_color=("#FFFFFF", "#1E3A8A"),
                                    button_color=("#1E3A8A", "#2B4F8C"),
                                    button_hover_color=("#2B4F8C", "#1E3A8A"),
                                    text_color=("#1E3A8A", "#FFFFFF"))
        dropdown.pack(side="left", expand=True, fill="x", padx=5)

        # Customer information
        row2_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        row2_frame.pack(fill="x", padx=20, pady=10)
        
        khachhang_label = ctk.CTkLabel(row2_frame, text="Khách hàng:", **label_style)
        khachhang_label.pack(side="left", padx=5)
        self.khachhang_entry = ctk.CTkEntry(row2_frame, **entry_style)
        self.khachhang_entry.pack(side="left", expand=True, fill="x", padx=5)
        
        cmnd_label = ctk.CTkLabel(row2_frame, text="CMND:", **label_style)
        cmnd_label.pack(side="left", padx=5)
        self.cmnd_entry = ctk.CTkEntry(row2_frame, **entry_style)
        self.cmnd_entry.pack(side="left", expand=True, fill="x", padx=5)

        # Address
        row3_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        row3_frame.pack(fill="x", padx=20, pady=10)
        
        diachi_label = ctk.CTkLabel(row3_frame, text="Địa chỉ:", **label_style)
        diachi_label.pack(side="left", padx=5)
        self.diachi_entry = ctk.CTkEntry(row3_frame, **entry_style)
        self.diachi_entry.pack(side="left", expand=True, fill="x", padx=5)

        # Opening date
        row4_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        row4_frame.pack(fill="x", padx=20, pady=10)
        current_date = datetime.now()

        ngaymo_label = ctk.CTkLabel(row4_frame, text="Ngày mở sổ:", **label_style)
        ngaymo_label.pack(side="left", padx=5)
        self.ngaymo_entry = ctk.CTkEntry(row4_frame, **entry_style)
        self.ngaymo_entry.pack(side="left", expand=True, fill="x", padx=5)
        self.ngaymo_entry.insert(0, current_date.strftime("%Y-%m-%d"))
        self.ngaymo_entry.configure(state='readonly')
        
        # Deposit amount
        row5_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        row5_frame.pack(fill="x", padx=20, pady=10)

        sotiengui_label = ctk.CTkLabel(row5_frame, text="Số tiền gửi:", **label_style)
        sotiengui_label.pack(side="left", padx=5)
        self.sotiengui_entry = ctk.CTkEntry(row5_frame, **entry_style)
        self.sotiengui_entry.pack(side="left", expand=True, fill="x", padx=5)
        
        # Action buttons with hover effects
        button_frame = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        button_frame.pack(pady=20)
        
        button_style = {
            "corner_radius": 10,
            "font": ctk.CTkFont(size=14, family="Segoe UI"),
            "hover": True,
            "height": 40,
            "width": 120
        }
        
        save_button = ctk.CTkButton(button_frame, 
                                  text="Lưu", 
                                  command=self.insert_new_record,
                                  fg_color=("#1E3A8A", "#2B4F8C"),
                                  hover_color=("#2B4F8C", "#1E3A8A"),
                                  **button_style)
        save_button.pack(side="left", padx=10)
        
        cancel_button = ctk.CTkButton(button_frame, 
                                     text="Hủy", 
                                     command=self.clear_bankbook_fields,
                                     fg_color=("#DC3545", "#C82333"),
                                     hover_color=("#C82333", "#DC3545"),
                                     **button_style)
        cancel_button.pack(side="left", padx=10)

    def insert_new_record(self):
        """Insert a new savings account record"""
        try:
            # Get form data
            maso = self.maso_entry.get()
            loaitk = self.selected_option.get()
            khachhang = self.khachhang_entry.get()
            cmnd = self.cmnd_entry.get()
            diachi = self.diachi_entry.get()
            ngaymo = self.ngaymo_entry.get()
            sotiengui = self.sotiengui_entry.get()
            
            print("sotiengui", sotiengui)
            # Validate ID number
            if self.checkCMND(cmnd):
                messagebox.showerror("Error", "CMND đã tồn tại trong hệ thống!")
                self.cmnd_entry.focus()
                return
            elif self.checkdinhdangCMND(cmnd) == False:
                self.cmnd_entry.focus()
                return      

            # Validate account number
            if self.checkmaso(maso):
                messagebox.showerror("Error", "Mã số đã tồn tại trong hệ thống!")
                self.maso_entry.focus()
                return

            # Validate minimum deposit amount
            if not self.checkminimumDeposit(loaitk, sotiengui):
                self.sotiengui_entry.focus()
                return
            
            # Validate customer name
            if not self.checkCustomerName(khachhang):
                messagebox.showerror("Error", "Tên khách hàng không hợp lệ!")
                self.khachhang_entry.focus()
                return

            # Insert record
            result = self.bankbook_bus.insert_new_record(
                maso, loaitk, khachhang, cmnd, diachi, ngaymo, sotiengui
            )

            if result:
                messagebox.showinfo("Thành công", "Mở sổ tiết kiệm thành công")
                self.clear_bankbook_fields()
                self.maso_entry.configure(state='normal')
                self.maso_entry.delete(0, "end")
                self.maso_entry.insert(0, self.auto_increase_maso())
            else:
                messagebox.showerror("Error", "Không thể mở sổ tiết kiệm")
        except Exception as e:
            print(f"Error inserting data: {e}")

    def clear_bankbook_fields(self):
        """Clear all form fields"""
        try:
            self.maso_entry.delete(0, "end")
            self.khachhang_entry.delete(0, "end")
            self.cmnd_entry.delete(0, "end")
            self.diachi_entry.delete(0, "end")
            self.ngaymo_entry.delete(0, "end")
            self.sotiengui_entry.delete(0, "end")
        except Exception as e:
            print(f"Error clearing fields: {e}")

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
        Lookup_Bankbook_GUI.Lookup_Bankbook_GUI(self.right_frame)
    
    def prepare_monthly_report(self):
        """Display monthly report generation screen"""
        self.clear_right_frame()
        Prepare_monthly_report_GUI.Prepare_monthly_report_GUI(self.right_frame)
    
    def checkCMND(self, cmnd):
        """Check if ID number already exists"""
        check = self.bankbook_bus.checkCMND(cmnd)
        return check
    
    def checkdinhdangCMND(self, cmnd):
        pattern = r"^\d{9}$"
        check = bool(re.match(pattern, cmnd))
        if check == False :
            messagebox.showerror("Error","Sai định dạng CMND, vui lòng nhập đúng 9 số!")
            print(check)
            return False
        else :
            return True
        
    def checkminimumDeposit(self, loaitk, sotiengui):
        """Check if the deposit amount meets the minimum requirement"""
        message = self.bankbook_bus.checkminimumDeposit(loaitk, sotiengui)
        if message != "Số tiền gửi hợp lệ.":
            messagebox.showerror("Thông báo", message)
            return False
        return True
    
    def checkmaso(self, maso):
        """Check if account number already exists"""
        check = self.bankbook_bus.checkmaso(maso)
        return check
    
    # def checkdinhdangMaSo(self, maso):
    #     pattern = r"^STK\d{10}$"
    #     check = bool(re.match(pattern, maso))
    #     if check == False :
    #         print(check)
    #         return False
    #     else :
    #         return True

    def change_rules(self):
        """Display rules change screen"""
        self.clear_right_frame()
        Change_rules_GUI.Change_rules_GUI(self.right_frame)

    def auto_increase_maso(self, event=None):
        """Automatically increase the account number when the entry is focused"""
        try:
            new_maso = self.bankbook_bus.generate_new_maso()
            if new_maso:
                return new_maso
            else:
                messagebox.showerror("Lỗi", "Không thể tạo mã số mới. Vui lòng thử lại!")
                return None
        except Exception as e:
            print(f"Error generating account number in GUI: {e}")
        return None
    
    def checkCustomerName(self, khachhang):
        """Check if the customer name is valid"""
        pattern = r"^[a-zA-Z\s]+$"
        check = bool(re.match(pattern, khachhang))
        if not check:
            return False
        return True
    
# if __name__ == "__main__":
#     app = BankbookGUI()
#     app.mainloop()