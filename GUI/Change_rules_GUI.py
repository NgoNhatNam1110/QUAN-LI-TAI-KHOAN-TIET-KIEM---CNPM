import customtkinter as ctk
import sqlite3
from utils.db_utils import DatabaseConnection

class Change_rules_GUI:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.db = DatabaseConnection()
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

        from DAL.Change_rules_DAL import ChangeRulesDAL
        self.dal = ChangeRulesDAL()

        self.fetch_and_display_data()

        # Table headers
        headers = ["Mã Quy Định", "Tên Loại Tiết Kiệm", "Tiền Gửi Tối Thiểu", "Kỳ Hạn (tháng)", "Lãi Suất (%)", "Thời Gian Gửi Tối Thiểu"]
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
            for col_idx, key in enumerate(["maQD", "loaiTK", "tien_toithieu", "ky_han", "lai", "tgian"]):
                cell_frame = ctk.CTkFrame(self.table_container, border_width=1, border_color="#b0b0b0", fg_color=bg_color)
                cell_frame.grid(row=row_idx, column=col_idx, sticky="nsew", padx=1, pady=1)
                cell_label = ctk.CTkLabel(cell_frame, text=str(row_data[key]), font=ctk.CTkFont(size=12))
                cell_label.pack(padx=5, pady=5)

        # Ensure the table expands to fit the screen width
        for col in range(len(data[0]) if data else 7):  # Default to 7 columns if no data
            self.table_container.grid_columnconfigure(col, weight=1)

    def fetch_and_display_data(self):
        try:
            # Connect to the database
            connection = self.db.connect()
            cursor = connection.cursor()

            # Query to fetch term types
            query = "SELECT ts.maQuyDinh, ts.loaiTietKiem, ts.tienGuiToiThieu, ts.kyHan, ts.laiSuat, ltk.thoiGianGuiToiThieu FROM ThamSo ts JOIN LoaiTietKiem ltk ON ts.loaiTietKiem = ltk.loaiTietKiem"
            cursor.execute(query)
            rows = cursor.fetchall()

            # Format data for table population
            data = []
            # Validate row structure before unpacking
            for row in rows:
                if len(row) == 6:
                    maQD, loaiTK, tien_toithieu,ky_han,lai, tgian = row
                    data.append({
                        "maQD": maQD,
                        "loaiTK": loaiTK,
                        "tien_toithieu": tien_toithieu,
                        "ky_han": ky_han,
                        "lai": lai,
                        "tgian": tgian
                    })
                else:
                    print(f"Skipping invalid row: {row}")

            # Populate table with data using the new method (with select box)
            self.populate_table(data)

            # Close the connection
            self.db.close(connection)
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"Error: {e}")

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
        headers = ["Tên Loại Tiết Kiệm", "Tiền Gửi Tối Thiểu", "Kỳ Hạn (tháng)", "Lãi Suất (%)", "Thời Gian Gửi Tối Thiểu"]
        for i, header in enumerate(headers):
            label = ctk.CTkLabel(add_window, text=header)
            label.grid(row=i, column=0, padx=10, pady=5)
            entry = ctk.CTkEntry(add_window)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries[header] = entry
        def save_new_rule():
            values = [entry.get() for entry in entries.values()]
            try:
                connection = self.db.connect()
                cursor = connection.cursor()
                # Lấy mã quy định lớn nhất hiện tại
                cursor.execute("SELECT MAX(CAST(SUBSTR(maQuyDinh, 3) AS INTEGER)) FROM ThamSo WHERE maQuyDinh LIKE 'QD%'")
                max_id = cursor.fetchone()[0]
                if max_id is None:
                    new_id = 1
                else:
                    new_id = max_id + 1
                maQD = f"QD{new_id:03d}"
                # Thêm vào DAL (DAL sẽ tự động thêm vào LoaiTietKiem nếu cần)
                from DAL.Change_rules_DAL import ChangeRulesDAL
                dal = ChangeRulesDAL()
                dal.add_rule(values[0], values[1], values[2], values[3], values[4])
                print("New rule added successfully.")
                self.fetch_and_display_data()
                self.selected_row = None
            except sqlite3.Error as e:
                print(f"Database error: {e}")
            except Exception as e:
                print(f"Error: {e}")
            finally:
                self.db.close(connection)
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
        headers = ["Tên Loại Tiết Kiệm", "Tiền Gửi Tối Thiểu", "Kỳ Hạn (tháng)", "Lãi Suất (%)", "Thời Gian Gửi Tối Thiểu"]
        row_keys = ["loaiTK", "tien_toithieu", "ky_han", "lai", "tgian"]
        for i, (header, key) in enumerate(zip(headers, row_keys)):
            label = ctk.CTkLabel(edit_window, text=header)
            label.grid(row=i, column=0, padx=10, pady=5)
            entry = ctk.CTkEntry(edit_window)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entry.insert(0, str(self.selected_row[key]))
            entries[key] = entry
        def save_changes():
            updated_values = {key: entry.get() for key, entry in entries.items()}
            try:
                from DAL.Change_rules_DAL import ChangeRulesDAL
                dal = ChangeRulesDAL()
                dal.update_rule(
                    self.selected_row["maQD"],
                    updated_values["loaiTK"],
                    updated_values["tien_toithieu"],
                    updated_values["ky_han"],
                    updated_values["lai"],
                    updated_values["tgian"]
                )
                print("Database updated successfully.")
                self.fetch_and_display_data()
                self.selected_row = None
            except sqlite3.Error as e:
                print(f"Database error: {e}")
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
                from DAL.Change_rules_DAL import ChangeRulesDAL
                dal = ChangeRulesDAL()
                dal.delete_rule(self.selected_row["maQD"], self.selected_row["loaiTK"])
                print("Rule deleted successfully.")
                self.selected_row = None
                self.fetch_and_display_data()
            except sqlite3.Error as e:
                print(f"Database error: {e}")
            except Exception as e:
                print(f"Error: {e}")
