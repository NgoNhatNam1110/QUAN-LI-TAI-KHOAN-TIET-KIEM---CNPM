import sys
import os
from unittest.mock import MagicMock
import sqlite3
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from BUS.Change_rules_BUS import ChangeRulesBUS
from threading import Thread

class TestChangeRules(unittest.TestCase):
    def setUp(self):
        self.bus = ChangeRulesBUS()
        # Mock the DAL layer to isolate the BUS logic
        self.bus.dal = MagicMock()

    def test_get_all_rules(self):
        # Mock the return value of fetch_all_rules
        self.bus.dal.fetch_all_rules.return_value = [
            {"maQD": "QD001", "loaiTK": "6 tháng", "tien_toithieu": 1000000, "ky_han": 6, "lai": 4.5, "tgian": 30}
        ]
        result = self.bus.get_all_rules()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["maQD"], "QD001")

    def test_get_all_rules_empty(self):
        # Mock an empty database
        self.bus.dal.fetch_all_rules.return_value = []
        result = self.bus.get_all_rules()
        self.assertEqual(len(result), 0)  # Should return an empty list

    def test_add_new_rule(self):
        # Test adding a new rule
        self.bus.add_new_rule("12 tháng", 2000000, 12, 5.0, 60)
        self.bus.dal.add_rule.assert_called_once_with("12 tháng", 2000000, 12, 5.0, 60)

    def test_update_rule(self):
        # Test updating an existing rule
        self.bus.update_rule("QD001", "12 tháng", 2000000, 12, 5.0, 60)
        self.bus.dal.update_rule.assert_called_once_with("QD001", "12 tháng", 2000000, 12, 5.0, 60)

    def test_delete_rule(self):
        # Test deleting a rule
        self.bus.delete_rule("QD001", "12 tháng")
        self.bus.dal.delete_rule.assert_called_once_with("QD001", "12 tháng")

    def test_validate_loaitk(self):
        # Mock the return value of validate_loaitk
        self.bus.dal.validate_loaitk.return_value = True
        result = self.bus.validate_loaitk("12 tháng")
        self.assertFalse(result)  # Should return False because the type exists

        self.bus.dal.validate_loaitk.return_value = False
        result = self.bus.validate_loaitk("24 tháng")
        self.assertTrue(result)  # Should return True because the type does not exist

    def test_add_duplicate_rule(self):
        # Mock validate_loaitk to return True (indicating the rule already exists)
        self.bus.dal.validate_loaitk.return_value = True
        result = self.bus.validate_loaitk("12 tháng")
        self.assertFalse(result)  # Should return False because the rule exists

    def test_concurrent_access(self):
        def add_rule():
            self.bus.add_new_rule("12 tháng", 2000000, 12, 5.0, 60)

        threads = [Thread(target=add_rule) for _ in range(10)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        # Ensure add_rule was called 10 times
        self.assertEqual(self.bus.dal.add_rule.call_count, 10)

    def test_count_rules(self):
        # Mock the DAL to return a specific count
        self.bus.dal.count_rules.return_value = 10
        result = self.bus.dal.count_rules()
        self.assertEqual(result, 10)  # Should return the mocked count

    def test_database_connection_error(self):
        # Mock the DAL to raise an exception
        self.bus.dal.fetch_all_rules.side_effect = sqlite3.OperationalError("Database connection failed")
        with self.assertRaises(sqlite3.OperationalError):
            self.bus.get_all_rules()

    def test_get_all_rules_high_volume(self):
        # Mock a large dataset
        self.bus.dal.fetch_all_rules.return_value = [
            {"maQD": f"QD{i:03d}", "loaiTK": f"{i} tháng", "tien_toithieu": 1000 * i, "ky_han": i, "lai": 4.5, "tgian": 30}
            for i in range(1, 1001)  # Simulate 1000 rules
        ]
        result = self.bus.get_all_rules()
        self.assertEqual(len(result), 1000)  # Should return 1000 rules

if __name__ == "__main__":
    unittest.main()