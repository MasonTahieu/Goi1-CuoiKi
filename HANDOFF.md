# Bàn giao dự án bộ lọc cổ phiếu VN30

**Ngày cập nhật 16/11/2026.** File này giúp người tiếp quản hiểu đề tài, mở lại sản phẩm, tìm bằng chứng và tiếp tục từ đúng chỗ đang dừng.

## Sửa vận hành web ngày 16/11/2026

- Kiểm chứng có cache tính trước cho cả bốn cấu hình, gắn SHA-256 dữ liệu và mã. Không dùng cache cũ khi dữ liệu/công thức đổi. Workflow hằng ngày tự tạo và commit cùng kho; Vercel chỉ đọc tệp. Fallback tính lại và giữ tối đa 16 kết quả trong bộ nhớ.
- Bốn payload trùng bộ bằng chứng daily-v2 hiện có; đọc cache cục bộ khoảng 0,07–0,12 giây. Toàn bộ **373 kiểm thử offline đạt** sau khi bổ sung mã lỗi xác thực an toàn.
- Entry point Vercel chọn mặc định FastConnect V3 khi profile bỏ trống/unselected; cấu hình chạy máy cá nhân vẫn phải chọn rõ.
- Phát hiện tài liệu triển khai cũ chưa yêu cầu khóa SSI trên Vercel, trong khi tab nến mới cần gọi API trực tiếp. Đã sửa hướng dẫn: `SSI_API_KEY` và `SSI_API_SECRET` phải được cấu hình riêng trên Vercel; GitHub Secrets không tự chuyển sang. Không đóng gói `.env`.
- Đã push bản sửa `a02af58` (merge `abfc35b`) và bổ sung chẩn đoán `97d72ba`. Vercel đã triển khai thành công. Bảng hạng trả HTTP 200, đủ 30 mã; cả bốn cấu hình Kiểm chứng HTTP 200, khoảng 0,3–2 giây (trước đó khoảng 12 giây), IC trùng bằng chứng. Hai lần đo gần nhất cho cấu hình cân bằng: giá trị 0,773 giây, khối lượng 0,735 giây.
- **Biểu đồ chưa hoàn tất trên Vercel:** đã sửa profile, đã có hai biến Secret ở Production và redeploy; nhưng cả nến ngày và nến 5 phút còn bị SSI từ chối khi đăng nhập. Chẩn đoán hiện trả `HTTP 401, mã SSI 401105` (API Key/Secret không hợp lệ). Bộ khóa trong `.env` trên máy đã thử đăng nhập trực tiếp thành công; không có căn cứ kết luận lỗi do IP.
- Lần nhập tự động qua ô mật khẩu bị công cụ trình duyệt thay bằng `<redacted>`, nên không được dùng cách đọc lại giá trị ô mật khẩu để chuyển khóa. Người dùng đã nhập lại và lưu cả hai biến; deployment sau đó vẫn trả 401105. Cần đối chiếu cặp khóa thực lưu trên Vercel với cặp hợp lệ trong `.env`, không in khóa/token ra log hoặc Git. Chỉ đánh dấu xong biểu đồ sau khi `/api/history?source=daily&symbol=VJC&timeframe=1d&range=5` và bản `timeframe=5m&range=100` trả HTTP 200 với nến thực.


## Cập nhật giao diện ngày 15/11/2026

Đã giảm mật độ thông tin: một hàng tổng quan, cấu hình và thời gian thu thập mở khi cần; bảng hạng bỏ nền màu từng ô, tăng khoảng cách dòng; dữ liệu tính điểm và biểu đồ phụ nằm trong mục mở rộng. Các tab phân tích dùng toàn chiều rộng. Kiểm chứng tách các biến thể trọng số khỏi bảng so sánh chính. Công thức, điểm và dữ liệu giữ nguyên. Đã kiểm tra lọc Top 5, các mục mở rộng, bố cục màn hình nhỏ và 19 kiểm thử web hiện có. Bản giao diện nằm trong đợt commit cùng daily-v2; xem lịch sử Git và trạng thái triển khai để xác định bản công khai.

## Cập nhật phương pháp ngày 15/11/2026 — ưu tiên đọc mục này

- Đã sửa bản cuối ngày thành **daily-v2**: cân bằng mua–bán ngoại `(B−S)/(B+S)`, cùng đơn vị giá trị/khối lượng; số 0 khác dữ liệu thiếu, loại số âm/boolean/không hữu hạn. Hiển thị quy mô mua/bán/ròng.
- Bảng hạng, tab Kiểm chứng và CSV dùng cùng phương pháp và lựa chọn ngoại. Top/Bottom bao gồm đồng điểm ở ranh giới thứ 5.
- Kiểm chứng chốt danh sách trước khi ghép lợi suất; không thay mã thiếu giá tương lai; không nối qua khoảng trống phiên chưa xác nhận. Mặc định chỉ dùng ngày làm việc liền nhau; có thể cung cấp lịch phiên đã đối chiếu qua CLI.
- Đã bổ sung so từng yếu tố, bỏ yếu tố trên cùng tập mã, đổi trọng số định trước và che từng đầu vào để đo độ nhạy. Bỏ t-test/kết luận tự động và ước lượng số phiên cần thiết trước đây.
- Đã đồng bộ `webdata/ssi_daily.sqlite` từ bản dữ liệu 20 phiên đã thu trước đó (19/10–13/11/2026), 600 dòng VN30. Bản cũ được giữ tại `runtime/daily_v2_previous_webdata.sqlite`. Không gọi SSI hay dùng token mới trong lần sửa này.
- Bằng chứng mới: [theo giá trị](evidence/daily_v2/value/KIEM_TRA_PHIEN_KE_TIEP.md), [theo khối lượng](evidence/daily_v2/volume/KIEM_TRA_PHIEN_KE_TIEP.md). Mỗi bộ có đầu vào cố định, mã SHA-256, cấu hình, phiên bản thư viện/mã, thành viên và kết quả từng tình huống.
- 19 cặp ngày được xét; 18 cặp tính được IC. Phiên 12/11 thiếu dữ liệu ngoại nên không có điểm. Cấu hình cân bằng: IC giá trị ~0,00953, khối lượng ~0,00927; chỉ là mô tả, chưa xác lập khả năng dự báo.
- Checklist và kết quả nghiệm thu: [DAILY_V2_NGHIEM_THU.md](docs/DAILY_V2_NGHIEM_THU.md).
- Đặc tả hiện hành: [CO_SO_PHUONG_PHAP.md](report/CO_SO_PHUONG_PHAP.md). Lệnh tái lập trong README (`validate-daily`, không cần xác thực).
- Đã chạy toàn bộ 361 kiểm thử offline qua; đã kiểm tra giao diện cục bộ và đổi lựa chọn khối ngoại. Phiên bản này đã được chuẩn bị trong đợt commit/push theo yêu cầu người dùng; trạng thái chạy công khai cần đối chiếu lần triển khai tương ứng.
- Bản trong phiên bốn yếu tố giữ phạm vi thử nghiệm riêng; các kết luận lịch sử bên dưới phải đọc theo phiên bản và thời điểm của chúng. Báo cáo/video nộp cần dùng daily-v2 nếu chọn phạm vi cuối ngày.

