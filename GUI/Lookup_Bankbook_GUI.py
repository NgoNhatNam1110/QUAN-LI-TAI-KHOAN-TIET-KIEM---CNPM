import customtkinter as ctk

class Lookup_Bankbook_GUI:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.create_screen_lookup_bankbook()
    
    def create_screen_lookup_bankbook(self):
        # Main container
        main_container = ctk.CTkFrame(self.parent_frame)
        main_container.pack(padx=20, pady=20, fill="both", expand=True)

        # Header and Title
        header_frame = ctk.CTkFrame(main_container, fg_color=("#1f538d"), border_width=1)
        header_frame.pack(fill="x")

        

        # Title with border
        title_frame = ctk.CTkFrame(header_frame, fg_color=("#1f538d"))
        title_frame.pack(side="left", fill="x", expand=True, padx=1, pady=1)
        title_label = ctk.CTkLabel(title_frame, text="Danh Sách Sổ Tiết Kiệm", text_color="white", font=ctk.CTkFont(size=14, weight="bold"))
        title_label.pack(padx=10, pady=5)

        # Table container
        table_container = ctk.CTkFrame(main_container, border_width=1)
        table_container.pack(fill="both", expand=True, pady=(1, 0))

        # Headers row
        headers = ["STT", "Mã Số", "Loại Tiết Kiệm", "Khách Hàng", "Số Dư"]
        for col, header in enumerate(headers):
            header_frame = ctk.CTkFrame(table_container, fg_color=("#1f538d"), border_width=1)
            header_frame.grid(row=0, column=col, sticky="nsew", padx=(0,1), pady=(0,1))
            header_label = ctk.CTkLabel(header_frame, text=header, text_color="white", font=ctk.CTkFont(size=12, weight="bold"))
            header_label.pack(padx=10, pady=5)

        # Configure column weights
        table_container.grid_columnconfigure(0, weight=1)  # STT
        table_container.grid_columnconfigure(1, weight=2)  # Mã Số
        table_container.grid_columnconfigure(2, weight=2)  # Loại Tiết Kiệm
        table_container.grid_columnconfigure(3, weight=3)  # Khách Hàng
        table_container.grid_columnconfigure(4, weight=2)  # Số Dư

        # Data rows
        for row in range(2):
            for col in range(5):
                if col == 0:
                    # STT column
                    cell_frame = ctk.CTkFrame(table_container, border_width=0)
                    cell_frame.grid(row=row+1, column=col, sticky="nsew", padx=(0,1), pady=(0,1))
                    cell_label = ctk.CTkLabel(cell_frame, text=str(row+1))
                    cell_label.pack(padx=10, pady=8)
                else:
                    # Other columns
                    cell_frame = ctk.CTkFrame(table_container, border_width=0)
                    cell_frame.grid(row=row+1, column=col, sticky="nsew", padx=(0,1), pady=(0,1))
                    cell_label = ctk.CTkLabel(cell_frame, text="")
                    cell_label.pack(padx=10, pady=8)