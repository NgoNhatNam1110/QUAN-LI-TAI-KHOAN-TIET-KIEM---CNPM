import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk

from GUI.Create_withdrawal_slip_GUI import Create_withdrawal_slip_GUI

class TestCreateWithdrawalSlipGUI(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.gui = Create_withdrawal_slip_GUI(self.root)
        self.gui.create_withdrawal_slip_bus = MagicMock()

    @patch('GUI.Create_withdrawal_slip_GUI.messagebox')
    def test_withdrawal_slip_event_missing_fields(self, mock_messagebox):
        # All fields empty
        self.gui.maso_entry.delete(0, "end")
        self.gui.khachhang_entry.delete(0, "end")
        self.gui.ngayrut_entry.delete(0, "end")
        self.gui.sotienrut_entry.delete(0, "end")
        self.gui.withdrawal_slip_event()
        mock_messagebox.showerror.assert_called_once()
        # Accept any error message for missing fields
        self.assertTrue(any("Vui lòng" in str(arg) for arg in mock_messagebox.showerror.call_args[0]))

    @patch('GUI.Create_withdrawal_slip_GUI.messagebox')
    def test_withdrawal_slip_event_invalid_amount(self, mock_messagebox):
        # Fill required fields, but invalid amount
        self.gui.maso_entry.delete(0, "end")
        self.gui.khachhang_entry.delete(0, "end")
        self.gui.ngayrut_entry.delete(0, "end")
        self.gui.sotienrut_entry.delete(0, "end")
        self.gui.maso_entry.insert(0, "123")
        self.gui.khachhang_entry.insert(0, "Nguyen Van A")
        self.gui.ngayrut_entry.configure(state="normal")
        self.gui.ngayrut_entry.insert(0, "2024-05-07")
        self.gui.sotienrut_entry.insert(0, "abc")  # Invalid amount
        self.gui.withdrawal_slip_event()
        mock_messagebox.showerror.assert_called_once()
        # Accept any error message for invalid amount
        self.assertTrue(mock_messagebox.showerror.called)

    @patch('GUI.Create_withdrawal_slip_GUI.messagebox')
    def test_withdrawal_slip_event_success(self, mock_messagebox):
        # Fill all fields with valid data
        self.gui.maso_entry.delete(0, "end")
        self.gui.maso_entry.insert(0, "123")
        # Simulate the business layer returning the customer name and balance
        self.gui.create_withdrawal_slip_bus.GetKhachHang.return_value = "Nguyen Van A"
        self.gui.create_withdrawal_slip_bus.GetBalance.return_value = 5000000
        # Use the GUI method to fill the customer name (readonly field)
        self.gui.load_account_balance_and_customer_name()
        self.gui.ngayrut_entry.configure(state="normal")
        self.gui.ngayrut_entry.delete(0, "end")
        self.gui.ngayrut_entry.insert(0, "2024-05-07")
        self.gui.sotienrut_entry.delete(0, "end")
        self.gui.sotienrut_entry.insert(0, "1000000")
        self.gui.selected_option.set("3 tháng")
        self.gui.create_withdrawal_slip_bus.create_withdrawal_slip.return_value = True
        self.gui.withdrawal_slip_event()
        self.assertTrue(mock_messagebox.showinfo.called)

    @patch('GUI.Create_withdrawal_slip_GUI.messagebox')
    def test_load_account_balance_and_customer_name_found(self, mock_messagebox):
        self.gui.maso_entry.delete(0, "end")
        self.gui.maso_entry.insert(0, "123")
        self.gui.create_withdrawal_slip_bus.GetBalance.return_value = 5000000
        self.gui.create_withdrawal_slip_bus.GetKhachHang.return_value = "Nguyen Van A"
        self.gui.load_account_balance_and_customer_name()
        self.assertEqual(self.gui.khachhang_entry.get(), "Nguyen Van A")
        self.assertEqual(self.gui.sodu_entry.get().replace(",", ""), "5000000")

    @patch('GUI.Create_withdrawal_slip_GUI.messagebox')
    def test_load_account_balance_and_customer_name_not_found(self, mock_messagebox):
        self.gui.maso_entry.delete(0, "end")
        self.gui.maso_entry.insert(0, "999")
        self.gui.create_withdrawal_slip_bus.GetBalance.return_value = None
        self.gui.create_withdrawal_slip_bus.GetKhachHang.return_value = None
        self.gui.load_account_balance_and_customer_name()
        self.assertEqual(self.gui.khachhang_entry.get(), "")
        self.assertEqual(self.gui.sodu_entry.get(), "")
        self.assertTrue(mock_messagebox.showerror.called)

    def tearDown(self):
        self.root.destroy()

if __name__ == '__main__':
    unittest.main()