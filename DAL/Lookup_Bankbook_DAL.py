from utils.db_utils import DatabaseConnection
import sqlite3
from datetime import datetime

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
            FROM SoTietKiem s
            JOIN KhachHang k ON s.maKhachHang = k.maKhachHang
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

    def search_bankbooks(self, ma_so, loai_tk, khach_hang):
        """
        Search bankbooks based on criteria
        
        Args:
            ma_so (str): Bankbook number to search for
            loai_tk (str): Savings type to search for
            khach_hang (str): Customer name to search for
            
        Returns:
            list: List of dictionaries containing matching bankbooks
        """
        try:
            # Connect to the database
            connection = self.db.connect()
            cursor = connection.cursor()
            
            # Build the query based on provided criteria
            query = """
                SELECT 
                    ROW_NUMBER() OVER (ORDER BY maSo) AS STT,
                    maSo AS MaSo,
                    loaiTietKiem AS LoaiTietKiem,
                    hoTen AS KhachHang,
                    soDu AS SoDu
                FROM SoTietKiem
                WHERE 1=1
            """
            params = []
            
            if ma_so:
                query += " AND maSo LIKE ?"
                params.append(f"%{ma_so}%")
            
            if loai_tk:
                query += " AND loaiTietKiem LIKE ?"
                params.append(f"%{loai_tk}%")
            
            if khach_hang:
                query += " AND hoTen LIKE ?"
                params.append(f"%{khach_hang}%")
            
            query += " ORDER BY maSo"
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            # Convert rows to dictionaries
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
            print(f"Error in DAL layer while searching bankbooks: {e}")
            return []
            
        finally:
            # Ensure the connection is closed
            if 'connection' in locals() and connection:
                connection.close()