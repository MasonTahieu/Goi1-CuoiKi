# Kiểm chứng phương pháp daily-v2

Rổ VN30; 23 phiên từ 2026-10-19 đến 2026-11-18; 22 cặp liền phiên được xét, 0 khoảng trống bị bỏ.

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
| balanced | 22 | +0,019 | 0,243 | 22 | −0,079 |
| momentum | 22 | +0,036 | 0,231 | 22 | +0,083 |

## Độ nhạy danh sách theo dõi

Jaccard = số mã giao / số mã hợp (0–1). Bỏ yếu tố và đổi trọng số giữ nguyên tập mã hợp lệ.
Che một đầu vào bắt buộc cho từng mã rồi chấm lại nhóm còn lại; đây là tình huống thử, không phải lỗi dữ liệu thực tế. Kết quả chi tiết có cả so sánh Top trên các mã chung để tách ảnh hưởng loại mã và đổi phân vị.

| Cấu hình | Loại | Biến thể | Số tình huống | Jaccard TB | Jaccard nhỏ nhất | Số tình huống đổi Top | Mã ra TB | Mã vào TB |
|---|---|---|---:|---:|---:|---:|---:|---:|
| balanced | ablation | foreign | 23 | 0,571 | 0,000 | 22 | 1,435 | 1,783 |
| balanced | ablation | liquidity | 23 | 0,541 | 0,111 | 22 | 1,565 | 1,696 |
| balanced | ablation | momentum | 23 | 0,523 | 0,250 | 22 | 1,696 | 1,739 |
| balanced | missing | one_missing_member | 681 | 0,927 | 0,444 | 170 | 0,201 | 0,256 |
| balanced | single_factor | foreign | 23 | 0,391 | 0,111 | 22 | 2,435 | 2,304 |
| balanced | single_factor | liquidity | 23 | 0,297 | 0,000 | 23 | 2,957 | 2,826 |
| balanced | single_factor | momentum | 23 | 0,402 | 0,111 | 23 | 2,304 | 2,174 |
| balanced | weights | foreign+0.1 | 23 | 0,901 | 0,667 | 8 | 0,348 | 0,261 |
| balanced | weights | foreign-0.1 | 23 | 0,886 | 0,667 | 9 | 0,391 | 0,304 |
| balanced | weights | liquidity+0.1 | 23 | 0,898 | 0,429 | 7 | 0,391 | 0,261 |
| balanced | weights | liquidity-0.1 | 23 | 0,828 | 0,667 | 13 | 0,565 | 0,478 |
| balanced | weights | momentum | 23 | 0,741 | 0,375 | 17 | 0,783 | 0,913 |
| balanced | weights | momentum+0.1 | 23 | 0,915 | 0,667 | 7 | 0,304 | 0,217 |
| balanced | weights | momentum-0.1 | 23 | 0,819 | 0,333 | 12 | 0,652 | 0,522 |
| momentum | ablation | foreign | 23 | 0,634 | 0,333 | 21 | 1,261 | 1,261 |
| momentum | ablation | liquidity | 23 | 0,680 | 0,222 | 19 | 1,174 | 1,043 |
| momentum | ablation | momentum | 23 | 0,396 | 0,000 | 23 | 2,391 | 2,304 |
| momentum | missing | one_missing_member | 681 | 0,926 | 0,571 | 204 | 0,260 | 0,198 |
| momentum | single_factor | foreign | 23 | 0,367 | 0,100 | 23 | 2,609 | 2,348 |
| momentum | single_factor | liquidity | 23 | 0,264 | 0,000 | 23 | 3,217 | 2,957 |
| momentum | single_factor | momentum | 23 | 0,515 | 0,250 | 23 | 1,826 | 1,565 |
| momentum | weights | balanced | 23 | 0,741 | 0,375 | 17 | 0,913 | 0,783 |
| momentum | weights | foreign+0.1 | 23 | 0,916 | 0,571 | 8 | 0,391 | 0,130 |
| momentum | weights | foreign-0.1 | 23 | 0,851 | 0,571 | 13 | 0,565 | 0,348 |
| momentum | weights | liquidity+0.1 | 23 | 0,844 | 0,571 | 13 | 0,609 | 0,348 |
| momentum | weights | liquidity-0.1 | 23 | 0,835 | 0,571 | 13 | 0,609 | 0,435 |
| momentum | weights | momentum+0.1 | 23 | 0,902 | 0,571 | 9 | 0,435 | 0,174 |
| momentum | weights | momentum-0.1 | 23 | 0,891 | 0,667 | 11 | 0,435 | 0,217 |

## Diễn giải

- balanced: Mô tả 22 cặp phiên: IC trung bình +0,019. Kết quả chưa xác lập khả năng dự báo hay hiệu quả đầu tư. Điểm giúp ưu tiên danh sách theo dõi; độ ổn định của danh sách không chứng minh lợi nhuận.
- momentum: Mô tả 22 cặp phiên: IC trung bình +0,036. Kết quả chưa xác lập khả năng dự báo hay hiệu quả đầu tư. Điểm giúp ưu tiên danh sách theo dõi; độ ổn định của danh sách không chứng minh lợi nhuận.
- **Điều chỉnh quyền:** `refPrice` trống ở mọi dòng. Có 2/660 dòng `priceChangePercent` lệch quá 0,3 điểm % so với đóng cửa/đóng cửa (GVR 2026-10-21, VNM 2026-10-22). Cần đối chiếu với lịch giao dịch không hưởng quyền.

Thay đổi công thức là phiên bản phương pháp mới; các kết quả daily-v1 không được dùng để chứng minh daily-v2.
Dữ liệu, cấu hình, danh sách Top/Bottom, các ca thiếu và toàn bộ phép so sánh nằm trong evaluation.json.
