# Phương pháp xếp hạng và kiểm chứng — daily-v2

Ngày cập nhật: 15/11/2026. Tài liệu này là đặc tả hiện hành của bản **cuối ngày ba yếu tố**. Các kết quả `daily-v1` trước đây là lịch sử, không chứng minh phiên bản này.

## 1. Mục tiêu và phạm vi kết luận

Điểm tổng hợp mô tả mã nào nổi bật tương đối trong rổ VN30 theo các tiêu chí công bố, giúp nhà đầu tư và môi giới ưu tiên danh sách theo dõi. Điểm không phải xác suất tăng giá, định giá nội tại hay khuyến nghị mua/bán. Độ ổn định của danh sách không chứng minh khả năng sinh lời.

Dữ liệu: SSI FastConnect V3, tổng hợp từng mã từng ngày. Rổ lấy theo thành phần lúc thu thập; phân tích là hồi cứu trên các mã đã thu, chưa tái dựng thành phần VN30 và dữ liệu sẵn có theo từng ngày quá khứ. Không dùng dữ liệu này để tuyên bố một chiến lược đầu tư lịch sử có thể thực hiện.

## 2. Các yếu tố

| Yếu tố | Công thức đầu vào | Ý nghĩa và giới hạn |
|---|---|---|
| Biến động giá từ mở cửa (nhãn ngắn: Động lượng) | `100 × (closePrice/openPrice − 1)` | Diễn biến giá trong phiên; không đồng nhất với momentum nhiều tháng trong nghiên cứu |
| Thanh khoản theo giá trị khớp | `totalTradingValue` | Đại diện quy mô giao dịch khớp; không đo đầy đủ chi phí, tác động giá hoặc độ sâu; có thể nghiêng về cổ phiếu quy mô lớn |
| Cân bằng mua–bán khối ngoại | `(B − S)/(B + S)` | B và S là mua và bán ngoại, cùng ngày, cùng mã, cùng đơn vị; giá trị dùng `foreignBuyValue/foreignSellValue`, khối lượng dùng `foreignBuyVolume/foreignSellVolume` |

Số ngoại SSI có thể bao gồm thỏa thuận. Công thức mới dùng cùng phạm vi ở tử và mẫu, không lấy số ngoại tổng chia cho riêng giá trị khớp. Nó vẫn không tách được tác động thỏa thuận và không đo riêng áp lực khớp lệnh.

**Quy mô khác tỷ lệ:** mua 1 triệu và bán 0 cho tỷ lệ 1; mua 100 tỷ và bán 0 cũng cho tỷ lệ 1. Giao diện hiển thị mua, bán và ròng cùng đơn vị với tùy chọn đang chọn. Không diễn giải tỷ lệ cao là dòng tiền lớn.

**Số 0 và dữ liệu thiếu:** B = S = 0 được quy ước tỷ lệ thô bằng 0, gắn nhãn không có giao dịch ngoại. Đây không phải điểm phân vị trung tính 50 cố định. Null, chuỗi không đọc được, boolean, số không hữu hạn hoặc âm bị loại. Một bên bằng 0, bên kia dương cho tỷ lệ ±1 hợp lệ. Không thêm epsilon và không đặt ngưỡng dòng tiền tùy ý.

Giá mở và đóng phải hữu hạn, dương; giá trị khớp hữu hạn, dương. Mỗi mã chỉ một dòng trong một nhóm/ngày. Thiếu một yếu tố: không chấm điểm tổng, không chia lại trọng số. Ít hơn 10 mã hợp lệ: dừng xếp hạng. Ngưỡng 10 là quy tắc vận hành, không phải cỡ mẫu có ý nghĩa thống kê.

## 3. Chuẩn hóa và kết hợp

Với n mã hợp lệ, xếp hạng tăng dần từng biến đầu vào; các giá trị bằng nhau dùng hạng trung bình r. Điểm yếu tố là `100 × (r − 1)/(n − 1)`. Nếu cả nhóm bằng nhau: mọi mã có điểm 50. Mọi yếu tố trong bản cuối ngày đều có chiều điểm tăng theo giá trị đầu vào.

Điểm tổng `S = Σ(w_j × P_j)`, trọng số không âm và tổng bằng 1:

- Cân bằng: 1/3, 1/3, 1/3 (33/33/33 chỉ là nhãn làm tròn).
- Ưu tiên động lượng: 0,50; 0,25; 0,25.

