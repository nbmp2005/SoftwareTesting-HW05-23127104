# Kịch bản Video Demo – HW05 AI-Assisted Performance Testing
**Nguyễn Bình Minh Phương – 23127104**

> **Video đã xuất bản:** [https://youtu.be/6lmRExvkqj4](https://youtu.be/6lmRExvkqj4) — metadata YouTube xác nhận thời lượng 6:31 ngày 03/09/2026.
>
> **Cập nhật sau khi quay:** Stress và Spike đã được rerun bằng UUID ngày 03/09/2026, đều 0% lỗi. Các con số lỗi trong lời thoại bên dưới mô tả attempt pre-fix được quay trong video; kết quả canonical mới nằm tại `results/rerun-uuid-20260903/` và `report/MAIN_REPORT.md`.

---

## CHUẨN BỊ CHUNG TRƯỚC KHI BẬT RECORD

| Hạng mục | Trạng thái cần đạt |
|---|---|
| Backend EShop | Đang chạy: `node server.js` tại port 3000 |
| Database | Đã seed lại về trạng thái gốc |
| Task Manager | Mở tab **Performance** → CPU + Memory, thu nhỏ chiếm nửa màn hình bên phải |
| Terminal | Chiếm nửa màn hình bên trái, `cd` vào thư mục repo |
| JMeter | Đường dẫn thật: `C:\Users\cpshc\Downloads\apache-jmeter-5.6.3\apache-jmeter-5.6.3\bin\jmeter.bat` |
| OBS/phần mềm quay | Output 1920x1080, test audio trước |
| Thông báo | Đã tắt (Do Not Disturb) |

> **Quy ước trong file này:**
> - `[HÀNH ĐỘNG]` = bạn làm gì trên màn hình
> - `"..."` = lời thoại nói ra mic
> - Số liệu đã được điền thật từ raw JTL — không cần thay lại

---

## ĐOẠN 0 — Giới thiệu (0:00–0:50)

**Bố trí màn hình:** Desktop tổng quan — terminal backend bên trái, Task Manager bên phải.

---

**Lời thoại mẫu:**

"Xin chào thầy cô. Em là Nguyễn Bình Minh Phương, MSSV 23127104.
Video này demo bài HW05 – AI-Assisted Performance Testing cho hệ thống EShop.

Em sẽ chạy bốn scenario: Load, Stress, Spike và Soak, trên cùng một workflow quản trị gồm sáu bước:
Login admin → GET danh sách users → GET danh sách coupons → POST tạo category → POST tạo product → POST tạo coupon.
Đây là Workflow 5 – Admin Catalog & Promo Operations."

[Chỉ vào terminal backend]

"Đây là backend EShop đang chạy ở port 3000."

[Chỉ vào Task Manager]

"Và đây là Task Manager để theo dõi CPU và RAM song song trong suốt video."

---

## ĐOẠN 1 — Walkthrough JMX (0:50–1:50)

**Bố trí màn hình:** Mở JMeter GUI → File → Open → chọn `jmeter/23127104_Load_20260830.jmx`. Panel cây bên trái sẽ hiện ra danh sách các node.

---

**Lời thoại mẫu + hướng dẫn click từng bước:**

"Trước khi chạy, em giới thiệu nhanh cấu trúc test plan để thầy cô thấy em đã thiết kế gì."

---

**Bước 1** — [Click vào node **"HTTP Request Defaults"** trong cây bên trái]

"Đây là HTTP Request Defaults — ô Server Name đang là `localhost`, Port `3000`. Tất cả sampler bên dưới sẽ tự dùng địa chỉ này, không cần gõ lại từng cái."

---

**Bước 2** — [Click vào node **"CSV - admin credentials (recycle)"**]

"Đây là CSV Data Set Config — đọc file `test-data/admin_credentials.csv`. Hai cột là `credential_email` và `credential_password`. Recycle đang bật — khi hết dòng CSV thì đọc lại từ đầu. Sharing mode là All threads — tất cả virtual user chia sẻ chung một con trỏ đọc file."

---

**Bước 3** — [Click vào node **"Load: 10 VU CANDIDATE, ramp 30s, hold 5min"**]

"Đây là Thread Group — **10 virtual user**, ramp-up **30 giây**, tổng duration **330 giây** (~5,5 phút). Loop là -1 tức là lặp vô hạn trong khoảng thời gian scheduler cho phép."

---

**Bước 4** — [Expand Thread Group → click vào **"1 - Login admin"**]

"Sampler đầu tiên: POST tới `/api/login`, body JSON gồm email và password lấy từ CSV. Bên dưới nó có một node con tên **'Extract token'** — đó là JSON Extractor, lấy giá trị `$.token` từ response và lưu vào biến `token` để các bước sau dùng."

---

**Bước 5** — [Click vào **"2 - GET admin users"**]

"Sampler thứ hai: GET `/api/admin/users`. Lúc này Authorization header đã mang `Bearer ${token}` — token vừa lấy ở bước 1."

---

**Bước 6** — [Click vào **"4 - POST create category"**]

"Sampler tạo category: POST `/api/categories`. Bên dưới có **'Extract category_id'** — JSON Extractor lấy `$.id` từ response lưu vào `category_id`. Bước tạo product ngay sau sẽ dùng `category_id` này trong body."

---

**Bước 7** — [Click vào **"Summary Report"** — node ở gần cuối cây, ngoài Thread Group]

"Đây là listener **Summary Report** — listener type 1 trong ba loại khác nhau mà em dùng xuyên ba scenario. Khi chạy non-GUI thì listener này sẽ không ghi ra màn hình nhưng dữ liệu vẫn được lưu vào file JTL."

---

**Nói thêm về Human Review (không cần bấm thêm):**

"Khi AI đề xuất test plan, bản gốc thiếu hai thứ quan trọng: không có listener nào được thêm vào, và không có Response Assertion nào cho các bước tạo dữ liệu như create category, create product, create coupon. Em đã tự bổ sung cả hai. Mỗi sampler quan trọng hiện đều có node **'Assert ... 200'** bên dưới — đó là Response Assertion kiểm tra HTTP 200."

---

## ĐOẠN 2 — Load Test (1:50–3:30)

**Bố trí màn hình:** Terminal bên trái (chiếm 60%), Task Manager bên phải (chiếm 40%).

---

**Lời thoại mẫu:**

"Bây giờ em chạy Load test. File test plan tên `23127104_Load_20260830.jmx`, cấu hình: **10 virtual user, ramp-up 30 giây, giữ tải ổn định khoảng 5 phút.**"

[Bấm Enter chạy lệnh — để camera thấy rõ dòng lệnh:]

```powershell
C:\Users\cpshc\Downloads\apache-jmeter-5.6.3\apache-jmeter-5.6.3\bin\jmeter.bat -n `
  -t jmeter/23127104_Load_20260830.jmx `
  -Jrun_id=demo01 `
  -l results/demo/load/23127104_Load_demo.jtl `
  -e -o results/demo/load/html-report
```

"Trong lúc chạy, thầy cô có thể thấy song song Task Manager bên phải — CPU và RAM đang tăng theo tải đang được tạo ra."

[Chờ chạy xong — nếu muốn tua nhanh phần giữa thì giữ nguyên đoạn đầu và đoạn cuối khi kết quả hiện ra]

"Test đã chạy xong. Em mở HTML report vừa sinh ra."

[Chuyển sang trình duyệt, mở `results/demo/load/html-report/index.html`]

"Kết quả Load test lần này:
- Tổng số mẫu: **2.483**
- Error rate: **0,00%** — không có lỗi nào
- Throughput: **7,55 request/giây**
- p95: **17 mili giây** (p90: 14ms, p99: 21ms)

Toàn bộ response đều là HTTP 200. Kết quả nhất quán với lần chạy tháng 8 (2.516 samples, p95 17ms) — hệ thống ổn định hoàn toàn ở mức 10 VU."

---

## ĐOẠN 3 — Stress Test (3:30–5:00)

**Bố trí màn hình:** Terminal bên trái + Task Manager bên phải. Sau khi chạy xong chuyển sang file JSON hoặc Aggregate Report.

---

**Lời thoại mẫu:**

"Tiếp theo là Stress test, tăng tải theo 5 bậc: **10, 20, 30, 40, 50 virtual user**, mỗi bậc giữ 140 giây (ramp 20s + hold 120s). Listener type 2 dùng cho scenario này là **Aggregate Report**."

[Chạy lệnh — để camera thấy Task Manager tăng theo từng bậc:]

```powershell
C:\Users\cpshc\Downloads\apache-jmeter-5.6.3\apache-jmeter-5.6.3\bin\jmeter.bat -n `
  -t jmeter/23127104_Stress_20260830.jmx `
  -Jrun_id=demo02 `
  -l results/demo/stress/23127104_Stress_demo.jtl `
  -e -o results/demo/stress/html-report
```

[Chờ chạy hoặc dùng kết quả có sẵn từ `results/23127104_Stress_20260830_analysis.json`]

[Mở Aggregate Report hoặc JSON analysis]

"Đây là điểm cần phân tích kỹ. Bậc 1 ở **10 VU: 0% error, p95 16ms — ổn định**.
Từ bậc 2 trở đi, error rate tăng đột ngột lên **8,09% ở 20 VU**, rồi 10,93%, 12,23%, 13,06% ở các bậc cao hơn.

Tuy nhiên — đây là phát hiện quan trọng của human review — **toàn bộ 1.680 failures đều tập trung ở bước POST create coupon, là HTTP 500, không phải do hệ thống bị quá tải.**

Bằng chứng: số coupon failures của từng bậc 2–5 lần lượt là **167, 338, 504, 671** — khớp chính xác với số coupon đã tạo thành công ở bậc ngay trước đó. Đây là dấu hiệu counter coupon bị reset giữa các Thread Group, dẫn đến code bị trùng lặp.

Vì vậy, bậc cao nhất thật sự ổn định theo HTTP/JTL là **bậc 1 — 10 VU**. Kết quả Stress bậc 2–5 bị vô hiệu do lỗi test-data. Em đã ghi bug này vào GitHub Issues."

[Mở browser, truy cập `https://github.com/nbmp2005/SoftwareTesting-HW05-23127104/issues/2`]

"Đây là **BUG-STRESS-001** — tại thời điểm quay, fix UUID chưa được rerun. Sau video, rerun đã xác nhận 15.397 samples và 0 lỗi."

---

## ĐOẠN 4 — Spike Test (5:00–6:15)

**Bố trí màn hình:** Terminal + Task Manager. Sau chạy xong mở 3 file phase JSON.

---

**Lời thoại mẫu:**

"Spike test mô phỏng tải tăng đột biến: baseline **8 VU trong 65 giây**, tăng vọt lên **40 VU trong 8 giây rồi giữ 45 giây**, sau đó giảm về **8 VU để quan sát phục hồi**. Listener type 3 dùng ở đây là **View Results Tree** — dùng khi debug GUI."

[Chạy lệnh:]

```powershell
C:\Users\cpshc\Downloads\apache-jmeter-5.6.3\apache-jmeter-5.6.3\bin\jmeter.bat -n `
  -t jmeter/23127104_Spike_20260830.jmx `
  -Jrun_id=demo03 `
  -l results/demo/spike/23127104_Spike_demo.jtl `
  -e -o results/demo/spike/html-report
```

"Thầy cô có thể thấy Task Manager tăng vọt ngay khi vào pha spike 40 VU, rồi giảm dần khi quay về baseline."

[Mở `results/spike-phase-analysis/pre-spike_analysis.json`]

"Phase pre-spike 8 VU: **393 samples, 0 failures** — hoàn toàn ổn định."

[Mở `results/spike-phase-analysis/spike_analysis.json`]

"Phase spike burst 40 VU: **1.545 samples, 63 failures** — lỗi ở coupon."

[Mở `results/spike-phase-analysis/recovery_analysis.json`]

"Phase recovery 8 VU: **394 samples, 63 failures. Toàn bộ 63 coupon request trong phase này đều lỗi.**

Pattern: 63 coupon đã tạo ở pre-spike → counter reset khi sang Thread Group recovery → 63 code cũ bị dùng lại. Đây xác nhận là **data collision, không phải SUT chưa phục hồi được**.

Sau khi quay, rerun UUID đã xác nhận burst và recovery đều 0 lỗi; recovery p95 20 ms."

[Mở `https://github.com/nbmp2005/SoftwareTesting-HW05-23127104/issues/1`]

"Bug được ghi tại **BUG-SPIKE-001**."

---

## ĐOẠN 5 — Soak/Endurance Test (6:15–7:15)

**Bố trí màn hình:** Terminal + Task Manager. Giữ 3 mốc chụp screenshot: đầu, giữa (~phút 6), cuối. Có thể tua nhanh đoạn giữa.

---

**Lời thoại mẫu:**

"Cuối cùng là Soak test — giữ tải ổn định **10 VU liên tục trong 12 phút** để tìm ngưỡng chịu tải bền vững của máy em."

[Chạy lệnh:]

```powershell
C:\Users\cpshc\Downloads\apache-jmeter-5.6.3\apache-jmeter-5.6.3\bin\jmeter.bat -n `
  -t jmeter/23127104_Soak_20260830.jmx `
  -Jrun_id=demo04 `
  -l results/demo/soak/23127104_Soak_demo.jtl `
  -e -o results/demo/soak/html-report
```

[Quay 3 mốc — chụp/đọc Task Manager tại từng mốc:]

"Đây là tài nguyên lúc bắt đầu: CPU khoảng **10%**, RAM khoảng **12,6 GB đang dùng / 15,7 GB total (80%)**.

[Tua nhanh đoạn giữa — giữ nguyên tốc độ tại mốc giữa phút 6]

Giữa run (~phút 6): CPU vẫn khoảng **10%**, RAM không tăng đáng kể.

[Tiếp tục đến cuối]

Cuối run: CPU **10%**, RAM ổn định — không có xu hướng tăng liên tục không dừng."

[Mở `results/23127104_Soak_20260830_analysis.json` + 3 window JSON]

"Kết luận:
- Whole-run: **5.634 samples, 0 failures, 0% error**
- Throughput ổn định: **7,84 RPS**
- p95 ba cửa sổ thời gian: **17ms / 17ms / 17ms** — không drift

Hệ thống của em ổn định ở mức **7,84 RPS**, RAM không tăng liên tục nên không có dấu hiệu memory leak rõ ràng trong 12 phút test — đây là ngưỡng endurance đo được trên phần cứng của em."

> **Lưu ý trung thực khi trình bày:** "Tuy nhiên, do chỉ có một snapshot resource tại phút 4 chứ không có trend liên tục, em chưa thể tuyên bố đây là threshold tuyệt đối — cần thu resource time series đầy đủ để xác nhận."

---

## ĐOẠN 6 — Task 2: AI Misinterpretation Hunt (7:15–8:00)

**Bố trí màn hình:** Mở `results/23127104_Load_20260830_analysis.json` song song với báo cáo hoặc bản nháp AI cũ.

---

**Lời thoại mẫu:**

"Task 2 yêu cầu dùng AI phân tích kết quả, rồi human review phát hiện lỗi. Đây là điểm AI sai trong bản nháp cũ:"

[Chỉ vào claim cũ của AI / trích trong report]

"AI claim p95 Load là **25,5ms** và gọi `GET coupons` là bottleneck vì max 34ms."

[Mở JSON, chỉ vào `__overall__.elapsed_ms.p95`]

"Raw JTL cho p95 overall là **17ms**. AI sai **8,5ms — tương đương 50% so với giá trị đúng.**"

[Chỉ vào `GET coupons` row]

"p95 của `GET coupons` chỉ là **9ms**. Max 34ms là outlier đơn lẻ — AI nhầm max với bottleneck. Bottleneck thật cần resource time series và server profiler, không chỉ client-side latency."

---

## ĐOẠN 7 — Tổng kết (8:00–8:30)

**Bố trí màn hình:** Desktop tổng quan — Task Manager + terminal.

---

**Lời thoại mẫu:**

"Tóm lại:
- **Load**: 10 VU, 0% lỗi, p95 17ms — ổn định.
- **Stress pre-fix trong video**: 5 bậc, 1.680 lỗi HTTP 500 do data collision; UUID rerun sau video có 0 lỗi.
- **Spike pre-fix trong video**: 126 lỗi coupon do counter reset; UUID rerun sau video có 0 lỗi và đạt recovery criteria.
- **Soak**: 12 phút, 0% lỗi, p95 17ms ổn định — ngưỡng endurance đo được là 7,84 RPS.

Bài học lớn nhất: **mọi claim AI phải truy ngược về raw JTL và cấu hình JMX**. Error rate cao không tự động nghĩa SUT bị overload — phải phân tích pattern dữ liệu trước khi kết luận.

Cảm ơn thầy cô đã xem. Em là Nguyễn Bình Minh Phương, MSSV 23127104."

---

## CHECKLIST HẬU KỲ

- [x] Video >= 6 phút (metadata: 6:31)
- [ ] JMeter/terminal + Task Manager visible cùng frame khi đang chạy test
- [ ] Đã quay đủ 3 mốc resource cho Soak (đầu, giữa, cuối)
- [ ] Mở link bằng cửa sổ ẩn danh để xác nhận privacy **Unlisted** và audio tiếng Việt rõ
- [x] Cập nhật link YouTube vào `README.md` và `report/MAIN_REPORT.md` (Mục 16)
- [x] Cập nhật `report/SUBMISSION_CHECKLIST.md`
- [ ] Commit cuối: `docs: add demo video links`
