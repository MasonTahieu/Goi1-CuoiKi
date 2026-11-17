# Kiểm chứng phương pháp daily-v2

Rổ VN30; 22 phiên từ 2026-10-19 đến 2026-11-17; 21 cặp liền phiên được xét, 0 khoảng trống bị bỏ.

Khối ngoại theo **volume**, cân bằng (mua − bán)/(mua + bán).
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
| balanced | 21 | +0,031 | 0,242 | 21 | +0,004 |
| momentum | 21 | +0,040 | 0,236 | 21 | +0,073 |

## Độ nhạy danh sách theo dõi

Jaccard = số mã giao / số mã hợp (0–1). Bỏ yếu tố và đổi trọng số giữ nguyên tập mã hợp lệ.
Che một đầu vào bắt buộc cho từng mã rồi chấm lại nhóm còn lại; đây là tình huống thử, không phải lỗi dữ liệu thực tế. Kết quả chi tiết có cả so sánh Top trên các mã chung để tách ảnh hưởng loại mã và đổi phân vị.

| Cấu hình | Loại | Biến thể | Số tình huống | Jaccard TB | Jaccard nhỏ nhất | Số tình huống đổi Top | Mã ra TB | Mã vào TB |
|---|---|---|---:|---:|---:|---:|---:|---:|
| balanced | ablation | foreign | 22 | 0,597 | 0,250 | 21 | 1,273 | 1,500 |
| balanced | ablation | liquidity | 22 | 0,546 | 0,111 | 21 | 1,545 | 1,682 |
| balanced | ablation | momentum | 22 | 0,535 | 0,250 | 21 | 1,636 | 1,682 |
| balanced | missing | one_missing_member | 651 | 0,928 | 0,444 | 159 | 0,203 | 0,249 |
| balanced | single_factor | foreign | 22 | 0,364 | 0,111 | 22 | 2,545 | 2,409 |
| balanced | single_factor | liquidity | 22 | 0,310 | 0,111 | 22 | 2,864 | 2,727 |
| balanced | single_factor | momentum | 22 | 0,409 | 0,111 | 22 | 2,273 | 2,136 |
| balanced | weights | foreign+0.1 | 22 | 0,896 | 0,667 | 8 | 0,364 | 0,273 |
| balanced | weights | foreign-0.1 | 22 | 0,896 | 0,667 | 8 | 0,364 | 0,273 |
| balanced | weights | liquidity+0.1 | 22 | 0,908 | 0,429 | 6 | 0,364 | 0,227 |
| balanced | weights | liquidity-0.1 | 22 | 0,835 | 0,667 | 12 | 0,545 | 0,455 |
| balanced | weights | momentum | 22 | 0,758 | 0,429 | 16 | 0,727 | 0,818 |
| balanced | weights | momentum+0.1 | 22 | 0,926 | 0,667 | 6 | 0,273 | 0,182 |
| balanced | weights | momentum-0.1 | 22 | 0,826 | 0,333 | 11 | 0,636 | 0,500 |
| momentum | ablation | foreign | 22 | 0,643 | 0,333 | 20 | 1,227 | 1,182 |
| momentum | ablation | liquidity | 22 | 0,673 | 0,222 | 18 | 1,182 | 1,091 |
| momentum | ablation | momentum | 22 | 0,414 | 0,222 | 22 | 2,227 | 2,182 |
| momentum | missing | one_missing_member | 651 | 0,927 | 0,571 | 186 | 0,244 | 0,207 |
| momentum | single_factor | foreign | 22 | 0,367 | 0,100 | 22 | 2,591 | 2,364 |
| momentum | single_factor | liquidity | 22 | 0,276 | 0,111 | 22 | 3,091 | 2,864 |
| momentum | single_factor | momentum | 22 | 0,513 | 0,250 | 22 | 1,818 | 1,591 |
| momentum | weights | balanced | 22 | 0,758 | 0,429 | 16 | 0,818 | 0,727 |
| momentum | weights | foreign+0.1 | 22 | 0,920 | 0,571 | 7 | 0,364 | 0,136 |
| momentum | weights | foreign-0.1 | 22 | 0,852 | 0,571 | 12 | 0,545 | 0,364 |
| momentum | weights | liquidity+0.1 | 22 | 0,844 | 0,571 | 12 | 0,591 | 0,364 |
| momentum | weights | liquidity-0.1 | 22 | 0,835 | 0,571 | 12 | 0,591 | 0,455 |
| momentum | weights | momentum+0.1 | 22 | 0,905 | 0,571 | 8 | 0,409 | 0,182 |
| momentum | weights | momentum-0.1 | 22 | 0,894 | 0,667 | 10 | 0,409 | 0,227 |

## Diễn giải

- balanced: Mô tả 21 cặp phiên: IC trung bình +0,031. Kết quả chưa xác lập khả năng dự báo hay hiệu quả đầu tư. Điểm giúp ưu tiên danh sách theo dõi; độ ổn định của danh sách không chứng minh lợi nhuận.
- momentum: Mô tả 21 cặp phiên: IC trung bình +0,040. Kết quả chưa xác lập khả năng dự báo hay hiệu quả đầu tư. Điểm giúp ưu tiên danh sách theo dõi; độ ổn định của danh sách không chứng minh lợi nhuận.
- **Điều chỉnh quyền:** `refPrice` trống ở mọi dòng. Có 2/630 dòng `priceChangePercent` lệch quá 0,3 điểm % so với đóng cửa/đóng cửa (GVR 2026-10-21, VNM 2026-10-22). Cần đối chiếu với lịch giao dịch không hưởng quyền.

Thay đổi công thức là phiên bản phương pháp mới; các kết quả daily-v1 không được dùng để chứng minh daily-v2.
Dữ liệu, cấu hình, danh sách Top/Bottom, các ca thiếu và toàn bộ phép so sánh nằm trong evaluation.json.
