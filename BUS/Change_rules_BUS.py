from DAL.Change_rules_DAL import ChangeRulesDAL

class ChangeRulesBUS:
    def __init__(self):
        self.dal = ChangeRulesDAL()

    def get_all_rules(self):
        """Fetch all rules from the database."""
        return self.dal.fetch_all_rules()

    def add_new_rule(self, loaiTK, tien_toithieu, ky_han, lai, tgian):
        """Add a new rule to the database."""
        self.dal.add_rule(loaiTK, tien_toithieu, ky_han, lai, tgian)

    def update_rule(self, maQD, loaiTK, tien_toithieu, ky_han, lai, tgian):
        """Update an existing rule in the database."""
        self.dal.update_rule(maQD, loaiTK, tien_toithieu, ky_han, lai, tgian)

    def delete_rule(self, maQD, loaiTK):
        """Delete a rule from the database."""
        self.dal.delete_rule(maQD, loaiTK)
    
    def validate_loaitk(self, loaiTK):
        """Validate the type of savings."""
        if self.dal.validate_loaitk(loaiTK):
            return False
        return True