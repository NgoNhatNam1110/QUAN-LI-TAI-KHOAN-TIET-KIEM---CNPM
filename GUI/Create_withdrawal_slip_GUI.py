import customtkinter as ctk
import uuid 
from utils.db_utils import DatabaseConnection

class Create_withdrawal_slip_GUI:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.db = DatabaseConnection()  # Initialize the database connection utility
        self.create_screen_withdrawal_slip()
    
    def create_screen_withdrawal_slip(self):
        # Title
        title_label = ctk.CTkLabel(self.parent_frame, text="Lập Phiếu Rút Tiền", font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=20)

        # Create main form frame
        form_frame = ctk.CTkFrame(self.parent_frame)
        form_frame.pack(pady=20, padx=20, fill="x")

        # Row 1
        row1_frame = ctk.CTkFrame(form_frame)
        row1_frame.pack(fill="x", padx=10, pady=5)
        
        maso_label = ctk.CTkLabel(row1_frame, text="Mã số:")
        maso_label.pack(side="left", padx=5)
        self.maso_entry = ctk.CTkEntry(row1_frame)  # Store as instance variable
        self.maso_entry.pack(side="left", expand=True, fill="x", padx=5)
        
        khachhang_label = ctk.CTkLabel(row1_frame, text="Khách hàng:")
        khachhang_label.pack(side="left", padx=5)
        self.khachhang_entry = ctk.CTkEntry(row1_frame)  # Store as instance variable
        self.khachhang_entry.pack(side="left", expand=True, fill="x", padx=5)

        # Row 2
        row2_frame = ctk.CTkFrame(form_frame)
        row2_frame.pack(fill="x", padx=10, pady=5)
        
        ngayrut_label = ctk.CTkLabel(row2_frame, text="Ngày rút:")
        ngayrut_label.pack(side="left", padx=5)
        self.ngayrut_entry = ctk.CTkEntry(row2_frame)  # Store as instance variable
        self.ngayrut_entry.pack(side="left", expand=True, fill="x", padx=5)
        
        sotienrut_label = ctk.CTkLabel(row2_frame, text="Số tiền rút:")
        sotienrut_label.pack(side="left", padx=5)
        self.sotienrut_entry = ctk.CTkEntry(row2_frame)  # Store as instance variable
        self.sotienrut_entry.pack(side="left", expand=True, fill="x", padx=5)

        # Buttons frame
        button_frame = ctk.CTkFrame(self.parent_frame)
        button_frame.pack(pady=20)
        
        save_button = ctk.CTkButton(button_frame, text="Lập phiếu", command=self.withdrawal_slip_event)
        save_button.pack(side="left", padx=10)
        
        cancel_button = ctk.CTkButton(button_frame, text="Huỷ", command=self.clear_fields)  # Link to clear fields
        cancel_button.pack(side="left", padx=10)

    def withdrawal_slip_event(self):
        print("Save button clicked")
        connection = None  # Initialize connection
        try:
            # Retrieve input values
            maso = self.maso_entry.get()
            khachhang = self.khachhang_entry.get()
            ngayrut = self.ngayrut_entry.get()
            sotienrut = self.sotienrut_entry.get()
            
            # Validate inputs
            if not maso or not khachhang or not ngayrut or not sotienrut:
                print("Field(s) cannot be empty")
                return
            
            # Connect to the database
            connection = self.db.connect() 
            cursor = connection.cursor()

            # Validate if the bankbook exists and matches the customer name
            query = "SELECT SoDu FROM SoTietKiem WHERE maSo = ? AND hoTen = ?"
            cursor.execute(query, (maso, khachhang))
            result = cursor.fetchone()
            
            if result:
                current_balance = result[0]
                print("Bankbook exists in the database with balance:", current_balance)

                # Check if the withdrawal amount exceeds the current balance
                if float(sotienrut) > current_balance:
                    print("Insufficient balance for withdrawal")
                    return
                
                # Insert transaction type into LoaiGiaoDich (if not exists)
                insert_loai_giaodich_query = """
                INSERT INTO LoaiGiaoDich (loaiGiaodich, moTa)
                VALUES ('RutTien', 'Rút tiền khỏi tài khoản')
                ON CONFLICT (loaiGiaodich) DO NOTHING;
                """
                cursor.execute(insert_loai_giaodich_query)
                
                # Generate a random unique maGiaoDich
                random_magiaodich = str(uuid.uuid4())  
                
                # Insert transaction into Giaodich
                insert_giaodich_query = """
                INSERT INTO Giaodich (maGiaoDich, maSo, loaiGiaoDich, SoTien, ngayGiaoDich)
                VALUES (?, ?, 'RutTien', ?, ?);
                """
                cursor.execute(insert_giaodich_query, (random_magiaodich, maso, sotienrut, ngayrut))
                connection.commit()
                
                # Update the SoDu in SoTietKiem
                update_sodu_query = """
                UPDATE SoTietKiem
                SET SoDu = SoDu - ?
                WHERE maSo = ?;
                """
                cursor.execute(update_sodu_query, (sotienrut, maso))
                connection.commit()
                
                print("Withdrawal slip saved successfully with maGiaoDich:", random_magiaodich)
            else:
                print("Bankbook not found or customer name does not match")
                
        except Exception as e:
            print(f"Error fetching withdrawal slip data: {e}")
        finally:
            if connection:
                connection.close()  
                
    def clear_fields(self):
        print("Clear button clicked")  # Debugging statement
        try:
            self.maso_entry.delete(0, "end")
            self.khachhang_entry.delete(0, "end")
            self.ngayrut_entry.delete(0, "end")
            self.sotienrut_entry.delete(0, "end")
            print("Fields cleared successfully")  # Debugging statement
        except Exception as e:
            print(f"Error clearing fields: {e}")  # Debugging statement
