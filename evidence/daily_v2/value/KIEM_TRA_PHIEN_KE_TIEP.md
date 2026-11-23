# Kiểm chứng phương pháp daily-v2

Rổ VN30; 26 phiên từ 2026-10-19 đến 2026-11-23; 25 cặp liền phiên được xét, 0 khoảng trống bị bỏ.

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
| balanced | 25 | +0,015 | 0,230 | 25 | −0,070 |
| momentum | 25 | +0,022 | 0,225 | 25 | +0,082 |

## Độ nhạy danh sách theo dõi

Jaccard = số mã giao / số mã hợp (0–1). Bỏ yếu tố và đổi trọng số giữ nguyên tập mã hợp lệ.
Che một đầu vào bắt buộc cho từng mã rồi chấm lại nhóm còn lại; đây là tình huống thử, không phải lỗi dữ liệu thực tế. Kết quả chi tiết có cả so sánh Top trên các mã chung để tách ảnh hưởng loại mã và đổi phân vị.

| Cấu hình | Loại | Biến thể | Số tình huống | Jaccard TB | Jaccard nhỏ nhất | Số tình huống đổi Top | Mã ra TB | Mã vào TB |
|---|---|---|---:|---:|---:|---:|---:|---:|
| balanced | ablation | foreign | 26 | 0,548 | 0,000 | 25 | 1,577 | 1,846 |
| balanced | ablation | liquidity | 26 | 0,546 | 0,100 | 25 | 1,577 | 1,654 |
| balanced | ablation | momentum | 26 | 0,530 | 0,250 | 25 | 1,654 | 1,731 |
| balanced | missing | one_missing_member | 768 | 0,925 | 0,444 | 209 | 0,215 | 0,259 |
| balanced | single_factor | foreign | 26 | 0,393 | 0,111 | 25 | 2,423 | 2,269 |
| balanced | single_factor | liquidity | 26 | 0,289 | 0,000 | 26 | 3,000 | 2,846 |
| balanced | single_factor | momentum | 26 | 0,407 | 0,111 | 26 | 2,269 | 2,231 |
| balanced | weights | foreign+0.1 | 26 | 0,918 | 0,667 | 8 | 0,308 | 0,192 |
| balanced | weights | foreign-0.1 | 26 | 0,858 | 0,429 | 12 | 0,500 | 0,385 |
| balanced | weights | liquidity+0.1 | 26 | 0,864 | 0,429 | 11 | 0,500 | 0,346 |
| balanced | weights | liquidity-0.1 | 26 | 0,842 | 0,667 | 14 | 0,538 | 0,423 |
| balanced | weights | momentum | 26 | 0,739 | 0,375 | 20 | 0,808 | 0,885 |
| balanced | weights | momentum+0.1 | 26 | 0,906 | 0,667 | 9 | 0,346 | 0,231 |
| balanced | weights | momentum-0.1 | 26 | 0,821 | 0,333 | 14 | 0,654 | 0,500 |
| momentum | ablation | foreign | 26 | 0,628 | 0,250 | 24 | 1,269 | 1,308 |
| momentum | ablation | liquidity | 26 | 0,669 | 0,222 | 22 | 1,192 | 1,077 |
| momentum | ablation | momentum | 26 | 0,401 | 0,000 | 26 | 2,346 | 2,346 |
| momentum | missing | one_missing_member | 768 | 0,923 | 0,571 | 237 | 0,250 | 0,223 |
| momentum | single_factor | foreign | 26 | 0,354 | 0,100 | 26 | 2,654 | 2,423 |
| momentum | single_factor | liquidity | 26 | 0,271 | 0,000 | 26 | 3,154 | 2,923 |
| momentum | single_factor | momentum | 26 | 0,519 | 0,250 | 26 | 1,769 | 1,654 |
| momentum | weights | balanced | 26 | 0,739 | 0,375 | 20 | 0,885 | 0,808 |
| momentum | weights | foreign+0.1 | 26 | 0,875 | 0,571 | 12 | 0,500 | 0,269 |
| momentum | weights | foreign-0.1 | 26 | 0,846 | 0,429 | 14 | 0,577 | 0,385 |
| momentum | weights | liquidity+0.1 | 26 | 0,862 | 0,571 | 13 | 0,538 | 0,308 |
| momentum | weights | liquidity-0.1 | 26 | 0,810 | 0,571 | 16 | 0,692 | 0,500 |
| momentum | weights | momentum+0.1 | 26 | 0,887 | 0,571 | 11 | 0,462 | 0,231 |
| momentum | weights | momentum-0.1 | 26 | 0,897 | 0,667 | 12 | 0,385 | 0,231 |

## Diễn giải

- balanced: Mô tả 25 cặp phiên: IC trung bình +0,015. Kết quả chưa xác lập khả năng dự báo hay hiệu quả đầu tư. Điểm giúp ưu tiên danh sách theo dõi; độ ổn định của danh sách không chứng minh lợi nhuận.
- momentum: Mô tả 25 cặp phiên: IC trung bình +0,022. Kết quả chưa xác lập khả năng dự báo hay hiệu quả đầu tư. Điểm giúp ưu tiên danh sách theo dõi; độ ổn định của danh sách không chứng minh lợi nhuận.
- **Điều chỉnh quyền:** `refPrice` trống ở mọi dòng. Có 2/750 dòng `priceChangePercent` lệch quá 0,3 điểm % so với đóng cửa/đóng cửa (GVR 2026-10-21, VNM 2026-10-22). Cần đối chiếu với lịch giao dịch không hưởng quyền.

Thay đổi công thức là phiên bản phương pháp mới; các kết quả daily-v1 không được dùng để chứng minh daily-v2.
Dữ liệu, cấu hình, danh sách Top/Bottom, các ca thiếu và toàn bộ phép so sánh nằm trong evaluation.json.
