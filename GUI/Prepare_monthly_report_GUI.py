import customtkinter as ctk
from tkcalendar import Calendar
import tkinter as tk
from datetime import datetime
import sys
import os

# Add the parent directory to system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now import from BUS directory
from BUS.Prepare_monthly_report_BUS import Prepare_monthly_report_BUS

class Prepare_monthly_report_GUI:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.prepare_monthly_report_bus = Prepare_monthly_report_BUS()
        self.create_screen_report()
        self.table_container = None  # Will be set in create_screen_report
    
    def create_screen_report(self):
        # Main container
        main_container = ctk.CTkFrame(self.parent_frame)
        main_container.pack(padx=20, pady=20, fill="both", expand=True)

        # Header
        header_frame = ctk.CTkFrame(main_container, fg_color=("#1f538d"), border_width=1)
        header_frame.pack(fill="x")

        # Title with border
        title_frame = ctk.CTkFrame(header_frame, fg_color=("#1f538d"))
        title_frame.pack(side="left", fill="x", expand=True, padx=1, pady=1)
        title_label = ctk.CTkLabel(title_frame, text="Báo Cáo Doanh Số Hoạt Động Ngày", text_color="white", font=ctk.CTkFont(size=14, weight="bold"))
        title_label.pack(padx=10, pady=5)

        # Date input frame
        date_frame = ctk.CTkFrame(main_container)
        date_frame.pack(fill="x", pady=10)
        
        # Calendar frame on the left
        calendar_frame = tk.Frame(date_frame)
        calendar_frame.pack(side="left", padx=10)
        
        # Create calendar with current date
        current_date = datetime.now()
        self.calendar = Calendar(calendar_frame, selectmode='day', 
                               year=current_date.year, 
                               month=current_date.month, 
                               day=current_date.day,
                               background="#333333", 
                               foreground='white',
                               bordercolor="#1f538d",
                               headersbackground="#1f538d",
                               headersforeground='white',
                               selectbackground='#1f538d',
                               normalbackground="#ffffff",
                               normalforeground="#000000",
                               weekendbackground="#ffffff",
                               weekendforeground="#000000")
        self.calendar.pack()

        # Selected date display
        date_display_frame = ctk.CTkFrame(date_frame)
        date_display_frame.pack(side="left", padx=20)
        
        date_label = ctk.CTkLabel(date_display_frame, text="Ngày đã chọn:", font=ctk.CTkFont(size=12))
        date_label.pack(pady=5)
        
        self.selected_date_label = ctk.CTkLabel(date_display_frame, 
                                               text=current_date.strftime("%d/%m/%Y"),
                                               font=ctk.CTkFont(size=14, weight="bold"))
        self.selected_date_label.pack(pady=5)
        
        # Bind calendar selection to update label
        self.calendar.bind('<<CalendarSelected>>', self.update_selected_date)

        # Table container
        table_container = ctk.CTkFrame(main_container, border_width=1)
        table_container.pack(fill="both", expand=True, pady=(1, 0))

        # Headers row
        headers = ["STT", "Loại Tiết Kiệm", "Tổng Thu", "Tổng Chi", "Chênh Lệch"]
        for col, header in enumerate(headers):
            header_frame = ctk.CTkFrame(table_container, fg_color=("#1f538d"), border_width=1)
            header_frame.grid(row=0, column=col, sticky="nsew", padx=(0,1), pady=(0,1))
            header_label = ctk.CTkLabel(header_frame, text=header, text_color="white", font=ctk.CTkFont(size=12, weight="bold"))
            header_label.pack(padx=10, pady=5)

        # Configure column weights
        table_container.grid_columnconfigure(0, weight=1)  # STT
        table_container.grid_columnconfigure(1, weight=2)  # Loại Tiết Kiệm
        table_container.grid_columnconfigure(2, weight=2)  # Tổng Thu
        table_container.grid_columnconfigure(3, weight=2)  # Tổng Chi
        table_container.grid_columnconfigure(4, weight=2)  # Chênh Lệch

        # Data rows (2 empty rows as shown in the image)
        for row in range(2):
            for col in range(5):
                if col == 0:
                    # STT column
                    cell_frame = ctk.CTkFrame(table_container, border_width=1)
                    cell_frame.grid(row=row+1, column=col, sticky="nsew", padx=(0,1), pady=(0,1))
                    cell_label = ctk.CTkLabel(cell_frame, text=str(row+1))
                    cell_label.pack(padx=10, pady=8)
                else:
                    # Other columns
                    cell_frame = ctk.CTkFrame(table_container, border_width=1)
                    cell_frame.grid(row=row+1, column=col, sticky="nsew", padx=(0,1), pady=(0,1))
                    cell_label = ctk.CTkLabel(cell_frame, text="")
                    cell_label.pack(padx=10, pady=8)

        # Buttons frame
        button_frame = ctk.CTkFrame(main_container)
        button_frame.pack(pady=20)
        
        generate_button = ctk.CTkButton(button_frame, text="Tạo báo cáo", command=self.generate_report)
        generate_button.pack(side="left", padx=10)
        
        reset_button = ctk.CTkButton(button_frame, text="Reset", command=self.clear_fields)
        reset_button.pack(side="left", padx=10)

    def update_selected_date(self, event=None):
        selected_date = self.calendar.get_date()
        date_obj = datetime.strptime(selected_date, '%m/%d/%y')
        formatted_date = date_obj.strftime("%d/%m/%Y")
        self.selected_date_label.configure(text=formatted_date)

    def generate_report(self):
        """
        Generate and display the report based on selected date
        """
        try:
            # Get the selected date and convert to required format
            selected_date = self.calendar.get_date()
            date_obj = datetime.strptime(selected_date, '%m/%d/%y')
            formatted_date = date_obj.strftime("%Y-%m-%d")

            # Get data from BUS layer
            data = self.prepare_monthly_report_bus.load_bankbook_to_table(formatted_date)
            
            if not data:
                print("No data found for the selected date")
                self.clear_table()
                return

            # Clear existing data
            self.clear_table()

            # Populate table with new data
            for row_idx, row_data in enumerate(data, start=1):
                # STT column
                cell_frame = ctk.CTkFrame(self.table_container, border_width=1)
                cell_frame.grid(row=row_idx, column=0, sticky="nsew", padx=(0,1), pady=(0,1))
                cell_label = ctk.CTkLabel(cell_frame, text=str(row_idx))
                cell_label.pack(padx=10, pady=8)

                # Loại Tiết Kiệm column
                cell_frame = ctk.CTkFrame(self.table_container, border_width=1)
                cell_frame.grid(row=row_idx, column=1, sticky="nsew", padx=(0,1), pady=(0,1))
                cell_label = ctk.CTkLabel(cell_frame, text=row_data['TenLoaiTietKiem'])
                cell_label.pack(padx=10, pady=8)

                # Format currency values
                tong_thu = "{:,.0f}".format(row_data['TongThu'])
                tong_chi = "{:,.0f}".format(row_data['TongChi'])
                chenh_lech = "{:,.0f}".format(row_data['ChenhLech'])

                # Tổng Thu column
                cell_frame = ctk.CTkFrame(self.table_container, border_width=1)
                cell_frame.grid(row=row_idx, column=2, sticky="nsew", padx=(0,1), pady=(0,1))
                cell_label = ctk.CTkLabel(cell_frame, text=tong_thu)
                cell_label.pack(padx=10, pady=8)

                # Tổng Chi column
                cell_frame = ctk.CTkFrame(self.table_container, border_width=1)
                cell_frame.grid(row=row_idx, column=3, sticky="nsew", padx=(0,1), pady=(0,1))
                cell_label = ctk.CTkLabel(cell_frame, text=tong_chi)
                cell_label.pack(padx=10, pady=8)

                # Chênh Lệch column
                cell_frame = ctk.CTkFrame(self.table_container, border_width=1)
                cell_frame.grid(row=row_idx, column=4, sticky="nsew", padx=(0,1), pady=(0,1))
                cell_label = ctk.CTkLabel(cell_frame, text=chenh_lech)
                cell_label.pack(padx=10, pady=8)

        except Exception as e:
            print(f"Error generating report: {e}")

    def clear_fields(self):
        # Reset calendar to current date
        current_date = datetime.now()
        self.calendar.selection_set(current_date)
        self.selected_date_label.configure(text=current_date.strftime("%d/%m/%Y"))
    
    def clear_table(self):
        """
        Clear all data rows from the table, keeping headers
        """
        if self.table_container:
            for widget in self.table_container.grid_slaves():
                if int(widget.grid_info()['row']) > 0:
                    widget.destroy()
    
    
        
