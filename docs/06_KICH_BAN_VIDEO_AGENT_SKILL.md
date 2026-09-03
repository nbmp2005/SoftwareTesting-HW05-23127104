# Kịch bản Video 2 — Demo Agent Skill Kit (end-to-end)
**Nguyễn Bình Minh Phương – 23127104**

---

## CHUẨN BỊ TRƯỚC KHI BẬT RECORD

| Hạng mục | Trạng thái cần đạt |
|---|---|
| Trình duyệt chat AI | Mở sẵn phiên chat mới với Gemini/Claude/ChatGPT |
| File Explorer | Mở sẵn thư mục `agent-skill-kit/` |
| VS Code | Mở sẵn repo HW05 |
| Các file JTL thật | `results/23127104_Load_20260830.jtl` tồn tại |
| Script Python | `agent-skill-kit/hw05-performance-testing/scripts/analyze_jtl.py` tồn tại |
| Terminal | Mở sẵn tại repo root |
| OBS | Output 1920x1080, test audio trước |

> **Quy ước:**
> - `[HÀNH ĐỘNG]` = làm gì trên màn hình
> - `"..."` = lời thoại nói ra mic
> - `>>> PROMPT >>>` = đoạn text copy-paste vào chat AI, đọc to trước khi gửi

---

## PHẦN A — Giới thiệu tổng quan bộ 4 skill (90–120 giây)

**Bố trí màn hình:** File Explorer mở `agent-skill-kit/`, lần lượt click mở từng thư mục khi nhắc tên.

---

[Chỉ vào thư mục `agent-skill-kit/` trong File Explorer]

"Video này em demo bộ 4 Agent Skill em tự xây cho toàn bộ quy trình performance testing của HW05. Thay vì 1 skill ôm hết mọi việc, em tách thành 4 skill chuyên trách, mỗi skill là một 'nhân vật' phụ trách đúng 1 giai đoạn."

[Click mở thư mục `jmeter-test-designer/`, mở `SKILL.md`]

"Một — **jmeter-test-designer**, Kỹ sư Thiết kế Workload. Thiết kế Load, Stress, Spike, Soak và sinh file JMX. Không sinh JMX trước khi em xác nhận rõ ràng từng bước."

[Click mở thư mục `perf-evidence-collector/`, mở `SKILL.md`]

"Hai — **perf-evidence-collector**, Điều tra viên Bằng chứng. Sau khi test chạy xong, nó kiểm kê evidence vật lý: JTL, screenshot, log. Không tin lời kể."

[Click mở thư mục `jtl-data-analyzer/`, mở `SKILL.md`]

"Ba — **jtl-data-analyzer**, Chuyên gia Phân tích Dữ liệu. Đọc JTL qua script Python — không đọc bằng mắt — tính metric và tự soi lại bài phân tích của chính mình để tìm lỗi."

[Click mở thư mục `submission-auditor/`, mở `SKILL.md`]

"Bốn — **submission-auditor**, Giám khảo Kiểm toán Cuối cùng. Trước khi nộp bài, nó kiểm tra chéo toàn bộ thư mục: report, JMX, log, ảnh — tìm chỗ không nhất quán. Chỉ đọc, không tự sửa."

"Bốn skill này nối tiếp nhau thành pipeline, và dùng chung một file `report-artifacts.md` làm bản đồ quy định rõ skill nào được sửa phần nào trong report, tránh ghi đè lên nhau."

---

## PHẦN B — DEMO SÂU: jmeter-test-designer (3–4 phút)

### B0 — Giới thiệu triết lý (30 giây)

**Bố trí màn hình:** VS Code mở `agent-skill-kit/jmeter-test-designer/SKILL.md`, cuộn qua phần "Trạng thái bắt buộc" và "Hard gates".

---

[Cuộn tới dòng `STEP_1_CONTEXT_APPROVED = false`]

