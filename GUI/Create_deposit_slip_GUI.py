import customtkinter as ctk

class Create_deposit_slip_GUI:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.create_screen_deposit_slip()

    def create_screen_deposit_slip(self):
        # Title
        title_label = ctk.CTkLabel(self.parent_frame, text="Lập Phiếu Gửi Tiền", font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=20)

        # Create main form frame
        form_frame = ctk.CTkFrame(self.parent_frame)
        form_frame.pack(pady=20, padx=20, fill="x")

        # Row 1
        row1_frame = ctk.CTkFrame(form_frame)
        row1_frame.pack(fill="x", padx=10, pady=5)
        
        maso_label = ctk.CTkLabel(row1_frame, text="Mã số:")
        maso_label.pack(side="left", padx=5)
        maso_entry = ctk.CTkEntry(row1_frame)
        maso_entry.pack(side="left", expand=True, fill="x", padx=5)
        
        khachhang_label = ctk.CTkLabel(row1_frame, text="Khách hàng:")
        khachhang_label.pack(side="left", padx=5)
        khachhang_entry = ctk.CTkEntry(row1_frame)
        khachhang_entry.pack(side="left", expand=True, fill="x", padx=5)

        # Row 2
        row2_frame = ctk.CTkFrame(form_frame)
        row2_frame.pack(fill="x", padx=10, pady=5)
        
        ngaygui_label = ctk.CTkLabel(row2_frame, text="Ngày gửi:")
        ngaygui_label.pack(side="left", padx=5)
        ngaygui_entry = ctk.CTkEntry(row2_frame)
        ngaygui_entry.pack(side="left", expand=True, fill="x", padx=5)
        
        sotiengui_label = ctk.CTkLabel(row2_frame, text="Số tiền gửi:")
        sotiengui_label.pack(side="left", padx=5)
        sotiengui_entry = ctk.CTkEntry(row2_frame)
        sotiengui_entry.pack(side="left", expand=True, fill="x", padx=5)

        # Buttons frame
        button_frame = ctk.CTkFrame(self.parent_frame)
        button_frame.pack(pady=20)
        
        save_button = ctk.CTkButton(button_frame, text="Lập phiếu")
        save_button.pack(side="left", padx=10)
        
        cancel_button = ctk.CTkButton(button_frame, text="Hủy")
        cancel_button.pack(side="left", padx=10)