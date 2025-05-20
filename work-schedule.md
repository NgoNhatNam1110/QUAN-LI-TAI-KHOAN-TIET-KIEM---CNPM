## 📅 Lịch Sử Phát Triển Dự Án & Quy trình làm việc nhóm

## 📌 Thành viên nhóm
- Nhâm Minh Đạt - 3121411052
- Ngô Nhật Nam - 3121411136
- Nguyễn Chí Tân - 3121411192
- Nguyễn Tuấn Long - 3121411125

---

## 🚧 Giai đoạn 1: Mô hình Waterfall (Lập kế hoạch & Xây dựng ban đầu)

### Thời gian
- **Tuần 1–6**: Thu thập yêu cầu, lập kế hoạch, thiết kế hệ thống và triển khai ban đầu

### Hoạt động chính
- Mỗi thành viên tạo một nhánh riêng để phát triển phần việc của mình:
  - `branch/datnham0212`
  - `branch/ngonhatnam1110`
  - `branch/tannguyen180303`
  - `branch/AerieL114`
- Gộp vào `main` sau khi hoàn thành các mốc lớn 
- Ít lặp lại; tập trung vào lập kế hoạch trước

### Các commit nổi bật
- `Add requirements document` (Thêm tài liệu yêu cầu)
- `Design system architecture` (Thiết kế kiến trúc hệ thống)
- `Implement prototype features` (Triển khai các tính năng mẫu)

---

## 🔁 Giai đoạn 2: Chuyển sang Agile (Phát triển lặp)

### Thời gian
- **Tuần 7–14**: Phát triển theo sprint, lặp lại

### Hoạt động chính
- Tiếp tục sử dụng các nhánh riêng biệt cho từng thành viên
- Sử dụng các tab Issues & Insight để theo dõi công việc và tiến độ
- Gộp các tính năng qua pull request
- Sprint hàng tuần và họp tổng kết nhỏ

### Đóng góp nổi bật
- Commit thường xuyên, chu kỳ merge nhanh
- Cải tiến dần dần (ví dụ: hiệu năng, giao diện, sửa lỗi)

---

## 📈 Tổng kết đóng góp tới nhánh main GitHub

> Lưu ý: Trong quá trình phát triển, có những thời điểm một số thành viên do lý do kỹ thuật hoặc cá nhân không thể chủ động commit lên repository. Khi đó, nhóm trưởng sẽ hỗ trợ commit thay để đảm bảo tiến độ chung của dự án.
> Bảng dưới đây thể hiện số commit thực tế của từng thành viên:

| Thành viên         | Số commit | Tính năng đã thêm                                                                 | Công việc nổi bật                |
|--------------------|-----------|----------------------------------------------------------------------------------|----------------------------------|
| Nhâm Minh Đạt      | 108       | Đăng nhập, tạo Database, viết trigger cho Database                                | Merge nhánh của các thành viên vào main, Unit Testing, Integration Testing & Deployment bằng Docker |
| Ngô Nhật Nam       | 57        | Mở hồ sơ, gửi tiền, rút tiền, lập báo cáo                        | Sửa lỗi nhanh, cải thiện giao diện |
| Nguyễn Chí Tân     | 20        | Thay đổi thông số, quy định hệ thống sổ                                          | Hỗ trợ tính năng gửi tiền, rút tiền, System Testing              |
| Nguyễn Tuấn Long   | 17        | Kiểm tra tính hợp lệ dữ liệu nhập vào của mở sổ, gửi tiền, rút tiền & thay đổi thông số                               | Tổng hợp bài viết báo cáo & soạn powerpoint |

---

## 🧭 Tag & Mốc phát hành

- `v0.1` (2025-03-20): Kết thúc giai đoạn Waterfall, hoàn thành prototype và tài liệu yêu cầu
- `v0.5` (2025-04-20): Hoàn thiện các chức năng chính, bắt đầu kiểm thử tích hợp
- `v1.0` (2025-05-20): Ra mắt MVP sau các sprint Agile, hoàn thiện kiểm thử, deploy lên Docker và ghi tài liệu báo cáo
