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
                    DATE(ngay_giao_dich) AS ngay,
                    SUM(CASE WHEN loai_giao_dich = 'mo' THEN 1 ELSE 0 END) AS so_mo,
                    SUM(CASE WHEN loai_giao_dich = 'dong' THEN 1 ELSE 0 END) AS so_dong
                FROM GiaoDich
                WHERE strftime('%m', ngay_giao_dich) = ? AND strftime('%Y', ngay_giao_dich) = ?
                GROUP BY DATE(ngay_giao_dich)
                ORDER BY DATE(ngay_giao_dich)
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