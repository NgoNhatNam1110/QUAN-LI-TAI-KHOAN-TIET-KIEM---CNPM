# QUẢN LÝ TÀI KHOẢN TIẾT KIỆM

## Giới thiệu

Dự án **Quản Lý Tài Khoản Tiết Kiệm** nhằm xây dựng một hệ thống phần mềm hỗ trợ quản lý các tài khoản tiết kiệm tại ngân hàng. Ứng dụng cho phép tạo mới, chỉnh sửa, xóa và tra cứu thông tin tài khoản tiết kiệm, quản lý giao dịch gửi/rút tiền, tính lãi suất, và xuất báo cáo thống kê. Hệ thống hướng tới việc đơn giản hóa quy trình quản lý, nâng cao hiệu quả và độ chính xác cho nhân viên ngân hàng.

---

## Quy trình làm việc nhóm

- **Khi commit, hãy thông báo cho cả nhóm.**
- **Luôn cập nhật code mới nhất trước khi làm việc:**
  ```bash
  git fetch origin
  git rebase origin/main
  git pull
  ```

---

## Các bài lab

- [Tổng hợp các bài lab](https://drive.google.com/drive/folders/1kXrWVUvHAVzwAi-PhuXUS5f_ch7qbP1H?usp=sharing)

---

## Yêu cầu

- Python 3.x
- Các thư viện trong `requirements.txt`

---

## Cài đặt thư viện Python

Chạy lệnh sau trong terminal:
```bash
pip install -r requirements.txt
```

---

## Kiểm thử phần mềm

Hệ thống đã được kiểm thử tự động với các loại kiểm thử sau:

- **Unit Test:**  
  Kiểm thử từng lớp riêng biệt (DAL, BUS, GUI) với các trường hợp thành công, thất bại, ngoại lệ, dữ liệu biên và dữ liệu không hợp lệ.

- **Integration Test:**  
  Kiểm thử luồng tích hợp giữa các lớp (GUI ↔ BUS ↔ DAL), đảm bảo dữ liệu và lỗi được truyền đúng, các chức năng hoạt động xuyên suốt.

- **Các trường hợp kiểm thử chính:**  
  - Lập phiếu rút tiền thành công.
  - Thiếu trường thông tin, nhập sai định dạng, số tiền rút vượt quá số dư, hoặc nhỏ hơn mức tối thiểu.
  - Kiểm tra lấy thông tin khách hàng, số dư, danh sách kỳ hạn.
  - Kiểm thử các hàm phụ trợ và xử lý ngoại lệ.

> Xem thư mục `tests/` để biết chi tiết các trường hợp kiểm thử.

---

## Hướng dẫn chạy ứng dụng bằng Docker

### **Trên Windows**

#### 1. Cài đặt Docker Desktop và VcXsrv

- Tải và cài đặt [Docker Desktop](https://www.docker.com/products/docker-desktop/) cho Windows.
- Tải và cài đặt [VcXsrv](https://sourceforge.net/projects/vcxsrv/) để hiển thị giao diện đồ họa từ container.

#### 2. Khởi động VcXsrv

- Mở VcXsrv, chọn "Multiple windows", nhấn Next cho gần đến khi hoàn tất, và **bật tùy chọn "Disable access control"**.

#### 3. Xác định địa chỉ IP của máy tính Windows

- Mở Command Prompt hoặc PowerShell, chạy:
  ```powershell
  ipconfig
  ```
- Ghi lại địa chỉ IPv4 (ví dụ: `192.168.1.100`).

#### 4. Build và chạy Docker container

- Mở terminal tại thư mục dự án, chạy:
  ```bash
  docker build -t quanly-tietkiem .
  docker run -e DISPLAY=<ĐỊA_CHỈ_IP_CỦA_BẠN>:0.0 quanly-tietkiem
  ```
  Thay `<ĐỊA_CHỈ_IP_CỦA_BẠN>` bằng địa chỉ IP vừa tìm được ở bước trên.

#### 5. Ứng dụng sẽ hiển thị giao diện trên màn hình Windows của bạn.

---

### **Trên Linux**

#### 1. Cài đặt Docker

- Cài đặt Docker theo hướng dẫn chính thức: [https://docs.docker.com/engine/install/](https://docs.docker.com/engine/install/)

#### 2. Cho phép container truy cập X11

- Chạy lệnh sau để cho phép Docker truy cập vào X11:
  ```bash
  xhost +
  ```

#### 3. Build và chạy Docker container

- Mở terminal tại thư mục dự án, chạy:
  ```bash
  docker build -t quanly-tietkiem .
  docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix quanly-tietkiem
  ```

#### 4. Ứng dụng sẽ hiển thị giao diện trên màn hình Linux của bạn.

---

### **Trên macOS**

> **Lưu ý:** macOS không hỗ trợ X11 trực tiếp. Bạn cần cài đặt một X11 server như [XQuartz](https://www.xquartz.org/).

#### 1. Cài đặt Docker Desktop và XQuartz

- Tải và cài đặt [Docker Desktop](https://www.docker.com/products/docker-desktop/) cho macOS.
- Tải và cài đặt [XQuartz](https://www.xquartz.org/).

#### 2. Khởi động XQuartz

- Mở XQuartz, vào menu `Preferences > Security`, bật tùy chọn **"Allow connections from network clients"**.
- Khởi động lại XQuartz.
- Mở terminal mới và chạy:
  ```bash
  xhost +
  ```

#### 3. Xác định địa chỉ IP của máy

- Chạy lệnh sau để lấy địa chỉ IP:
  ```bash
  ipconfig getifaddr en0
  ```
  (hoặc thử `en1` nếu không có kết quả)

#### 4. Build và chạy Docker container

- Mở terminal tại thư mục dự án, chạy:
  ```bash
  docker build -t quanly-tietkiem .
  docker run -e DISPLAY=<ĐỊA_CHỈ_IP_CỦA_BẠN>:0 quanly-tietkiem
  ```
  Thay `<ĐỊA_CHỈ_IP_CỦA_BẠN>` bằng địa chỉ IP vừa tìm được ở bước trên.

#### 5. Ứng dụng sẽ hiển thị giao diện trên màn hình macOS của bạn thông qua XQuartz.

---

## Báo cáo PPT

- [File powerpoint](https://www.canva.com/design/DAGlWQ2M9Nk/Nm8XIsh8G7Ly1WQIuSuVBg/edit?utm_content=DAGlWQ2M9Nk&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)

---

