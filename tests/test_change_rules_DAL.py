import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from unittest.mock import MagicMock
from DAL.Change_rules_DAL import ChangeRulesDAL

class TestChangeRulesDAL(unittest.TestCase):
    def setUp(self):
        self.dal = ChangeRulesDAL()
        self.dal.db = MagicMock()

    def test_fetch_all_rules(self):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        self.dal.db.connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            ("QD001", "TK1", 1000000, 12, 5.5, 6),
            ("QD002", "TK2", 2000000, 6, 4.5, 3)
        ]
        result = self.dal.fetch_all_rules()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["maQD"], "QD001")
        self.assertEqual(result[1]["loaiTK"], "TK2")

    def test_add_rule(self):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        self.dal.db.connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        # Simulate LoaiTietKiem does not exist
        mock_cursor.fetchone.side_effect = [
            (0,),  # LoaiTietKiem not exists
            (1,),  # max_id
        ]
        self.dal.add_rule("TK3", 3000000, 9, 6.0, 4)
        self.assertTrue(mock_conn.commit.called)

    def test_update_rule_success(self):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        self.dal.db.connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.side_effect = [
            (1,),  # LoaiTietKiem exists
            (12, 5.5, 6)  # existing values
        ]
        result = self.dal.update_rule("QD001", "TK1", 1000000, 12, 5.5, 6)
        self.assertTrue(result)
        self.assertTrue(mock_conn.commit.called)

    def test_update_rule_fail(self):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        self.dal.db.connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.side_effect = [
            (0,)  # LoaiTietKiem does not exist
        ]
        result = self.dal.update_rule("QD001", "TKX", 1000000, 12, 5.5, 6)
        self.assertFalse(result)

    def test_delete_rule(self):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        self.dal.db.connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (0,)
        self.dal.delete_rule("QD001", "TK1")
        self.assertTrue(mock_conn.commit.called)

    def test_count_rules(self):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        self.dal.db.connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (5,)
        count = self.dal.count_rules()
        self.assertEqual(count, 5)

    def test_validate_loaitk_true(self):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        self.dal.db.connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (1,)
        result = self.dal.validate_loaitk("TK1")
        self.assertTrue(result)

    def test_validate_loaitk_false(self):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        self.dal.db.connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (0,)
        result = self.dal.validate_loaitk("TKX")
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()