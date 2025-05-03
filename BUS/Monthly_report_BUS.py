from DAL.Monthly_report_DAL import Monthly_report_DAL

class Monthly_report_BUS:
    def __init__(self):
        self.monthly_report_dal = Monthly_report_DAL()

    def get_monthly_report(self, month, year):
        """Get the monthly report data and process it"""
        try:
            # Fetch data from DAL
            rows = self.monthly_report_dal.fetch_monthly_report(month, year)
            if rows is None:
                return None

            # Process data into a structured format
            data = []
            for row in rows:
                ngay, so_mo, so_dong = row
                chenh_lech = so_mo - so_dong
                data.append({
                    "Ngay": ngay,
                    "SoMo": so_mo,
                    "SoDong": so_dong,
                    "ChenhLech": chenh_lech
                })
            return data
        except Exception as e:
            print(f"Error in business layer: {e}")
            return None