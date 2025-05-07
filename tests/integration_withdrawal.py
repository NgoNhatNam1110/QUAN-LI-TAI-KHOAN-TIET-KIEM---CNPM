import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk

from GUI.Create_withdrawal_slip_GUI import Create_withdrawal_slip_GUI

class TestWithdrawalIntegration(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.gui = Create_withdrawal_slip_GUI(self.root)

    @patch('DAL.Create_withdrawal_slip_DAL.DatabaseConnection')
    @patch('GUI.Create_withdrawal_slip_GUI.messagebox')
    def test_successful_withdrawal(self, mock_messagebox, mock_dbconn):
        # Mock DAL methods to simulate a successful withdrawal
        self.gui.create_withdrawal_slip_bus.create_withdrawal_slip_dal.create_withdrawal_slip = MagicMock(return_value=True)
        self.gui.create_withdrawal_slip_bus.create_withdrawal_slip_dal.getInterests = MagicMock(return_value=["3 tháng"])
        self.gui.create_withdrawal_slip_bus.create_withdrawal_slip_dal.getBalance = MagicMock(return_value=5000000)
        self.gui.create_withdrawal_slip_bus.create_withdrawal_slip_dal.getKhachHang = MagicMock(return_value="Nguyen Van A")

        # Simulate user input
        self.gui.maso_entry.delete(0, "end")
        self.gui.maso_entry.insert(0, "123")
        self.gui.load_account_balance_and_customer_name()
        self.gui.ngayrut_entry.configure(state="normal")
        self.gui.ngayrut_entry.delete(0, "end")
        self.gui.ngayrut_entry.insert(0, "2024-05-07")
        self.gui.sotienrut_entry.delete(0, "end")
        self.gui.sotienrut_entry.insert(0, "1000000")
        self.gui.selected_option.set("3 tháng")

        # Trigger the withdrawal event
        self.gui.withdrawal_slip_event()
        mock_messagebox.showinfo.assert_called_with("Success", "Lập phiếu rút tiền thành công!")

    @patch('DAL.Create_withdrawal_slip_DAL.DatabaseConnection')
    @patch('GUI.Create_withdrawal_slip_GUI.messagebox')
    def test_withdrawal_invalid_amount(self, mock_messagebox, mock_dbconn):
        # Simulate user input with invalid amount
        self.gui.maso_entry.delete(0, "end")
        self.gui.maso_entry.insert(0, "123")
        self.gui.khachhang_entry.configure(state="normal")
        self.gui.khachhang_entry.delete(0, "end")
        self.gui.khachhang_entry.insert(0, "Nguyen Van A")
        self.gui.khachhang_entry.configure(state="readonly")
        self.gui.ngayrut_entry.configure(state="normal")
        self.gui.ngayrut_entry.delete(0, "end")
        self.gui.ngayrut_entry.insert(0, "2024-05-07")
        self.gui.sotienrut_entry.delete(0, "end")
        self.gui.sotienrut_entry.insert(0, "abc")  # Invalid
        self.gui.selected_option.set("3 tháng")

        self.gui.withdrawal_slip_event()
        mock_messagebox.showerror.assert_called()
        self.assertIn("Số tiền rút không hợp lệ", str(mock_messagebox.showerror.call_args[0][1]))

    @patch('DAL.Create_withdrawal_slip_DAL.DatabaseConnection')
    @patch('GUI.Create_withdrawal_slip_GUI.messagebox')
    def test_withdrawal_missing_fields(self, mock_messagebox, mock_dbconn):
        # Leave all fields empty
        self.gui.maso_entry.delete(0, "end")
        self.gui.khachhang_entry.configure(state="normal")
        self.gui.khachhang_entry.delete(0, "end")
        self.gui.khachhang_entry.configure(state="readonly")
        self.gui.ngayrut_entry.configure(state="normal")
        self.gui.ngayrut_entry.delete(0, "end")
        self.gui.sotienrut_entry.delete(0, "end")
        self.gui.selected_option.set("3 tháng")

        self.gui.withdrawal_slip_event()
        mock_messagebox.showerror.assert_called()
        self.assertIn("Vui lòng nhập đầy đủ", str(mock_messagebox.showerror.call_args[0][1]))

    def tearDown(self):
        self.root.destroy()

if __name__ == '__main__':
    unittest.main()