Đây là lựa chọn thiết kế, không được ước lượng hoặc chọn tối ưu bằng lợi suất trong mẫu. Phép cộng cho phép điểm mạnh ở một yếu tố bù điểm yếu ở yếu tố khác. Phân vị bỏ thông tin khoảng cách tuyệt đối; thứ hạng cao vẫn có thể xảy ra khi mọi mã cùng giảm. Không diễn giải chênh lệch điểm thành chênh lệch lợi suất.

Điểm tổng làm tròn 10 chữ số thập phân trước xếp hạng để thống nhất xử lý nhiễu số thực. Đồng điểm có cùng hạng kiểu 1, 2, 2, 4. Thứ tự chữ cái chỉ để hiển thị.

**Top 5:** lấy tất cả mã có điểm ít nhất bằng điểm của mã thứ 5; số mã có thể lớn hơn 5. Bottom 5 tương tự. Dùng đúng quy tắc này ở giao diện, so độ nhạy và kiểm chứng. Chỉ số Jaccard = số mã giao / số mã hợp để so hai danh sách có kích thước thay đổi.

Điểm là tương đối trong tập đủ dữ liệu tại một ngày. Thay đổi tập mã có thể làm đổi điểm dù giá trị thô của một mã không đổi. Mỗi lần tính lưu mã cấu hình và mã tập hợp thành viên.

## 4. Kiểm chứng đúng mục tiêu sàng lọc

Trên từng ngày và từng tùy chọn giá trị/khối lượng:

1. So Top tổng hợp với Top của từng yếu tố.
2. Lần lượt bỏ từng yếu tố, chuẩn hóa lại trọng số còn lại; giữ nguyên tập mã hợp lệ của mô hình đầy đủ để tránh lẫn tác động thay tập mã.
3. So hai cấu hình trọng số, và các biến thể định trước: tăng/giảm 0,10 ở từng trọng số rồi chuẩn hóa tổng về 1. Không chọn biến thể thắng theo lợi suất.
4. Che một đầu vào bắt buộc của từng mã, loại mã theo chính sách complete-case rồi tính lại phân vị nhóm còn lại. Báo cả thay đổi danh sách đầy đủ và thay đổi trên tập mã chung. Đây là thử nghiệm độ nhạy, không phải tỷ lệ mất dữ liệu thực tế.
5. Báo số mã ra/vào, Jaccard trung bình/nhỏ nhất, tương quan hạng trên mã chung và số tình huống thay danh sách. Tình huống làm nhóm còn dưới 10 mã được ghi không xếp hạng.

Không đặt ngưỡng tùy ý để tuyên bố mô hình “đạt học thuật”. Các phép này cho biết cấu trúc, mức nhạy và giới hạn của công cụ.

## 5. Lợi suất phiên sau: phép mô tả bổ sung

- Điểm ngày t chỉ dùng tổng hợp ngày t. Chốt Top/Bottom trước khi ghép dữ liệu tương lai.
- Lợi suất chính: `100 × (close[t+1]/open[t+1] − 1)`, nhãn **lợi suất mở cửa–đóng cửa phiên kế tiếp**. Không gọi là “lợi suất mua được”; chưa mô phỏng chi phí, giá khớp, chu kỳ thanh toán hoặc thực thi.
- Thiếu lợi suất bất kỳ thành viên Top/Bottom: bỏ chênh lệch của cặp phiên đó, ghi lý do; không bổ sung mã hạng kế tiếp. Hai nhóm giao nhau do đồng điểm: không tính chênh lệch.
- IC là tương quan hạng Spearman giữa điểm và lợi suất trên các mã có dữ liệu. IC từng yếu tố và tổng hợp dùng cùng tập mã; công bố số mã có lợi suất, số mã đã xếp hạng và mã thiếu. Việc chỉ quan sát mã đủ lợi suất vẫn là giới hạn của mẫu, không phải đã loại mọi thiên lệch dữ liệu thiếu.
- Báo trung bình, độ lệch chuẩn và tỷ lệ cặp IC dương; đơn vị tổng hợp là **cặp phiên**, không coi các dòng mã–ngày là quan sát độc lập.
- Không tự kết luận ý nghĩa thống kê từ ngưỡng t; không xuất ước lượng “cần N phiên để chứng minh”. Mẫu ngắn không chứng minh có hoặc không có khả năng dự báo. Muốn nghiên cứu dự báo cần thiết kế kiểm định riêng, xử lý phụ thuộc thời gian, thử nhiều mô hình và kiểm tra trên giai đoạn mới.
- `priceChangePercent` SSI là phép so sánh phụ, chưa xác nhận đầy đủ điều chỉnh quyền; dấu hiệu lệch không tự chứng minh ngày giao dịch không hưởng quyền.