---

**Trạng thái:** sản phẩm đã chạy công khai với dữ liệu SSI thật ở chế độ cuối ngày. Stream đã chạy trên GitHub Actions hai buổi ngày 10/11. Đủ 5/5 điều kiện để bật điểm trong phiên, nhưng chưa bật. **Chưa có bản nộp được:** stream mới có 3 nửa phiên và chưa có phiên trọn vẹn. Lịch tự động của GitHub không chạy đúng giờ nên phải bấm tay mỗi sáng. Báo cáo, video và ZIP phải làm lại.

| Hạng mục | Hiện trạng |
|---|---|
| Trang web | https://cuoiki.vercel.app, mở sẵn nguồn **Cuối ngày · SSI thật** |
| Mã nguồn | [MasonTahieu/CuoiKi](https://github.com/MasonTahieu/CuoiKi), nhánh `main`, repo công khai. Bản sửa xác thực ngày 11/11 đạt **338/338 kiểm thử** offline và đã lên GitHub ở commit [`c2d6660`](https://github.com/MasonTahieu/CuoiKi/commit/c2d6660) |
| Phạm vi | Chỉ rổ VN30. Giảng viên đã xác nhận dùng SSI làm nguồn chính và phạm vi này |
| Dữ liệu ngày (REST) | 16 phiên VN30 thật (19/10–09/11/2026) trong `webdata/ssi_daily.sqlite`. Không cần OTP |
| Tự động hằng ngày | GitHub Actions lấy dữ liệu theo lịch 15:20, 15:50 và 16:20 thứ Hai–thứ Sáu, Vercel hiển thị. Lịch chạy trễ: phiên 09/11 chạy lúc 01:50 và 02:56 sáng hôm sau. Phiên 10/11 chưa chạy lúc 19:05. Muốn có ngay thì bấm tay workflow **SSI daily summaries** sau 15:20 |
| Stream trong phiên | **Đã thu thật, không cần OTP**, đủ 30 mã: chiều 09/11 trên máy; sáng và chiều 10/11 trên GitHub. Tổng cuối ngày khớp REST (tỷ lệ 1,0, đo ngày 09/11). Chiều 10/11 dừng sớm lúc 14:33 vì SSI từ chối xác thực, xem [mục 2c](#công-việc-còn-lại) |
| Thu stream tự động | Workflow `ssi-stream.yml`: khung 08:55–11:35 và 12:55–15:05, thứ Hai–thứ Sáu. Chỉ commit bản tóm tắt vào `evidence/v3_sessions/stream/`, không lưu nhật ký thô. **Lịch không chạy đúng giờ** (ngày 10/11 các lần theo lịch chạy lúc 15:23–15:50, quá khung nên tự thoát). Phải bấm tay, xem [Thu 10 phiên](#thu-stream-10-phiên-việc-hằng-ngày) |
| Mô hình 4 yếu tố | Mới chạy trên dữ liệu giả lập. `SSI_SEMANTICS_VERIFIED` vẫn `false`, nên điểm trong phiên trên dữ liệu thật đang khóa. **Đủ 5/5 điều kiện** từ 10/11 (đã thấy cờ `LO` lúc 13:00). Người học quyết định có bật hay không |
| Báo cáo, video, ZIP | Gói ngày 05/11 lỗi thời và đã gỡ. Có sẵn bản nháp phần V3 và phần cơ sở tài chính |

**Việc gần nhất:**
1. Sáng 11/11, trong khoảng 08:00–08:50, bấm **Run workflow** cho **SSI stream capture** hai lần, theo [Thu 10 phiên](#thu-stream-10-phiên-việc-hằng-ngày).
2. Bản sửa xác thực ngày 11/11 đã lên GitHub ở commit `c2d6660`. Các workflow mới trên `main` sẽ dùng bản sửa. Các workflow đã tạo trước khi push vẫn dùng phiên bản tại thời điểm được tạo.
3. Quyết định có bật `SSI_SEMANTICS_VERIFIED` không.

Xem [Công việc còn lại](#công-việc-còn-lại).

**Kết quả chính trên dữ liệu thật:**
- **Khối ngoại gồm cả giao dịch thỏa thuận:** FPT và VNM ngày 09/11 có bước nhảy mua và bán khớp đến từng đồng với thỏa thuận REST. Giá trị khớp thì không gồm thỏa thuận. Trường hợp xấu nhất, tổng điểm vẫn có Spearman trung bình 0,95 và giữ 3,8/5 mã top 5. Trang web đã ghi "Khối ngoại gồm thỏa thuận". [Kết quả](evidence/v3_history/KHOI_NGOAI_THOA_THUAN.md)
- **Stream trên GitHub, 10/11:** sáng 10:17–11:35 nhận 90.855 gói, chiều 12:55–14:33 nhận 191.257 gói. Cả hai buổi không có lỗi giải mã, không gói nào bị từ chối. Mỗi lần đổi token (khoảng 14 phút một lần), kết nối mở lại trong 1–4 giây. Trong khớp lệnh liên tục có 26–29/30 mã dùng được; 1–3 mã thiếu trường ở mỗi mốc, chưa rõ là mã nào. Spearman giữa hai mốc cách nhau 15 phút là 0,74–0,88. [Sáng](evidence/v3_sessions/stream/stream-2026-11-10-sang.json) · [Chiều](evidence/v3_sessions/stream/stream-2026-11-10-chieu.json)
- **Stream so với REST (09/11):** khối lượng, giá trị, mua bán của khối ngoại và giá mở cửa đều khớp, tỷ lệ 0,9999999–1,0000002 trên 29–30 mã. [Kết quả](evidence/v3_smoke/20261109-dong-cua/KET_QUA.md)
- **Stream 5 phút (09/11, 13:18–13:23):** nhận 8.414 gói, lỗi giải mã 0, từ chối 0, mất kết nối 0, trùng 369 (4,4%). Với ngưỡng thử 90/30 giây, 30/30 mã dùng được và thứ hạng 13:20 so với 13:23 có Spearman 0,93. Đây chỉ là một mẫu ngắn giữa phiên chiều. [Kết quả](evidence/v3_smoke/20261109-131820/SMOKE.md)
- **Kiểm tra phiên kế tiếp cũ:** kết quả daily-v1 đã được thay thế bởi bằng chứng daily-v2 ở đầu file. Ước lượng số phiên cần thiết và suy luận theo t cũ đã bị rút bỏ; không dùng để bảo vệ.
- **Lý do bỏ HNX30:** 11/30 mã giao dịch dưới 1 tỷ đồng mỗi phiên, 43% dòng thiếu dữ liệu khối ngoại. [Số liệu](evidence/v3_history/PHAM_VI_VN30.md)
- **REST thật:** giá trị khớp = giá bình quân × khối lượng (trung vị tỷ lệ 1,0000). `securitiesSummary?index=` trả về chính chỉ số nên code lấy theo từng mã. [Kết quả REST](evidence/v3_history/KET_QUA_REST_THAT.md)

**Bảo mật:** khóa SSI nằm trong `.env` trên máy (không đưa lên GitHub) và GitHub Secrets. Khóa từng được dán vào chat; nên thu hồi và tạo khóa mới nếu chưa làm, rồi cập nhật cả hai nơi.

## Đề tài và mục đích

**Tên đề tài:** Xây dựng hệ thống sàng lọc và xếp hạng cổ phiếu đa yếu tố trong phiên cho rổ VN30 sử dụng SSI FastConnect, phục vụ nhà đầu tư và môi giới.

Người dùng chọn mốc quan sát, xem mã nổi bật theo các yếu tố, rồi mở chi tiết để hiểu vì sao một mã có điểm cao, thấp hoặc chưa được xếp hạng. Sản phẩm giúp thu hẹp danh sách cần nghiên cứu. Phạm vi là dữ liệu thị trường cổ phiếu, xếp hạng tương đối trong rổ VN30 và chạy theo chế độ chỉ đọc.

Dự án ban đầu hướng tới VN30 và VPBankS NEO API. Đã lấy được token NEO nhưng yêu cầu đọc dữ liệu thị trường trả HTTP 401 với mã `NEOINP000401`. Giảng viên đã xác nhận dùng SSI FastConnect làm nguồn chính. Ngày 07/11/2026 phạm vi thu hẹp về rổ VN30, vì trên 15 phiên SSI thật HNX30 có 11/30 mã giao dịch dưới 1 tỷ đồng mỗi phiên và 43% dòng thiếu dữ liệu khối ngoại. [Số liệu](evidence/v3_history/PHAM_VI_VN30.md) Thư mục mã nguồn vẫn mang tên `neo-vn30-screener` và giữ nhánh NEO để truy vết. Tên ZIP giữ mẫu `MSSV_HoTen_NEOAPI_FinTech.zip` theo quy cách đề. [Đề (bản cập nhật)](../261BFF401101_261BFF401102_GPMUD1_DETHICUOIKY_DOAN_CAPNHAT.docx)

## Tiến trình đã làm

| Task | Kết quả đã có | Đọc tiếp |
|---|---|---|
| 1. Giải mã SSI | Chuẩn hóa các bản tin F, X, X-Quote, X-Trade, R và B theo tài liệu FCData v2. Giữ thời điểm nguồn, trường vắng, giá trị null và cờ ước tính khối ngoại. | [Đặc tả](docs/TASK_1_GIAI_MA_SSI.md) · [Mẫu giải mã](evidence/task1/KET_QUA_MAU.md) |
| 2. Thu thập giả lập | Collector nhận gói qua một giao diện kết nối, ghép bản cập nhật theo từng trường, bỏ gói trùng, xử lý mất kết nối và dựng lại dữ liệu nền. Ghi được vào SQLite. | [Đặc tả](docs/TASK_2_COLLECTOR_GIA_LAP.md) · [Mẫu luồng](evidence/task2/KET_QUA_MAU.md) |
| 3. SQLite, phát lại và chất lượng | Ghi theo lô, đọc theo nguồn, lần thu thập và mốc hoặc ID sự kiện. Kiểm tra trường thiếu, cũ, trễ, lỗi kiểu dữ liệu, khoảng gián đoạn và độ phủ. Đã sửa thông báo cho bản ghi giải mã hỏng thiếu trường bắt buộc. | [Đặc tả](docs/TASK_3_LUU_TRU_REPLAY_CHAT_LUONG.md) · [Tám mốc mẫu](evidence/task3/KET_QUA_MAU.md) |
| 4. Bốn yếu tố và điểm | Kiểm chứng tính tay, phân vị, đồng hạng, ngưỡng nhóm, hai bộ trọng số và hai cách tính khối ngoại. | [Công thức](docs/TASK_4_KIEM_CHUNG_BON_YEU_TO.md) · [Kết quả mẫu](evidence/task4/KET_QUA_MAU.md) |
| 5. Giao diện | Bảng điểm và nhật ký SSI mẫu, bộ lọc theo nhóm/mã, chi tiết từng yếu tố, biểu đồ cột và đường, dấu thời gian, lý do chưa xếp hạng, làm mới kho và CSV kèm cấu hình. | [Hướng dẫn thử](docs/TASK_5_GIAO_DIEN.md) |
| 6. Kiểm thử toàn tuyến | Chạy từ gói SSI giả lập qua SQLite đến bảng điểm và CSV. Thử mất kết nối, xác thực, timeout, REST 429/503/403 và dữ liệu ngày. Sửa ba lỗi ở trạng thái kết nối, bản ghi REST sai kiểu và vô hiệu hóa token khi gặp 401. | [Ma trận T01–T24](docs/TASK_6_KIEM_THU_TOAN_TUYEN.md) · [Kết quả pytest](evidence/task6-tests.xml) |
| 7. Báo cáo và gói chạy | PDF 11 trang, MP4 khoảng 32 giây, kịch bản demo và ZIP có thư viện cài offline. Đã kiểm lại T24 trên đúng bản ZIP bàn giao. Họ tên, MSSV và mã lớp trên bìa được để trống theo yêu cầu. | [Biên bản kiểm tra](evidence/task7/KIEM_TRA_GOI.md) · [Kịch bản demo](report/KICH_BAN_DEMO.md) |
| 9. Giao diện web mới (06/11) | Thay Streamlit bằng dashboard nền tối theo chuẩn ngành (tham chiếu SSI iBoard, FireAnt/Simplize), do người học chọn. Python thư viện chuẩn phục vụ JSON, HTML/CSS/JS tự viết, chạy offline. Bảng xếp hạng có thanh đóng góp và thanh phân vị từng yếu tố, khung giải thích mã, mỗi mã một nhãn trạng thái. 8 ca kiểm thử API/server. Có so sánh hạng và điểm với mốc trước (mũi tên cạnh hạng, dòng so sánh trong khung giải thích, vạch điểm cũ trên biểu đồ). | [PRODUCT.md](PRODUCT.md) · [Hợp đồng thiết kế](.impeccable/surfaces/src-web-static-index-html.md) |
| 8. Bộ nối FastConnect V3 (06/11) | Client đăng nhập và REST, adapter WebSocket bọc SDK, bộ giải mã V3 dùng chung bản ghi nội bộ với v2, chính sách chất lượng riêng cho V3 (không có trạng thái từng mã, suy phiên theo lịch khi thiếu cờ), smoke test, thu theo khung giờ, lịch sử 10 phiên, đánh giá nhiều phiên. 43 ca kiểm thử mới, gồm phát lại nhật ký V3 trên Streamlit. | [Hướng dẫn V3](docs/V3_KET_NOI.md) · [Nháp bổ sung báo cáo](report/BO_SUNG_BAO_CAO_V3.md) |
| 10. REST thật và chế độ cuối ngày (07/11) | Có API Key. Lấy dữ liệu ngày thật theo từng mã, thêm phương pháp `daily-v1` (3 yếu tố) và nguồn "Cuối ngày · SSI thật", chạy được ngoài giờ giao dịch. | [Kết quả REST](evidence/v3_history/KET_QUA_REST_THAT.md) |
| 11. Triển khai (07/11) | Vercel phục vụ trang, GitHub Actions lấy dữ liệu hằng ngày và commit vào `webdata/`. Miễn phí, không cần thẻ, máy tắt vẫn chạy. Khóa SSI chỉ nằm trong GitHub Secrets, không đưa lên Vercel. | [Hướng dẫn](docs/TRIEN_KHAI_VERCEL.md) |
| 12. Thu hẹp về VN30 (07/11) | Client, thu thập, xếp hạng, API, giao diện, kịch bản giả lập và bằng chứng chỉ còn VN30. Dữ liệu HNX30 được lưu số liệu rồi gỡ khỏi kho. | [Lý do](evidence/v3_history/PHAM_VI_VN30.md) |
| 13. Giao diện bổ sung (07/11) | Dải nhịp thị trường, thẻ Lịch sử hạng (bản đồ nhiệt), thẻ Kiểm chứng, tô màu ô yếu tố theo phân vị, biểu đồ động lượng × dòng tiền ngoại. Dữ liệu demo đổi nhãn "Minh họa", xếp sau nguồn thật. | [DESIGN.md](DESIGN.md) |
| 14. Rà phương pháp (07–08/11) | Kiểm tra phiên kế tiếp tính theo lợi suất mua được (mở cửa → đóng cửa phiên sau), nêu ngưỡng phát hiện của mẫu. Thêm cơ sở tài chính có nguồn. Trang ghi rõ phạm vi khối ngoại chưa xác minh, dữ liệu thật không còn nhãn "Demo". | [Kết quả](evidence/v3_sessions/KIEM_TRA_PHIEN_KE_TIEP.md) · [Cơ sở tài chính](report/CO_SO_PHUONG_PHAP.md) |
| 15. Stream thật và thu tự động (09–10/11) | Thu chiều 09/11 trên máy, đối chiếu với REST lúc đóng cửa. Sửa thời gian TRADE có mili giây, thời gian chờ kết nối lại, danh sách thành phần chỉ còn một dòng, và ngưỡng riêng cho khối ngoại. Xác minh khối ngoại gồm thỏa thuận. Thêm lệnh `stream-window` và workflow `ssi-stream.yml`. Ngày 10/11 thu hai buổi trên GitHub. 312/312 kiểm thử. | [Đóng cửa 09/11](evidence/v3_smoke/20261109-dong-cua/KET_QUA.md) · [Thỏa thuận](evidence/v3_history/KHOI_NGOAI_THOA_THUAN.md) · [Tóm tắt stream](evidence/v3_sessions/stream/) |

## Phương pháp chấm điểm

| Yếu tố | Cách tính |
|---|---|
| Động lượng | `100 × (giá khớp gần nhất / giá mở cửa − 1)` |
| Thanh khoản | Trung bình phân vị của tổng giá trị khớp, độ sâu sổ lệnh ba mức mỗi bên và chênh lệch giá mua bán tốt nhất. Chênh lệch hẹp hơn được điểm cao hơn. |
| Dòng tiền ngoại tương đối | Mặc định dùng `(giá trị ngoại mua − bán) / tổng giá trị khớp` cùng phạm vi. Có cấu hình đối chiếu riêng theo khối lượng. |
| Mất cân bằng cung cầu | `(tổng lượng chào mua − tổng lượng chào bán) / tổng lượng chào hai bên`, lấy ba mức mỗi bên. |

Đây là mô hình trong phiên (`intraday-v1`). Chế độ cuối ngày hiện dùng `daily-v2` (xem đặc tả mới): ba yếu tố động lượng (đóng cửa so với mở cửa), thanh khoản (chỉ giá trị khớp) và dòng tiền ngoại, trọng số 33/33/33 hoặc 50/25/25, không có sổ lệnh nên không có cung–cầu. Hai phương pháp không so trực tiếp với nhau.

Điểm từng yếu tố là phân vị 0–100 trong nhóm hợp lệ tại cùng mốc. Mô hình trong phiên dùng trọng số **25/25/25/25**, hoặc **40/20/20/20** khi ưu tiên động lượng. Điểm hòa nhận cùng hạng. Mỗi nhóm cần **ít nhất 10 mã hợp lệ**. Dữ liệu thiếu, quá cũ, ngoài phiên liên tục LO hoặc thiếu xác minh nguồn thật có thể khiến mã chưa được chấm. Bộ lọc mã và ngưỡng điểm trên giao diện áp dụng sau khi tính hạng.

CSV giữ nhóm, nguồn, lần thu thập, mốc, mã phương pháp, mã cấu hình và mã tập so sánh. Các trường này giúp phân biệt việc hạng đổi do đổi trọng số, đổi dữ liệu hoặc đổi tập mã đủ điều kiện. [Quy tắc xếp hạng và cấu hình](docs/TASK_4_KIEM_CHUNG_BON_YEU_TO.md)

Sản phẩm mô tả vị trí tương đối tại một mốc, không khẳng định điểm cao thì giá sẽ tăng. Từng yếu tố dựa trên tài liệu nào, khác tài liệu ở đâu và các hạn chế đã biết nằm trong [cơ sở tài chính](report/CO_SO_PHUONG_PHAP.md).

## Kiến trúc và chỗ cần tìm trong mã nguồn

```text
Nguồn dữ liệu → Giải mã và thu thập → Nhật ký SQLite
             → Phát lại và kiểm tra chất lượng → Tính yếu tố và xếp hạng → UI / CSV
```

| Vị trí | Vai trò |
|---|---|
| `src/ssi_api/` | Profile SSI, REST v2, decoder v2/V3, collector và công cụ phát lại. V3: `v3_client.py` (đăng nhập và REST), `v3_stream.py` (WebSocket), `v3_decoder.py`, `v3_ops.py` (smoke, thu phiên, lịch sử, đối chiếu), `v3_sample.py` (gói tin giả lập). `stream_collector.py` chọn bộ giải mã theo profile. |
| `src/analytics/sessions.py` | Đánh giá nhiều phiên: độ phủ theo mốc, Spearman giữa các mốc và giữa các cấu hình, khoảng cập nhật để chọn ngưỡng dữ liệu cũ, độ bền yếu tố theo ngày. |
| `src/analytics/validation.py` | Kiểm tra phiên kế tiếp: IC, chênh lệch top–bottom, ngưỡng phát hiện. `evaluate-v3` tự ghi lại kết quả vào `evidence/v3_sessions/`. |
| `src/ranking/daily.py`, `src/data/daily_store.py` | Phương pháp `daily-v2` và kho dữ liệu ngày. |
| `SSI_V3.ps1` | Năm lệnh `kiemtra`, `smoke`, `lichsu`, `phien`, `danhgia`. Chưa có `stream-window`; lệnh đó chạy bằng `python -X utf8 -m src.cli stream-window --otp-mode none`. |
| `.github/workflows/ssi-stream.yml` | Thu stream theo khung giờ, ghi bản tóm tắt `stream-<ngày>-sang.json` và `stream-<ngày>-chieu.json`. Hai lần chạy dùng chung nhóm `ssi-stream` nên lần thứ hai xếp hàng chờ lần đầu. |
| `src/data/` | Lưu và đọc SQLite, chuẩn hóa, chất lượng và tạo dữ liệu giả lập. |
| `src/finance/factors.py`, `src/ranking/engine.py` | Bốn yếu tố, phân vị, trọng số, ngưỡng hợp lệ và xếp hạng. |
| `src/web/` | Giao diện chính từ 06/11: `server.py` (HTTP thư viện chuẩn, chỉ 127.0.0.1), `api.py` (JSON từ pipeline sẵn có), `static/` (HTML/CSS/JS). Chạy bằng `RUN_APP.ps1`. |
| `api/index.py`, `vercel.json`, `pyproject.toml`, `requirements.txt` | Triển khai Vercel. Vercel cài thư viện theo `pyproject.toml`, nên danh sách này phải khớp `requirements.txt` (có test kiểm tra). |
| `.github/workflows/ssi-daily.yml`, `webdata/` | Lấy dữ liệu ngày tự động và kho dữ liệu mà trang công khai đọc. |
| `app.py`, `src/app/` | Giao diện Streamlit cũ, giữ làm dự phòng (`RUN_APP.ps1 -Streamlit`). |
| `src/cli.py` | Kiểm tra cấu hình, chạy bảng điểm demo và thu thập REST. |
| `tests/`, `evidence/`, `report/` | Ca kiểm thử tự động, bằng chứng kết quả, kịch bản demo và tài liệu báo cáo. |
| `.env.example`, `requirements-win-py313.lock.txt`, `requirements-local.txt` | Cấu hình mẫu trống, 46 phụ thuộc đã khóa cho Windows x64, CPython 3.13, và bộ thư viện đầy đủ cho máy cá nhân. |

Kho SSI mặc định là `runtime/ssi.sqlite`, kho dữ liệu ngày trên máy là `runtime/ssi_daily.sqlite` (trang công khai đọc `webdata/ssi_daily.sqlite`). Lệnh demo bảng điểm tạo `runtime/synthetic.sqlite` và `runtime/synthetic_ranking.csv`. Lệnh tạo nhật ký mẫu ghi `runtime/task3-synthetic.sqlite`. Hai nhật ký dựng từ giao diện demo nằm ở kho tạm. Nguồn, lần thu thập và phiên kết nối được theo dõi riêng. Thời điểm lưu và hiển thị theo giờ Việt Nam UTC+7.

## Mở lại và kiểm tra nhanh

Không cần cài gì để xem sản phẩm: mở https://cuoiki.vercel.app. Lần mở đầu sau một lúc không ai dùng mất khoảng 10–15 giây.

Để chạy trên máy, mở PowerShell tại thư mục chứa `app.py`. Chạy lệnh cài khi môi trường chưa có thư viện, rồi mở ứng dụng.

```powershell
.\CAI_THU_VIEN.ps1
.\RUN_APP.ps1
```

Giao diện web chạy cục bộ tại `http://127.0.0.1:8501` (thêm `-Streamlit` để mở giao diện cũ). Mặc định `DATA_PROVIDER=ssi` và `APP_MODE=demo`. Các lệnh dùng môi trường chung `~/.venv` theo mặc định. Truyền cùng `-VenvPath` cho các script nếu cần dùng một môi trường Python 3.13 khác. [README](README.md)

- **Cuối ngày · SSI thật:** nguồn mặc định khi có kho dữ liệu ngày. Xem thêm thẻ Lịch sử hạng và Kiểm chứng.
- **Minh họa · Bảng điểm giả lập:** 12 mã VN30 hư cấu. Thử đổi trọng số, lọc mã và xuất CSV.
- **Minh họa · Nhật ký SSI mẫu:** các mã hư cấu để minh họa chất lượng. Chọn lần **Mất kết nối và phục hồi**, xem mốc 10:00:06 rồi 10:00:13. Chọn lần **Dữ liệu khối ngoại cũ** để xem tuổi nguồn 63 giây vượt ngưỡng thử nghiệm 60 giây. [Hướng dẫn giao diện](docs/TASK_5_GIAO_DIEN.md)
- **Kiểm chứng toàn tuyến:** bộ riêng 11 mã VN30 hư cấu. Khi chỉ còn 9 mã hợp lệ (dưới ngưỡng 10), nhóm dừng xếp hạng và nêu lý do. Ca HOSETEST11 lên từ 55 điểm/hạng 4 đến 64 điểm/hạng 1 khi đổi trọng số. Đây là kết quả trên dữ liệu dựng để kiểm thử. [Kết quả toàn tuyến](docs/TASK_6_KIEM_THU_TOAN_TUYEN.md)

```powershell
.\CHECK_PROJECT.ps1
& "$HOME\.venv\Scripts\Activate.ps1"
python -X utf8 -m src.cli readiness
python -X utf8 -m src.cli demo-pipeline
python -X utf8 -m src.ssi_api.replay_sample
python -X utf8 -m src.ssi_api.replay --db runtime/task3-synthetic.sqlite --list-runs
```

Các lệnh trên kiểm tra cấu hình, chạy demo và phát lại mẫu cục bộ. Chế độ `APP_MODE=replay` cho chọn lần thu thập và mốc trong kho. Chế độ `APP_MODE=live` đọc kho đã có theo giờ hiện tại và có thể làm mới mỗi 10 hoặc 30 giây. Việc thu dữ liệu vào kho thuộc về collector.

## Bộ hồ sơ bàn giao

Gói nộp ngày 05/11/2026 (ZIP, PDF, MP4) là bản trước SSI V3 và giao diện web. Gói này đã được gỡ khỏi máy ngày 07/11/2026 để làm gọn thư mục; cần dựng lại sau khi có dữ liệu thật.

Công cụ dựng lại nằm trong `runtime/task7-build/` (không đưa lên GitHub):

| Tệp | Vai trò |
|---|---|
| `BaoCao_ban_soan.docx`, `write_report.py`, `write_pdf.py` | Bản soạn và script tạo báo cáo PDF |
| `capture.cjs`, `check_video.cjs` | Chụp ảnh màn hình, dựng và kiểm video demo |
| `package.py`, `check_zip.py` | Đóng gói ZIP có thư viện cài offline và kiểm lại gói |

Bản ZIP cũ đã được nghiệm thu ngày 05/11/2026. Gói không kèm tệp `.env` cá nhân, khóa API, kho SQLite vận hành hay lịch sử Git. File HANDOFF này là ghi chú bàn giao bổ sung trong thư mục mã nguồn. [Biên bản và SHA-256](evidence/task7/KIEM_TRA_GOI.md)

## Thu stream 10 phiên: việc hằng ngày

**Vì sao phải thu:** đề yêu cầu tự thu và lưu đủ dữ liệu để kiểm chứng mọi nhận định về diễn biến theo thời gian. Đề khuyến nghị tối thiểu 5 phiên và ưu tiên 10 phiên. SSI không cho lấy lại dữ liệu trong phiên của ngày đã qua, nên ngày nào không thu thì mất.

**Cách làm mỗi ngày giao dịch (thứ Hai–thứ Sáu):**
1. Trong khoảng 08:00–08:50, mở [SSI stream capture](https://github.com/MasonTahieu/CuoiKi/actions/workflows/ssi-stream.yml). Từ trang Actions, chọn **SSI stream capture** ở cột trái thì nút mới hiện.
2. Bấm **Run workflow**, để trống ô số giây, bấm nút xanh. Làm lại lần nữa. Lần đầu chờ đến 08:55 rồi thu đến 11:35. Lần thứ hai xếp hàng, chạy khi lần đầu xong, chờ đến 12:55 rồi thu đến 15:05.
3. Không cần tắt: mỗi lần tự dừng và tự commit bản tóm tắt. Bấm trên điện thoại cũng được; nếu không thấy nút, bật chế độ trang cho máy tính.
4. Bấm muộn (sau 08:55) thì lần thu bắt đầu ngay và thiếu phần đầu khung. Bấm sau 15:05 thì lần chạy tự thoát, không hại gì.
5. Từ 08:00 đến 15:20, không chạy stream trên máy và không đổi khóa SSI. SSI chỉ giữ một phiên cho mỗi API Key.

**Lịch tự động trong workflow vẫn giữ**, nhưng GitHub chỉ chạy lịch khi còn tài nguyên, trễ có khi tới 10 giờ. Phương án thay việc bấm tay: Task Scheduler trên máy bấm hộ bằng token chỉ cấp cho repo này, hoặc dịch vụ cron bên ngoài. Hai cách này cần người học tự tạo token. Chưa chọn.

| Ngày | Sáng (08:55–11:35) | Chiều (12:55–15:05) | Ghi chú |
|---|---|---|---|
| 09/11 | không thu | 13:34–15:05, trên máy | Có đối chiếu REST lúc đóng cửa |
| 10/11 | 10:17–11:35 | 12:55–14:33 | Sáng bấm muộn. Chiều dừng sớm vì lỗi xác thực |
| 11, 12, 13, 16, 17, 18, 19, 20/11 | | | Còn 8 ngày để đủ 10 ngày |

## Công việc còn lại

**1. Smoke test đã xong (09/11/2026), kết quả đo được**
- Stream không đòi OTP (`--otp-mode none`). Đã sửa một lỗi: gói TRADE có mili giây trong `t` (`2026/11/09 13:15:40.198`) nên ban đầu bị từ chối toàn bộ. Đã thêm test bằng gói tin thật.
- Gói ROOM (khối ngoại) đến 60 giây một lần, `t` luôn ở giây 00, trễ so với `t` đến 27,2 giây (trung vị 18,8). Tuổi tối đa khi bình thường là 60 + 27 = 87 giây, nên ngưỡng chung 60/10 giây không hợp với nhóm này. Giá và sổ lệnh trễ dưới 1 giây, vẫn hợp với 60/10.
- ROOM không có snapshot khi vừa đăng ký: khoảng 40–70 giây đầu các mã có thể thiếu trường khối ngoại.
- TRADE chạy trước đồng hồ máy khoảng 0,3 giây, dưới ngưỡng lệch 5 giây.
- 5 phút không nhận gói `market.flag`, nên phiên vẫn suy theo lịch.
- `securitiesSummary` của hôm nay trả 0 dòng khi đang trong phiên, nên chỉ đối chiếu được sau đóng cửa.
- Bản thu 13:34–15:05 (144.055 gói, không lỗi giải mã) bổ sung: gói ROOM trễ đến 30,5 giây; `MARKET_FLAG` báo `ATC` lúc 14:30 và `C` lúc 14:45, không có `PT`; không có gói TRADE trong ATC, kết quả khớp ATC đến sau 14:45. [Số liệu](evidence/v3_smoke/20261109-dong-cua/KET_QUA.md)
- Lịch dữ liệu ngày đã tự chạy cho phiên 09/11, nhưng trễ khoảng 10 giờ (01:50 và 02:56 sáng 10/11). Kho hiện có phiên 09/11.

**2. Đã sửa ngày 09/11 sau bản thu**
- **Lỗi 1, bộ thu lúc đổi token:** token sống 15 phút, SDK mở lại kết nối mỗi khoảng 14 phút, `collect_stream` coi là mất kết nối và thời gian chờ `2^n` giây không đặt lại. Đã đặt lại sau 60 giây có dữ liệu và giới hạn chờ 30 giây. Khoảng 1 phút sau mỗi lần đổi token, các mã vẫn thiếu trường khối ngoại đến đợt ROOM kế tiếp; ghi rõ điều này trong báo cáo.
- **Lỗi 2, danh sách thành phần:** `securitiesByBoard?index=VN30` lúc 15:49 chỉ trả một dòng `VN30`, lúc 14:58 vẫn trả 30 mã. Trước đây kết quả đó được chấp nhận nên workflow có thể ghi dữ liệu rác. Giờ mã từ chối danh sách khác 30 mã, dùng lại thành phần của phiên đầy đủ gần nhất kèm `member_warning`, và báo lỗi nếu không có phiên nào.
- **Ngưỡng:** 100/35 giây cho khối ngoại, 120/10 giây cho giá và sổ lệnh (`V3_LIMITS`). [Căn cứ](docs/V3_KET_NOI.md). Chưa có số đo phiên sáng và ATO.
- Lịch phiên dự phòng: 14:45 chuyển sang `C` theo cờ thật, bỏ `PT`.

**2b. Việc tiếp theo về stream**
- Bấm tay mỗi sáng đến khi đủ 10 ngày, theo [Thu 10 phiên](#thu-stream-10-phiên-việc-hằng-ngày). Hoặc chọn một phương án bấm hộ.
- Nhật ký thô không được lưu vì repo công khai và khoảng 4 GB mỗi phiên. Bản tóm tắt có độ trễ, nhịp, cờ phiên, kết nối, đánh giá theo mốc và đối chiếu REST. Muốn phát lại với ngưỡng khác thì phải thu trên máy.
- `.\SSI_V3.ps1 -Lenh danhgia`: kiểm tra lại ngưỡng bằng phân vị khoảng cập nhật, ghi căn cứ cho ngưỡng tối thiểu 10 mã.
- ~~Khối ngoại có gồm giao dịch thỏa thuận không~~: đã xác minh là có, xem [kết quả](evidence/v3_history/KHOI_NGOAI_THOA_THUAN.md).
- `SSI_SEMANTICS_VERIFIED`: đủ 5/5 điều kiện ở mục 4 của [hướng dẫn V3](docs/V3_KET_NOI.md). Đơn vị, giá trị khớp và khối ngoại đã có từ đối chiếu ngày 09/11. Cờ `ATC` có ngày 09/11 và 10/11, cờ `LO` có lúc 13:00 ngày 10/11. Chưa có chênh âm lớn hơn 5 giây. Còn chờ người học quyết định bật.
- Ghi tên các mã báo `MISSING_FIELDS` vào bản tóm tắt. Hiện chỉ có số đếm (1–3 mã mỗi mốc), nên chưa biết là mã ít giao dịch hay lỗi trường.
- Thêm `stream-window` vào `SSI_V3.ps1`, sửa đoạn mô tả giới hạn OTP đã cũ trong tài liệu.
- Thêm thanh khoản tương đối (so với trung bình 20 phiên của chính mã) khi đủ dữ liệu, vì điểm thanh khoản hiện gần như đo quy mô.

**2c. Lỗi mới ngày 10/11: SSI từ chối xác thực lúc 14:33**
- Lúc đổi token 14:33, bước lấy danh sách VN30 bị SSI từ chối (`AuthError`). Bộ thu coi đây là lỗi adapter và dừng hẳn. Bước đối chiếu REST sau đó cũng lỗi. Buổi chiều mất 14:33–15:05, gồm cả ATC.
- Không phải do token hết hạn: đo lại lúc 19:05, access token sống 900 giây, refresh token sống 8 giờ. Lúc đó không có lần chạy GitHub nào khác, và phiên làm việc với Claude cũng không chạy gì từ 14:20 đến 14:39. Có thể khóa đã được dùng đăng nhập ở nơi khác, hoặc SSI hủy phiên phía máy chủ. Chưa rõ nguyên nhân.
- **Đã sửa ngày 11/11 trong commit `c2d6660`:** với `--otp-mode none`, khi REST hoặc bước lấy/đổi token WebSocket bị từ chối xác thực, đăng nhập lại một lần rồi thử lại thao tác. Nếu xác thực vẫn thất bại, vô hiệu hóa phiên để bước đối chiếu cuối phiên cũng dừng gọi mạng. Lỗi xác thực khi lấy thành phần VN30 được chuyển thành `auth_failed` trong nhật ký và bản tóm tắt. Nhật ký chỉ ghi thông báo cố định.
- **Kiểm thử bản sửa:** 338/338 kiểm thử toàn dự án đạt, cùng lệnh `src.cli check`. Các ca mới bao gồm REST phục hồi thành công, đăng nhập lại thất bại, yêu cầu thử lại thất bại, token WebSocket hết hạn hoặc refresh bị từ chối, giữ loại lỗi SDK để worker dừng, giữ cách xử lý OTP `prompt`/`smart`, và thu từ kết nối lại qua SQLite với đủ 30 mã giả lập. Thử nghiệm offline, cần theo dõi hành vi SSI thật sau khi đưa bản sửa lên GitHub.
- Độ trễ chiều 10/11 cao hơn buổi sáng: QUOTE p99 26,8 giây (sáng tối đa 1,9 giây), TRADE p99 22,1 giây. Chưa rõ lý do; cần xem buổi chiều các ngày sau có lặp lại không.

**3. Hoàn thiện bài nộp**
- Viết lại báo cáo PDF 8–12 trang theo khung 10 mục của đề, dùng [bản nháp V3](report/BO_SUNG_BAO_CAO_V3.md) và [cơ sở tài chính](report/CO_SO_PHUONG_PHAP.md). Đọc bài gốc trước khi trích chi tiết hơn bản nháp, vì các nguồn mới được đối chiếu qua tóm tắt.
- Chụp lại ảnh giao diện và quay lại video với dữ liệu thật.
- Đóng gói lại ZIP: cập nhật `package.py`, thêm wheel `ssi-sdk`, `httpx`, `httpcore`, cài lại trong môi trường sạch, chạy toàn bộ test, kiểm tra `.env` không nằm trong gói.
- Điền họ tên, MSSV, mã lớp và đặt tên tệp đúng quy cách.
- Rà README theo 5 mục đề yêu cầu: cài đặt, cấu hình, cách chạy, cấu trúc dữ liệu, giới hạn.
- Chuẩn bị bảo vệ: mục 13 của đề yêu cầu giải thích được mã, công thức và quyết định thiết kế.

**Phương án dự phòng:** nếu stream không xử lý kịp, sản phẩm vẫn nộp được bằng dữ liệu ngày thật, vì đề chấp nhận ít nhất 2 nhóm API thay cho luồng WebSocket. Khi đó báo cáo phải ghi rõ mô hình 4 yếu tố mới kiểm trên dữ liệu giả lập.

**Điểm chưa chắc chắn, chỉ kiểm được bằng dữ liệu thật:**
- cờ ATO và cờ `LO` lúc 09:15 chưa quan sát được, vì chưa lần thu nào bắt đầu trước 09:00. Đã thấy `LO` lúc 13:00 và `BREAK` lúc 11:30;
- `securitiesByBoard` trả 1 dòng theo quy luật nào. Đã gặp lúc 15:49, chưa gặp trong giờ giao dịch;
- nguyên nhân lỗi xác thực lúc 14:33 ngày 10/11 (mục 2c);
- `priceChangePercent` xử lý ngày giao dịch không hưởng quyền thế nào (`refPrice` đang trống, mẫu chưa có ngày như vậy).

**Chạy test trên máy này:** thư mục tạm mặc định của pytest bị chặn quyền, sinh lỗi `PermissionError` ở bước chuẩn bị. Thêm `-p no:cacheprovider --basetemp=<thư mục ghi được>`.
