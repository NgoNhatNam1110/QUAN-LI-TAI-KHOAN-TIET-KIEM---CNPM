# QUẢN LÝ TÀI KHOẢN TIẾT KIỆM

> **License:** Dự án sử dụng giấy phép [MIT License](https://opensource.org/licenses/MIT) – bạn có thể tự do sử dụng, sao chép, chỉnh sửa, phân phối lại hoặc tích hợp vào dự án khác, kể cả mục đích thương mại, chỉ cần giữ lại thông tin bản quyền gốc.

## Giới thiệu

Dự án **Quản Lý Tài Khoản Tiết Kiệm** nhằm xây dựng một hệ thống phần mềm hỗ trợ quản lý các tài khoản tiết kiệm tại ngân hàng. Ứng dụng cho phép tạo mới, chỉnh sửa, xóa và tra cứu thông tin tài khoản tiết kiệm, quản lý giao dịch gửi/rút tiền, tính lãi suất, và xuất báo cáo thống kê. Hệ thống hướng tới việc đơn giản hóa quy trình quản lý, nâng cao hiệu quả và độ chính xác cho nhân viên ngân hàng.

---

## Công cụ sử dụng

- **Ngôn ngữ lập trình:** Python 3.11 trở lên
- **Thư viện giao diện:** customtkinter, tkcalendar
- **Kết nối cơ sở dữ liệu:** pyodbc
- **Kiểm thử:** unittest (thư viện chuẩn Python)
- **Quản lý môi trường & đóng gói:** Docker
- **Hệ quản trị cơ sở dữ liệu:** SQL Server (hoặc tương thích ODBC)
- **Hỗ trợ hiển thị GUI trên Docker:** VcXsrv (Windows), XQuartz (macOS), X11 (Linux)
- **Quản lý mã nguồn:** Git

---

## Dòng thời gian dự án (Tuần 1 → Tuần 14)

Tuần:        1    2    3    4    5    6    7    8    9   10   11   12   13   14
            ─┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────
Giai đoạn:  ██████████████  Waterfall       │ 🔁 Bắt đầu Agile ▷ ▷ ▷ ▷ ▷ ▷ ▷ ▷
Hoạt động:  📋 Lập KH + Thiết kế            │ 🔄 Sprint 1 → 7: Code + Test + Feedback
Git flow:   ⎇ Nhánh riêng, ít merge         │ ⎇ Nhánh riêng, merge thường xuyên
Họp nhóm:   🔇 Không thường xuyên           │ 📅 Họp sprint hàng tuần
Theo dõi:   📄 Tài liệu tay, commit lớn     │ 📌 GitHub Issues + Pull requests

---

## Kiểm thử phần mềm

Hệ thống đã được kiểm thử tự động với các loại kiểm thử sau:

| Loại kiểm thử      | Mô tả                                                                                                                        | Các trường hợp chính                                                                                                    |
|--------------------|------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------|
| **Unit Test**      | Kiểm thử từng lớp riêng biệt (DAL, BUS, GUI) với các trường hợp thành công, thất bại, ngoại lệ, dữ liệu biên và không hợp lệ. | - Lập phiếu rút tiền thành công<br>- Thiếu trường thông tin, nhập sai định dạng<br>- Số tiền rút vượt quá số dư<br>- Số tiền rút nhỏ hơn mức tối thiểu<br>- Kiểm tra lấy thông tin khách hàng, số dư, danh sách kỳ hạn<br>- Kiểm thử các hàm phụ trợ và xử lý ngoại lệ |
| **Integration Test** | Kiểm thử luồng tích hợp giữa các lớp (GUI ↔ BUS ↔ DAL), đảm bảo dữ liệu và lỗi được truyền đúng, các chức năng hoạt động xuyên suốt. | - Lập phiếu rút tiền thành công<br>- Truyền dữ liệu và lỗi giữa các lớp<br>- Kiểm thử các luồng chức năng chính |

> Xem thư mục `tests/` để biết chi tiết các trường hợp kiểm thử.

---

## Triển khai phần mềm

Ứng dụng được đóng gói dưới dạng Docker image và có thể chạy trên mọi hệ điều hành có hỗ trợ Docker.

👉 **Image Docker**  
Docker Hub: `datnham0212/quanly-tietkiem`

### ⚙️ Các bước triển khai

1. **Cài đặt Docker trên máy (Windows, macOS hoặc Linux):**  
   https://www.docker.com/products/docker-desktop

2. **Tải image từ Docker Hub:**
   ```bash
   docker pull datnham0212/quanly-tietkiem

3. **Chạy ứng dụng:**
    ```bash
    docker run datnham0212/quanly-tietkiem

🔺 Lưu ý: Ứng dụng có giao diện đồ họa (GUI), vì vậy cần thiết lập display phù hợp nếu chạy trong môi trường Docker. Khuyến nghị chạy trực tiếp trên máy thật trong quá trình phát triển hoặc thử nghiệm.  
Hoặc sử dụng VcXsrv (có hướng dẫn ở file `schedule.md`) để thiết lập display.
---

## Báo cáo PPT

- [File powerpoint](https://www.canva.com/design/DAGlWQ2M9Nk/Nm8XIsh8G7Ly1WQIuSuVBg/edit?utm_content=DAGlWQ2M9Nk&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)

---


