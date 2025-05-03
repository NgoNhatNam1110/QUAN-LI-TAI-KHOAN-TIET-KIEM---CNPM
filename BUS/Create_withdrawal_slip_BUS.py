from DAL.Create_withdrawal_slip_DAL import Create_withdrawal_slip_DAL

class Create_withdrawal_slip_BUS:
    def __init__(self):
        self.create_withdrawal_slip_dal = Create_withdrawal_slip_DAL()

    def create_withdrawal_slip(self, maso, khachhang, ngayrut, sotienrut, kyhansaukhirut):
        try:
            # Perform any necessary business logic or validation here
            if not maso or not khachhang or not ngayrut or not sotienrut:
                print("All fields are required.")
                return False

            # Call the DAL layer to create the withdrawal slip
            return self.create_withdrawal_slip_dal.create_withdrawal_slip(maso, khachhang, ngayrut, sotienrut, kyhansaukhirut)
        except Exception as e:
            print(f"Error in BUS layer: {e}")
            return False
    
    def GetInterestOptions(self):
        try:
            interest_options = self.create_withdrawal_slip_dal.getInterests()
            return interest_options
        except Exception as e:
            print(f"Error in business layer: {e}")
            return None
