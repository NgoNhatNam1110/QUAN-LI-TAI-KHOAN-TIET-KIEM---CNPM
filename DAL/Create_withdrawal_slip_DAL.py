import uuid
from utils.db_utils import DatabaseConnection
from tkinter import messagebox

class Create_withdrawal_slip_DAL:
    def __init__(self):
        self.db = DatabaseConnection()

    def create_withdrawal_slip(self, maso, khachhang, ngayrut, sotienrut, kyhansaukhirut):
        try:
            # Connect to the database
            connection = self.db.connect()
            cursor = connection.cursor()

            # Validate if the bankbook exists and matches the customer name
            query = "SELECT SoDu FROM SoTietKiem WHERE maSo = ? AND hoTen = ?"
            cursor.execute(query, (maso, khachhang))
            result = cursor.fetchone()

            if result:
                current_balance = result[0]
                
                # Get minum balance from LoaiTietKiem
                query = "SELECT tienGuiToiThieu FROM ThamSo WHERE loaiTietKiem = ?"
                minimum_balance = cursor.execute(query, (kyhansaukhirut,)).fetchone()[0]

                # Check if the withdrawal amount exceeds the current balance
                if not self.check_insuffient_balance(sotienrut, current_balance):
                    messagebox.showerror(
                        "Lỗi",
                        "Số tiền rút không được lớn hơn số dư tài khoản!"
                    )
                    return False
                
                # Check if the balance after withdrawal is > minimum balance
                if float(current_balance) - float(sotienrut) < float(minimum_balance):
                    messagebox.showerror(
                        "Lỗi",
                        f"Số dư tài khoản không được nhỏ hơn số tiền gửi tối thiểu của loại kỳ hạn : {int(minimum_balance)} VNĐ!"
                    )
                    return False
                
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

                # Update the SoDu in SoTietKiem
                update_sodu_query = """
                UPDATE SoTietKiem
                SET SoDu = SoDu - ?
                WHERE maSo = ?;
                """
                cursor.execute(update_sodu_query, (sotienrut, maso))

                # Update the KyHan in SoTietKiem
                # Update the KyHan in SoTietKiem
                update_kyhan_query = """
                UPDATE SoTietKiem
                SET LoaiTietKiem = ?
                WHERE maSo = ? AND hoTen = ?;
                """
                cursor.execute(update_kyhan_query, (kyhansaukhirut, maso, khachhang))
                
                # Commit the transaction
                connection.commit()
                return True
            else:
                messagebox.showerror(   
                    "Lỗi",
                    "Số tài khoản hoặc tên khách hàng không đúng!"
                )
                return False

        except Exception as e:
            print(f"Error in DAL layer: {e}")
            return False
        finally:
            if 'connection' in locals() and connection:
                connection.close()
                
    def getInterests(self):
        try:
            connection = self.db.connect()
            cursor = connection.cursor()
            cursor.execute("SELECT loaiTietKiem FROM LoaiTietKiem")
            interest_options = [row[0] for row in cursor.fetchall()]
            return interest_options
        except Exception as e:
            print(f"Error fetching interest options: {e}")
            return None
    
    def check_insuffient_balance(self, sotienrut, current_balance):
        if float(sotienrut) > current_balance:
            print("Withdrawal amount exceeds current balance")
            return False
        else :
            return True
    
        