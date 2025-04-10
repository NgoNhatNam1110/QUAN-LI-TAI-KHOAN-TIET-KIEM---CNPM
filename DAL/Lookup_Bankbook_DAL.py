from utils.db_utils import DatabaseConnection

class Lookup_Bankbook_DAL:
    def __init__(self):
        self.db = DatabaseConnection()

    def get_all_bankbooks(self):
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

            # Process rows into a list of dictionaries
            result = []
            for row in rows:
                result.append({
                    "STT": row[0],
                    "MaSo": row[1],
                    "LoaiTietKiem": row[2],
                    "KhachHang": row[3],
                    "SoDu": row[4]
                })

            return result

        except Exception as e:
            print(f"Error in DAL layer while fetching bankbooks: {e}")
            return []

        finally:
            # Ensure the connection is closed
            if 'connection' in locals() and connection:
                connection.close()