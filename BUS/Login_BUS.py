from DAL.Login_DAL import Login_DAL

class Login_BUS:
    def __init__(self):
        self.login_dal = Login_DAL()

    def validate_login(self, username, password):
        try:
            # Perform any necessary business logic or validation here
            if not username or not password:
                print("Username and password are required.")
                return None

            # Call the DAL layer to validate login
            return self.login_dal.validate_login(username, password)
        except Exception as e:
            print(f"Error in BUS layer: {e}")
            return None