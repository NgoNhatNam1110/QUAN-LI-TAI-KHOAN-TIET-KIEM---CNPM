from BUS.Monthly_report_BUS import Monthly_report_BUS
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
import customtkinter as ctk
from GUI import Prepare_monthly_report_GUI

class Monthly_report_GUI(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.parent = parent
        self.monthly_report_bus = Monthly_report_BUS()

        # Main container with gradient background
        self.main_container = ctk.CTkFrame(self, fg_color=("#F0F8FF", "#1E3A8A"))
        self.main_container.pack(padx=20, pady=20, fill="both", expand=True)

        # Header with title
        header_frame = ctk.CTkFrame(self.main_container, fg_color=("#1E3A8A", "#2B4F8C"), corner_radius=15)
        header_frame.pack(fill="x", pady=(0, 10))

        title_label = ctk.CTkLabel(header_frame, 
                                   text="Báo Cáo Mở/Đóng Sổ Tháng", 
                                   text_color="white", 
                                   font=ctk.CTkFont(size=18, weight="bold", family="Segoe UI"))
        title_label.pack(padx=10, pady=10)

        # Month selection
        month_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        month_frame.pack(pady=10)

        month_label = ctk.CTkLabel(month_frame, text="Chọn tháng:", font=ctk.CTkFont(size=14, family="Segoe UI"), text_color="#1E3A8A")
        month_label.pack(side="left", padx=10)

        self.month_combobox = ttk.Combobox(month_frame, values=[f"{i:02}" for i in range(1, 13)], width=5)
        self.month_combobox.set("01")  # Default value
        self.month_combobox.pack(side="left", padx=5)

        self.year_combobox = ttk.Combobox(month_frame, values=[str(year) for year in range(2000, 2100)], width=7)
        self.year_combobox.set(str(datetime.now().year))  # Default value
        self.year_combobox.pack(side="left", padx=5)

        # Create the table
        self.create_table()

        # Control buttons
        button_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        button_frame.pack(pady=20)

        button_style = {
            "corner_radius": 10,
            "font": ctk.CTkFont(size=14, family="Segoe UI"),
            "hover": True,
            "height": 40,
            "width": 120
        }

        self.generate_button = ctk.CTkButton(button_frame, 
                                             text="Tạo Báo Cáo", 
                                             command=self.generate_report,
                                             fg_color=("#1E3A8A", "#2B4F8C"),
                                             hover_color=("#2B4F8C", "#1E3A8A"),
                                             **button_style)
        self.generate_button.pack(side="left", padx=10)

        self.back_button = ctk.CTkButton(button_frame, 
                                         text="Quay Lại", 
                                         command=self.load_prepare_monthly_report_screen,
                                         fg_color=("#DC3545", "#C82333"),
                                         hover_color=("#C82333", "#DC3545"),
                                         **button_style)
        self.back_button.pack(side="left", padx=10)

    def create_table(self):
        """Create the table container and headers"""
        self.table_container = ctk.CTkFrame(self.main_container, border_width=1, corner_radius=15)
        self.table_container.pack(fill="both", expand=True, pady=(10, 0))

        headers = ["STT", "Ngày", "Số Mở", "Số Đóng", "Chênh Lệch"]
        for col, header in enumerate(headers):
            header_frame = ctk.CTkFrame(self.table_container, fg_color=("#1E3A8A", "#2B4F8C"), corner_radius=15)
            header_frame.grid(row=0, column=col, sticky="nsew", padx=(0, 1), pady=(0, 1))
            header_label = ctk.CTkLabel(header_frame, 
                                        text=header, 
                                        text_color="white", 
                                        font=ctk.CTkFont(size=12, weight="bold", family="Segoe UI"))
            header_label.pack(padx=10, pady=5)

        self.table_container.grid_columnconfigure(0, weight=1)
        self.table_container.grid_columnconfigure(1, weight=2)
        self.table_container.grid_columnconfigure(2, weight=2)
        self.table_container.grid_columnconfigure(3, weight=2)
        self.table_container.grid_columnconfigure(4, weight=2)

    def populate_table(self, data):
        """Populate the table with data"""
        for widget in self.table_container.grid_slaves():
            if int(widget.grid_info()['row']) > 0:
                widget.destroy()

        for row_idx, row_data in enumerate(data, start=1):
            frames = []
            for col in range(5):
                cell_frame = ctk.CTkFrame(self.table_container, border_width=1, fg_color=("#FFFFFF", "#1E3A8A"), corner_radius=8)
                cell_frame.grid(row=row_idx, column=col, sticky="nsew", padx=(0, 1), pady=(0, 1))
                frames.append(cell_frame)

            ctk.CTkLabel(frames[0], text=str(row_idx), font=ctk.CTkFont(size=12), text_color=("#1E3A8A", "#FFFFFF")).pack(padx=10, pady=8)
            ctk.CTkLabel(frames[1], text=row_data['Ngay'], font=ctk.CTkFont(size=12), text_color=("#1E3A8A", "#FFFFFF")).pack(padx=10, pady=8)
            ctk.CTkLabel(frames[2], text=row_data['SoMo'], font=ctk.CTkFont(size=12), text_color=("#1E3A8A", "#FFFFFF")).pack(padx=10, pady=8)
            ctk.CTkLabel(frames[3], text=row_data['SoDong'], font=ctk.CTkFont(size=12), text_color=("#1E3A8A", "#FFFFFF")).pack(padx=10, pady=8)
            ctk.CTkLabel(frames[4], text=row_data['ChenhLech'], font=ctk.CTkFont(size=12), text_color=("#1E3A8A", "#FFFFFF")).pack(padx=10, pady=8)

    def generate_report(self):
        """Fetch data from the business layer and populate the table"""
        month = self.month_combobox.get()
        year = self.year_combobox.get()

        if not month or not year:
            messagebox.showerror("Lỗi", "Vui lòng chọn tháng và năm!")
            return

        data = self.monthly_report_bus.get_monthly_report(month, year)
        if data is None:
            messagebox.showerror("Lỗi", "Không thể tạo báo cáo. Vui lòng thử lại!")
        else:
            self.populate_table(data)
            messagebox.showinfo("Thành công", "Báo cáo đã được tạo thành công!")
    
    def load_prepare_monthly_report_screen(self):
        """Load the Prepare Monthly Report screen"""
        from GUI.Prepare_monthly_report_GUI import Prepare_monthly_report_GUI

        # Clear the current frame
        for widget in self.parent.winfo_children():
            widget.destroy()

        # Load the Prepare Monthly Report GUI
        prepare_report_screen = Prepare_monthly_report_GUI(self.parent)
        