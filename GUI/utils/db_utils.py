import sqlite3

class DatabaseConnection:
    def __init__(self, db_path="db.db"):
        self.db_path = db_path
        self.connection = None

    def connect(self):
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path)
        return self.connection

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None