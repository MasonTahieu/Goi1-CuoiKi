# Checklist phương pháp cuối ngày — 15/11/2026

Phạm vi: bộ lọc/xếp hạng VN30 cuối ngày ba yếu tố, hỗ trợ ưu tiên danh sách theo dõi. Phiên bản `daily-v2`; không xác nhận mô hình bốn yếu tố trong phiên.

- [x] Chốt công thức cân bằng mua–bán ngoại, cùng phạm vi và cùng đơn vị ở tử/mẫu.
- [x] Phân biệt không giao dịch với thiếu dữ liệu; loại số âm, boolean và số không hữu hạn.
- [x] Hiển thị mua, bán, mua ròng bên cạnh tỷ lệ; xuất các số này trong CSV.
- [x] Bảng hạng và tab Kiểm chứng dùng đúng trọng số, chế độ giá trị/khối lượng.
- [x] Top/Bottom bao gồm mọi mã đồng điểm ở ranh giới; không dùng thứ tự chữ cái để chọn thành viên.
- [x] Chốt danh sách trước khi ghép lợi suất tương lai; không thay mã thiếu giá, không đo chênh lệch khi hai nhóm giao nhau.
- [x] Không nối qua phiên thiếu; lịch mặc định bảo thủ, có lựa chọn cung cấp lịch phiên đã đối chiếu qua CLI.
- [x] Bổ sung so từng yếu tố, bỏ yếu tố trên cùng tập mã, đổi trọng số định trước và thử thiếu từng mã.
- [x] Bỏ kết luận theo ngưỡng t và ước lượng số phiên cần để phát hiện IC.
- [x] Công bố số cặp, số mã đủ lợi suất, mã thiếu và lý do bỏ; IC từng yếu tố dùng cùng tập mã với điểm tổng hợp.
- [x] Lưu dữ liệu đầu vào, dấu thời gian thu thập, cấu hình, thành viên theo ngày, mã SHA-256 và phiên bản thư viện/mã.
- [x] Cập nhật đặc tả phương pháp, README, HANDOFF; đánh dấu báo cáo daily-v1 là tài liệu lưu trữ.
- [x] Chuẩn bị workflow xuất bằng chứng mới cho cả hai chế độ khi chạy lần sau.

## Kiểm tra đã thực hiện

- Toàn bộ bộ kiểm thử: **361 passed**. Sau điều chỉnh cuối về đầu vào lợi suất và kiểm tra tham số HTTP, chạy lại nhóm liên quan: **29 passed**.
- Kiểm tra cú pháp JavaScript: qua. `git diff --check`: không có lỗi khoảng trắng.
- Kiểm tra giao diện cục bộ: bảng hạng hiển thị tỷ lệ và mua/bán/ròng; tab Kiểm chứng hiển thị đúng chế độ giá trị và khối lượng với kết quả khác nhau.
- Chạy lại từ ảnh chụp đầu vào bằng CLI: **toàn bộ evaluation.json trùng khớp**, gồm mọi tình huống độ nhạy. SHA-256 đầu vào và mã tính của cả hai bộ bằng chứng đều khớp.

## Dữ liệu và kết quả hiện hành

600 dòng VN30, 20 phiên từ 19/10 đến 13/11/2026; dữ liệu đã thu từ SSI trước lượt sửa này, không gọi API để tạo kết quả mới. Có 19 cặp ngày được xét và 18 cặp tính được IC. Ngày 12/11 thiếu dữ liệu ngoại nên không xếp hạng.

| Cách tính ngoại | Trọng số | IC trung bình | Top–Bottom trung bình (điểm %) |
|---|---|---:|---:|
| Giá trị | Cân bằng | 0,009531 | −0,021089 |
| Giá trị | 50/25/25 | 0,020366 | 0,019893 |
| Khối lượng | Cân bằng | 0,009269 | −0,013624 |
| Khối lượng | 50/25/25 | 0,019813 | 0,019893 |

Đây là kết quả mô tả, chưa xác lập khả năng dự báo hay hiệu quả đầu tư. Không dùng số dòng mã–ngày làm số quan sát độc lập cho thống kê IC theo phiên.

- [Đặc tả phương pháp](../report/CO_SO_PHUONG_PHAP.md)
- [Bằng chứng giá trị](../evidence/daily_v2/value/KIEM_TRA_PHIEN_KE_TIEP.md)
- [Bằng chứng khối lượng](../evidence/daily_v2/volume/KIEM_TRA_PHIEN_KE_TIEP.md)

## Giới hạn và trạng thái triển khai

Lịch mặc định chưa là lịch ngày nghỉ đầy đủ của sở giao dịch: khoảng trống chưa xác nhận bị bỏ, không đoán. Thành viên lịch sử và các bản sửa dữ liệu trước thời điểm thu thập chưa được tái dựng. Đây là giới hạn công bố của phân tích hồi cứu, không phải bằng chứng đầu tư theo thông tin có sẵn trong quá khứ.

Đã sửa và kiểm tra trên máy. Chưa commit, push hoặc triển khai bản daily-v2 này lên Vercel. Các chỉnh sửa có sẵn trước lượt làm việc, gồm phần biểu đồ OHLC, được giữ lại. Bộ báo cáo/video nộp chưa được dựng lại trong lượt này.
