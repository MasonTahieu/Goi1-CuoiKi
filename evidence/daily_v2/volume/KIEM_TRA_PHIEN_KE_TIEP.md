# Kiểm chứng phương pháp daily-v2

Rổ VN30; 25 phiên từ 2026-10-19 đến 2026-11-20; 24 cặp liền phiên được xét, 0 khoảng trống bị bỏ.

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
| balanced | 24 | +0,022 | 0,233 | 24 | −0,053 |
| momentum | 24 | +0,032 | 0,223 | 24 | +0,110 |

## Độ nhạy danh sách theo dõi

Jaccard = số mã giao / số mã hợp (0–1). Bỏ yếu tố và đổi trọng số giữ nguyên tập mã hợp lệ.
Che một đầu vào bắt buộc cho từng mã rồi chấm lại nhóm còn lại; đây là tình huống thử, không phải lỗi dữ liệu thực tế. Kết quả chi tiết có cả so sánh Top trên các mã chung để tách ảnh hưởng loại mã và đổi phân vị.

| Cấu hình | Loại | Biến thể | Số tình huống | Jaccard TB | Jaccard nhỏ nhất | Số tình huống đổi Top | Mã ra TB | Mã vào TB |
|---|---|---|---:|---:|---:|---:|---:|---:|
| balanced | ablation | foreign | 25 | 0,547 | 0,000 | 24 | 1,560 | 1,880 |
| balanced | ablation | liquidity | 25 | 0,551 | 0,111 | 24 | 1,520 | 1,640 |
| balanced | ablation | momentum | 25 | 0,513 | 0,250 | 24 | 1,720 | 1,800 |
| balanced | missing | one_missing_member | 739 | 0,926 | 0,444 | 190 | 0,199 | 0,265 |
| balanced | single_factor | foreign | 25 | 0,394 | 0,111 | 24 | 2,400 | 2,280 |
| balanced | single_factor | liquidity | 25 | 0,288 | 0,000 | 25 | 3,000 | 2,880 |
| balanced | single_factor | momentum | 25 | 0,399 | 0,111 | 25 | 2,280 | 2,280 |
| balanced | weights | foreign+0.1 | 25 | 0,909 | 0,667 | 8 | 0,320 | 0,240 |
| balanced | weights | foreign-0.1 | 25 | 0,859 | 0,429 | 11 | 0,480 | 0,400 |
| balanced | weights | liquidity+0.1 | 25 | 0,879 | 0,429 | 9 | 0,440 | 0,320 |
| balanced | weights | liquidity-0.1 | 25 | 0,829 | 0,667 | 14 | 0,560 | 0,480 |
| balanced | weights | momentum | 25 | 0,735 | 0,375 | 19 | 0,800 | 0,920 |
| balanced | weights | momentum+0.1 | 25 | 0,909 | 0,667 | 8 | 0,320 | 0,240 |
| balanced | weights | momentum-0.1 | 25 | 0,807 | 0,333 | 14 | 0,680 | 0,560 |
| momentum | ablation | foreign | 25 | 0,620 | 0,250 | 23 | 1,320 | 1,320 |
| momentum | ablation | liquidity | 25 | 0,669 | 0,222 | 21 | 1,200 | 1,080 |
| momentum | ablation | momentum | 25 | 0,383 | 0,000 | 25 | 2,440 | 2,400 |
| momentum | missing | one_missing_member | 739 | 0,926 | 0,571 | 218 | 0,253 | 0,206 |
| momentum | single_factor | foreign | 25 | 0,358 | 0,100 | 25 | 2,640 | 2,400 |
| momentum | single_factor | liquidity | 25 | 0,264 | 0,000 | 25 | 3,200 | 2,960 |
| momentum | single_factor | momentum | 25 | 0,513 | 0,250 | 25 | 1,800 | 1,680 |
| momentum | weights | balanced | 25 | 0,735 | 0,375 | 19 | 0,920 | 0,800 |
| momentum | weights | foreign+0.1 | 25 | 0,896 | 0,571 | 10 | 0,440 | 0,200 |
| momentum | weights | foreign-0.1 | 25 | 0,840 | 0,429 | 14 | 0,600 | 0,400 |
| momentum | weights | liquidity+0.1 | 25 | 0,856 | 0,571 | 13 | 0,560 | 0,320 |
| momentum | weights | liquidity-0.1 | 25 | 0,822 | 0,571 | 15 | 0,640 | 0,480 |
| momentum | weights | momentum+0.1 | 25 | 0,896 | 0,571 | 10 | 0,440 | 0,200 |
| momentum | weights | momentum-0.1 | 25 | 0,893 | 0,667 | 12 | 0,400 | 0,240 |

## Diễn giải

- balanced: Mô tả 24 cặp phiên: IC trung bình +0,022. Kết quả chưa xác lập khả năng dự báo hay hiệu quả đầu tư. Điểm giúp ưu tiên danh sách theo dõi; độ ổn định của danh sách không chứng minh lợi nhuận.
- momentum: Mô tả 24 cặp phiên: IC trung bình +0,032. Kết quả chưa xác lập khả năng dự báo hay hiệu quả đầu tư. Điểm giúp ưu tiên danh sách theo dõi; độ ổn định của danh sách không chứng minh lợi nhuận.
- **Điều chỉnh quyền:** `refPrice` trống ở mọi dòng. Có 2/720 dòng `priceChangePercent` lệch quá 0,3 điểm % so với đóng cửa/đóng cửa (GVR 2026-10-21, VNM 2026-10-22). Cần đối chiếu với lịch giao dịch không hưởng quyền.

Thay đổi công thức là phiên bản phương pháp mới; các kết quả daily-v1 không được dùng để chứng minh daily-v2.
Dữ liệu, cấu hình, danh sách Top/Bottom, các ca thiếu và toàn bộ phép so sánh nằm trong evaluation.json.