**Lịch phiên:** khi có danh sách phiên chính thức đã đối chiếu, truyền tệp lịch có `source` và `sessions` vào lệnh kiểm chứng. Khi chưa có, chỉ ghép ngày dữ liệu liền ngày làm việc (bỏ thứ Bảy/Chủ nhật). Không nối qua khoảng trống ngày làm việc; nghỉ lễ chưa xác nhận cũng bị bỏ. Đây là cơ chế bảo thủ, không phải lịch sở giao dịch hoàn chỉnh. Báo các cặp bị bỏ; không coi “ngày tiếp theo có dữ liệu” mặc nhiên là phiên kế tiếp.

## 6. Tái lập và phiên bản dữ liệu

Bằng chứng tại `evidence/daily_v2/value` và `evidence/daily_v2/volume` gồm:

- `input_daily.json`: đúng các dòng dữ liệu đầu vào VN30, gồm thời gian thu thập khi có.
- `manifest.json`: SHA-256 dữ liệu/mã tính, phiên bản thư viện, phạm vi ngày, thành viên theo ngày, trọng số, cách tính ngoại, lịch phiên.
- `evaluation.json`: toàn bộ kết quả, danh sách Top/Bottom, lý do thiếu và từng phép độ nhạy.
- `kiem_tra_phien_ke_tiep.csv`, `do_nhay_sang_loc.csv` và báo cáo Markdown.

Kho SQLite vận hành vẫn có thể cập nhật dữ liệu ngày; ảnh chụp đầu vào của từng đợt báo cáo phải được giữ cùng mã nguồn tương ứng. Khi thu mới, xuất sang thư mục đợt mới để giữ dấu vết. Việc lưu ảnh chụp từ bây giờ không khôi phục các phiên bản nguồn đã bị ghi đè trước đó.

## 7. Bản trong phiên là phương pháp riêng

Bản trong phiên dùng thêm sổ lệnh và công thức khối ngoại cũ; vẫn là thử nghiệm riêng. Không dùng kết quả daily-v2 để xác nhận bốn yếu tố trong phiên. Khối lượng chào ba mức là trạng thái sổ lệnh, không đồng nhất dòng lệnh OFI. Các giới hạn về thỏa thuận, độ sâu và dữ liệu cũ phải được kiểm chứng riêng trước khi nâng phạm vi cam kết.

## 8. Cơ sở tham khảo và ranh giới sử dụng

- [OECD/JRC (2008), Handbook on Constructing Composite Indicators](https://www.oecd.org/en/publications/handbook-on-constructing-composite-indicators-methodology-and-user-guide_9789264043466-en.html): khung lựa chọn biến, chuẩn hóa, trọng số, dữ liệu thiếu và độ nhạy. Không chứng minh khả năng sinh lời của chỉ số dự án.
- [CFA Institute, Backtesting & Simulation](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/backtesting-and-simulation): giới hạn backtest, thông tin tương lai và thành phần mẫu lịch sử.
- [Newey & West (1987)](https://www.nber.org/papers/t0055): cơ sở tham khảo khi thiết kế suy luận có tự tương quan/phương sai thay đổi. Dự án hiện không tuyên bố đã thực hiện kiểm định này.
- Jegadeesh (1990), Evidence of predictable behavior of security returns: nghiên cứu lợi suất tháng; không xác nhận biến động giá một phiên của dự án.
- Amihud (2002), Illiquidity and stock returns: nghiên cứu thước đo kém thanh khoản khác; dự án không dùng công thức Amihud.
- Froot, O’Connell & Seasholes (2001), The portfolio flows of international investors; Vo (2017), Trading of foreign investors and stock returns in an emerging market: lý do quan tâm dòng vốn ngoại, không xác nhận công thức cân bằng B/S hay trọng số cụ thể trong dự án.
- Cont, Kukanov & Stoikov (2014), The price impact of order book events: dòng lệnh ở giá tốt nhất khác ảnh chụp ba mức của bản thử nghiệm trong phiên.

Công thức cân bằng mua–bán và cách kết hợp là lựa chọn thiết kế có công bố, không được trình bày như một mô hình đầu tư đã được các bài trên kiểm định.
