from utils.db_utils import DatabaseConnection

class Monthly_report_DAL:
    def __init__(self):
        self.db = DatabaseConnection()

    def fetch_monthly_report(self, month, year):
        """Fetch data for the monthly report from the database"""
        try:
            connection = self.db.connect()
            cursor = connection.cursor()

            # Query to fetch data
            query = """
                SELECT 
                    DATE(ngayGiaoDich) AS ngay,
                    SUM(CASE WHEN loaiGiaoDich = 'mo' THEN 1 ELSE 0 END) AS so_mo,
                    SUM(CASE WHEN loaiGiaoDich = 'dong' THEN 1 ELSE 0 END) AS so_dong
                FROM GiaoDich
                WHERE strftime('%m', ngayGiaoDich) = ? AND strftime('%Y', ngayGiaoDich) = ?
                GROUP BY DATE(ngayGiaoDich)
                ORDER BY DATE(ngayGiaoDich)
            """
            cursor.execute(query, (month, year))
            rows = cursor.fetchall()
            return rows
        except Exception as e:
            print(f"Error fetching monthly report: {e}")
            return None
        finally:
            if 'connection' in locals() and connection:
                connection.close()