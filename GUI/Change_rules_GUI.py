import customtkinter as ctk
import sqlite3
from utils.db_utils import DatabaseConnection
from BUS.Change_rules_BUS import ChangeRulesBUS  # Import the BUS layer
from tkinter import messagebox

class Change_rules_GUI:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.bus = ChangeRulesBUS()  # Use the BUS layer
        self.table_container = None
        self.selected_row = None
        self.create_screen_change_rules()
    
    def create_screen_change_rules(self):
        """Create the main change rules screen"""
        # Main container with gradient background
        main_container = ctk.CTkFrame(self.parent_frame, fg_color=("#F0F8FF", "#1E3A8A"))
        main_container.pack(padx=20, pady=20, fill="both", expand=True)

        # Header and Title
        header_frame = ctk.CTkFrame(main_container, fg_color=("#1E3A8A", "#2B4F8C"), corner_radius=15)
        header_frame.pack(fill="x", pady=10)

        title_label = ctk.CTkLabel(header_frame, 
                                  text="Danh Sách Các Quy Định", 
                                  font=ctk.CTkFont(size=24, weight="bold", family="Segoe UI"),
                                  text_color="white")
        title_label.pack(padx=10, pady=10)

        # Button frame for actions
        button_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        button_frame.pack(pady=10)

        button_style = {
            "corner_radius": 10,
            "font": ctk.CTkFont(size=14, family="Segoe UI"),
            "hover": True,
            "height": 40,
            "width": 150
        }

        edit_button = ctk.CTkButton(button_frame, 
                                    text="Chỉnh sửa quy định", 
                                    command=self.edit_rule,
                                    fg_color=("#1E3A8A", "#2B4F8C"),
                                    hover_color=("#2B4F8C", "#1E3A8A"),
                                    **button_style)
        edit_button.pack(side="left", padx=10)

        add_button = ctk.CTkButton(button_frame, 
                                   text="Thêm quy định", 
                                   command=self.add_rule,
                                   fg_color=("#1E3A8A", "#2B4F8C"),
                                   hover_color=("#2B4F8C", "#1E3A8A"),
                                   **button_style)
        add_button.pack(side="left", padx=10)

        delete_button = ctk.CTkButton(button_frame, 
                                      text="Xóa quy định", 
                                      command=self.delete_rule,
                                      fg_color=("#DC3545", "#C82333"),
                                      hover_color=("#C82333", "#DC3545"),
                                      **button_style)
        delete_button.pack(side="left", padx=10)

        # Table container
        table_container_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        table_container_frame.pack(fill="both", expand=True, pady=(10, 0))

        self.table_canvas = ctk.CTkCanvas(table_container_frame, borderwidth=0, highlightthickness=0)
        self.table_canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar = ctk.CTkScrollbar(table_container_frame, orientation="vertical", command=self.table_canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.table_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.table_container = ctk.CTkFrame(self.table_canvas, fg_color="transparent")
        self.table_window = self.table_canvas.create_window((0, 0), window=self.table_container, anchor="nw")

        def resize_table_container(event):
            canvas_width = event.width
            self.table_canvas.itemconfig(self.table_window, width=canvas_width)

        self.table_canvas.bind("<Configure>", resize_table_container)

        self.fetch_and_display_data()

        # Table headers
        headers = ["Mã Quy Định", "Tên Loại Tiết Kiệm", "Tiền Gửi Tối Thiểu", "Kỳ Hạn (tháng)", "Lãi Suất", "Thời Gian Gửi Tối Thiểu"]
        for col, header in enumerate(headers):
            header_frame = ctk.CTkFrame(self.table_container, fg_color=("#1E3A8A", "#2B4F8C"), corner_radius=8)
            header_frame.grid(row=0, column=col, sticky="nsew", padx=(0, 1), pady=(0, 1))
            header_label = ctk.CTkLabel(header_frame, 
                                        text=header, 
                                        font=ctk.CTkFont(size=12, weight="bold", family="Segoe UI"),
                                        text_color="white")
            header_label.pack(padx=10, pady=5)

        # Configure column weights to make the table fit the screen
        for col in range(len(headers)):
            self.table_container.grid_columnconfigure(col, weight=1)

    def clear_table(self):
        """Clear all data rows from the table while keeping headers"""
        for widget in self.table_container.grid_slaves():
            if int(widget.grid_info()['row']) > 0:
                widget.destroy()

    def populate_table(self, data):
        """Populate the table with data"""
        self.clear_table()
        for row_idx, row_data in enumerate(data, start=1):
            bg_color = "#f5f6fa" if row_idx % 2 == 0 else "#ffffff"
            row_frames = []
            for col_idx, key in enumerate(["maQD", "loaiTK", "tien_toithieu", "ky_han", "lai", "tgian"]):
                cell_frame = ctk.CTkFrame(self.table_container, border_width=1, border_color="#b0b0b0", fg_color=bg_color)
                cell_frame.grid(row=row_idx, column=col_idx, sticky="nsew", padx=1, pady=1)
                cell_label = ctk.CTkLabel(cell_frame, text=str(row_data[key]), font=ctk.CTkFont(size=12))
                cell_label.pack(padx=5, pady=5)

                cell_frame.bind("<Button-1>", lambda event, row=row_data: self.on_row_click(row))
                cell_label.bind("<Button-1>", lambda event, row=row_data: self.on_row_click(row))

                row_frames.append(cell_frame)

            row_data["frames"] = row_frames  # Thêm lại "frames" vào row_data

        self.table_container.update()

        # Ensure the table expands to fit the screen width
        for col in range(len(data[0]) if data else 7):  # Default to 7 columns if no data
            self.table_container.grid_columnconfigure(col, weight=1)

    def fetch_and_display_data(self):
        try:
            # Fetch data using the BUS
            data = self.bus.get_all_rules()
            # Populate the table with the fetched data
            self.populate_table(data)
        except Exception as e:
            print(f"Error fetching and displaying data: {e}")

    def clear_frame(self):
        for widget in self.parent_frame.winfo_children():
            widget.destroy()

    def submit_rule(self):
        new_rule = self.rule_entry.get()
        if new_rule:
            print(f"New rule submitted: {new_rule}")
            # Add logic to save the new rule to the database or configuration file
            self.clear_frame()
        else:
            print("No rule entered.")

    def add_edit_button(self):
        pass  # Đã gộp vào button_frame

    def add_add_button(self):
        pass  # Đã gộp vào button_frame

    def add_rule(self):
        """Show popup to add a new rule"""
        add_window = ctk.CTkToplevel(self.parent_frame)
        add_window.title("Thêm quy định mới")
        add_window.attributes('-topmost', True)
        entries = {}
        headers = ["Tên Loại Tiết Kiệm", "Tiền Gửi Tối Thiểu", "Kỳ Hạn (tháng)", "Lãi Suất", "Thời Gian Gửi Tối Thiểu"]
        for i, header in enumerate(headers):
            label = ctk.CTkLabel(add_window, text=header)
            label.grid(row=i, column=0, padx=10, pady=5)
            entry = ctk.CTkEntry(add_window)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries[header] = entry
        
        def save_new_rule():
            values = {key: entry.get() for key, entry in entries.items()}
            # Retrieve the value of "Tên Loại Tiết Kiệm"
            loaitk = values["Tên Loại Tiết Kiệm"]
            # Validate the inputs
            if not self.validate_loaitk(loaitk):
                messagebox.showerror("Lỗi", "Đã tồn tại loại tiết kiệm này!")
            elif not self.validate_input(values["Tiền Gửi Tối Thiểu"], values["Kỳ Hạn (tháng)"], values["Lãi Suất"], values["Thời Gian Gửi Tối Thiểu"]):
                print(values["Tiền Gửi Tối Thiểu"], values["Kỳ Hạn (tháng)"], values["Lãi Suất"], values["Thời Gian Gửi Tối Thiểu"])
                messagebox.showerror("Lỗi", "Vui lòng nhập đúng thông số!")
                return

            values = [entry.get() for entry in entries.values()]
            try:
                self.bus.add_new_rule(*values)  # Delegate to the BUS
                print("New rule added successfully.")
                self.selected_row = None
                self.fetch_and_display_data()
            except Exception as e:
                print(f"Error: {e}")
            add_window.destroy()
        save_button = ctk.CTkButton(add_window, text="Lưu", command=save_new_rule)
        save_button.grid(row=len(headers), column=0, columnspan=2, pady=10)

    def edit_rule(self):
        if not self.selected_row:
            import tkinter.messagebox as mbox
            mbox.showinfo("Thông báo", "Vui lòng chọn một dòng để chỉnh sửa.")
            return
        # Tạo cửa sổ popup để chỉnh sửa
        edit_window = ctk.CTkToplevel(self.parent_frame)
        edit_window.title("Chỉnh sửa quy định")
        edit_window.attributes('-topmost', True)
        entries = {}
        headers = ["Tên Loại Tiết Kiệm", "Tiền Gửi Tối Thiểu", "Kỳ Hạn (tháng)", "Lãi Suất", "Thời Gian Gửi Tối Thiểu"]
        row_keys = ["loaiTK", "tien_toithieu", "ky_han", "lai", "tgian"]
        for i, (header, key) in enumerate(zip(headers, row_keys)):
            label = ctk.CTkLabel(edit_window, text=header)
            label.grid(row=i, column=0, padx=10, pady=5)
            entry = ctk.CTkEntry(edit_window)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entry.insert(0, str(self.selected_row[key]))

            # Make "Tên Loại Tiết Kiệm" read-only
            if header == "Tên Loại Tiết Kiệm":
                entry.configure(state="readonly")
            entries[key] = entry

        def save_changes():
            if not self.validate_input(self.selected_row["tien_toithieu"], self.selected_row["ky_han"], self.selected_row["lai"], self.selected_row["tgian"]):
                messagebox.showerror("Lỗi", "Vui lòng nhập đúng thông số!")
            updated_values = {key: entry.get() for key, entry in entries.items()}
            try:
                self.bus.update_rule(
                    self.selected_row["maQD"],
                    updated_values["loaiTK"],
                    updated_values["tien_toithieu"],
                    updated_values["ky_han"],
                    updated_values["lai"],
                    updated_values["tgian"]
                )
                self.selected_row = None
                self.fetch_and_display_data()
                # print("Database updated successfully.")
            except Exception as e:
                print(f"Error: {e}")
            edit_window.destroy()
        save_button = ctk.CTkButton(edit_window, text="Lưu", command=save_changes)
        save_button.grid(row=len(headers), column=0, columnspan=2, pady=10)

    def delete_rule(self):
        if not self.selected_row:
            import tkinter.messagebox as mbox
            mbox.showinfo("Thông báo", "Vui lòng chọn một dòng để xóa.")
            return
        import tkinter.messagebox as mbox
        confirm = mbox.askyesno("Xác nhận xóa", "Bạn có chắc chắn muốn xóa quy định này?")
        if confirm:
            try:
                self.bus.delete_rule(self.selected_row["maQD"], self.selected_row["loaiTK"])  # Delegate to the BUS
                print("Rule deleted successfully.")
                self.selected_row = None
                self.fetch_and_display_data()
            except Exception as e:
                print(f"Error: {e}")
    
    def on_row_click(self, row):
        """Handle row click event"""
        # Reset all rows to default color
        for widget in self.table_container.grid_slaves():
            if int(widget.grid_info()['row']) > 0:
                widget.configure(fg_color="#ffffff")
        # Highlight the selected row
        for frame in row["frames"]:
            frame.configure(fg_color="#d3d3d3")
        self.selected_row = row
        print("Selected row:", self.selected_row)

    def validate_input(self, tien_toithieu, ky_han, lai, tgian):
        """Validate the input data"""
        try:
            # Convert inputs to appropriate types
            tien_toithieu = float(tien_toithieu)
            ky_han = int(ky_han)
            lai = float(lai)
            tgian = int(tgian)

            # Ensure all values are positive
            if tien_toithieu <= 0 or ky_han <= 0 or lai <= 0 or tgian <= 0:
                return False

            return True
        except ValueError:
            # If conversion fails, return False
            return False

    def validate_loaitk(self, loaiTK):
        # Kiểm tra xem loại tiết kiệm có tồn tại trong cơ sở dữ liệu hay không
        return self.bus.validate_loaitk(loaiTK)