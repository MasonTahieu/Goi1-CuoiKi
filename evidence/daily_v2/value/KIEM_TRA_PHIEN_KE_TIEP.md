# Kiểm chứng phương pháp daily-v2

Rổ VN30; 21 phiên từ 2026-10-19 đến 2026-11-16; 20 cặp liền phiên được xét, 0 khoảng trống bị bỏ.

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
| balanced | 20 | +0,028 | 0,248 | 20 | +0,024 |
| momentum | 20 | +0,039 | 0,241 | 20 | +0,068 |

## Độ nhạy danh sách theo dõi

Jaccard = số mã giao / số mã hợp (0–1). Bỏ yếu tố và đổi trọng số giữ nguyên tập mã hợp lệ.
Che một đầu vào bắt buộc cho từng mã rồi chấm lại nhóm còn lại; đây là tình huống thử, không phải lỗi dữ liệu thực tế. Kết quả chi tiết có cả so sánh Top trên các mã chung để tách ảnh hưởng loại mã và đổi phân vị.

| Cấu hình | Loại | Biến thể | Số tình huống | Jaccard TB | Jaccard nhỏ nhất | Số tình huống đổi Top | Mã ra TB | Mã vào TB |
|---|---|---|---:|---:|---:|---:|---:|---:|
| balanced | ablation | foreign | 21 | 0,589 | 0,250 | 20 | 1,333 | 1,524 |
| balanced | ablation | liquidity | 21 | 0,551 | 0,100 | 20 | 1,571 | 1,667 |
| balanced | ablation | momentum | 21 | 0,535 | 0,250 | 20 | 1,667 | 1,667 |
| balanced | missing | one_missing_member | 622 | 0,925 | 0,444 | 168 | 0,225 | 0,246 |
| balanced | single_factor | foreign | 21 | 0,374 | 0,111 | 21 | 2,524 | 2,333 |
| balanced | single_factor | liquidity | 21 | 0,300 | 0,111 | 21 | 2,952 | 2,762 |
| balanced | single_factor | momentum | 21 | 0,420 | 0,111 | 21 | 2,238 | 2,048 |
| balanced | weights | foreign+0.1 | 21 | 0,907 | 0,667 | 7 | 0,381 | 0,190 |
| balanced | weights | foreign-0.1 | 21 | 0,883 | 0,667 | 9 | 0,429 | 0,286 |
| balanced | weights | liquidity+0.1 | 21 | 0,880 | 0,429 | 8 | 0,476 | 0,286 |
| balanced | weights | liquidity-0.1 | 21 | 0,851 | 0,667 | 11 | 0,524 | 0,381 |
| balanced | weights | momentum | 21 | 0,765 | 0,429 | 16 | 0,714 | 0,762 |
| balanced | weights | momentum+0.1 | 21 | 0,915 | 0,667 | 7 | 0,333 | 0,190 |
| balanced | weights | momentum-0.1 | 21 | 0,825 | 0,333 | 11 | 0,667 | 0,476 |
| momentum | ablation | foreign | 21 | 0,650 | 0,333 | 19 | 1,238 | 1,095 |
| momentum | ablation | liquidity | 21 | 0,673 | 0,222 | 17 | 1,190 | 1,095 |
| momentum | ablation | momentum | 21 | 0,422 | 0,222 | 21 | 2,190 | 2,143 |
| momentum | missing | one_missing_member | 622 | 0,927 | 0,571 | 180 | 0,248 | 0,204 |
| momentum | single_factor | foreign | 21 | 0,373 | 0,100 | 21 | 2,571 | 2,333 |
| momentum | single_factor | liquidity | 21 | 0,277 | 0,111 | 21 | 3,095 | 2,857 |
| momentum | single_factor | momentum | 21 | 0,517 | 0,250 | 21 | 1,810 | 1,571 |
| momentum | weights | balanced | 21 | 0,765 | 0,429 | 16 | 0,762 | 0,714 |
| momentum | weights | foreign+0.1 | 21 | 0,900 | 0,571 | 8 | 0,429 | 0,190 |
| momentum | weights | foreign-0.1 | 21 | 0,845 | 0,571 | 12 | 0,571 | 0,381 |
| momentum | weights | liquidity+0.1 | 21 | 0,853 | 0,571 | 11 | 0,571 | 0,333 |
| momentum | weights | liquidity-0.1 | 21 | 0,820 | 0,571 | 12 | 0,667 | 0,476 |
| momentum | weights | momentum+0.1 | 21 | 0,900 | 0,571 | 8 | 0,429 | 0,190 |
| momentum | weights | momentum-0.1 | 21 | 0,905 | 0,667 | 9 | 0,381 | 0,190 |

## Diễn giải

- balanced: Mô tả 20 cặp phiên: IC trung bình +0,028. Kết quả chưa xác lập khả năng dự báo hay hiệu quả đầu tư. Điểm giúp ưu tiên danh sách theo dõi; độ ổn định của danh sách không chứng minh lợi nhuận.
- momentum: Mô tả 20 cặp phiên: IC trung bình +0,039. Kết quả chưa xác lập khả năng dự báo hay hiệu quả đầu tư. Điểm giúp ưu tiên danh sách theo dõi; độ ổn định của danh sách không chứng minh lợi nhuận.
- **Điều chỉnh quyền:** `refPrice` trống ở mọi dòng. Có 2/600 dòng `priceChangePercent` lệch quá 0,3 điểm % so với đóng cửa/đóng cửa (GVR 2026-10-21, VNM 2026-10-22). Cần đối chiếu với lịch giao dịch không hưởng quyền.

Thay đổi công thức là phiên bản phương pháp mới; các kết quả daily-v1 không được dùng để chứng minh daily-v2.
Dữ liệu, cấu hình, danh sách Top/Bottom, các ca thiếu và toàn bộ phép so sánh nằm trong evaluation.json.
