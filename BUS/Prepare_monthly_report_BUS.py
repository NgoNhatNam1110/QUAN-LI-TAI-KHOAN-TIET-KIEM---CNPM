import sys
import os
# Add the parent directory to system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Now import from DAL directory
from DAL.Prepare_monthly_report_DAL import Prepare_monthly_report_DAL



class Prepare_monthly_report_BUS:
    def __init__(self):
        self.Prepare_monthly_report_DAL = Prepare_monthly_report_DAL()
        
    def load_bankbook_to_table(self, date):
        """
        Load bankbook data for monthly report through the DAL layer
        
        Args:
            date (str): The date to get report data for in YYYY-MM-DD format
            
        Returns:
            list: List of dictionaries containing report data
            or None if there's an error
        """
        try:
            # Basic date format validation
            if not date or len(date.split('-')) != 3:
                print("Invalid date format. Expected YYYY-MM-DD")
                return None
                
            # Call the DAL layer method to get the data
            result = self.Prepare_monthly_report_DAL.load_bankbook_to_table(date)
            return result
        except Exception as e:
            # Log the error if needed
            print(f"Error in BUS layer while loading bankbook data: {str(e)}")
            return None