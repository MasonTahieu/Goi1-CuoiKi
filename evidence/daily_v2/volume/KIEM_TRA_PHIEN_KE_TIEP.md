# Kiểm chứng phương pháp daily-v2

Rổ VN30; 20 phiên từ 2026-10-19 đến 2026-11-13; 19 cặp liền phiên được xét, 0 khoảng trống bị bỏ.

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
| balanced | 18 | +0,009 | 0,245 | 18 | −0,014 |
| momentum | 18 | +0,020 | 0,240 | 18 | +0,020 |

## Độ nhạy danh sách theo dõi

Jaccard = số mã giao / số mã hợp (0–1). Bỏ yếu tố và đổi trọng số giữ nguyên tập mã hợp lệ.
Che một đầu vào bắt buộc cho từng mã rồi chấm lại nhóm còn lại; đây là tình huống thử, không phải lỗi dữ liệu thực tế. Kết quả chi tiết có cả so sánh Top trên các mã chung để tách ảnh hưởng loại mã và đổi phân vị.

| Cấu hình | Loại | Biến thể | Số tình huống | Jaccard TB | Jaccard nhỏ nhất | Số tình huống đổi Top | Mã ra TB | Mã vào TB |
|---|---|---|---:|---:|---:|---:|---:|---:|
| balanced | ablation | foreign | 19 | 0,613 | 0,375 | 18 | 1,211 | 1,421 |
| balanced | ablation | liquidity | 19 | 0,564 | 0,111 | 18 | 1,474 | 1,632 |
| balanced | ablation | momentum | 19 | 0,527 | 0,250 | 18 | 1,684 | 1,737 |
| balanced | missing | one_missing_member | 562 | 0,929 | 0,444 | 137 | 0,208 | 0,240 |
| balanced | single_factor | foreign | 19 | 0,372 | 0,111 | 19 | 2,526 | 2,368 |
| balanced | single_factor | liquidity | 19 | 0,325 | 0,111 | 19 | 2,789 | 2,632 |
| balanced | single_factor | momentum | 19 | 0,448 | 0,250 | 19 | 2,053 | 1,895 |
| balanced | weights | foreign+0.1 | 19 | 0,888 | 0,667 | 7 | 0,421 | 0,263 |
| balanced | weights | foreign-0.1 | 19 | 0,897 | 0,667 | 7 | 0,368 | 0,263 |
| balanced | weights | liquidity+0.1 | 19 | 0,911 | 0,429 | 5 | 0,368 | 0,211 |
| balanced | weights | liquidity-0.1 | 19 | 0,845 | 0,667 | 10 | 0,526 | 0,421 |
| balanced | weights | momentum | 19 | 0,802 | 0,667 | 13 | 0,579 | 0,632 |
| balanced | weights | momentum+0.1 | 19 | 0,932 | 0,667 | 5 | 0,263 | 0,158 |
| balanced | weights | momentum-0.1 | 19 | 0,816 | 0,333 | 10 | 0,684 | 0,526 |
| momentum | ablation | foreign | 19 | 0,670 | 0,429 | 17 | 1,158 | 0,947 |
| momentum | ablation | liquidity | 19 | 0,679 | 0,222 | 15 | 1,158 | 1,105 |
| momentum | ablation | momentum | 19 | 0,432 | 0,250 | 19 | 2,105 | 2,105 |
| momentum | missing | one_missing_member | 562 | 0,927 | 0,571 | 160 | 0,240 | 0,208 |
| momentum | single_factor | foreign | 19 | 0,369 | 0,100 | 19 | 2,579 | 2,368 |
| momentum | single_factor | liquidity | 19 | 0,289 | 0,111 | 19 | 3,000 | 2,789 |
| momentum | single_factor | momentum | 19 | 0,516 | 0,250 | 19 | 1,789 | 1,579 |
| momentum | weights | balanced | 19 | 0,802 | 0,667 | 13 | 0,632 | 0,579 |
| momentum | weights | foreign+0.1 | 19 | 0,916 | 0,571 | 6 | 0,368 | 0,158 |
| momentum | weights | foreign-0.1 | 19 | 0,851 | 0,667 | 11 | 0,526 | 0,368 |
| momentum | weights | liquidity+0.1 | 19 | 0,877 | 0,667 | 9 | 0,474 | 0,263 |
| momentum | weights | liquidity-0.1 | 19 | 0,832 | 0,571 | 11 | 0,579 | 0,474 |
| momentum | weights | momentum+0.1 | 19 | 0,898 | 0,571 | 7 | 0,421 | 0,211 |
| momentum | weights | momentum-0.1 | 19 | 0,921 | 0,667 | 7 | 0,316 | 0,158 |

## Diễn giải

- balanced: Mô tả 18 cặp phiên: IC trung bình +0,009. Kết quả chưa xác lập khả năng dự báo hay hiệu quả đầu tư. Điểm giúp ưu tiên danh sách theo dõi; độ ổn định của danh sách không chứng minh lợi nhuận.
- momentum: Mô tả 18 cặp phiên: IC trung bình +0,020. Kết quả chưa xác lập khả năng dự báo hay hiệu quả đầu tư. Điểm giúp ưu tiên danh sách theo dõi; độ ổn định của danh sách không chứng minh lợi nhuận.
- **Điều chỉnh quyền:** `refPrice` trống ở mọi dòng. Có 2/570 dòng `priceChangePercent` lệch quá 0,3 điểm % so với đóng cửa/đóng cửa (GVR 2026-10-21, VNM 2026-10-22). Cần đối chiếu với lịch giao dịch không hưởng quyền.

Thay đổi công thức là phiên bản phương pháp mới; các kết quả daily-v1 không được dùng để chứng minh daily-v2.
Dữ liệu, cấu hình, danh sách Top/Bottom, các ca thiếu và toàn bộ phép so sánh nằm trong evaluation.json.