"jmeter-test-designer có một state machine với 3 approval gate. Nhìn vào đây — có 6 cờ trạng thái, ban đầu tất cả là false. AI bị cấm tuyệt đối sinh file JMX hoặc đưa ra bất kỳ con số tải nào khi các cờ này chưa được bật."

[Cuộn tới phần Hard gates — Gate A]

"Đây là Gate A — danh sách những thứ bị cấm trước khi Bước 1 và 2 được duyệt. AI không được tự đoán endpoint, success code, số VU, ramp-up, hay threshold. Triết lý là: AI không giả định — thứ gì còn thiếu phải hỏi em, không được tự điền cho xong."

---

### B1 — Demo kích hoạt skill trực tiếp

**Bố trí màn hình:** Chuyển sang cửa sổ chat AI. Bật record terminal bên cạnh nếu cần.

---

"Bây giờ em demo trực tiếp. Em gõ prompt kích hoạt skill vào chat AI."

[Mở chat AI, copy-paste prompt sau — đọc to khi gõ:]

```
>>> PROMPT >>>
Kích hoạt skill jmeter-test-designer.

Ngữ cảnh: Em cần thiết kế JMeter test plan cho workflow quản trị EShop — Workflow 5.
SUT: http://localhost:3000 (Node.js backend, SQLite database).
Workflow gồm 6 bước theo thứ tự:
1. POST /api/login — đăng nhập admin, lấy JWT token
2. GET /api/admin/users — đọc danh sách users (cần Authorization: Bearer {token})
3. GET /api/coupons — đọc danh sách coupons
4. POST /api/categories — tạo category mới
5. POST /api/products — tạo product thuộc category vừa tạo
6. POST /api/admin/coupons — phát hành coupon với code duy nhất

Bắt đầu Bước 1: phỏng vấn SUT Context. Xuất bảng context đầy đủ, đánh dấu rõ ô nào còn MISSING hoặc CONFLICT cần em xác nhận.
```

[Gửi prompt — chờ AI phản hồi, để camera thấy AI xuất bảng SUT Context với các ô MISSING]

"Thầy cô thấy AI xuất ra bảng SUT Context — các ô chưa biết được đánh dấu MISSING. Skill bắt AI hỏi em trước thay vì tự bịa."


