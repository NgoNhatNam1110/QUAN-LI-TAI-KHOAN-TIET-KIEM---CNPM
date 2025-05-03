from DAL.BankbookDAL import BankbookDAL
from tkinter import messagebox

class BankbookBUS:
    def __init__(self):
        self.bankbook_dal = BankbookDAL()

    def insert_new_record(self, maso, loaitk, khachhang, cmnd, diachi, ngaymo, sotiengui):
        try:
            # Perform any necessary business logic or validation here
            if not maso or not loaitk or not khachhang or not cmnd or not diachi or not ngaymo or not sotiengui:
                messagebox.showerror(
                    "Error",
                    "Vui lòng nhập đầy đủ các trường dữ liệu"
                )
                return False

            # Call the DAL layer to insert the record
            return self.bankbook_dal.insert_new_record(
                maso, loaitk, khachhang, cmnd, diachi, ngaymo, sotiengui
            )
        except Exception as e:
            print(f"Error in business layer: {e}")
            return False
    
    def checkmaso(self, maso):
        check = self.bankbook_dal.checkmaso(maso)
        return check
    
    def checkCMND(self, cmnd):
        check = self.bankbook_dal.checkCMND(cmnd)
        return check
    
    def GetInterestOptions(self):
        try:
            interest_options = self.bankbook_dal.getInterests()
            return interest_options
        except Exception as e:
            print(f"Error in business layer: {e}")
            return None
        
    def checkminimumDeposit(self, loaitk, sotiengui):
        try:
            sotientoithieu = self.bankbook_dal.checkminimumDeposit(loaitk)
            if sotientoithieu is None:
                return "Không thể kiểm tra số tiền gửi tối thiểu. Vui lòng thử lại."
            if float(sotiengui) < float(sotientoithieu):
                return f"Số tiền gửi phải lớn hơn hoặc bằng {sotientoithieu}."
            return "Số tiền gửi hợp lệ."
        except ValueError:
            return "Số tiền gửi không hợp lệ. Vui lòng nhập một số hợp lệ."
        except Exception as e:
            print(f"Error in business layer: {e}")
            return "Đã xảy ra lỗi khi kiểm tra số tiền gửi."
    
    def generate_new_maso(self):
        """Generate a new account number based on the maximum account number"""
        try:
            max_maso = self.bankbook_dal.get_max_maso()
            if max_maso:
                max_number = int(max_maso[3:])  # Lấy phần số sau "STK"
                new_maso = f"STK{max_number + 1:010}"  # Tăng số và định dạng lại
            else:
                new_maso = "STK0000000001"  # Mã số đầu tiên nếu chưa có dữ liệu
            return new_maso
        except Exception as e:
            print(f"Error generating new account number: {e}")
            return None