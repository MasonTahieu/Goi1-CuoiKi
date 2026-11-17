# Triển khai miễn phí: Vercel + GitHub Actions

Sau khi làm theo hướng dẫn này, hệ thống vẫn chạy khi máy bạn tắt và không cần thẻ:

```text
GitHub Actions (15:20, thứ Hai–thứ Sáu)
   └─ lấy dữ liệu ngày của 30 mã VN30 từ SSI (REST, không cần OTP) ─▶ commit webdata/ssi_daily.sqlite
                                                                    │ push
Vercel (tự triển khai lại khi có commit) ◀──────────────────────────┘
   └─ trang web: Cuối ngày · SSI thật
```

| Tệp | Vai trò |
|---|---|
| `api/index.py` | Hàm Python trên Vercel. Dùng lại đúng bộ xử lý của `src/web/server.py` |
| `vercel.json` | Chuyển mọi đường dẫn về hàm trên; đóng gói `src/` và `webdata/` |
| `requirements.txt` | Phụ thuộc gọn cho Vercel và CI: pandas, numpy, python-dotenv, requests, tzdata |
| `requirements-ci.txt` | Thêm `ssi-sdk` cho workflow lấy dữ liệu |
| `requirements-local.txt` | Bộ đầy đủ cho máy cá nhân (Streamlit, pytest, SDK) |
| `.python-version` | Python 3.12 trên Vercel |
| `.vercelignore` | Không đưa `.env`, `runtime/`, test, tài liệu và giao diện Streamlit lên Vercel |
| `.github/workflows/ssi-daily.yml` | Lịch lấy dữ liệu ngày, đánh giá nhiều phiên, commit kết quả |
| `webdata/ssi_daily.sqlite` | Dữ liệu ngày thật (đã có sẵn 10 phiên từ 26/10 đến 06/11) |
| `webdata/validation.json` | Kiểm chứng tính trước cho bốn cấu hình; kiểm SHA-256 dữ liệu và mã trước khi dùng |

## Bước 0. Nên làm trước

