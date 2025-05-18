import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from unittest.mock import MagicMock
from BUS.Create_withdrawal_slip_BUS import Create_withdrawal_slip_BUS

class TestCreateWithdrawalSlipBUS(unittest.TestCase):
    def setUp(self):
        self.bus = Create_withdrawal_slip_BUS()
        # Mock the DAL layer to isolate the BUS logic
        self.bus.create_withdrawal_slip_dal = MagicMock()

    def test_create_withdrawal_slip_success(self):
        self.bus.create_withdrawal_slip_dal.create_withdrawal_slip.return_value = True
        result = self.bus.create_withdrawal_slip("123", "Nguyen Van A", "2024-05-07", "1000000", "3 tháng")
        self.assertTrue(result)
        self.bus.create_withdrawal_slip_dal.create_withdrawal_slip.assert_called_once_with("123", "Nguyen Van A", "2024-05-07", "1000000", "3 tháng")

    def test_create_withdrawal_slip_missing_fields(self):
        result = self.bus.create_withdrawal_slip("", "Nguyen Van A", "2024-05-07", "1000000", "3 tháng")
        self.assertFalse(result)
        self.bus.create_withdrawal_slip_dal.create_withdrawal_slip.assert_not_called()

    def test_create_withdrawal_slip_dal_failure(self):
        self.bus.create_withdrawal_slip_dal.create_withdrawal_slip.return_value = False
        result = self.bus.create_withdrawal_slip("123", "Nguyen Van A", "2024-05-07", "1000000", "3 tháng")
        self.assertFalse(result)

    def test_create_withdrawal_slip_exception(self):
        self.bus.create_withdrawal_slip_dal.create_withdrawal_slip.side_effect = Exception("DB error")
        result = self.bus.create_withdrawal_slip("123", "Nguyen Van A", "2024-05-07", "1000000", "3 tháng")
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()