import customtkinter as ctk


class BankbookGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("BankBook Management ")
        self.geometry("800x600")

        # Cấu hình grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Khung bên trái
        self.left_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.left_frame.grid(row=0, column=0, sticky="nsew")
        
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Thông tin sinh viên
        self.account_detail_label = ctk.CTkLabel(self.left_frame, text="Thông tin tài khoản :", font=ctk.CTkFont(size=18, weight="bold"))
        self.account_detail_label.pack(pady=20)

        self.account_label = ctk.CTkLabel(self.left_frame, text="Tài khoản : load tài khoản")
        self.account_label.pack(pady=5)

        self.id_account_label = ctk.CTkLabel(self.left_frame, text="ID : load id")
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

        # Khung bên phải
        self.right_frame = ctk.CTkFrame(self, corner_radius=0)
        self.right_frame.grid(row=0, column=1, sticky="nsew")

        # Hiển thị thông tin mặc định
        self.create_bankbook()

    def clear_right_frame(self):
        # Xóa tất cả widget trong khung bên phải
        for widget in self.right_frame.winfo_children():
            widget.destroy()

    def create_bankbook(self):
        self.clear_right_frame()
        
        # Title
        title_label = ctk.CTkLabel(self.right_frame, text="Sổ Tiết Kiệm", font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=20)

        # Create main form frame
        form_frame = ctk.CTkFrame(self.right_frame)
        form_frame.pack(pady=20, padx=20, fill="x")

        # Row 1
        row1_frame = ctk.CTkFrame(form_frame)
        row1_frame.pack(fill="x", padx=10, pady=5)
        
        maso_label = ctk.CTkLabel(row1_frame, text="Mã số:")
        maso_label.pack(side="left", padx=5)
        maso_entry = ctk.CTkEntry(row1_frame)
        maso_entry.pack(side="left", expand=True, fill="x", padx=5)
        
        loaitk_label = ctk.CTkLabel(row1_frame, text="Loại tiết kiệm:")
        loaitk_label.pack(side="left", padx=5)
        loaitk_entry = ctk.CTkEntry(row1_frame)
        loaitk_entry.pack(side="left", expand=True, fill="x", padx=5)

        # Row 2
        row2_frame = ctk.CTkFrame(form_frame)
        row2_frame.pack(fill="x", padx=10, pady=5)
        
        khachhang_label = ctk.CTkLabel(row2_frame, text="Khách hàng:")
        khachhang_label.pack(side="left", padx=5)
        khachhang_entry = ctk.CTkEntry(row2_frame)
        khachhang_entry.pack(side="left", expand=True, fill="x", padx=5)
        
        cmnd_label = ctk.CTkLabel(row2_frame, text="CMND:")
        cmnd_label.pack(side="left", padx=5)
        cmnd_entry = ctk.CTkEntry(row2_frame)
        cmnd_entry.pack(side="left", expand=True, fill="x", padx=5)

        # Row 3
        row3_frame = ctk.CTkFrame(form_frame)
        row3_frame.pack(fill="x", padx=10, pady=5)
        
        diachi_label = ctk.CTkLabel(row3_frame, text="Địa chỉ:")
        diachi_label.pack(side="left", padx=5)
        diachi_entry = ctk.CTkEntry(row3_frame)
        diachi_entry.pack(side="left", expand=True, fill="x", padx=5)
        
        ngaymo_label = ctk.CTkLabel(row3_frame, text="Ngày mở sổ:")
        ngaymo_label.pack(side="left", padx=5)
        ngaymo_entry = ctk.CTkEntry(row3_frame)
        ngaymo_entry.pack(side="left", expand=True, fill="x", padx=5)

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
        
        save_button = ctk.CTkButton(button_frame, text="Lưu")
        save_button.pack(side="left", padx=10)
        
        cancel_button = ctk.CTkButton(button_frame, text="Hủy")
        cancel_button.pack(side="left", padx=10)

    def create_deposit_slip(self):
        self.clear_right_frame()
        register_label = ctk.CTkLabel(self.right_frame, text="Đây là trang lập phiếu gửi tiền.")
        register_label.pack(pady=20)

    def create_withdrawal_slip(self):
        self.clear_right_frame()
        score_label = ctk.CTkLabel(self.right_frame, text="Đây là trang lập phiếu rút tiền.")
        score_label.pack(pady=20)
    
    def lookup_bankbook(self):
        self.clear_right_frame()
        score_label = ctk.CTkLabel(self.right_frame, text="Đây là trang tra cứu sổ.")
        score_label.pack(pady=20)
    
    def prepare_monthly_report(self):
        self.clear_right_frame()
        score_label = ctk.CTkLabel(self.right_frame, text="Đây là trang lập báo cáo tháng.")
        score_label.pack(pady=20)
    
    def change_rules(self):
        self.clear_right_frame()
        score_label = ctk.CTkLabel(self.right_frame, text="Đây là trang thay đổi qui định.")
        score_label.pack(pady=20)

# if __name__ == "__main__":
#     app = BankbookGUI()
#     app.mainloop()