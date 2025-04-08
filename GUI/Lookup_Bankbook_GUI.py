import customtkinter as ctk
from utils.db_utils import DatabaseConnection

class Lookup_Bankbook_GUI:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.db = DatabaseConnection()  # Initialize the database connection utility
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
        self.populate_table(table_container)

    def populate_table(self, table_container):
        try:
            # Connect to the database
            connection = self.db.connect()
            cursor = connection.cursor()

            # Query the database for bankbook data from SoTietKiem
            query = """
            SELECT 
                ROW_NUMBER() OVER (ORDER BY maSo) AS STT,  -- Matches "STT" header
                maSo AS MaSo,                              -- Matches "Mã Số" header
                loaiTietKiem AS LoaiTietKiem,              -- Matches "Loại Tiết Kiệm" header
                hoTen AS KhachHang,                        -- Matches "Khách Hàng" header
                soDu AS SoDu                               -- Matches "Số Dư" header
            FROM SoTietKiem
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            # Populate the table with data
            for row_index, row in enumerate(rows):
                for col_index, value in enumerate(row):
                    cell_frame = ctk.CTkFrame(table_container, border_width=0)
                    cell_frame.grid(row=row_index + 1, column=col_index, sticky="nsew", padx=(0, 1), pady=(0, 1))
                    cell_label = ctk.CTkLabel(cell_frame, text=str(value))
                    cell_label.pack(padx=10, pady=8)

            print("Data fetched and displayed successfully.")

        except Exception as e:
            print(f"Error populating table: {e}")

        finally:
            # Ensure the connection is closed
            if 'connection' in locals() and connection:
                connection.close()