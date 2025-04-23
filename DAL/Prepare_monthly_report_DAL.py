import customtkinter as ctk

from utils.db_utils import DatabaseConnection

class Prepare_monthly_report_DAL:
    def __init__(self) -> None:
        self.db = DatabaseConnection()
        self.connection = self.db.connect()
        self.cursor = self.connection.cursor()

    def load_bankbook_to_table(self, date):
        try:
            print(f"Executing query with date: {date}")
            
            # Check total transactions in database
            debug_query = "SELECT COUNT(*) FROM GiaoDich"
            self.cursor.execute(debug_query)
            total_transactions = self.cursor.fetchone()[0]
            print(f"Total transactions in database: {total_transactions}")
            
            # Get transaction details for debugging
            transaction_query = """
                SELECT gd.maSo, gd.loaiGiaoDich, gd.soTien, gd.ngayGiaoDich,
                       stk.loaiTietKiem
                FROM GiaoDich gd
                LEFT JOIN SoTietKiem stk ON gd.maSo = stk.maSo
                WHERE gd.ngayGiaoDich = ?
            """
            self.cursor.execute(transaction_query, (date,))
            transaction = self.cursor.fetchone()
            if transaction:
                print(f"Transaction details:")
                print(f"MaSo: {transaction[0]}")
                print(f"LoaiGiaoDich: {transaction[1]}")
                print(f"SoTien: {transaction[2]}")
                print(f"NgayGiaoDich: {transaction[3]}")
                print(f"LoaiTietKiem: {transaction[4]}")
            else:
                print("No transaction found for the given date")
            
            # Query to get daily report data
            query = """
            SELECT 
                stk.loaiTietKiem as TenLoaiTietKiem,
                COALESCE(SUM(CASE WHEN gd.loaiGiaoDich = 'GuiTien' THEN gd.soTien ELSE 0 END), 0) as TongThu,
                COALESCE(SUM(CASE WHEN gd.loaiGiaoDich = 'RutTien' THEN gd.soTien ELSE 0 END), 0) as TongChi,
                COALESCE(SUM(CASE 
                    WHEN gd.loaiGiaoDich = 'GuiTien' THEN gd.soTien 
                    WHEN gd.loaiGiaoDich = 'RutTien' THEN -gd.soTien 
                    ELSE 0 
                END), 0) as ChenhLech
            FROM SoTietKiem stk
            LEFT JOIN GiaoDich gd ON stk.maSo = gd.maSo
            WHERE gd.ngayGiaoDich = ?
            GROUP BY stk.loaiTietKiem
            """
            
            # Execute query and get results
            self.cursor.execute(query, (date,))
            print("Query executed successfully")
            
            results = self.cursor.fetchall()
            print(f"Number of rows returned: {len(results)}")
            
            # Process results into list of dictionaries
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
            print(f"Error loading data: {e}")
            return []

        finally:
            pass