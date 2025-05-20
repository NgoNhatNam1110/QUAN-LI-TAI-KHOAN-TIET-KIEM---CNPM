# 📅 Lịch trình dự án & Quy trình làm việc nhóm

## 📄 Tài liệu dự án
- [Đề xuất dự án](https://docs.google.com/document/d/153xh0cEmbYlkVlcoY1W4nTPBzntlDcRmDmL-hXv4CYE/edit?usp=sharing)
- [Kế hoạch dự án](https://docs.google.com/document/d/1MdLO3yEn-LvBMJ8tdqb9geIdqbVyi-BI8f3mQRcgHt8/edit?usp=sharing)

---

## 👥 Quy trình làm việc nhóm

- **Thông báo cho cả nhóm khi bạn commit.**
- **Luôn cập nhật code mới nhất trước khi làm việc:**

```bash
# Lấy và rebase về nhánh main mới nhất
$ git fetch origin
$ git rebase origin/main
$ git pull
```

---

## 📝 Bài tập Lab

- [Tổng hợp các bài Lab](https://drive.google.com/drive/folders/1kXrWVUvHAVzwAi-PhuXUS5f_ch7qbP1H?usp=sharing)

---

## ⚙️ Yêu cầu phần mềm

- Python 3.x
- Tất cả thư viện trong `requirements.txt`

---

## 📦 Cài đặt thư viện Python

Chạy lệnh sau trong terminal:

```bash
pip install -r requirements.txt
```

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
