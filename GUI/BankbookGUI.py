import customtkinter as ctk


class BankbookGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("BankBook ")
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
        info_label = ctk.CTkLabel(self.right_frame, text="Đây là trang mở sổ tiết kiệm.")
        info_label.pack(pady=20)

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