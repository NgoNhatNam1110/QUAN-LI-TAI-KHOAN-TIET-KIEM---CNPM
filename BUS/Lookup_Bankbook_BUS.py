from DAL.Lookup_Bankbook_DAL import Lookup_Bankbook_DAL

class Lookup_Bankbook_BUS:
    def __init__(self):
        self.lookup_bankbook_dal = Lookup_Bankbook_DAL()

    def get_all_bankbooks(self):
        try:
            # Call the DAL layer to fetch all bankbooks
            return self.lookup_bankbook_dal.get_all_bankbooks()
        except Exception as e:
            print(f"Error in BUS layer while fetching bankbooks: {e}")
            return []