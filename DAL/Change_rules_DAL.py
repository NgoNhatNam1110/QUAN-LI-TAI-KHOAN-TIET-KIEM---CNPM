import sqlite3
from utils.db_utils import DatabaseConnection

class ChangeRulesDAL:
    def __init__(self):
        self.db = DatabaseConnection()

    def fetch_all_rules(self):
        try:
            connection = self.db.connect()
            cursor = connection.cursor()
            query = """
                SELECT ts.maQuyDinh, ts.loaiTietKiem, ts.tienGuiToiThieu, ts.kyHan, ts.laiSuat, ltk.thoiGianGuiToiThieu
                FROM ThamSo ts
                JOIN LoaiTietKiem ltk ON ts.loaiTietKiem = ltk.loaiTietKiem
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            data = []
            for row in rows:
                if len(row) == 6:
                    maQD, loaiTK, tien_toithieu, ky_han, lai, tgian = row
                    data.append({
                        "maQD": maQD,
                        "loaiTK": loaiTK,
                        "tien_toithieu": tien_toithieu,
                        "ky_han": ky_han,
                        "lai": lai,
                        "tgian": tgian
                    })
            return data
        finally:
            self.db.close(connection)

    def add_rule(self, loaiTK, tien_toithieu, ky_han, lai, tgian):
        try:
            connection = self.db.connect()
            cursor = connection.cursor()
            # Thêm vào LoaiTietKiem nếu chưa có
            cursor.execute("SELECT COUNT(*) FROM LoaiTietKiem WHERE loaiTietKiem = ?", (loaiTK,))
            if cursor.fetchone()[0] == 0:
                cursor.execute("INSERT INTO LoaiTietKiem (loaiTietKiem, kyHan, laiSuat, thoiGianGuiToiThieu) VALUES (?, ?, ?, ?)", (loaiTK, ky_han, lai, tgian))
            # Thêm vào ThamSo
            cursor.execute("SELECT MAX(CAST(SUBSTR(maQuyDinh, 3) AS INTEGER)) FROM ThamSo WHERE maQuyDinh LIKE 'QD%'")
            max_id = cursor.fetchone()[0]
            new_id = 1 if max_id is None else max_id + 1
            maQD = f"QD{new_id:03d}"
            insert_query = """
                INSERT INTO ThamSo (maQuyDinh, loaiTietKiem, tienGuiToiThieu, kyHan, laiSuat)
                VALUES (?, ?, ?, ?, ?)
            """
            cursor.execute(insert_query, (maQD, loaiTK, tien_toithieu, ky_han, lai))
            connection.commit()
        finally:
            self.db.close(connection)

    def update_rule(self, maQD, loaiTK, tien_toithieu, ky_han, lai, tgian):
        try:
            connection = self.db.connect()
            cursor = connection.cursor()

            # Update ThamSo table
            update_query_thamso = """
                UPDATE ThamSo
                SET loaiTietKiem = ?, tienGuiToiThieu = ?, kyHan = ?, laiSuat = ?
                WHERE maQuyDinh = ?
            """
            cursor.execute(update_query_thamso, (loaiTK, tien_toithieu, ky_han, lai, maQD))

            # Check if loaiTietKiem exists in LoaiTietKiem table
            cursor.execute("SELECT COUNT(*) FROM LoaiTietKiem WHERE loaiTietKiem = ?", (loaiTK,))
            if cursor.fetchone()[0] > 0:
                # Fetch existing values for comparison
                cursor.execute("SELECT kyHan, laiSuat, thoiGianGuiToiThieu FROM LoaiTietKiem WHERE loaiTietKiem = ?", (loaiTK,))
                existing_values = cursor.fetchone()

                # Update only if values have changed
                if existing_values != (ky_han, lai, tgian):
                    update_query_loaitietkiem = """
                        UPDATE LoaiTietKiem
                        SET kyHan = ?, laiSuat = ?, thoiGianGuiToiThieu = ?
                        WHERE loaiTietKiem = ?
                    """
                    cursor.execute(update_query_loaitietkiem, (ky_han, lai, tgian, loaiTK))
            else:
                raise ValueError(f"LoaiTietKiem '{loaiTK}' does not exist in the database.")

            # Commit the transaction
            connection.commit()
            return True  # Indicate success
        except Exception as e:
            print(f"Error updating rule: {e}")
            return False  # Indicate failure
        finally:
            self.db.close(connection)

    def delete_rule(self, maQD, loaiTK):
        try:
            connection = self.db.connect()
            cursor = connection.cursor()
            # Xóa ở ThamSo
            cursor.execute("DELETE FROM ThamSo WHERE maQuyDinh = ?", (maQD,))
            # Nếu loaiTK truyền vào, kiểm tra nếu không còn ở ThamSo thì xóa ở LoaiTietKiem
            if loaiTK:
                cursor.execute("SELECT COUNT(*) FROM ThamSo WHERE loaiTietKiem = ?", (loaiTK,))
                if cursor.fetchone()[0] == 0:
                    cursor.execute("DELETE FROM LoaiTietKiem WHERE loaiTietKiem = ?", (loaiTK,))
            connection.commit()
        finally:
            self.db.close(connection)

    def count_rules(self):
        """count amount of rows in table ThamSo"""
        try:
            connection = self.db.connect()
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM ThamSo")
            count = cursor.fetchone()[0]
            return count
        finally:
            self.db.close(connection)

    def validate_loaitk(self, loaiTK):
        try:
            connection = self.db.connect()
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM LoaiTietKiem WHERE loaiTietKiem = ?", (loaiTK,))
            count = cursor.fetchone()[0]
            return count > 0
        finally:
            self.db.close(connection)
    