import customtkinter as ctk
from BUS.Lookup_Bankbook_BUS import Lookup_Bankbook_BUS

class Lookup_Bankbook_GUI:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.lookup_bankbook_bus = Lookup_Bankbook_BUS()  # Initialize the business layer
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
        self.table_container = ctk.CTkFrame(main_container, border_width=1)
        self.table_container.pack(fill="both", expand=True, pady=(1, 0))

        # Headers row
        headers = ["STT", "Mã Số", "Loại Tiết Kiệm", "Khách Hàng", "Số Dư"]
        for col, header in enumerate(headers):
            header_frame = ctk.CTkFrame(self.table_container, fg_color=("#1f538d"), border_width=1)
            header_frame.grid(row=0, column=col, sticky="nsew", padx=(0,1), pady=(0,1))
            header_label = ctk.CTkLabel(header_frame, text=header, text_color="white", font=ctk.CTkFont(size=12, weight="bold"))
            header_label.pack(padx=10, pady=5)

        # Configure column weights
        self.table_container.grid_columnconfigure(0, weight=1)  # STT
        self.table_container.grid_columnconfigure(1, weight=2)  # Mã Số
        self.table_container.grid_columnconfigure(2, weight=2)  # Loại Tiết Kiệm
        self.table_container.grid_columnconfigure(3, weight=3)  # Khách Hàng
        self.table_container.grid_columnconfigure(4, weight=2)  # Số Dư

        # Populate the table
        self.populate_table()

    def populate_table(self):
        try:
            # Fetch data from the business layer
            data = self.lookup_bankbook_bus.get_all_bankbooks()

            # Populate the table with data
            for row_index, row in enumerate(data):
                for col_index, value in enumerate(row.values()):
                    cell_frame = ctk.CTkFrame(self.table_container, border_width=0)
                    cell_frame.grid(row=row_index + 1, column=col_index, sticky="nsew", padx=(0, 1), pady=(0, 1))
                    cell_label = ctk.CTkLabel(cell_frame, text=str(value))
                    cell_label.pack(padx=10, pady=8)

            print("Data fetched and displayed successfully.")

        except Exception as e:
            print(f"Error populating table: {e}")