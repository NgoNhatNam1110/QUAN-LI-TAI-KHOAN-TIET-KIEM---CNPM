import customtkinter as ctk
import uuid 
from utils.db_utils import DatabaseConnection


class Create_deposit_slip_GUI:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.db = DatabaseConnection()  # Initialize the database connection utility
        print(f"Parent frame: {self.parent_frame}")  # Debugging statement
        self.create_screen_deposit_slip()

    def create_screen_deposit_slip(self):
        # Title with gradient background
        title_frame = ctk.CTkFrame(self.parent_frame, corner_radius=15, fg_color=("#1E3A8A", "#2B4F8C"))
        title_frame.pack(pady=20, padx=20, fill="x")
        
        title_label = ctk.CTkLabel(title_frame, 
                                  text="Lập Phiếu Gửi Tiền", 
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
        self.khachhang_entry.pack(side="left", expand=True, fill="x", padx=5)

        # Row 2
        row2_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        row2_frame.pack(fill="x", padx=20, pady=10)
        current_date = datetime.now()
        
        ngaygui_label = ctk.CTkLabel(row2_frame, text="Ngày gửi:", **label_style)
        ngaygui_label.pack(side="left", padx=5)
        self.ngaygui_entry = ctk.CTkEntry(row2_frame, **entry_style)
        self.ngaygui_entry.pack(side="left", expand=True, fill="x", padx=5)
        self.ngaygui_entry.insert(0, current_date.strftime("%Y-%m-%d"))
        self.ngaygui_entry.configure(state="readonly")
        
        sotiengui_label = ctk.CTkLabel(row2_frame, text="Số tiền gửi:", **label_style)
        sotiengui_label.pack(side="left", padx=5)
        self.sotiengui_entry = ctk.CTkEntry(row2_frame, **entry_style)
        self.sotiengui_entry.pack(side="left", expand=True, fill="x", padx=5)

        # Buttons frame with hover effects
        button_frame = ctk.CTkFrame(self.parent_frame, fg_color="transparent")
        button_frame.pack(pady=20)
        
        save_button = ctk.CTkButton(button_frame, text="Lập phiếu", command=self.deposit_slip_event)  # Link to deposit_slip_event
        save_button.pack(side="left", padx=10)
        
        cancel_button = ctk.CTkButton(button_frame, text="Huỷ", command=self.clear_fields)  # Link to cancel_event
        cancel_button.pack(side="left", padx=10)

    def deposit_slip_event(self):
        print("Deposit slip button clicked")
        connection = None  # Initialize connection
        try:
            # Retrieve input values
            maso = self.maso_entry.get()
            khachhang = self.khachhang_entry.get()
            ngaygui = self.ngaygui_entry.get()
            sotiengui = self.sotiengui_entry.get()

            # Validate inputs
            if not maso or not khachhang or not ngaygui or not sotiengui:
                messagebox.showerror(
                    "Error",
                    "Vui lòng nhập đầy đủ các trường dữ liệu"
                )
                return

            # Connect to the database
            connection = self.db.connect()
            cursor = connection.cursor()

            # Validate if the bankbook exists and matches the customer name
            query = "SELECT * FROM SoTietKiem WHERE maSo = ? AND hoTen = ?"
            cursor.execute(query, (maso, khachhang))
            result = cursor.fetchone()

            if result:
                print("Bankbook exists in the database:", result)

                # Insert transaction type into LoaiGiaoDich (if not exists)
                insert_loai_giaodich_query = """
                INSERT INTO LoaiGiaoDich (loaiGiaodich, moTa)
                VALUES ('GuiTien', 'Gửi tiền vào tài khoản')
                ON CONFLICT (loaiGiaodich) DO NOTHING;
                """
                cursor.execute(insert_loai_giaodich_query)

                # Generate a random unique maGiaoDich
                random_magiaodich = str(uuid.uuid4())  

                # Insert transaction into Giaodich
                insert_giaodich_query = """
                INSERT INTO Giaodich (maGiaoDich, maSo, loaiGiaoDich, SoTien, ngayGiaoDich)
                VALUES (?, ?, 'GuiTien', ?, ?);
                """
                cursor.execute(insert_giaodich_query, (random_magiaodich, maso, sotiengui, ngaygui))
                connection.commit()

                # Update the SoDu in SoTietKiem
                update_sodu_query = """
                UPDATE SoTietKiem
                SET SoDu = SoDu + ?
                WHERE maSo = ?;
                """
                cursor.execute(update_sodu_query, (sotiengui, maso))
                connection.commit()

                print("Deposit slip saved successfully with maGiaoDich:", random_magiaodich)
            else:
                print("Bankbook not found or customer name does not match")

        except Exception as e:
            print(f"Error during deposit slip event: {e}")
        finally:
            if connection:
                connection.close()

    def clear_fields(self):
        print("Cancel button clicked")
        try:
            self.maso_entry.delete(0, "end")
            self.khachhang_entry.delete(0, "end")
            self.ngaygui_entry.delete(0, "end")
            self.sotiengui_entry.delete(0, "end")
            print("Fields cleared successfully")
        except Exception as e:
            print(f"Error clearing fields: {e}")