1. **Thu hồi khóa SSI cũ và tạo khóa mới** trên Developer Portal, vì khóa cũ đã được dán vào chat. Sửa `SSI_API_KEY` và `SSI_API_SECRET` trong `.env` trên máy.
2. Tạo tài khoản [GitHub](https://github.com) và đăng nhập [Vercel](https://vercel.com) bằng chính tài khoản GitHub đó. Cả hai miễn phí, không cần thẻ.

## Bước 1. Repo trên GitHub (đã xong)

Repo [MasonTahieu/Goi1-CuoiKi](https://github.com/MasonTahieu/Goi1-CuoiKi), nhánh `main`, đang để **công khai**.

| | Công khai (hiện tại) | Riêng tư |
|---|---|---|
| Ai xem được mã và `webdata/` | Mọi người | Chỉ bạn và người được mời |
| Phút GitHub Actions | Không giới hạn, đủ cho thu stream cả phiên sau này | 2.000 phút/tháng, chỉ đủ cho job cuối ngày |
| Dữ liệu SSI | Công khai trong repo; điều khoản FastConnect cấp dữ liệu cho chủ tài khoản | Không lộ ra ngoài |

Đổi chế độ: **Settings → General → Danger Zone → Change repository visibility**. Khóa SSI nằm trong GitHub Secrets nên không lộ ở chế độ nào.

## Bước 2. Đẩy mã nguồn lên (đã xong)

Lần đầu đã được đẩy lên từ máy này. Đã kiểm 177 tệp: không có `.env`, không có `runtime/`, không tệp nào chứa giá trị khóa trong `.env`.

Thư mục dự án thuộc một tài khoản Windows khác, nên git báo `dubious ownership`. Khi tự chạy git tại đây, thêm ngoại lệ một lần:

```powershell
git config --global --add safe.directory "E:/Gói phần mềm 1/Cuối kì/neo-vn30-screener"
```

Sau đó, mỗi lần sửa mã: `git add .`, kiểm `git status` không có `.env`, rồi `git commit` và `git push`. Trước khi push nên chạy `git pull --rebase`, vì workflow hằng ngày cũng commit dữ liệu lên `main`.

## Bước 3. Thêm khóa SSI vào GitHub Secrets

Trong repo, vào **Settings → Secrets and variables → Actions → New repository secret** và tạo hai secret:

| Tên | Giá trị |
|---|---|
| `SSI_API_KEY` | API Key (bản mới) |
| `SSI_API_SECRET` | API Secret (bản mới) |

**Không** thêm Private Key. Dự án không dùng khóa đó.

## Bước 4. Chạy thử workflow một lần

1. Sau khi SSI công bố tổng hợp phiên, mở [SSI daily summaries](https://github.com/MasonTahieu/Goi1-CuoiKi/actions/workflows/ssi-daily.yml), chọn **Run workflow → main**.
2. Mở lượt chạy và kiểm tra bước **Fetch the last 15 sessions** có ngày cần dùng. Nếu có dữ liệu mới, workflow commit kho và kết quả Kiểm chứng, sau đó Vercel triển khai lại.
3. Khi Vercel báo **Ready**, mở [website](https://cuoiki.vercel.app), bấm **Kiểm tra lại** nếu đang có cảnh báo và đối chiếu ngày phiên trên bảng. Workflow xanh nhưng chưa có ngày cần dùng thì xem lại ngày SSI trả về.

## Bước 5. Triển khai trên Vercel

1. Trên Vercel, chọn **Add New → Project** và **Import** repo vừa tạo.
2. **Framework Preset:** `Other`. **Root Directory:** để trống (gốc repo). Không cần lệnh build.
3. **Environment Variables:**

   | Tên | Giá trị |
   |---|---|
   | `APP_MODE` | `demo` |
   | `DATA_PROVIDER` | `ssi` |
   | `SSI_DAILY_DATABASE` | `webdata/ssi_daily.sqlite` |
   | `SSI_API_PROFILE` | `fastconnect_v3` (entry point cũng chọn mặc định này trên Vercel) |
   | `SSI_OTP_MODE` | `none` |
   | `SSI_API_KEY` | API Key SSI, chỉ lưu phía máy chủ, cần cho tab nến |
   | `SSI_API_SECRET` | API Secret SSI, chỉ lưu phía máy chủ, cần cho tab nến |

   Bảng hạng và Kiểm chứng đọc dữ liệu đã lưu, không cần khóa. Tab **Biểu đồ** gọi SSI trực tiếp nên cần hai khóa trên Vercel (Production; thêm Preview nếu dùng bản xem trước), rồi redeploy. GitHub Secrets chỉ cấp cho workflow, không tự chuyển sang Vercel. Không đưa khóa vào `vercel.json`, JavaScript, Git hoặc log; không dùng Private Key.

   Khi nhập thủ công, chỉ dán giá trị của từng biến, không gồm tên biến, dấu `=` hoặc dấu nháy của cú pháp `.env`. Không chuyển khóa bằng cách đọc lại ô mật khẩu qua công cụ trình duyệt: công cụ có thể trả ký hiệu `<redacted>` thay cho khóa. Mã SSI `401105` có nghĩa API Key/Secret không hợp lệ; cần đối chiếu đúng cặp khóa trước khi kết luận vấn đề IP/quyền dữ liệu. Sau redeploy, kiểm tra tab nến; bảng hạng chạy được chưa chứng minh kết nối nến thành công.
4. Bấm **Deploy**. Xong sẽ có địa chỉ dạng `https://vn30-hnx30-screener.vercel.app`.
6. Mở địa chỉ đó. Trang chỉ phục vụ dữ liệu **Cuối ngày · SSI thật**. Bảng điểm giả lập và nhật ký SSI mẫu dùng cho chạy cục bộ.

## Hằng ngày diễn ra thế nào

- GitHub đặt lịch **15:20, 15:50 và 16:20, thứ Hai–thứ Sáu** theo giờ Việt Nam. Workflow lấy lại 15 phiên gần nhất, chạy lại đánh giá nhiều phiên rồi commit. Vercel cập nhật web khi bản mới sẵn sàng.
- Sau **16:30**, web nhắc nếu kho chưa có ngày làm việc gần nhất. Cảnh báo dùng lịch thứ Hai–thứ Sáu và ghi rõ ngày nghỉ có thể không có phiên.
- Workflow tạo lại `webdata/validation.json` sau mỗi đợt lấy dữ liệu. Cache không khớp dữ liệu/mã sẽ bị bỏ và tính lại; vì vậy cần chạy `python -m src.web.validation_cache --db webdata/ssi_daily.sqlite` nếu cập nhật thủ công.
- **Máy bạn không cần bật.** Repo riêng tư có 2.000 phút Actions miễn phí mỗi tháng; job này dùng khoảng 2 phút mỗi ngày.

## Lịch độc lập trên Cloudflare

Mã và cấu hình ở `ops/ssi-daily-trigger/`. Worker chạy vào **15:25 và 16:05**, thứ Hai–thứ Sáu, giờ Việt Nam. Mỗi lần nó xem phiên đang phục vụ. Nếu đã có đủ điểm 30 mã cho ngày đó, nó bỏ qua. Nếu còn thiếu, nó gọi đúng workflow `ssi-daily.yml` của nhánh `main`. Worker không mở URL công khai. Các lịch GitHub vẫn chạy dự phòng.

1. Tạo token GitHub loại **fine-grained**, chọn riêng repo `Goi1-CuoiKi` và quyền **Actions: Read and write**. Đặt ngày hết hạn phù hợp với thời gian dùng. [Quyền gọi Workflow Dispatch](https://docs.github.com/en/rest/actions/workflows?apiVersion=2026-03-10#create-a-workflow-dispatch-event)
2. Trong `ops/ssi-daily-trigger/`, đăng nhập CLI Cloudflare và triển khai Worker bằng `npx wrangler deploy`. Ngay sau đó chạy `npx wrangler secret put GITHUB_ACTIONS_TOKEN` và nhập token khi được hỏi. Khóa SSI tiếp tục nằm ở cấu hình hiện có.
3. Sau mốc đã đặt, kiểm tra log Worker có `dispatched` hoặc `already_published`. Với lượt `dispatched`, kiểm tra GitHub Actions và ngày phiên mới trên web. Lịch Cloudflare kích hoạt workflow, còn thời điểm hiển thị phụ thuộc vào lúc SSI có dữ liệu, hàng chờ GitHub và lần triển khai Vercel.

## Giới hạn hiện tại

- **Chưa thu stream trong phiên trên GitHub Actions.**
  - Việc này chờ smoke test thứ Hai: định dạng thật, có cần OTP không, quyền đăng ký topic.
  - Thu stream cả ngày dùng khoảng 5 giờ/ngày, vượt hạn mức 2.000 phút/tháng của repo riêng tư. Khi đó cần chuyển repo công khai và mã hóa dữ liệu, hoặc chọn cách khác. Sẽ quyết định sau smoke test.
- **Lịch có thể trễ hoặc bị bỏ qua:** nếu web còn thiếu phiên cần trình diễn, dùng quy trình **Run workflow** ở Bước 4. [Lịch GitHub Actions](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule)
- **Một phiên đăng nhập cho mỗi API Key:** tránh chạy lệnh SSI trên máy đúng lúc 15:20.
- **Địa chỉ Vercel là công khai:** ai có địa chỉ đều xem được. Nếu cần, có thể thêm mật khẩu sau.
