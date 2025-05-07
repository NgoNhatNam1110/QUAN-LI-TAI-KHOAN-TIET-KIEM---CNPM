import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from unittest.mock import MagicMock, patch
from DAL.Create_withdrawal_slip_DAL import Create_withdrawal_slip_DAL

class TestCreateWithdrawalSlipDAL(unittest.TestCase):
    def setUp(self):
        self.dal = Create_withdrawal_slip_DAL()
        self.dal.db = MagicMock()

    @patch('DAL.Create_withdrawal_slip_DAL.messagebox')
    def test_create_withdrawal_slip_success(self, mock_messagebox):
        # Mock database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        self.dal.db.connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Mock account exists and has enough balance
        mock_cursor.fetchone.side_effect = [
            (5000000,),  # SELECT SoDu FROM SoTietKiem WHERE maSo = ? AND hoTen = ?
            (1000000,)   # SELECT tienGuiToiThieu FROM ThamSo WHERE loaiTietKiem = ?
        ]

        # Mock check_insuffient_balance to return True
        self.dal.check_insuffient_balance = MagicMock(return_value=True)

        result = self.dal.create_withdrawal_slip("123", "Nguyen Van A", "2024-05-07", 1000000, "3 tháng")
        self.assertTrue(result)
        mock_conn.commit.assert_called_once()

    @patch('DAL.Create_withdrawal_slip_DAL.messagebox')
    def test_create_withdrawal_slip_account_not_found(self, mock_messagebox):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        self.dal.db.connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Account not found
        mock_cursor.fetchone.return_value = None

        result = self.dal.create_withdrawal_slip("999", "Wrong Name", "2024-05-07", 1000000, "3 tháng")
        self.assertFalse(result)
        mock_messagebox.showerror.assert_called_once()

    @patch('DAL.Create_withdrawal_slip_DAL.messagebox')
    def test_create_withdrawal_slip_insufficient_balance(self, mock_messagebox):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        self.dal.db.connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Account exists
        mock_cursor.fetchone.side_effect = [
            (5000000,),  # SELECT SoDu FROM SoTietKiem WHERE maSo = ? AND hoTen = ?
            (1000000,)   # SELECT tienGuiToiThieu FROM ThamSo WHERE loaiTietKiem = ?
        ]

        # Withdrawal amount exceeds balance
        self.dal.check_insuffient_balance = MagicMock(return_value=False)

        result = self.dal.create_withdrawal_slip("123", "Nguyen Van A", "2024-05-07", 6000000, "3 tháng")
        self.assertFalse(result)
        mock_messagebox.showerror.assert_called_once()

    @patch('DAL.Create_withdrawal_slip_DAL.messagebox')
    def test_create_withdrawal_slip_below_minimum_balance(self, mock_messagebox):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        self.dal.db.connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Account exists
        mock_cursor.fetchone.side_effect = [
            (5000000,),  # SELECT SoDu FROM SoTietKiem WHERE maSo = ? AND hoTen = ?
            (1000000,)   # SELECT tienGuiToiThieu FROM ThamSo WHERE loaiTietKiem = ?
        ]

        # Withdrawal amount is allowed, but leaves less than minimum balance
        self.dal.check_insuffient_balance = MagicMock(return_value=False)

        result = self.dal.create_withdrawal_slip("123", "Nguyen Van A", "2024-05-07", 4500000, "3 tháng")
        self.assertFalse(result)
        mock_messagebox.showerror.assert_called_once()

    def test_getInterests_success(self):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        self.dal.db.connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [("3 tháng",), ("6 tháng",)]
        result = self.dal.getInterests()
        self.assertEqual(result, ["3 tháng", "6 tháng"])

    def test_getInterests_exception(self):
        self.dal.db.connect.side_effect = Exception("DB error")
        result = self.dal.getInterests()
        self.assertIsNone(result)

    def test_check_insuffient_balance(self):
        self.assertFalse(self.dal.check_insuffient_balance(2000000, 1000000))
        self.assertTrue(self.dal.check_insuffient_balance(500000, 1000000))

    def test_getBalance_success(self):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        self.dal.db.connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (5000000,)
        result = self.dal.getBalance("123")
        self.assertEqual(result, 5000000)

    def test_getBalance_exception(self):
        self.dal.db.connect.side_effect = Exception("DB error")
        result = self.dal.getBalance("123")
        self.assertIsNone(result)

    def test_getKhachHang_success(self):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        self.dal.db.connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = ("Nguyen Van A",)
        result = self.dal.getKhachHang("123")
        self.assertEqual(result, "Nguyen Van A")

    def test_getKhachHang_exception(self):
        self.dal.db.connect.side_effect = Exception("DB error")
        result = self.dal.getKhachHang("123")
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()