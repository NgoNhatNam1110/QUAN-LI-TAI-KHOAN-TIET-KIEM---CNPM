import sqlite3
from datetime import datetime, timedelta

def add_sample_data():
    try:
        # Connect to database
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()

        # Add sample savings types
        cursor.execute("""
            INSERT OR IGNORE INTO LoaiTietKiem (loaiTietKiem, kyHan, laiSuat) 
            VALUES 
                ('Không kỳ hạn', 0, 0.5),
                ('3 tháng', 3, 4.5),
                ('6 tháng', 6, 5.0),
                ('12 tháng', 12, 6.0)
        """)

        # Add sample transaction types
        cursor.execute("""
            INSERT OR IGNORE INTO LoaiGiaoDich (loaiGiaoDich, moTa) 
            VALUES 
                ('Gửi tiền', 'Gửi tiền vào sổ tiết kiệm'),
                ('Rút tiền', 'Rút tiền từ sổ tiết kiệm'),
                ('Tất toán', 'Tất toán sổ tiết kiệm')
        """)

        # Add sample savings accounts
        today = datetime.now()
        sample_accounts = [
            ('STK001', 'Nguyễn Văn A', '123456789', '3 tháng', 10000000, 
             (today - timedelta(days=60)).strftime('%Y-%m-%d'), 10000000, 'Hà Nội'),
            ('STK002', 'Trần Thị B', '987654321', '6 tháng', 20000000, 
             (today - timedelta(days=30)).strftime('%Y-%m-%d'), 20000000, 'Hồ Chí Minh'),
            ('STK003', 'Lê Văn C', '456789123', '12 tháng', 50000000, 
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
            ('GD001', 'STK001', 'Gửi tiền', 10000000, 
             (today - timedelta(days=60)).strftime('%Y-%m-%d')),
            ('GD002', 'STK002', 'Gửi tiền', 20000000, 
             (today - timedelta(days=30)).strftime('%Y-%m-%d')),
            ('GD003', 'STK003', 'Gửi tiền', 50000000, 
             today.strftime('%Y-%m-%d')),
            ('GD004', 'STK004', 'Gửi tiền', 15000000, 
             (today - timedelta(days=90)).strftime('%Y-%m-%d')),
            ('GD005', 'STK005', 'Gửi tiền', 30000000, 
             (today - timedelta(days=15)).strftime('%Y-%m-%d'))
        ]

        cursor.executemany("""
            INSERT OR IGNORE INTO GiaoDich 
            (maGiaoDich, maSo, loaiGiaoDich, soTien, ngayGiaoDich)
            VALUES (?, ?, ?, ?, ?)
        """, sample_transactions)

        # Add sample parameters
        cursor.execute("""
            INSERT OR IGNORE INTO ThamSo 
            (maQuyDinh, loaiTietKiem, tienGuiToiThieu, kyHan, laiSuat, quyDinhKhac)
            VALUES 
                ('QD001', 'Không kỳ hạn', 1000000, 0, 0.5, 'Không có kỳ hạn'),
                ('QD002', '3 tháng', 1000000, 3, 4.5, 'Kỳ hạn 3 tháng'),
                ('QD003', '6 tháng', 1000000, 6, 5.0, 'Kỳ hạn 6 tháng'),
                ('QD004', '12 tháng', 1000000, 12, 6.0, 'Kỳ hạn 12 tháng')
        """)

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