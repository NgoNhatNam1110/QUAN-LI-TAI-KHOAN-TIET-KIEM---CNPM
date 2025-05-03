from DAL.Create_deposit_slip_DAL import Create_deposit_slip_DAL

class Create_deposit_slip_BUS:
    def __init__(self):
        self.create_deposit_slip_dal = Create_deposit_slip_DAL()

    def create_deposit_slip(self, maso, khachhang, ngaygui, sotiengui):
        try:
            # Perform any necessary business logic or validation here
            if not maso or not khachhang or not ngaygui or not sotiengui:
                print("All fields are required.")
                return False

            # Call the DAL layer to create the deposit slip
            return self.create_deposit_slip_dal.create_deposit_slip(maso, khachhang, ngaygui, sotiengui)
        except Exception as e:
            print(f"Error in BUS layer: {e}")
            return False
    
    def GetKhachHang(self, maso):
        try:
            khachhang = self.create_deposit_slip_dal.getKhachHang(maso)
            return khachhang
        except Exception as e:
            print(f"Error in business layer: {e}")
            return None