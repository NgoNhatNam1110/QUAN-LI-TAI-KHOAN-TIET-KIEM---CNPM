from utils.db_utils import DatabaseConnection

class Login_DAL:
    def __init__(self):
        self.db = DatabaseConnection()

    def validate_login(self, username, password):
        try:
            # Connect to the database
            connection = self.db.connect()
            cursor = connection.cursor()

            # Query the database for the entered credentials
            query = "SELECT ID, NAME, PASSWORD, ROLE FROM Admin WHERE NAME = ? AND PASSWORD = ?"
            cursor.execute(query, (username, password))
            print(f"Executing query: {query} with params: {username}, {password}")
            result = cursor.fetchone()

            return result  # Return the result (None if no match found)

        except Exception as e:
            print(f"Error in DAL layer: {e}")
            return None
        finally:
            if 'connection' in locals() and connection:
                connection.close()