# Kiểm chứng phương pháp daily-v2

Rổ VN30; 29 phiên từ 2026-10-19 đến 2026-11-27; 27 cặp liền phiên được xét, 1 khoảng trống bị bỏ.

Khối ngoại theo **value**, cân bằng (mua − bán)/(mua + bán).
Dữ liệu được phân tích hồi cứu theo danh sách thành viên lúc thu thập; chưa phải kiểm thử đầu tư theo thông tin sẵn có trong quá khứ.
Nguồn và mã SHA-256 của dữ liệu đầu vào: manifest.json. Dữ liệu giữ cả thời gian thu thập khi có.

## Quy tắc đánh giá

- Top 5 gồm mọi mã đồng điểm tại ranh giới thứ 5; Bottom 5 tương tự. Không dùng thứ tự chữ cái để phá hòa.
- Chốt danh sách từ ngày t trước khi ghép lợi suất ngày sau. Thiếu lợi suất của thành viên: không tính chênh lệch Top–Bottom, không thay mã.
- Nếu hai nhóm giao nhau do đồng điểm: không tính chênh lệch. IC dùng các mã đủ lợi suất, báo số mã và mã bị thiếu trong tệp chi tiết.
- IC từng yếu tố và điểm tổng hợp dùng cùng tập mã. Không tính t, ngưỡng ý nghĩa hay số phiên đủ để phát hiện hiệu ứng.
- Chỉ nối hai ngày liền phiên theo lịch cung cấp, hoặc liền ngày làm việc khi chưa có lịch sở giao dịch; khoảng nghỉ chưa xác nhận bị bỏ.

## Lợi suất mở cửa–đóng cửa phiên kế tiếp

Chỉ là phép mô tả bổ sung; chưa mô phỏng khớp lệnh, chu kỳ thanh toán, chi phí hay khả năng giao dịch thực tế.

| Cấu hình | Cặp có IC | IC trung bình | Độ lệch chuẩn IC | Cặp có chênh lệch | Top–Bottom (điểm %) |
|---|---:|---:|---:|---:|---:|
| balanced | 27 | +0,004 | 0,226 | 27 | −0,085 |
| momentum | 27 | +0,008 | 0,228 | 27 | +0,040 |

## Độ nhạy danh sách theo dõi

Jaccard = số mã giao / số mã hợp (0–1). Bỏ yếu tố và đổi trọng số giữ nguyên tập mã hợp lệ.
Che một đầu vào bắt buộc cho từng mã rồi chấm lại nhóm còn lại; đây là tình huống thử, không phải lỗi dữ liệu thực tế. Kết quả chi tiết có cả so sánh Top trên các mã chung để tách ảnh hưởng loại mã và đổi phân vị.

| Cấu hình | Loại | Biến thể | Số tình huống | Jaccard TB | Jaccard nhỏ nhất | Số tình huống đổi Top | Mã ra TB | Mã vào TB |
|---|---|---|---:|---:|---:|---:|---:|---:|
| balanced | ablation | foreign | 29 | 0,541 | 0,000 | 28 | 1,621 | 1,897 |
| balanced | ablation | liquidity | 29 | 0,537 | 0,100 | 28 | 1,655 | 1,655 |
| balanced | ablation | momentum | 29 | 0,532 | 0,250 | 28 | 1,655 | 1,724 |
| balanced | missing | one_missing_member | 855 | 0,925 | 0,444 | 239 | 0,228 | 0,240 |
| balanced | single_factor | foreign | 29 | 0,382 | 0,111 | 28 | 2,517 | 2,310 |
| balanced | single_factor | liquidity | 29 | 0,276 | 0,000 | 29 | 3,138 | 2,931 |
| balanced | single_factor | momentum | 29 | 0,400 | 0,111 | 29 | 2,345 | 2,241 |
| balanced | weights | foreign+0.1 | 29 | 0,915 | 0,667 | 10 | 0,345 | 0,172 |
| balanced | weights | foreign-0.1 | 29 | 0,861 | 0,429 | 14 | 0,517 | 0,345 |
| balanced | weights | liquidity+0.1 | 29 | 0,856 | 0,429 | 14 | 0,552 | 0,345 |
| balanced | weights | liquidity-0.1 | 29 | 0,831 | 0,667 | 17 | 0,586 | 0,448 |
| balanced | weights | momentum | 29 | 0,734 | 0,375 | 23 | 0,862 | 0,862 |
| balanced | weights | momentum+0.1 | 29 | 0,892 | 0,667 | 12 | 0,414 | 0,241 |
| balanced | weights | momentum-0.1 | 29 | 0,828 | 0,333 | 16 | 0,655 | 0,448 |
| momentum | ablation | foreign | 29 | 0,632 | 0,250 | 27 | 1,241 | 1,276 |
| momentum | ablation | liquidity | 29 | 0,652 | 0,222 | 25 | 1,241 | 1,138 |
| momentum | ablation | momentum | 29 | 0,395 | 0,000 | 29 | 2,345 | 2,414 |
| momentum | missing | one_missing_member | 855 | 0,922 | 0,571 | 264 | 0,242 | 0,236 |
| momentum | single_factor | foreign | 29 | 0,355 | 0,100 | 29 | 2,621 | 2,414 |
| momentum | single_factor | liquidity | 29 | 0,250 | 0,000 | 29 | 3,276 | 3,069 |
| momentum | single_factor | momentum | 29 | 0,520 | 0,250 | 29 | 1,759 | 1,655 |
| momentum | weights | balanced | 29 | 0,734 | 0,375 | 23 | 0,862 | 0,862 |
| momentum | weights | foreign+0.1 | 29 | 0,876 | 0,571 | 13 | 0,483 | 0,276 |
| momentum | weights | foreign-0.1 | 29 | 0,851 | 0,429 | 15 | 0,552 | 0,379 |
| momentum | weights | liquidity+0.1 | 29 | 0,865 | 0,571 | 14 | 0,517 | 0,310 |
| momentum | weights | liquidity-0.1 | 29 | 0,798 | 0,429 | 18 | 0,724 | 0,552 |
| momentum | weights | momentum+0.1 | 29 | 0,888 | 0,571 | 12 | 0,448 | 0,241 |
| momentum | weights | momentum-0.1 | 29 | 0,897 | 0,667 | 13 | 0,379 | 0,241 |

## Diễn giải

- balanced: Mô tả 27 cặp phiên: IC trung bình +0,004. Kết quả chưa xác lập khả năng dự báo hay hiệu quả đầu tư. Điểm giúp ưu tiên danh sách theo dõi; độ ổn định của danh sách không chứng minh lợi nhuận.
- momentum: Mô tả 27 cặp phiên: IC trung bình +0,008. Kết quả chưa xác lập khả năng dự báo hay hiệu quả đầu tư. Điểm giúp ưu tiên danh sách theo dõi; độ ổn định của danh sách không chứng minh lợi nhuận.
- **Điều chỉnh quyền:** `refPrice` trống ở mọi dòng. Có 3/840 dòng `priceChangePercent` lệch quá 0,3 điểm % so với đóng cửa/đóng cửa (FPT 2026-11-06, GVR 2026-10-21, VNM 2026-10-22). Cần đối chiếu với lịch giao dịch không hưởng quyền.

Thay đổi công thức là phiên bản phương pháp mới; các kết quả daily-v1 không được dùng để chứng minh daily-v2.
Dữ liệu, cấu hình, danh sách Top/Bottom, các ca thiếu và toàn bộ phép so sánh nằm trong evaluation.json.
