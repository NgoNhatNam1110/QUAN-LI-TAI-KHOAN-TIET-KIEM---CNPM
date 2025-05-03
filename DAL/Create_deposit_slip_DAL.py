import uuid
from utils.db_utils import DatabaseConnection
from tkinter import messagebox
class Create_deposit_slip_DAL:
    def __init__(self):
        self.db = DatabaseConnection()

    def create_deposit_slip(self, maso, khachhang, ngaygui, sotiengui):
        try:
            # Connect to the database
            connection = self.db.connect()
            cursor = connection.cursor()

            # Validate if the bankbook exists and matches the customer name
            query = "SELECT * FROM SoTietKiem WHERE maSo = ? AND hoTen = ?"
            cursor.execute(query, (maso, khachhang))
            result = cursor.fetchone()

            if result:
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

                # Update the SoDu in SoTietKiem
                update_sodu_query = """
                UPDATE SoTietKiem
                SET SoDu = SoDu + ?
                WHERE maSo = ?;
                """
                cursor.execute(update_sodu_query, (sotiengui, maso))

                # Commit the transaction
                connection.commit()
                return True
            else:
                messagebox.showerror("Error","Không tìm thấy sổ tiết kiệm hoặc tên khách hàng!")
                return False

        except Exception as e:
            print(f"Error in DAL layer: {e}")
            return False
        finally:
            if 'connection' in locals() and connection:
                connection.close()
    
    def getKhachHang(self, maso):
        try:
            connection = self.db.connect()
            cursor = connection.cursor()
            cursor.execute("SELECT hoTen FROM SoTietKiem WHERE maSo = ?", (maso,))
            khachhang = cursor.fetchone()[0]
            return khachhang
        except Exception as e:
            print(f"Error fetching customer name: {e}")
            return None
        finally:
            if 'connection' in locals() and connection:
                connection.close()