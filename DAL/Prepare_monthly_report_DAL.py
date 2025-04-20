import customtkinter as ctk

from utils.db_utils import DatabaseConnection

class Prepare_monthly_report_DAL:
    def __init__(self) -> None:
        self.db = DatabaseConnection()
        self.connection = self.db.connect()
        self.cursor = self.connection.cursor()

    def load_bankbook_to_table(self, date):
        try:
            # SQL query to get daily report data
            query = """
            SELECT 
                lt.loaiTietKiem as TenLoaiTietKiem,
                COALESCE(SUM(CASE WHEN gd.loaiGiaoDich = 'Gửi tiền' THEN gd.soTien ELSE 0 END), 0) as TongThu,
                COALESCE(SUM(CASE WHEN gd.loaiGiaoDich = 'Rút tiền' THEN gd.soTien ELSE 0 END), 0) as TongChi,
                COALESCE(SUM(CASE 
                    WHEN gd.loaiGiaoDich = 'Gửi tiền' THEN gd.soTien 
                    WHEN gd.loaiGiaoDich = 'Rút tiền' THEN -gd.soTien 
                    ELSE 0 
                END), 0) as ChenhLech
            FROM LoaiTietKiem lt
            LEFT JOIN SoTietKiem stk ON lt.loaiTietKiem = stk.loaiTietKiem
            LEFT JOIN GiaoDich gd ON stk.maSo = gd.maSo
            WHERE DATE(gd.ngayGiaoDich) = ?
            GROUP BY lt.loaiTietKiem
            """
            
            # Execute query with the date parameter
            self.cursor.execute(query, (date,))
            
            # Fetch all results
            results = self.cursor.fetchall()
            
            # Process results into a list of dictionaries
            report_data = []
            for row in results:
                report_data.append({
                    'TenLoaiTietKiem': row[0],
                    'TongThu': float(row[1]),
                    'TongChi': float(row[2]),
                    'ChenhLech': float(row[3])
                })
            
            return report_data

        except Exception as e:
            print(f"Error loading bankbook data: {e}")
            return []

        finally:
            # Reset the cursor for next use
            if self.cursor:
                self.cursor.reset()