Duyệt SUT Context Bước 1.
```

[Chờ AI cập nhật trạng thái — camera thấy `STEP_1_CONTEXT_APPROVED = true`]

---

### B3 — Bước 2: Data Matrix (30 giây)

[Gửi prompt:]

```
>>> PROMPT >>>
Tiếp tục Bước 2: xuất Data Matrix — ai sinh dữ liệu, ai tiêu thụ, cách correlation giữa các bước.
```

[Chờ AI xuất bảng Data Matrix — camera thấy bảng token → category_id → product]

"Bảng này mô tả luồng correlation: token từ login vào header, category_id từ tạo category vào payload tạo product. Ở bước này AI vẫn chưa được đưa ra con số VU hay ramp-up."

[Gửi xác nhận:]

```
>>> PROMPT >>>
Duyệt Data Matrix Bước 2. Tiếp tục Bước 3.
```

---

### B4 — Bước 3: Workload Profile (30 giây)

[Chờ AI xuất bảng Profile Matrix 4 dòng Load/Stress/Spike/Soak]

"Bước 3 mới đưa ra con số tải — và chú ý: tất cả đều gắn nhãn CANDIDATE — CHƯA ĐO. AI không được gọi đây là threshold đo được."

[Gửi xác nhận:]

```
>>> PROMPT >>>
Duyệt Profile Matrix Bước 3. Sinh 4 file JMX: Load, Stress, Spike, Soak.
Kiểm tra: mỗi file phải có đủ HTTP sampler, CSV, listener khác loại nhau giữa 3 scenario, và không có stage bị chồng lấn về thời gian.
```

---

### B5 — Gate A bắt lỗi + sinh JMX thật (45 giây)

[Chờ AI sinh JMX và chạy validation]

"Skill không chỉ xuất file text — nó thực sự parse lại XML, đếm HTTP sampler, kiểm tra listener không lặp loại, in bảng timeline từng stage để em tự kiểm tra trước khi nhận file."

[Chỉ vào output validation của AI]

"Đây là bằng chứng Gate C được thực thi: không có file nào được sinh trước khi cả 3 approval gate đều qua. Mọi bước duyệt đều được ghi vào AI Audit Log — đây chính là nội dung bắt buộc ở mục 9 của đề."

---

## PHẦN C — 3 skill còn lại

### C1 — perf-evidence-collector (60–90 giây)

**Bố trí màn hình:** VS Code mở `agent-skill-kit/perf-evidence-collector/SKILL.md`.

---

[Cuộn tới phần Evidence Ledger — bảng trạng thái VERIFIED/MISSING]

"perf-evidence-collector — Điều tra viên Bằng chứng. Triết lý một câu: **có bằng chứng mới tin**. Nó duy trì Evidence Ledger, mỗi artifact chỉ có 5 trạng thái: VERIFIED, PRESENT–UNVERIFIED, MISSING, INVALID, hoặc NOT APPLICABLE."

[Cuộn tới phần "Cách hỏi bắt buộc"]

"Điểm đặc biệt: nó hỏi **từng mục một** — không được ném cả danh sách rồi để em tự chọn. Phải xác minh xong mục này mới hỏi mục tiếp."

[Chuyển sang chat AI, gửi prompt:]

```
>>> PROMPT >>>
Kích hoạt skill perf-evidence-collector.

Em đã chạy xong 4 scenario: Load, Stress, Spike, Soak.
Bắt đầu Checklist G — Global: kiểm tra phần cứng và môi trường.
Hostname máy: DESKTOP-J4TEK5A.
File evidence phần cứng: evidence/23127104_Hardware_20260830.png
```

[Chờ AI hỏi mục tiếp theo — để camera thấy nó hỏi từng mục một, không ném cả danh sách]

"Thầy cô thấy nó hỏi từng mục — đây là hành vi bắt buộc trong SKILL.md. Nó không tin lời em nói mà đòi path/link thật có thể kiểm tra."

[Gửi evidence Load:]

```
>>> PROMPT >>>
Evidence Load scenario:
- JMX: jmeter/23127104_Load_20260830.jmx
- JTL: results/23127104_Load_20260830.jtl (406579 bytes)
- HTML report: results/load-report/
- Resource screenshot: evidence/23127104_Load_Evidence_20260830.png
- CSV: test-data/admin_credentials.csv
```

---

### C2 — jtl-data-analyzer (60–90 giây)

**Bố trí màn hình:** VS Code mở `agent-skill-kit/jtl-data-analyzer/SKILL.md`.

---

[Cuộn tới Gate 1 — danh sách cấm]

"jtl-data-analyzer — Chuyên gia Phân tích Dữ liệu. Triết lý: **parser-first** — cấm AI đọc JTL bằng mắt rồi tự tính. Phải gọi script Python thật."

[Chuyển sang terminal + chat AI split-screen]

[Gửi prompt vào chat AI:]

```
>>> PROMPT >>>
Kích hoạt skill jtl-data-analyzer.

Phân tích Load JTL toàn run:
- JTL path: results/23127104_Load_20260830.jtl
- Script: agent-skill-kit/hw05-performance-testing/scripts/analyze_jtl.py

Bước 1: chạy lệnh parse, xác minh JSON output, sau đó báo cáo metric.
```

[Chờ AI gọi lệnh — camera thấy terminal chạy:]

```powershell
python -X utf8 agent-skill-kit/hw05-performance-testing/scripts/analyze_jtl.py `
  results/23127104_Load_20260830.jtl `
  --output results/23127104_Load_20260830_analysis.json
