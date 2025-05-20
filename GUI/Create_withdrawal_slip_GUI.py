import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from BUS.Create_withdrawal_slip_BUS import Create_withdrawal_slip_BUS

class Create_withdrawal_slip_GUI:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.create_withdrawal_slip_bus = Create_withdrawal_slip_BUS()  # Initialize the business layer
        self.create_screen_withdrawal_slip()
    
    def create_screen_withdrawal_slip(self):
        # Title with gradient background
        title_frame = ctk.CTkFrame(self.parent_frame, corner_radius=15, fg_color=("#1E3A8A", "#2B4F8C"))
        title_frame.pack(pady=20, padx=20, fill="x")
        
        title_label = ctk.CTkLabel(title_frame, 
                                  text="Lập Phiếu Rút Tiền", 
                                  font=ctk.CTkFont(size=24, weight="bold", family="Segoe UI"),
                                  text_color=("#FFFFFF", "#FFFFFF"))
        title_label.pack(pady=20)

        # Create main form frame with card-like appearance
        form_frame = ctk.CTkFrame(self.parent_frame, corner_radius=15, fg_color=("#F0F8FF", "#2B4F8C"))
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

        # Row 1
        row1_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        row1_frame.pack(fill="x", padx=20, pady=10)
        
        maso_label = ctk.CTkLabel(row1_frame, text="Mã số:", **label_style)
        maso_label.pack(side="left", padx=5)
        self.maso_entry = ctk.CTkEntry(row1_frame, **entry_style)
        self.maso_entry.pack(side="left", expand=True, fill="x", padx=5)
        
        khachhang_label = ctk.CTkLabel(row1_frame, text="Khách hàng:", **label_style)
        khachhang_label.pack(side="left", padx=5)
        self.khachhang_entry = ctk.CTkEntry(row1_frame, **entry_style)
        self.khachhang_entry.bind("<FocusOut>", self.load_account_balance_and_customer_name)
        self.khachhang_entry.pack(side="left", expand=True, fill="x", padx=5)
        self.khachhang_entry.configure(state="readonly")

        sodu_label = ctk.CTkLabel(row1_frame, text="Số dư (VNĐ):", **label_style)
        sodu_label.pack(side="left", padx=5)
        self.sodu_entry = ctk.CTkEntry(row1_frame, **entry_style)
        self.sodu_entry.pack(side="left", expand=True, fill="x", padx=5)
        self.maso_entry.bind("<FocusOut>", self.load_account_balance_and_customer_name)

        self.sodu_entry.configure(state="readonly")


        # Row 2
        row2_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        row2_frame.pack(fill="x", padx=20, pady=10)
        current_date = datetime.now()
        
        ngayrut_label = ctk.CTkLabel(row2_frame, text="Ngày rút:", **label_style)
        ngayrut_label.pack(side="left", padx=5)
        self.ngayrut_entry = ctk.CTkEntry(row2_frame, **entry_style)
        self.ngayrut_entry.pack(side="left", expand=True, fill="x", padx=5)
        self.ngayrut_entry.insert(0, current_date.strftime("%Y-%m-%d"))
        self.ngayrut_entry.configure(state="readonly")
        
        sotienrut_label = ctk.CTkLabel(row2_frame, text="Số tiền rút:", **label_style)
        sotienrut_label.pack(side="left", padx=5)
        self.sotienrut_entry = ctk.CTkEntry(row2_frame, **entry_style)
        self.sotienrut_entry.pack(side="left", expand=True, fill="x", padx=5)

        self.selected_option = ctk.StringVar(value="3 tháng")

        options = self.create_withdrawal_slip_bus.GetInterestOptions()
        kyhan_label = ctk.CTkLabel(row2_frame, text="Kỳ hạn:", **label_style)
        kyhan_label.pack(side="left", padx=5)
        dropdown = ctk.CTkOptionMenu(row2_frame, 
                                    variable=self.selected_option, 
                                    values=options,
                                    corner_radius=8,
                                    font=ctk.CTkFont(size=14, family="Segoe UI"),
                                    fg_color=("#FFFFFF", "#1E3A8A"),
                                    button_color=("#1E3A8A", "#2B4F8C"),
                                    button_hover_color=("#2B4F8C", "#1E3A8A"),
                                    text_color=("#1E3A8A", "#FFFFFF"))
        dropdown.pack(side="left", expand=True, fill="x", padx=5)

        # Buttons frame with hover effects
        button_frame = ctk.CTkFrame(self.parent_frame, fg_color="transparent")
        button_frame.pack(pady=20)
        
        button_style = {
            "corner_radius": 10,
            "font": ctk.CTkFont(size=14, family="Segoe UI"),
            "hover": True,
            "height": 40,
            "width": 120
        }
        
        save_button = ctk.CTkButton(button_frame, 
                                  text="Lập phiếu", 
                                  command=self.withdrawal_slip_event,
                                  fg_color=("#1E3A8A", "#2B4F8C"),
                                  hover_color=("#2B4F8C", "#1E3A8A"),
                                  **button_style)
        save_button.pack(side="left", padx=10)
        
        cancel_button = ctk.CTkButton(button_frame, 
                                     text="Huỷ", 
                                     command=self.clear_fields,
                                     fg_color=("#DC3545", "#C82333"),
                                     hover_color=("#C82333", "#DC3545"),
                                     **button_style)
        cancel_button.pack(side="left", padx=10)

    def withdrawal_slip_event(self):
        try:
            # Retrieve input values
            maso = self.maso_entry.get()
            khachhang = self.khachhang_entry.get()
            ngayrut = self.ngayrut_entry.get()
            sotienrut = self.sotienrut_entry.get()
            kyhansaukhirut = self.selected_option.get()
            
            # Validate inputs
            if not maso or not khachhang or not ngayrut or not sotienrut:
                messagebox.showerror(
                    "Lỗi",
                    "Vui lòng nhập đầy đủ các trường dữ liệu"
                )
                return
            
            # Validate the amount entered
            if not self.validate_so_tien_gui(sotienrut):
                messagebox.showerror(
                    "Error",
                    "Số tiền rút không hợp lệ!"
                )
                return
            
            # Call the business layer to handle the withdrawal slip creation
            result = self.create_withdrawal_slip_bus.create_withdrawal_slip(maso, khachhang, ngayrut, sotienrut, kyhansaukhirut)

            if result:
                messagebox.showinfo("Success", "Lập phiếu rút tiền thành công!")
                self.clear_fields()
            else:
                messagebox.showerror("Lỗi", "Lập phiếu rút tiền thất bại!")
        except Exception as e:
            print(f"Error during withdrawal slip event: {e}")

    def clear_fields(self):
        try:
            self.maso_entry.delete(0, "end")
            self.khachhang_entry.delete(0, "end")
            self.ngayrut_entry.delete(0, "end")
            self.sotienrut_entry.delete(0, "end")
            print("Fields cleared successfully")
        except Exception as e:
            print(f"Error clearing fields: {e}")
    
    def load_account_balance_and_customer_name(self, event=None):
        try:
            maso = self.maso_entry.get()
            if not maso:
                return

            # Call the business layer to get the account balance
            balance = self.create_withdrawal_slip_bus.GetBalance(maso)
            customer_name = self.create_withdrawal_slip_bus.GetKhachHang(maso)
            if customer_name is not None:
                self.khachhang_entry.configure(state="normal")  # Enable the entry to update the value
                self.khachhang_entry.delete(0, "end")
                self.khachhang_entry.insert(0, customer_name)  # Set the customer name
                self.khachhang_entry.configure(state="readonly")  # Set back to readonly
            else:
                messagebox.showerror("Lỗi", "Không tìm thấy khách hàng cho mã số này!")
                self.khachhang_entry.configure(state="normal")
                self.khachhang_entry.delete(0, "end")
                self.khachhang_entry.configure(state="readonly")

            if balance is not None:
                self.sodu_entry.configure(state="normal")  # Enable the entry to update the value
                self.sodu_entry.delete(0, "end")
                self.sodu_entry.insert(0, f"{balance:,}")  # Format the balance with commas
                self.sodu_entry.configure(state="readonly")  # Set back to readonly
            else:
                messagebox.showerror("Lỗi", "Không tìm thấy số dư cho mã số này!")
                self.sodu_entry.configure(state="normal")
                self.sodu_entry.delete(0, "end")
                self.sodu_entry.configure(state="readonly")
        except Exception as e:
            print(f"Error loading account balance: {e}")

    def validate_so_tien_gui(self, sotiengui):
        try:
            # Check if the input is a valid number
            float(sotiengui)
            return True
        except ValueError:
            return False