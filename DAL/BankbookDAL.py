from utils.db_utils import DatabaseConnection

class BankbookDAL:
    def __init__(self):
        self.db = DatabaseConnection()

    def insert_new_record(self, maso, loaitk, khachhang, cmnd, diachi, ngaymo, sotiengui):
        try:
            # Connect to the database
            connection = self.db.connect()
            cursor = connection.cursor()

            # SQL query to insert or update the bankbook record
            query = """
            INSERT INTO SoTietKiem (maSo, loaiTietKiem, hoTen, CMND, diaChi, ngayMoSo, soTienGui, soDu)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(maSo) DO UPDATE SET
                loaiTietKiem = excluded.loaiTietKiem,
                hoTen = excluded.hoTen,
                CMND = excluded.CMND,
                diaChi = excluded.diaChi,
                ngayMoSo = excluded.ngayMoSo,
                soTienGui = excluded.soTienGui,
                soDu = soDu + excluded.soTienGui
            """
            cursor.execute(query, (maso, loaitk, khachhang, cmnd, diachi, ngaymo, sotiengui, sotiengui))

            # Commit the transaction
            connection.commit()
            return True
        except Exception as e:
            print(f"Error in DAL layer: {e}")
            return False
        finally:
            # Ensure the connection is closed
            if 'connection' in locals() and connection:
                connection.close()
    
    def checkmaso(self, maso):
        if maso:
            try:
                connection = self.db.connect()
                cursor = connection.cursor()
                cursor.execute("SELECT COUNT(*) FROM SoTietKiem WHERE maSo = ?", (maso,))
                count = cursor.fetchone()[0]
                return count > 0
            except Exception as e:
                print(f"Error checking account number: {e}")
                return False
    
    def checkCMND(self, cmnd):
        if cmnd:
            try:
                connection = self.db.connect()
                cursor = connection.cursor()
                cursor.execute("SELECT COUNT(*) FROM SoTietKiem WHERE CMND = ?", (cmnd,))
                count = cursor.fetchone()[0]
                return count > 0
            except Exception as e:
                print(f"Error checking ID number: {e}")
                return False
    
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
        
    def checkminimumDeposit(self, loaitk):
        try:
            connection = self.db.connect()
            cursor = connection.cursor()
            cursor.execute("SELECT tienGuiToiThieu FROM ThamSo WHERE loaiTietKiem = ?", (loaitk,))
            minimum_deposit = cursor.fetchone()[0]
            return minimum_deposit
        except Exception as e:
            print(f"Error checking minimum deposit: {e}")
            return None
    
    def get_max_maso(self):
        """Fetch the maximum account number (maSo) from the database"""
        try:
            connection = self.db.connect()
            cursor = connection.cursor()
            query = "SELECT MAX(maSo) FROM SoTietKiem"
            cursor.execute(query)
            result = cursor.fetchone()
            return result[0] if result[0] else None
        except Exception as e:
            print(f"Error fetching max account number: {e}")
            return None
        finally:
            if 'connection' in locals() and connection:
                connection.close()