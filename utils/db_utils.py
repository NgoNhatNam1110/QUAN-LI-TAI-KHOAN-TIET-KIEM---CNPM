import sqlite3

class DatabaseConnection:
    def __init__(self, db_path="db.db"):
        self.db_path = db_path

    def connect(self):
        # Tạo kết nối mới mỗi lần gọi
        connection = sqlite3.connect(self.db_path, timeout=10)  # Tăng thời gian chờ
        connection.execute("PRAGMA journal_mode=WAL;")  # Bật chế độ WAL
        return connection

    def close(self, connection):
        # Đóng kết nối được truyền vào
        if connection:
            connection.close()