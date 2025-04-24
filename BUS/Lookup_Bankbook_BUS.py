from DAL.Lookup_Bankbook_DAL import Lookup_Bankbook_DAL

class Lookup_Bankbook_BUS:
    def __init__(self):
        """Initialize the business layer for bankbook lookup"""
        self.lookup_bankbook_dal = Lookup_Bankbook_DAL()

    def get_all_bankbooks(self):
        """Retrieve all bankbook records from the database"""
        try:
            # Call the DAL layer to fetch all bankbooks
            return self.lookup_bankbook_dal.get_all_bankbooks()
        except Exception as e:
            print(f"Error in business layer while fetching bankbooks: {e}")
            return []

    def search_bankbooks(self, ma_so, loai_tk, khach_hang):
        """Search bankbooks based on specified criteria
        
        Args:
            ma_so (str): Bankbook number to search for
            loai_tk (str): Savings type to search for
            khach_hang (str): Customer name to search for
            
        Returns:
            list: List of dictionaries containing matching bankbooks
        """
        try:
            # Call the DAL layer to search bankbooks
            return self.lookup_bankbook_dal.search_bankbooks(ma_so, loai_tk, khach_hang)
        except Exception as e:
            print(f"Error in business layer while searching bankbooks: {e}")
            return []