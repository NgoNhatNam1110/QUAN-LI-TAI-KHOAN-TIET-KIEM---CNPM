import sqlite3
import os

def init_database():
    # Check if database file exists
    db_path = "db.db"
    
    # Read SQL commands from create_db.txt
    with open("create_db.txt", "r") as f:
        sql_commands = f.read()
    
    # Connect to database and execute commands
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Split commands by semicolon and execute each one
        for command in sql_commands.split(';'):
            if command.strip():
                try:
                    cursor.execute(command)
                except sqlite3.OperationalError as e:
                    if "already exists" not in str(e):
                        print(f"Error executing command: {e}")
        
        # Check if sample data already exists
        cursor.execute("SELECT COUNT(*) FROM LoaiTietKiem")
        if cursor.fetchone()[0] == 0:
            # Insert some sample data
            cursor.execute("""
                INSERT INTO LoaiTietKiem (loaiTietKiem, kyHan, laiSuat) 
                VALUES 
                    ('Không kỳ hạn', 0, 0.5),
                    ('3 tháng', 3, 4.5),
                    ('6 tháng', 6, 5.0),
                    ('12 tháng', 12, 6.0)
            """)
        
        cursor.execute("SELECT COUNT(*) FROM KhachHang")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO KhachHang (maKhachHang, hoTen, CMND, diaChi) 
                VALUES 
                    ('KH001', 'Nguyễn Văn A', '123456789', 'Hà Nội'),
                    ('KH002', 'Trần Thị B', '987654321', 'Hồ Chí Minh')
            """)
        
        cursor.execute("SELECT COUNT(*) FROM SoTietKiem")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO SoTietKiem (maSo, maKhachHang, loaiTietKiem, soTienGui, ngayMoSo, soDu) 
                VALUES 
                    ('STK001', 'KH001', '3 tháng', 1000000, '2024-01-01', 1000000),
                    ('STK002', 'KH002', '6 tháng', 2000000, '2024-02-01', 2000000)
            """)
        
        conn.commit()
        print("Database initialized successfully!")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    init_database() 