import sqlite3
from datetime import datetime, timedelta

def add_sample_data():
    try:
        # Connect to database
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()


        # Add sample savings accounts
        today = datetime.now()
        sample_accounts = [
            ('STK001', 'Nguyễn Văn A', '123456789', '3 tháng', 10000000, 
             (today - timedelta(days=60)).strftime('%Y-%m-%d'), 10000000, 'Hà Nội'),
            ('STK002', 'Trần Thị B', '987654321', '6 tháng', 20000000, 
             (today - timedelta(days=30)).strftime('%Y-%m-%d'), 20000000, 'Hồ Chí Minh'),
            ('STK003', 'Lê Văn C', '456789123', '3 tháng', 50000000, 
             today.strftime('%Y-%m-%d'), 50000000, 'Đà Nẵng'),
            ('STK004', 'Phạm Thị D', '789123456', 'Không kỳ hạn', 15000000, 
             (today - timedelta(days=90)).strftime('%Y-%m-%d'), 15000000, 'Hải Phòng'),
            ('STK005', 'Hoàng Văn E', '321654987', '3 tháng', 30000000, 
             (today - timedelta(days=15)).strftime('%Y-%m-%d'), 30000000, 'Cần Thơ')
        ]

        cursor.executemany("""
            INSERT OR IGNORE INTO SoTietKiem 
            (maSo, hoTen, CMND, loaiTietKiem, soTienGui, ngayMoSo, soDu, diaChi)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, sample_accounts)

        # Add sample transactions
        sample_transactions = [
            ('GD001', 'STK001', 'GuiTien', 10000000, 
             (today - timedelta(days=60)).strftime('%Y-%m-%d')),
            ('GD002', 'STK002', 'GuiTien', 20000000, 
             (today - timedelta(days=30)).strftime('%Y-%m-%d')),
            ('GD003', 'STK003', 'GuiTien', 50000000, 
             today.strftime('%Y-%m-%d')),
            ('GD004', 'STK004', 'GuiTien', 15000000, 
             (today - timedelta(days=90)).strftime('%Y-%m-%d')),
            ('GD005', 'STK005', 'GuiTien', 30000000, 
             (today - timedelta(days=15)).strftime('%Y-%m-%d'))
        ]

        cursor.executemany("""
            INSERT OR IGNORE INTO GiaoDich 
            (maGiaoDich, maSo, loaiGiaoDich, soTien, ngayGiaoDich)
            VALUES (?, ?, ?, ?, ?)
        """, sample_transactions)
        # Commit changes
        conn.commit()
        print("Sample data added successfully!")

    except Exception as e:
        print(f"Error adding sample data: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    add_sample_data() 