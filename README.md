# Bộ lọc cổ phiếu VN30 đa yếu tố

Dashboard đồ án cuối kỳ môn Gói phần mềm 1, sử dụng **SSI FastConnect API V3**. Dự án xếp hạng tương đối các cổ phiếu trong rổ VN30, cho phép xem yếu tố nào đóng góp vào điểm của từng mã và giải thích vì sao một mã chưa đủ dữ liệu để xếp hạng.

**[Mở bản demo web](https://cuoiki.vercel.app/)** · [Tài liệu SSI FastConnect](https://developers.ssi.com.vn/) · [Phương pháp chấm điểm](report/CO_SO_PHUONG_PHAP.md)

## Tính năng

- **Xếp hạng** theo phiên, trọng số và cách tính khối ngoại. Có bộ lọc Top 5, mã tăng hạng và mã chưa xếp hạng, cùng chi tiết điểm từng yếu tố và xuất CSV.
- **Biểu đồ** giá và khối lượng theo mã. Khung ngày hỗ trợ khoảng xem 1, 5 và 10 năm tùy lịch sử SSI cung cấp. Khung 5 phút có thể tải thêm nến cũ trong phạm vi một năm gần nhất. Cuộn chuột hoặc chụm hai ngón để thu phóng, kéo ngang để đổi đoạn đang xem.
- **Lịch sử hạng và kiểm chứng** giúp theo dõi biến động thứ hạng qua các phiên và xem kết quả khi đổi trọng số, bỏ một yếu tố hoặc thiếu dữ liệu.
- **Chất lượng dữ liệu** cho biết mốc phân tích và lý do từng mã chưa có hạng. Bản cục bộ có dữ liệu minh họa và chế độ phát lại nhật ký SSI.

## Cài đặt và chạy trên Windows

Cần **CPython 3.13 x64** và PowerShell. Nếu dùng Git, tải mã nguồn bằng hai lệnh bên dưới. Nếu đã có thư mục dự án hoặc gói nộp, mở PowerShell tại thư mục chứa `RUN_APP.ps1`.

```powershell
git clone https://github.com/MasonTahieu/Goi1-CuoiKi.git
Set-Location Goi1-CuoiKi
```

Cài thư viện rồi mở dashboard. Các script dùng môi trường Python tại `~/.venv` theo mặc định. Script cài đặt dùng thư mục `offline_wheels/` khi gói có kèm thư mục này. Bản tải từ GitHub cần kết nối mạng ở bước cài thư viện.

```powershell
.\CAI_THU_VIEN.ps1
.\RUN_APP.ps1
```

Mở [dashboard cục bộ](http://127.0.0.1:8501/). Chọn một nguồn **Minh họa** để thử giao diện mà không cần khóa SSI. Để xem bảng xếp hạng bằng dữ liệu SSI đi kèm kho mã, chạy hai lệnh dưới đây trong một cửa sổ PowerShell tại thư mục dự án.

```powershell
$env:SSI_DAILY_DATABASE = 'webdata/ssi_daily.sqlite'
.\RUN_APP.ps1
```

## Sử dụng dashboard

1. Chọn **Cuối ngày · SSI thật** và mốc phiên cần xem.
2. Mở **Xếp hạng**, chọn trọng số và đơn vị dòng tiền ngoại theo giá trị hoặc khối lượng. Bấm một mã để xem điểm thành phần và lý do xếp hạng.
3. Mở **Biểu đồ** để xem nến và khối lượng của mã đó. Với khung 5 phút, dùng **Tải nến cũ hơn** để mở rộng khoảng xem. Nhấp đúp biểu đồ để đặt lại mức thu phóng.
4. Mở **Lịch sử hạng** để so sánh các phiên hoặc **Kiểm chứng** để xem kết quả của đúng cấu hình đang chọn.

### Kết nối SSI trên máy cá nhân

Biểu đồ nến lấy dữ liệu từ SSI FastConnect theo mã và khoảng xem, rồi giữ nến trong bộ nhớ trình duyệt để vẽ và thu phóng. Bảng xếp hạng cuối ngày đọc được từ kho SQLite đã có, kể cả khi ngoại tuyến.

Nếu chưa có `.env`, sao chép [`.env.example`](.env.example) thành `.env`. Đặt `DATA_PROVIDER=ssi`, `SSI_API_PROFILE=fastconnect_v3` và điền `SSI_API_KEY`, `SSI_API_SECRET` do SSI cấp. Giữ `.env` trên máy cá nhân.

```powershell
.\SSI_V3.ps1 -Lenh kiemtra
.\SSI_V3.ps1 -Lenh lichsu -SoPhien 15
```

Lệnh đầu kiểm tra cấu hình mà không gọi SSI. Lệnh sau lấy dữ liệu tổng hợp cuối ngày và mặc định lưu ở `runtime/ssi_daily.sqlite`. Biến môi trường `SSI_DAILY_DATABASE` cho phép chọn kho khác. [Hướng dẫn kết nối FastConnect V3](docs/V3_KET_NOI.md)

## Phương pháp và phạm vi

| Phương pháp | Dữ liệu và yếu tố | Cách sử dụng |
| --- | --- | --- |
| **Cuối ngày** (`daily-v2`) | REST `securitiesSummary`. Động lượng từ giá mở cửa đến giá đóng cửa, thanh khoản theo giá trị khớp và cân bằng mua–bán khối ngoại `(mua − bán) / (mua + bán)`. | Bảng xếp hạng trên bản web, với trọng số cân bằng hoặc ưu tiên động lượng. |
| **Trong phiên** (`intraday-v1`) | Nhật ký SSI WebSocket. Động lượng, thanh khoản, dòng tiền ngoại và mất cân bằng cung–cầu từ sổ lệnh. | Phạm vi thử nghiệm và phát lại. Để chấm trên dữ liệu trong phiên cần đủ dữ liệu và đáp ứng điều kiện chất lượng. |

Điểm mỗi yếu tố là phân vị trong tập mã đủ điều kiện tại cùng mốc. Điểm tổng là tổng có trọng số của các điểm thành phần. Mỗi nhóm cần ít nhất 10 mã hợp lệ. Mã thiếu yếu tố bắt buộc đứng ở trạng thái **Chưa xếp hạng**. Điểm hỗ trợ sàng lọc danh sách theo dõi. Kết quả kiểm chứng phiên kế tiếp mang tính mô tả và chưa xác lập khả năng dự báo. [Đặc tả và giới hạn phương pháp](report/CO_SO_PHUONG_PHAP.md)

## Cấu trúc thư mục

| Vị trí | Nội dung |
| --- | --- |
| [`src/ssi_api/`](src/ssi_api/) | Kết nối FastConnect, thu thập REST và WebSocket, giải mã, phát lại và truy vấn nến. |
| [`src/data/`](src/data/) | Kho SQLite, chuẩn hóa dữ liệu, kiểm tra chất lượng và dữ liệu minh họa. |
| [`src/ranking/`](src/ranking/) và [`src/analytics/`](src/analytics/) | Tính điểm, xếp hạng và kiểm chứng phương pháp qua nhiều phiên. |
| [`src/web/`](src/web/) và [`api/`](api/) | Máy chủ Python, giao diện HTML/CSS/JavaScript và điểm vào Vercel. |
| [`webdata/`](webdata/) | Kho SSI cuối ngày và kết quả kiểm chứng tính sẵn cho bản web. |
| [`tests/`](tests/) và [`evidence/`](evidence/) | Kiểm thử tự động, dữ liệu tái lập và bằng chứng thực nghiệm. |
| [`docs/`](docs/) và [`report/`](report/) | Hướng dẫn kỹ thuật, cơ sở phương pháp và kịch bản trình diễn. |

## Kiểm thử và tái lập

Sau khi cài thư viện, chạy kiểm tra cấu hình dự án và bộ kiểm thử cục bộ. Lệnh này không cần khóa SSI.

```powershell
.\CHECK_PROJECT.ps1
```

Để tái lập kiểm chứng theo giá trị khối ngoại từ bộ dữ liệu cố định, kích hoạt môi trường Python rồi chạy hai lệnh sau.

```powershell
& "$HOME\.venv\Scripts\Activate.ps1"
python -m src.cli validate-daily --input-json evidence/daily_v2/value/input_daily.json --foreign value --output runtime/reproduce_daily_v2
```

Xem [bằng chứng theo giá trị](evidence/daily_v2/value/KIEM_TRA_PHIEN_KE_TIEP.md), [bằng chứng theo khối lượng](evidence/daily_v2/volume/KIEM_TRA_PHIEN_KE_TIEP.md) và [hướng dẫn kiểm thử toàn tuyến](docs/TASK_6_KIEM_THU_TOAN_TUYEN.md).

## Triển khai và cập nhật dữ liệu

Vercel phục vụ bản web và đọc kho `webdata/ssi_daily.sqlite` cùng kết quả kiểm chứng từ kho mã. Biểu đồ nến cần `SSI_API_KEY` và `SSI_API_SECRET` riêng trong cấu hình Vercel. GitHub Actions dùng cùng tên biến trong **GitHub Secrets** để thu thập dữ liệu.

- **SSI daily summaries** đặt lịch lúc **15:20, 15:50 và 16:20** giờ Việt Nam từ thứ Hai đến thứ Sáu. Workflow lấy lại 15 phiên gần nhất và cập nhật kho dữ liệu cùng kết quả kiểm chứng. Có thể chạy tay bằng **Run workflow**. [Workflow dữ liệu cuối ngày](.github/workflows/ssi-daily.yml)
- **SSI stream capture** thường được khởi động bằng **Run workflow**. Để trống số giây để thu theo khung **08:55–11:35** hoặc **12:55–15:05** giờ Việt Nam. Bản tóm tắt thu thập được lưu trong kho mã. [Workflow thu trong phiên](.github/workflows/ssi-stream.yml) · [Bản tóm tắt](evidence/v3_sessions/stream/)

Xem [hướng dẫn triển khai và vận hành](docs/TRIEN_KHAI_VERCEL.md) và [ghi chú bàn giao](HANDOFF.md). Trao đổi về lỗi hoặc đề xuất tại [GitHub Issues](https://github.com/MasonTahieu/Goi1-CuoiKi/issues).
