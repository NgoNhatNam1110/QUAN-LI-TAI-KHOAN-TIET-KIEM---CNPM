import customtkinter as ctk

class Prepare_monthly_report_GUI:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.create_screen_report()
    
    def create_screen_report(self):
        # Main container
        main_container = ctk.CTkFrame(self.parent_frame)
        main_container.pack(padx=20, pady=20, fill="both", expand=True)

        # Header
        header_frame = ctk.CTkFrame(main_container, fg_color=("#1f538d"), border_width=1)
        header_frame.pack(fill="x")


        # Title with border
        title_frame = ctk.CTkFrame(header_frame, fg_color=("#1f538d"))
        title_frame.pack(side="left", fill="x", expand=True, padx=1, pady=1)
        title_label = ctk.CTkLabel(title_frame, text="Báo Cáo Doanh Số Hoạt Động Ngày", text_color="white", font=ctk.CTkFont(size=14, weight="bold"))
        title_label.pack(padx=10, pady=5)

        # Date input frame
        date_frame = ctk.CTkFrame(main_container)
        date_frame.pack(fill="x", pady=10)
        date_label = ctk.CTkLabel(date_frame, text="Ngày:", font=ctk.CTkFont(size=12))
        date_label.pack(side="left", padx=10)
        self.date_entry = ctk.CTkEntry(date_frame)
        self.date_entry.pack(side="left", padx=10)

        # Table container
        table_container = ctk.CTkFrame(main_container, border_width=1)
        table_container.pack(fill="both", expand=True, pady=(1, 0))

        # Headers row
        headers = ["STT", "Loại Tiết Kiệm", "Tổng Thu", "Tổng Chi", "Chênh Lệch"]
        for col, header in enumerate(headers):
            header_frame = ctk.CTkFrame(table_container, fg_color=("#1f538d"), border_width=1)
            header_frame.grid(row=0, column=col, sticky="nsew", padx=(0,1), pady=(0,1))
            header_label = ctk.CTkLabel(header_frame, text=header, text_color="white", font=ctk.CTkFont(size=12, weight="bold"))
            header_label.pack(padx=10, pady=5)

        # Configure column weights
        table_container.grid_columnconfigure(0, weight=1)  # STT
        table_container.grid_columnconfigure(1, weight=2)  # Loại Tiết Kiệm
        table_container.grid_columnconfigure(2, weight=2)  # Tổng Thu
        table_container.grid_columnconfigure(3, weight=2)  # Tổng Chi
        table_container.grid_columnconfigure(4, weight=2)  # Chênh Lệch

        # Data rows (2 empty rows as shown in the image)
        for row in range(2):
            for col in range(5):
                if col == 0:
                    # STT column
                    cell_frame = ctk.CTkFrame(table_container, border_width=1)
                    cell_frame.grid(row=row+1, column=col, sticky="nsew", padx=(0,1), pady=(0,1))
                    cell_label = ctk.CTkLabel(cell_frame, text=str(row+1))
                    cell_label.pack(padx=10, pady=8)
                else:
                    # Other columns
                    cell_frame = ctk.CTkFrame(table_container, border_width=1)
                    cell_frame.grid(row=row+1, column=col, sticky="nsew", padx=(0,1), pady=(0,1))
                    cell_label = ctk.CTkLabel(cell_frame, text="")
                    cell_label.pack(padx=10, pady=8)

        # Add separator
        separator = ctk.CTkFrame(main_container, height=2, fg_color=("#1f538d"))
        separator.pack(fill="x", pady=20)

        # Second table header
        header_frame2 = ctk.CTkFrame(main_container, fg_color=("#1f538d"), border_width=1)
        header_frame2.pack(fill="x")


        # Title for second table
        title_frame2 = ctk.CTkFrame(header_frame2, fg_color=("#1f538d"))
        title_frame2.pack(side="left", fill="x", expand=True, padx=1, pady=1)
        title_label2 = ctk.CTkLabel(title_frame2, text="Báo Cáo Mở/Đóng Sổ Tháng", text_color="white", font=ctk.CTkFont(size=14, weight="bold"))
        title_label2.pack(padx=10, pady=5)

        # Month input frame
        month_frame = ctk.CTkFrame(main_container)
        month_frame.pack(fill="x", pady=10)
        month_label = ctk.CTkLabel(month_frame, text="Tháng:", font=ctk.CTkFont(size=12))
        month_label.pack(side="left", padx=10)
        self.month_entry = ctk.CTkEntry(month_frame)
        self.month_entry.pack(side="left", padx=10)

        # Second table container
        table_container2 = ctk.CTkFrame(main_container, border_width=1)
        table_container2.pack(fill="both", expand=True, pady=(1, 0))

        # Headers row for second table
        headers2 = ["STT", "Ngày", "Số Mở", "Số Đóng", "Chênh Lệch"]
        for col, header in enumerate(headers2):
            header_frame = ctk.CTkFrame(table_container2, fg_color=("#1f538d"), border_width=1)
            header_frame.grid(row=0, column=col, sticky="nsew", padx=(0,1), pady=(0,1))
            header_label = ctk.CTkLabel(header_frame, text=header, text_color="white", font=ctk.CTkFont(size=12, weight="bold"))
            header_label.pack(padx=10, pady=5)

        # Configure column weights for second table
        table_container2.grid_columnconfigure(0, weight=1)  # STT
        table_container2.grid_columnconfigure(1, weight=2)  # Ngày
        table_container2.grid_columnconfigure(2, weight=2)  # Số Mở
        table_container2.grid_columnconfigure(3, weight=2)  # Số Đóng
        table_container2.grid_columnconfigure(4, weight=2)  # Chênh Lệch

        # Data rows for second table (2 empty rows)
        for row in range(2):
            for col in range(5):
                if col == 0:
                    # STT column
                    cell_frame = ctk.CTkFrame(table_container2, border_width=1)
                    cell_frame.grid(row=row+1, column=col, sticky="nsew", padx=(0,1), pady=(0,1))
                    cell_label = ctk.CTkLabel(cell_frame, text=str(row+1))
                    cell_label.pack(padx=10, pady=8)
                else:
                    # Other columns
                    cell_frame = ctk.CTkFrame(table_container2, border_width=1)
                    cell_frame.grid(row=row+1, column=col, sticky="nsew", padx=(0,1), pady=(0,1))
                    cell_label = ctk.CTkLabel(cell_frame, text="")
                    cell_label.pack(padx=10, pady=8)

        # Buttons frame
        button_frame = ctk.CTkFrame(main_container)
        button_frame.pack(pady=20)
        
        generate_button = ctk.CTkButton(button_frame, text="Tạo báo cáo", command=self.generate_report)
        generate_button.pack(side="left", padx=10)
        
        cancel_button = ctk.CTkButton(button_frame, text="Huỷ", command=self.clear_fields)
        cancel_button.pack(side="left", padx=10)

    def generate_report(self):
        # Add report generation logic here
        pass

    def clear_fields(self):
        # Clear the date field and any other fields
        self.date_entry.delete(0, "end")
        self.month_entry.delete(0, "end")
        