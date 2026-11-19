# Kiểm chứng phương pháp daily-v2

Rổ VN30; 24 phiên từ 2026-10-19 đến 2026-11-19; 23 cặp liền phiên được xét, 0 khoảng trống bị bỏ.

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
| balanced | 23 | +0,022 | 0,238 | 23 | −0,092 |
| momentum | 23 | +0,039 | 0,225 | 23 | +0,096 |

## Độ nhạy danh sách theo dõi

Jaccard = số mã giao / số mã hợp (0–1). Bỏ yếu tố và đổi trọng số giữ nguyên tập mã hợp lệ.
Che một đầu vào bắt buộc cho từng mã rồi chấm lại nhóm còn lại; đây là tình huống thử, không phải lỗi dữ liệu thực tế. Kết quả chi tiết có cả so sánh Top trên các mã chung để tách ảnh hưởng loại mã và đổi phân vị.

| Cấu hình | Loại | Biến thể | Số tình huống | Jaccard TB | Jaccard nhỏ nhất | Số tình huống đổi Top | Mã ra TB | Mã vào TB |
|---|---|---|---:|---:|---:|---:|---:|---:|
| balanced | ablation | foreign | 24 | 0,548 | 0,000 | 23 | 1,583 | 1,875 |
| balanced | ablation | liquidity | 24 | 0,546 | 0,100 | 23 | 1,583 | 1,667 |
| balanced | ablation | momentum | 24 | 0,522 | 0,250 | 23 | 1,708 | 1,750 |
| balanced | missing | one_missing_member | 710 | 0,926 | 0,444 | 189 | 0,218 | 0,246 |
| balanced | single_factor | foreign | 24 | 0,398 | 0,111 | 23 | 2,417 | 2,250 |
| balanced | single_factor | liquidity | 24 | 0,291 | 0,000 | 24 | 3,000 | 2,833 |
| balanced | single_factor | momentum | 24 | 0,395 | 0,111 | 24 | 2,333 | 2,292 |
| balanced | weights | foreign+0.1 | 24 | 0,912 | 0,667 | 8 | 0,333 | 0,208 |
| balanced | weights | foreign-0.1 | 24 | 0,870 | 0,667 | 11 | 0,458 | 0,333 |
| balanced | weights | liquidity+0.1 | 24 | 0,867 | 0,429 | 10 | 0,500 | 0,333 |
| balanced | weights | liquidity-0.1 | 24 | 0,842 | 0,667 | 13 | 0,542 | 0,417 |
| balanced | weights | momentum | 24 | 0,731 | 0,375 | 19 | 0,833 | 0,917 |
| balanced | weights | momentum+0.1 | 24 | 0,912 | 0,667 | 8 | 0,333 | 0,208 |
| balanced | weights | momentum-0.1 | 24 | 0,819 | 0,333 | 13 | 0,667 | 0,500 |
| momentum | ablation | foreign | 24 | 0,618 | 0,250 | 22 | 1,333 | 1,333 |
| momentum | ablation | liquidity | 24 | 0,669 | 0,222 | 20 | 1,208 | 1,083 |
| momentum | ablation | momentum | 24 | 0,389 | 0,000 | 24 | 2,417 | 2,375 |
| momentum | missing | one_missing_member | 710 | 0,925 | 0,571 | 213 | 0,256 | 0,207 |
| momentum | single_factor | foreign | 24 | 0,362 | 0,100 | 24 | 2,625 | 2,375 |
| momentum | single_factor | liquidity | 24 | 0,271 | 0,000 | 24 | 3,167 | 2,917 |
| momentum | single_factor | momentum | 24 | 0,506 | 0,250 | 24 | 1,833 | 1,708 |
| momentum | weights | balanced | 24 | 0,731 | 0,375 | 19 | 0,917 | 0,833 |
| momentum | weights | foreign+0.1 | 24 | 0,892 | 0,571 | 10 | 0,458 | 0,208 |
| momentum | weights | foreign-0.1 | 24 | 0,833 | 0,429 | 14 | 0,625 | 0,417 |
| momentum | weights | liquidity+0.1 | 24 | 0,850 | 0,571 | 13 | 0,583 | 0,333 |
| momentum | weights | liquidity-0.1 | 24 | 0,821 | 0,571 | 14 | 0,667 | 0,458 |
| momentum | weights | momentum+0.1 | 24 | 0,892 | 0,571 | 10 | 0,458 | 0,208 |
| momentum | weights | momentum-0.1 | 24 | 0,889 | 0,667 | 12 | 0,417 | 0,250 |

## Diễn giải

- balanced: Mô tả 23 cặp phiên: IC trung bình +0,022. Kết quả chưa xác lập khả năng dự báo hay hiệu quả đầu tư. Điểm giúp ưu tiên danh sách theo dõi; độ ổn định của danh sách không chứng minh lợi nhuận.
- momentum: Mô tả 23 cặp phiên: IC trung bình +0,039. Kết quả chưa xác lập khả năng dự báo hay hiệu quả đầu tư. Điểm giúp ưu tiên danh sách theo dõi; độ ổn định của danh sách không chứng minh lợi nhuận.
- **Điều chỉnh quyền:** `refPrice` trống ở mọi dòng. Có 2/690 dòng `priceChangePercent` lệch quá 0,3 điểm % so với đóng cửa/đóng cửa (GVR 2026-10-21, VNM 2026-10-22). Cần đối chiếu với lịch giao dịch không hưởng quyền.

Thay đổi công thức là phiên bản phương pháp mới; các kết quả daily-v1 không được dùng để chứng minh daily-v2.
Dữ liệu, cấu hình, danh sách Top/Bottom, các ca thiếu và toàn bộ phép so sánh nằm trong evaluation.json.
