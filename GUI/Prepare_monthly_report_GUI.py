import customtkinter as ctk
from tkcalendar import Calendar
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import sys
import os

# Add the parent directory to system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import from BUS directory
from BUS.Prepare_monthly_report_BUS import Prepare_monthly_report_BUS

class Prepare_monthly_report_GUI(ctk.CTk):
    def __init__(self, parent_frame, user_id, username, password):
        super().__init__()

        # Initialize user credentials
        self.user_id = user_id
        self.username = username
        self.password = password
        self.table_container = None

        # Initialize the main frame
        self.parent_frame = parent_frame
        self.prepare_monthly_report_bus = Prepare_monthly_report_BUS()

        
        self.title("Thay Đổi Quy Định")
        self.geometry("1200x800")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Left frame for navigation
        self.left_frame = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color=("#F0F8FF", "#1E3A8A"))
        self.left_frame.pack(side="left", fill="y")

        # Right frame for content
        self.right_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=("#FFFFFF", "#1E3A8A"))
        self.right_frame.pack(side="left", fill="both", expand=True)

        # Account information section
        account_card = ctk.CTkFrame(self.left_frame, corner_radius=15, fg_color=("#FFFFFF", "#2B4F8C"))
        account_card.pack(pady=20, padx=10, fill="x")

        self.account_detail_label = ctk.CTkLabel(account_card, 
                                                text="Thông Tin Tài Khoản", 
                                                font=ctk.CTkFont(size=18, weight="bold", family="Segoe UI"),
                                                text_color=("#1E3A8A", "#FFFFFF"))
        self.account_detail_label.pack(pady=10)

        # Navigation buttons
        button_style = {
            "corner_radius": 10,
            "font": ctk.CTkFont(size=14, family="Segoe UI"),
            "hover": True,
            "fg_color": ("#1E3A8A", "#2B4F8C"),
            "text_color": ("#FFFFFF", "#FFFFFF"),
            "height": 40
        }

        self.change_rules_button = ctk.CTkButton(self.left_frame, 
                                                text="Lập báo cáo", 
                                                command=self.create_screen_report,
                                                **button_style)
        self.change_rules_button.pack(pady=10, padx=10, fill="x")

        # Display default screen (phải đặt sau khi right_frame đã được tạo)
        self.create_screen_report()
    
    def create_screen_report(self):
        # Main container with gradient background
        self.clear_right_frame()
        self.main_container = ctk.CTkFrame(self.right_frame, fg_color=("#F0F8FF", "#1E3A8A"))
        self.main_container.pack(padx=20, pady=20, fill="both", expand=True)

        # self.main_container = ctk.CTkFrame(self.parent_frame, fg_color=("#F0F8FF", "#1E3A8A"))
        # self.main_container.pack(padx=20, pady=20, fill="both", expand=True)

        # Header with title
        header_frame = ctk.CTkFrame(self.main_container, fg_color=("#1E3A8A", "#2B4F8C"), corner_radius=15)
        header_frame.pack(fill="x", pady=(0, 10))

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
        if self.table_container is not None:
            self.table_container.destroy()

        self.table_container = ctk.CTkFrame(self.main_container, border_width=1, corner_radius=15, fg_color="#e3eefd")
        self.table_container.pack(fill="both", expand=True, pady=(1, 0), padx=10)

        # Header row (nằm ngang)
        header_row = ctk.CTkFrame(self.table_container, fg_color="#1E3A8A")
        header_row.pack(fill="x", padx=5, pady=(5, 0))

        headers = [
            ("STT", 60),
            ("Loại Tiết Kiệm", 160),
            ("Tổng Thu", 120),
            ("Tổng Chi", 120),
            ("Chênh Lệch", 120)
        ]
        for text, _ in headers:  # Bỏ width
            lbl = ctk.CTkLabel(
                header_row,
                text=text,
                fg_color="#1E3A8A",
                text_color="white",
                font=ctk.CTkFont(size=13, weight="bold", family="Segoe UI"),
                corner_radius=8
            )
            lbl.pack(side="left", padx=2, pady=2, fill="both", expand=True)  # fill="both", expand=True

    def clear_table(self):
        """Clear all data rows from the table while keeping headers"""
        if self.table_container is not None:
            # Remove all widgets except headers (row 0)
            for widget in self.table_container.winfo_children():
                if isinstance(widget, ctk.CTkFrame) and widget != self.table_container.winfo_children()[0]:
                    widget.destroy()
            self.table_container.update()
        else:
            self.create_table()

    def generate_report(self):
        """Generate and display the daily transaction report"""
        try:
            selected_date = self.calendar.get_date()
            date_obj = datetime.strptime(selected_date, '%m/%d/%y')
            formatted_date = date_obj.strftime("%Y-%m-%d")

            data = self.prepare_monthly_report_bus.load_bankbook_to_table(formatted_date)
            self.clear_table()

            if not data:
                return

            col_widths = [60, 160, 120, 120, 120]
            for row_idx, row_data in enumerate(data, start=1):
                row_frame = ctk.CTkFrame(self.table_container, fg_color="#f7faff")
                row_frame.pack(fill="x", padx=5, pady=1)

                values = [
                    str(row_idx),
                    str(row_data['TenLoaiTietKiem']),
                    "{:,.0f}".format(float(row_data['TongThu'])),
                    "{:,.0f}".format(float(row_data['TongChi'])),
                    "{:,.0f}".format(float(row_data['ChenhLech']))
                ]
                for i, value in enumerate(values):
                    cell = ctk.CTkLabel(
                        row_frame,
                        text=value,
                        fg_color="#f7faff",
                        text_color="#1E3A8A",
                        font=ctk.CTkFont(size=12, family="Segoe UI"),
                        corner_radius=6
                    )
                    cell.pack(side="left", padx=2, pady=2, fill="both", expand=True)  # fill="both", expand=True
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
        self.clear_right_frame()
        # Hiển thị giao diện báo cáo tháng trong right_frame
        monthly_report_screen = Monthly_report_GUI(self.right_frame, self)
        monthly_report_screen.pack(fill="both", expand=True)
    
    
    def clear_right_frame(self):
        """Clear all widgets in the right frame"""
        for widget in self.right_frame.winfo_children():
            widget.destroy()

