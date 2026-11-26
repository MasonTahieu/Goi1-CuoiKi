# Kiểm chứng phương pháp daily-v2

Rổ VN30; 28 phiên từ 2026-10-19 đến 2026-11-26; 26 cặp liền phiên được xét, 1 khoảng trống bị bỏ.

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
| balanced | 26 | +0,012 | 0,226 | 26 | −0,069 |
| momentum | 26 | +0,022 | 0,220 | 26 | +0,096 |

## Độ nhạy danh sách theo dõi

Jaccard = số mã giao / số mã hợp (0–1). Bỏ yếu tố và đổi trọng số giữ nguyên tập mã hợp lệ.
Che một đầu vào bắt buộc cho từng mã rồi chấm lại nhóm còn lại; đây là tình huống thử, không phải lỗi dữ liệu thực tế. Kết quả chi tiết có cả so sánh Top trên các mã chung để tách ảnh hưởng loại mã và đổi phân vị.

| Cấu hình | Loại | Biến thể | Số tình huống | Jaccard TB | Jaccard nhỏ nhất | Số tình huống đổi Top | Mã ra TB | Mã vào TB |
|---|---|---|---:|---:|---:|---:|---:|---:|
| balanced | ablation | foreign | 28 | 0,540 | 0,000 | 27 | 1,643 | 1,893 |
| balanced | ablation | liquidity | 28 | 0,541 | 0,100 | 27 | 1,643 | 1,643 |
| balanced | ablation | momentum | 28 | 0,531 | 0,250 | 27 | 1,679 | 1,714 |
| balanced | missing | one_missing_member | 826 | 0,925 | 0,444 | 234 | 0,230 | 0,241 |
| balanced | single_factor | foreign | 28 | 0,392 | 0,111 | 27 | 2,464 | 2,250 |
| balanced | single_factor | liquidity | 28 | 0,277 | 0,000 | 28 | 3,143 | 2,929 |
| balanced | single_factor | momentum | 28 | 0,399 | 0,111 | 28 | 2,357 | 2,250 |
| balanced | weights | foreign+0.1 | 28 | 0,912 | 0,667 | 10 | 0,357 | 0,179 |
| balanced | weights | foreign-0.1 | 28 | 0,856 | 0,429 | 14 | 0,536 | 0,357 |
| balanced | weights | liquidity+0.1 | 28 | 0,862 | 0,429 | 13 | 0,536 | 0,321 |
| balanced | weights | liquidity-0.1 | 28 | 0,837 | 0,667 | 16 | 0,571 | 0,429 |
| balanced | weights | momentum | 28 | 0,736 | 0,375 | 22 | 0,857 | 0,857 |
| balanced | weights | momentum+0.1 | 28 | 0,901 | 0,667 | 11 | 0,393 | 0,214 |
| balanced | weights | momentum-0.1 | 28 | 0,821 | 0,333 | 16 | 0,679 | 0,464 |
| momentum | ablation | foreign | 28 | 0,631 | 0,250 | 26 | 1,250 | 1,286 |
| momentum | ablation | liquidity | 28 | 0,652 | 0,222 | 24 | 1,250 | 1,143 |
| momentum | ablation | momentum | 28 | 0,395 | 0,000 | 28 | 2,357 | 2,393 |
| momentum | missing | one_missing_member | 826 | 0,922 | 0,571 | 259 | 0,245 | 0,238 |
| momentum | single_factor | foreign | 28 | 0,359 | 0,100 | 28 | 2,607 | 2,393 |
| momentum | single_factor | liquidity | 28 | 0,255 | 0,000 | 28 | 3,250 | 3,036 |
| momentum | single_factor | momentum | 28 | 0,514 | 0,250 | 28 | 1,786 | 1,679 |
| momentum | weights | balanced | 28 | 0,736 | 0,375 | 22 | 0,857 | 0,857 |
| momentum | weights | foreign+0.1 | 28 | 0,872 | 0,571 | 13 | 0,500 | 0,286 |
| momentum | weights | foreign-0.1 | 28 | 0,845 | 0,429 | 15 | 0,571 | 0,393 |
| momentum | weights | liquidity+0.1 | 28 | 0,872 | 0,571 | 13 | 0,500 | 0,286 |
| momentum | weights | liquidity-0.1 | 28 | 0,791 | 0,429 | 18 | 0,750 | 0,571 |
| momentum | weights | momentum+0.1 | 28 | 0,884 | 0,571 | 12 | 0,464 | 0,250 |
| momentum | weights | momentum-0.1 | 28 | 0,893 | 0,667 | 13 | 0,393 | 0,250 |

## Diễn giải

- balanced: Mô tả 26 cặp phiên: IC trung bình +0,012. Kết quả chưa xác lập khả năng dự báo hay hiệu quả đầu tư. Điểm giúp ưu tiên danh sách theo dõi; độ ổn định của danh sách không chứng minh lợi nhuận.
- momentum: Mô tả 26 cặp phiên: IC trung bình +0,022. Kết quả chưa xác lập khả năng dự báo hay hiệu quả đầu tư. Điểm giúp ưu tiên danh sách theo dõi; độ ổn định của danh sách không chứng minh lợi nhuận.
- **Điều chỉnh quyền:** `refPrice` trống ở mọi dòng. Có 2/810 dòng `priceChangePercent` lệch quá 0,3 điểm % so với đóng cửa/đóng cửa (GVR 2026-10-21, VNM 2026-10-22). Cần đối chiếu với lịch giao dịch không hưởng quyền.

Thay đổi công thức là phiên bản phương pháp mới; các kết quả daily-v1 không được dùng để chứng minh daily-v2.
Dữ liệu, cấu hình, danh sách Top/Bottom, các ca thiếu và toàn bộ phép so sánh nằm trong evaluation.json.
