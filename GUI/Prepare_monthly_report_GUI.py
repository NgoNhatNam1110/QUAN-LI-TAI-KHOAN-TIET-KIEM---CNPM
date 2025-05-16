import customtkinter as ctk
from tkcalendar import Calendar
import tkinter as tk
from datetime import datetime
import sys
import os

# Add the parent directory to system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import from BUS directory
from BUS.Prepare_monthly_report_BUS import Prepare_monthly_report_BUS

class Prepare_monthly_report_GUI:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.prepare_monthly_report_bus = Prepare_monthly_report_BUS()
        self.table_container = None
        self.create_screen_report()
    
    def create_screen_report(self):
        # Main container with gradient background
        self.main_container = ctk.CTkFrame(self.parent_frame, fg_color=("#F0F8FF", "#1E3A8A"))
        self.main_container.pack(padx=20, pady=20, fill="both", expand=True)

        # Header with title
        header_frame = ctk.CTkFrame(self.main_container, fg_color=("#1E3A8A", "#2B4F8C"), corner_radius=15)
        header_frame.pack(fill="x")

        title_frame = ctk.CTkFrame(header_frame, fg_color=("#1E3A8A", "#2B4F8C"))
        title_frame.pack(side="left", fill="x", expand=True, padx=1, pady=1)
        title_label = ctk.CTkLabel(title_frame, 
                                  text="Báo Cáo Doanh Số Hoạt Động Ngày", 
                                  text_color="white", 
                                  font=ctk.CTkFont(size=14, weight="bold", family="Segoe UI"))
        title_label.pack(padx=10, pady=5)

        # Date selection area
        date_frame = ctk.CTkFrame(self.main_container, fg_color=("#F0F8FF", "#2B4F8C"), corner_radius=15)
        date_frame.pack(fill="x", pady=10)
        
        # Calendar widget
        calendar_frame = tk.Frame(date_frame, bg="#F0F8FF")
        calendar_frame.pack(side="left", padx=10)
        
        current_date = datetime.now()
        self.calendar = Calendar(calendar_frame, selectmode='day', 
                               year=current_date.year, 
                               month=current_date.month, 
                               day=current_date.day,
                               background="#F0F8FF", 
                               foreground='#1E3A8A',
                               bordercolor="#1E3A8A",
                               headersbackground="#1E3A8A",
                               headersforeground='white',
                               selectbackground='#1E3A8A',
                               normalbackground="#FFFFFF",
                               normalforeground="#1E3A8A",
                               weekendbackground="#FFFFFF",
                               weekendforeground="#1E3A8A")
        self.calendar.pack()

        # Selected date display
        date_display_frame = ctk.CTkFrame(date_frame, fg_color=("#F0F8FF", "#2B4F8C"))
        date_display_frame.pack(side="left", padx=20)
        
        date_label = ctk.CTkLabel(date_display_frame, 
                                 text="Ngày đã chọn:", 
                                 font=ctk.CTkFont(size=12, family="Segoe UI"),
                                 text_color=("#1E3A8A", "#FFFFFF"))
        date_label.pack(pady=5)
        
        self.selected_date_label = ctk.CTkLabel(date_display_frame, 
                                               text=current_date.strftime("%d/%m/%Y"),
                                               font=ctk.CTkFont(size=14, weight="bold", family="Segoe UI"),
                                               text_color=("#1E3A8A", "#FFFFFF"))
        self.selected_date_label.pack(pady=5)
        
        # Bind calendar selection event
        self.calendar.bind('<<CalendarSelected>>', self.update_selected_date)

        # Create table container and headers
        self.create_table()

        # Control buttons with hover effects
        button_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        button_frame.pack(pady=20)
        
        button_style = {
            "corner_radius": 10,
            "font": ctk.CTkFont(size=14, family="Segoe UI"),
            "hover": True,
            "height": 40,
            "width": 120
        }
        
        generate_button = ctk.CTkButton(button_frame, 
                                      text="Tạo báo cáo", 
                                      command=self.generate_report,
                                      fg_color=("#1E3A8A", "#2B4F8C"),
                                      hover_color=("#2B4F8C", "#1E3A8A"),
                                      **button_style)
        generate_button.pack(side="left", padx=10)
        
        reset_button = ctk.CTkButton(button_frame, 
                                   text="Reset", 
                                   command=self.clear_fields,
                                   fg_color=("#DC3545", "#C82333"),
                                   hover_color=("#C82333", "#DC3545"),
                                   **button_style)
        reset_button.pack(side="left", padx=10)

        monthly_report_button = ctk.CTkButton(button_frame,
                                               text="Báo cáo tháng", 
                                               command=self.show_monthly_report,
                                               fg_color=("#1E3A8A", "#2B4F8C"),
                                               hover_color=("#2B4F8C", "#1E3A8A"),
                                               **button_style)
        monthly_report_button.pack(side="left", padx=10)

    def create_table(self):
        """Create the table container and headers"""
        # Destroy existing table if it exists
        if self.table_container is not None:
            self.table_container.destroy()

        # Create new table container
        self.table_container = ctk.CTkFrame(self.main_container, border_width=1, corner_radius=15)
        self.table_container.pack(fill="both", expand=True, pady=(1, 0))

        # Table headers
        headers = ["STT", "Loại Tiết Kiệm", "Tổng Thu", "Tổng Chi", "Chênh Lệch"]
        for col, header in enumerate(headers):
            header_frame = ctk.CTkFrame(self.table_container, fg_color=("#1E3A8A", "#2B4F8C"), corner_radius=15)
            header_frame.grid(row=0, column=col, sticky="nsew", padx=(0,1), pady=(0,1))
            header_label = ctk.CTkLabel(header_frame, 
                                      text=header, 
                                      text_color="white", 
                                      font=ctk.CTkFont(size=12, weight="bold", family="Segoe UI"))
            header_label.pack(padx=10, pady=5)

        # Configure column weights for responsive layout
        self.table_container.grid_columnconfigure(0, weight=1)  # STT
        self.table_container.grid_columnconfigure(1, weight=2)  # Loại Tiết Kiệm
        self.table_container.grid_columnconfigure(2, weight=2)  # Tổng Thu
        self.table_container.grid_columnconfigure(3, weight=2)  # Tổng Chi
        self.table_container.grid_columnconfigure(4, weight=2)  # Chênh Lệch

    def clear_table(self):
        """Clear all data rows from the table while keeping headers"""
        if self.table_container is not None:
            # Remove all widgets except headers (row 0)
            for widget in self.table_container.grid_slaves():
                if int(widget.grid_info()['row']) > 0:
                    widget.destroy()
            self.table_container.update()
        else:
            self.create_table()

    def generate_report(self):
        """Generate and display the daily transaction report"""
        try:
            # Get and format selected date
            selected_date = self.calendar.get_date()
            date_obj = datetime.strptime(selected_date, '%m/%d/%y')
            formatted_date = date_obj.strftime("%Y-%m-%d")

            # Fetch report data
            data = self.prepare_monthly_report_bus.load_bankbook_to_table(formatted_date)
            
            if not data:
                print("No data found for the selected date")
                self.clear_table()
                return

            # Ensure table exists and is clear
            if self.table_container is None:
                self.create_table()
            else:
                self.clear_table()

            # Populate table with data
            for row_idx, row_data in enumerate(data, start=1):
                # Create cell frames
                frames = []
                for col in range(5):
                    cell_frame = ctk.CTkFrame(self.table_container, 
                                            border_width=1, 
                                            fg_color=("#FFFFFF", "#1E3A8A"),
                                            corner_radius=8)
                    cell_frame.grid(row=row_idx, column=col, sticky="nsew", padx=(0,1), pady=(0,1))
                    frames.append(cell_frame)

                # Fill data into cells
                cell_label = ctk.CTkLabel(frames[0], 
                                        text=str(row_idx),
                                        font=ctk.CTkFont(size=12, family="Segoe UI"),
                                        text_color=("#1E3A8A", "#FFFFFF"))
                cell_label.pack(padx=10, pady=8)

                cell_label = ctk.CTkLabel(frames[1], 
                                        text=str(row_data['TenLoaiTietKiem']),
                                        font=ctk.CTkFont(size=12, family="Segoe UI"),
                                        text_color=("#1E3A8A", "#FFFFFF"))
                cell_label.pack(padx=10, pady=8)

                # Format currency values
                tong_thu = "{:,.0f}".format(float(row_data['TongThu']))
                tong_chi = "{:,.0f}".format(float(row_data['TongChi']))
                chenh_lech = "{:,.0f}".format(float(row_data['ChenhLech']))

                cell_label = ctk.CTkLabel(frames[2], 
                                        text=tong_thu,
                                        font=ctk.CTkFont(size=12, family="Segoe UI"),
                                        text_color=("#1E3A8A", "#FFFFFF"))
                cell_label.pack(padx=10, pady=8)

                cell_label = ctk.CTkLabel(frames[3], 
                                        text=tong_chi,
                                        font=ctk.CTkFont(size=12, family="Segoe UI"),
                                        text_color=("#1E3A8A", "#FFFFFF"))
                cell_label.pack(padx=10, pady=8)

                cell_label = ctk.CTkLabel(frames[4], 
                                        text=chenh_lech,
                                        font=ctk.CTkFont(size=12, family="Segoe UI"),
                                        text_color=("#1E3A8A", "#FFFFFF"))
                cell_label.pack(padx=10, pady=8)

            self.table_container.update()

        except Exception as e:
            print(f"Error generating report: {e}")
            import traceback
            traceback.print_exc()

    def clear_fields(self):
        """Reset the form to its initial state"""
        # Reset calendar to current date
        current_date = datetime.now()
        self.calendar.selection_set(current_date)
        
        # Update the selected date label
        self.selected_date_label.configure(text=current_date.strftime("%Y-%m-%d"))
        
        
        # Clear table data
        self.clear_table()
        
        # Force update the display
        self.parent_frame.update()

    def update_selected_date(self, event=None):
        """Update the displayed selected date when calendar selection changes"""
        selected_date = self.calendar.get_date()
        date_obj = datetime.strptime(selected_date, '%m/%d/%y')
        formatted_date = date_obj.strftime("%Y-%m-%d")
        self.selected_date_label.configure(text=formatted_date)
    
    def show_monthly_report(self):
        from GUI.Monthly_report_GUI import Monthly_report_GUI
        # Clear the current frame
        for widget in self.parent_frame.winfo_children():
            widget.destroy()

        monthly_report_screen = Monthly_report_GUI(self.parent_frame, self)
        monthly_report_screen.pack(fill="both", expand=True)