```

[Chờ AI xuất bảng metric từ JSON]

"AI đọc từ JSON output của script — không tự tính. Mọi con số đều kèm đường dẫn JSON path."

[Gửi tiếp để trigger misinterpretation hunt:]

```
>>> PROMPT >>>
Tiếp tục Bước 4: misinterpretation hunt.
Đối chiếu bài phân tích vừa viết với số liệu gốc trong JSON. Tìm chỗ nào AI vừa nói sai hoặc suy diễn quá đà, lập bảng delta cụ thể.
```

[Chờ AI tự tìm ra lỗi của mình và xuất bảng delta]

"Đây là phần ấn tượng nhất — AI tự kiểm toán lại chính bài phân tích của nó và báo cáo chỗ nó sai. Đây là nội dung Task 2 misinterpretation hunt của đề bài."

---

### C3 — submission-auditor (60 giây)

**Bố trí màn hình:** VS Code mở `agent-skill-kit/submission-auditor/SKILL.md`.

---

[Cuộn tới phần Severity — BLOCKER/ERROR/WARNING]

"submission-auditor — Giám khảo Kiểm toán Cuối cùng. Triết lý: **read-only, không tự sửa**. Nếu thấy lỗi, nó chỉ báo mức BLOCKER hay ERROR — tuyệt đối không tự điền TODO hay tạo file giả."

[Chuyển sang chat AI, gửi prompt:]

```
>>> PROMPT >>>
Kích hoạt skill submission-auditor.

Audit toàn bộ submission HW05. Bắt đầu từ:
Bước 1: quét TODO — dùng lệnh grep/rg tìm toàn project các chuỗi TODO, FIXME, REAL EVIDENCE REQUIRED.
Bước 2: so khớp phần cứng — đọc claim trong MAIN_REPORT.md Mục 4.1, đối chiếu với file evidence/23127104_Hardware_20260830.png.
Báo mọi lỗi với severity và artifact cụ thể.
```

[Chờ AI quét và xuất danh sách lỗi]

"Nó tìm ra những chỗ còn sót. Bây giờ em sửa ngay theo hướng dẫn nó báo."

[Sửa 1 lỗi nhỏ trực tiếp trên video nếu có — nếu audit sạch thì:]

"Verdict: READY FOR HUMAN FINAL REVIEW — không còn BLOCKER hay ERROR nào."

---

### C4 — Kết luận (15–20 giây)

**Bố trí màn hình:** Desktop tổng quan — 4 thư mục skill visible.

---

"Bốn skill này phối hợp thành một pipeline khép kín:
- Kỹ sư Thiết kế Workload làm việc có kiểm soát, không tự quyết.
- Điều tra viên Bằng chứng thu evidence không bịa.
- Chuyên gia Phân tích Dữ liệu không đọc log bằng mắt.
- Giám khảo Kiểm toán Cuối cùng không bỏ sót gì trước khi nộp.

Điều em rút ra quan trọng nhất: AI hữu ích nhất khi bị ép đi đúng quy trình — không phải khi được tin tưởng làm tắt.

Cảm ơn thầy cô. Em là Nguyễn Bình Minh Phương, MSSV 23127104."

---

## CHECKLIST HẬU KỲ VIDEO 2

- [ ] Video có đủ 4 phần A/B/C1/C2/C3
- [ ] Camera thấy rõ prompt được gõ vào chat AI
- [ ] Camera thấy AI thực sự phản hồi — không dùng ảnh tĩnh
- [ ] Phần jtl-data-analyzer: thấy lệnh python chạy trong terminal
- [ ] Phần submission-auditor: thấy ít nhất 1 finding thật
- [ ] Upload YouTube **Unlisted** (có thể cùng video với Video 1 nếu tổng dài hơn 6 phút)
- [ ] Cập nhật link vào `README.md` và `MAIN_REPORT.md` Mục 16
