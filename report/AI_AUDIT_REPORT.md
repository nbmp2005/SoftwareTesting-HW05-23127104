# AI Audit Report

> I use AI tools for the following tasks.

# Prompt 1:
- Name of the AI tool: OpenAI Codex
- Date/time: 2026-08-29T10:03:24+07:00
- Prompt: 
```
## Active file: .agents/skills/ai-audit-logger/SKILL.md

## Open tabs:
- SKILL.md: .agents/skills/ai-audit-logger/SKILL.md
- hw05.md: docs/hw05.md

## My request:
[$ai-audit-logger](C:\Users\cpshc\Y3\SoftwareTesting\SoftwareTesting-HW05\SoftwareTesting-HW05-23127104\\.agents\skills\ai-audit-logger\SKILL.md) Dựa vào yêu cầu đề bài, hãy giúp tôi

1. Giảng lại chi tiết toàn bộ nội dung kiến thức liên quan đến bài tập này
2. Giải thích chi tiết từng việc tôi phải làm cũng như workflow cụ thể
3. Tôi muốn xây một bộ agent skill kit để làm bài tập, hướng dẫn chi tiết
4. Viết toàn bộ những file md yêu cầu của đề bài thật chính xác

Đây là workflow phần bài làm của tôi

#### ⚙️ [ADMIN] Workflow 5: Quản trị viên Nhập hàng & Phát hành Voucher (Admin Catalog & Promo Operations)

> **Mục đích:** Kiểm thử tải của các thao tác ghi danh mục, thêm sản phẩm và quản lý người dùng/khuyến mãi của Admin.

- **1. [Auth-heavy]**: `POST /api/login` (Đăng nhập tài khoản Admin).
- **2. [Read-heavy]**: `GET /api/admin/users` (Xem danh sách tài khoản) $\rightarrow$ `GET /api/coupons` (Xem danh sách mã khuyến mãi).
- **3. [Transactional]**: `POST /api/categories` (Tạo danh mục mới) $\rightarrow$ `POST /api/products` (Tạo sản phẩm mới hoặc `POST /api/admin/import-products`) $\rightarrow$ `POST /api/admin/coupons` (Tạo voucher giảm giá).
```
- AI Output: 
```
Đã phân tích toàn bộ yêu cầu HW05 và đối chiếu Workflow 5 với source EShop; xác nhận endpoint, payload/correlation và các sai lệch authentication/lockout cần tách khỏi kết quả hiệu năng. Đã viết tài liệu kiến thức, workflow thực hiện, hướng dẫn Agent Skill Kit, README/self-assessment, Main Report, AI Critique, AI Audit Report và submission checklist. Đã tạo skill hw05-performance-testing gồm bốn reference theo chế độ, metadata và script phân tích JTL có unit test. Skill đã qua quick validation, hai unit test pass và liên kết Markdown hợp lệ. Các bằng chứng chưa tồn tại như JMX có ngày chạy thật, JTL, HTML report, hardware/resource screenshot, video, issue link, commit hash và measured threshold được giữ dưới dạng TODO (REAL EVIDENCE REQUIRED), không bị bịa.
```

# Prompt 2:
- Name of the AI tool: OpenAI Codex
- Date/time: 2026-08-29T23:06:08+07:00
- Prompt: 
```
[$ai-audit-logger](C:\Users\cpshc\Y3\SoftwareTesting\SoftwareTesting-HW05\SoftwareTesting-HW05-23127104\\.agents\skills\ai-audit-logger\SKILL.md) Hãy đọc file `agent-skill-kit/hw05-performance-testing/references/test-design.md` và viết lại cho tôi một file `SKILL.md` mới tên là **`jmeter-test-designer`**. Yêu cầu: Đừng viết kiểu cẩm nang chung chung. Hãy viết dưới dạng một quy trình (workflow) bắt buộc gồm các bước: Bước 1 (phỏng vấn lấy SUT context), Bước 2 (lập ma trận data), Bước 3 (xác định ngưỡng Load/Stress/Spike). Ép AI tuyệt đối không được sinh code JMX hoặc đưa ra con số nếu user chưa duyệt qua cấu hình ở Bước 1 và 2. Hãy tích hợp yêu cầu ghi log AI Audit sau mỗi bước.  
```
- AI Output: 
```
Đã dùng skill-creator để tạo `agent-skill-kit/jmeter-test-designer/SKILL.md` dưới dạng state machine ba bước bắt buộc. Skill có approval gate rõ ràng: cấm tuyệt đối JMX và mọi con số workload/ngưỡng trước khi SUT Context và Data Matrix được user duyệt và ghi audit; chỉ cho phép sinh/chỉnh JMX sau khi Profile Matrix Bước 3 cũng được duyệt, audit thành công và user yêu cầu riêng. Mỗi bước có đầu ra dạng bảng, quy tắc quay lại khi context thay đổi và định dạng append AI Audit với timestamp thật. Skill đã vượt qua quick validation ở chế độ UTF-8 và kiểm tra hard-gate bằng tìm kiếm nội dung.
```

# Prompt 3:
- Name of the AI tool: OpenAI Codex
- Date/time: 2026-08-29T23:13:26+07:00
- Prompt: 
```
[$ai-audit-logger](C:\Users\cpshc\Y3\SoftwareTesting\SoftwareTesting-HW05\SoftwareTesting-HW05-23127104\\.agents\skills\ai-audit-logger\SKILL.md) Hãy đọc file `agent-skill-kit/hw05-performance-testing/references/execution-evidence.md` và viết lại cho tôi một file `SKILL.md` mới tên là **`perf-evidence-collector`**. Yêu cầu: Thiết kế skill này như một bộ checklist ép buộc. Khi kích hoạt skill, AI phải hỏi user từng mục: Đã có ảnh chụp Task Manager chưa? Đã có file CSV chưa? Đã có JTL chưa? Nếu user cung cấp thiếu minh chứng thực tế, AI phải cảnh báo và đặt cờ `TODO (REAL EVIDENCE REQUIRED)`, tuyệt đối nghiêm cấm AI tự bịa ra thông số phần cứng, giả lập log server, hay tự tạo timestamp giả.  
```
- AI Output: 
```
Đã tạo `agent-skill-kit/perf-evidence-collector/SKILL.md` dưới dạng checklist tuần tự bắt buộc, mỗi lượt chỉ hỏi một artifact. Skill dùng Evidence Ledger với các trạng thái VERIFIED, PRESENT — UNVERIFIED, MISSING/INVALID kèm TODO (REAL EVIDENCE REQUIRED); câu trả lời “đã có” không đủ nếu thiếu path hoặc attachment kiểm tra được. Checklist bao phủ hardware, Task Manager cùng frame, CSV, raw JTL, JMX, HTML report, run notes, server log, response classification, soak và lockout recovery. Skill cấm bịa phần cứng, sửa/sinh JTL, mô phỏng server log và tạo timestamp quá khứ. Quick validator xác nhận skill hợp lệ và các invariant chống bịa đã được kiểm tra.
```

# Prompt 4:
- Name of the AI tool: OpenAI Codex
- Date/time: 2026-08-29T23:17:03+07:00
- Prompt: 
```
[$ai-audit-logger](C:\Users\cpshc\Y3\SoftwareTesting\SoftwareTesting-HW05\SoftwareTesting-HW05-23127104\\.agents\skills\ai-audit-logger\SKILL.md) Hãy đọc file `agent-skill-kit/hw05-performance-testing/references/result-analysis.md` và viết lại cho tôi một file `SKILL.md` mới tên là **`jtl-data-analyzer`**. Yêu cầu: Xây dựng quy trình bắt buộc: Bước 1 AI luôn phải gọi script `scripts/analyze_jtl.py` để parse file log thật thay vì tự đọc bằng mắt. Bước 2 AI mới được dùng output JSON để suy luận. Hãy tạo một phân đoạn ép AI phải tự 'soi' lại lỗi của chính mình (misinterpretation hunt) để viết đoạn AI Critique chuẩn xác, không được nói chung chung mà phải trích dẫn số liệu chênh lệch cụ thể  
```
- AI Output: 
```
Đã tạo `agent-skill-kit/jtl-data-analyzer/SKILL.md` với hard gate script-first và JSON-only. Skill bắt buộc xác minh raw CSV JTL, thực sự gọi parser canonical `agent-skill-kit/hw05-performance-testing/scripts/analyze_jtl.py`, kiểm tra exit code/JSON schema rồi mới cho phép metric và inference. Sau đó skill lập metric/claim ledger, kiểm tra overall double-count, chặn suy luận stage threshold từ JSON aggregate, và bắt buộc cross-check sample count, failure count, p95. Misinterpretation hunt giữ nguyên claim AI, đối chiếu file/label/window, tính absolute và relative delta; AI Critique chỉ được hoàn tất khi có sai lệch thật với số liệu cụ thể. Skill đã vượt qua quick validation và kiểm tra invariant.
```

# Prompt 5:
- Name of the AI tool: OpenAI Codex
- Date/time: 2026-08-29T23:20:20+07:00
- Prompt: 
```
[$ai-audit-logger](C:\Users\cpshc\Y3\SoftwareTesting\SoftwareTesting-HW05\SoftwareTesting-HW05-23127104\\.agents\skills\ai-audit-logger\SKILL.md) Hãy đọc file `agent-skill-kit/hw05-performance-testing/references/report-submission.md` và viết lại cho tôi một file `SKILL.md` mới tên là **`submission-auditor`**. Yêu cầu: Skill này hoạt động như một giám khảo khó tính. Hãy viết luồng làm việc ép AI kiểm tra chéo (cross-check) tất cả các file đã tạo ra. Bước 1: Quét toàn bộ project tìm các cờ `TODO`. Bước 2: So khớp thông số cấu hình phần cứng trong báo cáo với ảnh chụp màn hình. Bước 3: Kiểm tra format của AI Audit Log xem có đúng chuẩn không. Nếu phát hiện thiếu sót hoặc sai lệch, báo lỗi ngay thay vì tự động điền bừa  
```
- AI Output: 
```
Đã tạo `agent-skill-kit/submission-auditor/SKILL.md` như một auditor read-only nghiêm ngặt. Skill bắt buộc lập inventory, quét TODO toàn workspace bằng rg và phân loại blocker/false-positive; đối chiếu từng claim hostname/OS/CPU/RAM/storage/tool version trong report với ảnh thật; parse từng AI Audit entry để kiểm tra field, code fence, ISO timestamp, prompt/output và provenance. Sau ba bước bắt buộc, skill còn cross-check JMX/CSV/JTL/HTML, naming/date, scenario attempt, report metrics, Critique, continuous proposal, links và ZIP. Mỗi lỗi được báo ngay theo BLOCKER/ERROR/WARNING với file/line và action; skill cấm tự sửa hoặc điền evidence thiếu. Quick validator xác nhận skill hợp lệ.
```

# Prompt 6:
- Name of the AI tool: OpenAI Codex
- Date/time: 2026-08-30T08:51:18+07:00
- Prompt:
```
[$ai-audit-logger](C:\Users\cpshc\Y3\SoftwareTesting\SoftwareTesting-HW05\SoftwareTesting-HW05-23127104\\.agents\skills\ai-audit-logger\SKILL.md) Hãy cập nhật lại các skill trong agent skill kit để skill tự động generate cũng như cập nhật các file md cần thiết (report) 
```
- AI Output:
```
Đã bổ sung report artifact contract cho HW05 Performance Testing và tích hợp điểm cập nhật Markdown vào các skill thiết kế JMeter, thu thập evidence, phân tích JTL và submission audit. Quy tắc mới yêu cầu cập nhật tối thiểu theo heading, provenance cho từng fact, đồng bộ checklist/README và giữ TODO cho evidence chưa có; không ghi đè report hoặc bịa số liệu. Đã xác minh cấu trúc và liên kết sau chỉnh sửa.
```

# Prompt 7:
- Name of the AI tool: OpenAI Codex
- Date/time: 2026-08-30T10:19:25.5247237+07:00
- Prompt:
```
# Context from my IDE setup:

## Open tabs:
- test-design.md: agent-skill-kit/hw05-performance-testing/references/test-design.md
- execution-evidence.md: agent-skill-kit/hw05-performance-testing/references/execution-evidence.md
- report-artifacts.md: c:\Users\cpshc\AppData\Local\Temp\b3dc70af-c8f7-4b34-991c-b44ff837116f_agent-skill-kit-fixed.zip.16f\skills-fixed\references\report-artifacts.md
- result-analysis.md: agent-skill-kit/hw05-performance-testing/references/result-analysis.md
- SKILL.md: agent-skill-kit/submission-auditor/SKILL.md

## My request:
[$ai-audit-logger](C:\Users\cpshc\Y3\SoftwareTesting\SoftwareTesting-HW05\SoftwareTesting-HW05-23127104\\.agents\skills\ai-audit-logger\SKILL.md) Dùng skill jmeter-test-designer. Tôi muốn thiết kế Load/Stress/Spike/Soak test cho EShop backend, repo [https://github.com/ttbhanh/eshop-sut](https://github.com/ttbhanh/eshop-sut), workflow:
login admin -> GET /api/admin/users -> GET /api/coupons ->
POST /api/categories -> POST /api/products -> POST /api/admin/coupons.
Bắt đầu Bước 1: phỏng vấn SUT context.
```
- AI Output:
```
Đã khởi động Bước 1 của jmeter-test-designer; audit entry này ghi nhận yêu cầu và trạng thái các gate đều chưa được duyệt. Đang kiểm tra repository để lập SUT Context Record; chưa đưa ra workload number hoặc sinh JMX.
```

# Prompt 8:
- Name of the AI tool: OpenAI Codex
- Date/time: 2026-08-30T10:57:57.5548486+07:00
- Prompt:
```
# Context from my IDE setup:

## Open tabs:
- test-design.md: agent-skill-kit/hw05-performance-testing/references/test-design.md
- execution-evidence.md: agent-skill-kit/hw05-performance-testing/references/execution-evidence.md
- report-artifacts.md: c:\Users\cpshc\AppData\Local\Temp\b3dc70af-c8f7-4b34-991c-b44ff837116f_agent-skill-kit-fixed.zip.16f\skills-fixed\references\report-artifacts.md
- result-analysis.md: agent-skill-kit/hw05-performance-testing/references/result-analysis.md
- SKILL.md: agent-skill-kit/submission-auditor/SKILL.md

## My request:
[$ai-audit-logger](C:\Users\cpshc\Y3\SoftwareTesting\SoftwareTesting-HW05\SoftwareTesting-HW05-23127104\\.agents\skills\ai-audit-logger\SKILL.md) Dưới đây là kết quả kiểm tra SUT thực tế của tôi:

- **Commit SHA:** `85af3ba875c88283615e22cb108f13e2fccaf0e9`
- **Base URL:** `http://localhost:3000`
- **Admin credential đã test:** `admin@gmail.com`
- **Mỗi endpoint (status + response mẫu):**
  - `POST /api/login`: 200 OK. Response: `{"message": "Login successful", "token": "eyJ...", "user": {...}}`
  - `GET /api/admin/users`: 200 OK. Response: `[{"id": 1, "name": "Admin", ...}]`
  - `GET /api/coupons`: 200 OK. Response: `[{"id": 1, "code": "SUMMER", ...}]`
  - `POST /api/categories`: 200 OK. Response: `{"message": "Category created", "id": 15}`
  - `POST /api/products`: 200 OK. Response: `{"message": "Product created", "id": 42}`
  - `POST /api/admin/coupons`: 200 OK. Response: `{"message": "Coupon created", "id": 10}`
- **Token field:** `$.token` (từ API login)
- **Category ID field:** `$.id` (từ API create category, truyền vào trường `category_id` của API create product)
- **Reset database bằng cách:** Copy đè file `database.sqlite` sạch vào lại thư mục backend trước mỗi lần chạy test.
- **JMeter/backend/database chạy trên:** Cùng 1 máy (Localhost).
- **Lockout/Auth:** Đăng nhập sai 3 lần sẽ bị khóa 180s (tôi đã check code `server.js`). Có thể dùng chung 1 tài khoản admin đồng thời.

Hãy cập nhật lại SUT Context. Tôi xác nhận: **Duyệt SUT Context Bước 1.**
```
- AI Output:
```
SUT Context r1.0 đã được khóa theo dữ liệu smoke-test thực tế do user cung cấp và user đã phê duyệt rõ ràng. STEP_1_CONTEXT_APPROVED=true và audit này được append thành công, nên STEP_1_AUDIT_LOGGED=true. Không có workload number hoặc JMX được sinh; Bước 2 Data Matrix là bước kế tiếp.
```


# Prompt 9:
- Name of the AI tool: OpenAI Codex
- Date/time: 2026-08-30T11:00:56.6647031+07:00
- Prompt:
```
# Context from my IDE setup:

## Open tabs:
- test-design.md: agent-skill-kit/hw05-performance-testing/references/test-design.md
- execution-evidence.md: agent-skill-kit/hw05-performance-testing/references/execution-evidence.md
- report-artifacts.md: c:\Users\cpshc\AppData\Local\Temp\b3dc70af-c8f7-4b34-991c-b44ff837116f_agent-skill-kit-fixed.zip.16f\skills-fixed\references\report-artifacts.md
- result-analysis.md: agent-skill-kit/hw05-performance-testing/references/result-analysis.md
- SKILL.md: agent-skill-kit/submission-auditor/SKILL.md

## My request:
[$ai-audit-logger](C:\Users\cpshc\Y3\SoftwareTesting\SoftwareTesting-HW05\SoftwareTesting-HW05-23127104\\.agents\skills\ai-audit-logger\SKILL.md) Sang Bước 2: lập data matrix cho workflow trên, sẽ dùng 1 CSV run\_id/credential&#x20;
và cách sinh category/product/coupon code unique theo run\_id + iteration.
```
- AI Output:
```
Đã khởi tạo Bước 2 và lập Data Matrix nháp cho credential, run_id, token, category_id, cùng các dữ liệu mutation unique theo run_id + iteration. Data Matrix chưa được user phê duyệt; không có JMX hoặc workload number được sinh.
```

# Prompt 10:
- Name of the AI tool: OpenAI Codex
- Date/time: 2026-08-30T11:14:57.1267136+07:00
- Prompt:
```
# Context from my IDE setup:

## Active file: docs/hw05.md

## Active selection of the file:
Admin
## Open tabs:
- hw05.md: docs/hw05.md
- 04_HuongDanChiTiet.md: docs/04_HuongDanChiTiet.md
- test-design.md: agent-skill-kit/hw05-performance-testing/references/test-design.md
- execution-evidence.md: agent-skill-kit/hw05-performance-testing/references/execution-evidence.md
- report-artifacts.md: c:\Users\cpshc\AppData\Local\Temp\b3dc70af-c8f7-4b34-991c-b44ff837116f_agent-skill-kit-fixed.zip.16f\skills-fixed\references\report-artifacts.md

## My request:
[$ai-audit-logger](C:\Users\cpshc\Y3\SoftwareTesting\SoftwareTesting-HW05\SoftwareTesting-HW05-23127104\\.agents\skills\ai-audit-logger\SKILL.md) Dưới đây là các thông tin tôi chốt lại để giải quyết 3 ô Missing của Data Matrix:

- **Bảo vệ CSV:** Tôi đã tạo file `test-data/admin_credentials.csv` (có 5 dòng dữ liệu để recycle). Tôi đã cấu hình thêm `test-data/*.csv` vào `.gitignore` để đảm bảo password không bao giờ bị lộ lên public repo hoặc JTL report.
- **Product payload values:** Tôi chốt dùng các giá trị hằng số hợp lệ sau cho mọi request Create Product:
  - `price`: 150000
  - `description`: "Product generated by AI Performance Test"
  - `imageUrl`: "[https://example.com/demo.png](https://example.com/demo.png)"
- **Coupon payload values:** Tôi chốt dùng các giá trị hằng số hợp lệ sau cho mọi request Create Coupon:
  - `type`: "percent"
  - `discount_value`: 15
  - `min_order_amount`: 100000
  - `expired_at`: "2030-12-31T23:59:59.000Z" (ngày trong tương lai)
  - `max_uses_per_user`: 1

Mọi rủi ro bạn nêu ra (như xử lý extractor rỗng thành lỗi test data) tôi đều đồng ý. Tôi xác nhận: **Duyệt Data Matrix Bước 2.**
```
- AI Output:
```
Data Matrix r1.0 đã được khóa theo payload, CSV protection, và quy tắc xử lý extractor do user phê duyệt. STEP_2_DATA_APPROVED=true và audit này được append thành công, nên STEP_2_AUDIT_LOGGED=true. Gate Bước 3 được mở; chưa sinh JMX hoặc workload number.
```

# Prompt 11:
- Name of the AI tool: OpenAI Codex
- Date/time: 2026-08-30T11:24:23.0833953+07:00
- Prompt:
```
# Context from my IDE setup:

## Open tabs:
- hw05.md: docs/hw05.md
- 04_HuongDanChiTiet.md: docs/04_HuongDanChiTiet.md
- test-design.md: agent-skill-kit/hw05-performance-testing/references/test-design.md
- execution-evidence.md: agent-skill-kit/hw05-performance-testing/references/execution-evidence.md
- report-artifacts.md: c:\Users\cpshc\AppData\Local\Temp\b3dc70af-c8f7-4b34-991c-b44ff837116f_agent-skill-kit-fixed.zip.16f\skills-fixed\references\report-artifacts.md

## My request:
[$ai-audit-logger](C:\Users\cpshc\Y3\SoftwareTesting\SoftwareTesting-HW05\SoftwareTesting-HW05-23127104\\.agents\skills\ai-audit-logger\SKILL.md) Dưới đây là thông tin thực tế tôi cung cấp cho Bước 3 - Profile:

- **Mục tiêu Traffic (Các kịch bản đề xuất):**
  - **Load Test:** 20 Concurrent Users (VU), Ramp-up trong 10s, chạy 100 vòng lặp.
  - **Stress Test:** 100 VU, Ramp-up trong 50s, chạy 20 vòng lặp.
  - **Spike Test:** 200 VU, Ramp-up cực nhanh trong 2s, chạy 5 vòng lặp.
  - **Soak Test:** 20 VU, Ramp-up trong 10s, chạy liên tục trong 15 phút (thử nghiệm độ bền, rò rỉ RAM).
- **Tiêu chí chấp nhận (Acceptance Criteria):** Thời gian phản hồi phân vị thứ 95 (p95) < 2000ms. Tỷ lệ lỗi (Error rate) < 1% cho Load Test.
- **Think time / Pacing:** Tôi muốn mô phỏng người dùng thật nên giữa mỗi bước nghiệp vụ cần có khoảng nghỉ (Think time) từ 1000ms đến 2000ms (Gaussian Random Timer).
- **Môi trường phần cứng:** Backend (Node.js), DB (SQLite) và JMeter đều chạy chung trên 1 máy tính của tôi: Windows 11, HP Victus 15, RAM 16GB.
- **Điều kiện dừng an toàn:** Nếu Error rate > 50% trong 5 giây liên tục hoặc RAM vượt quá ngưỡng 90%, bài test sẽ dừng thủ công. Tôi chưa có kết quả smoke test baseline.
- **Yêu cầu Report/Listener:** Không lặp lại Listener giữa các JMX để tối ưu.
  - Load Test -> Summary Report
  - Stress Test -> Aggregate Report
  - Spike Test -> View Results Tree (để debug)
  - Soak Test -> Generate HTML Dashboard.

Đề nghị bạn lập bảng cấu hình Profile Matrix CANDIDATE dựa trên số liệu này. Sau khi bạn lập xong tôi sẽ chốt.
```
- AI Output:
```
Đã lập Profile Matrix nháp gồm Load, Stress, Spike và Soak. Mọi số liệu được gắn CANDIDATE — CHƯA ĐO; chưa có measured threshold hoặc JMX. Đã nêu conflict rằng View Results Tree chỉ dùng debug nhỏ, không dùng làm measurement listener, và các acceptance criteria ngoài Load còn thiếu quyết định của user.
```

# Prompt 12:
- Name of the AI tool: OpenAI Codex
- Date/time: 2026-08-30T11:35:16.8530267+07:00
- Prompt:
```
# Context from my IDE setup:

## Open tabs:
- hw05.md: docs/hw05.md
- 04_HuongDanChiTiet.md: docs/04_HuongDanChiTiet.md
- test-design.md: agent-skill-kit/hw05-performance-testing/references/test-design.md
- execution-evidence.md: agent-skill-kit/hw05-performance-testing/references/execution-evidence.md
- report-artifacts.md: c:\Users\cpshc\AppData\Local\Temp\b3dc70af-c8f7-4b34-991c-b44ff837116f_agent-skill-kit-fixed.zip.16f\skills-fixed\references\report-artifacts.md

## My request:
Dưới đây là các thông tin tôi bổ sung để giải quyết các ô MISSING trong Profile Matrix:

- **Recovery check (Load & Stress):** Sau khi bài test kết thúc, tôi sẽ chạy lại một kịch bản Smoke Test 1 VU (chạy bằng JMeter GUI hoặc Postman). Nếu API trả về 200 OK và response time < 500ms thì SUT được xác nhận là đã phục hồi.
- **Tiêu chí pass/fail của Stress Test:** Mục đích của Stress là tìm ra điểm gãy (breakpoint). Tiêu chí là xác định được mốc RPS (Request Per Second) mà tại đó Error Rate bắt đầu vượt quá 5% hoặc p95 vượt quá 5000ms.
- **Baseline & Recovery của Spike Test:**
  - Mức Baseline trước và sau Spike: 10 VU.
  - Tiêu chí recovery: Sau khi luồng Spike 200 VU kết thúc và trở về 10 VU, hệ thống phải ổn định lại trong vòng tối đa 1 phút (Error rate = 0%, p95 < 2000ms).
- **Tiêu chí trend của Soak Test:** Trong suốt 15 phút, Error Rate không được vượt quá 1%, và p95 ở phút thứ 15 không được tăng quá 20% so với p95 ở phút đầu tiên.
- **Xác nhận Rủi ro:** Tôi đồng ý ghi CPU/RAM bằng Resource Monitor để đối chiếu, và cam kết chỉ bật View Results Tree khi chạy Smoke Test (khi chạy đo thật sẽ chạy non-GUI `-n` và lưu raw JTL).

Tôi xác nhận mọi con số trên đều mang nhãn CANDIDATE. Đề nghị: **Duyệt Profile Matrix Bước 3 (Load/Stress/Spike/Soak) và các CANDIDATE — CHƯA ĐO.**
```
- AI Output:
```
Profile Matrix r1.0 đã được khóa với các candidate do user phê duyệt, gồm recovery, stress breakpoint, spike baseline/recovery, soak trend, non-GUI raw JTL, và Resource Monitor. STEP_3_PROFILE_APPROVED=true và audit này được append thành công, nên STEP_3_AUDIT_LOGGED=true. Thiết kế sẵn sàng nhận yêu cầu riêng để sinh/chỉnh JMX; chưa có JMX được sinh trong phản hồi này.
```

# Prompt 13:
- Name of the AI tool: OpenAI Codex
- Date/time: 2026-08-30T11:43:52.5708239+07:00
- Prompt:
```
# Context from my IDE setup:

## Active file: .gitignore

## Open tabs:
- .gitignore: .gitignore
- hw05.md: docs/hw05.md
- 04_HuongDanChiTiet.md: docs/04_HuongDanChiTiet.md
- test-design.md: agent-skill-kit/hw05-performance-testing/references/test-design.md
- execution-evidence.md: agent-skill-kit/hw05-performance-testing/references/execution-evidence.md

## My request:
[$ai-audit-logger](C:\Users\cpshc\Y3\SoftwareTesting\SoftwareTesting-HW05\SoftwareTesting-HW05-23127104\\.agents\skills\ai-audit-logger\SKILL.md) Tôi xác nhận cấu hình Scheduler cụ thể cho 2 kịch bản này như sau:

**1. Cấu hình các Stage giữ tải cho Stress Test (Stepping):**

- Stage 1: Tăng lên 20 VU (trong 5s) và giữ tải ở mốc này trong 30 giây.
- Stage 2: Tăng tiếp lên 50 VU (trong 5s) và giữ tải trong 30 giây.
- Stage 3: Tăng tiếp lên 80 VU (trong 5s) và giữ tải trong 30 giây.
- Stage 4: Tăng lên mốc tối đa 100 VU (trong 5s) và giữ tải trong 30 giây.
- (Tổng thời gian test rơi vào khoảng hơn 2 phút rưỡi, dễ dàng quan sát breakpoint tại từng mốc).

**2. Cấu hình Baseline và Burst cho Spike Test:**

- Giai đoạn 1 (Baseline trước bão): Chạy 10 VU giữ đều đặn trong 60 giây.
- Giai đoạn 2 (Spike burst): Bơm đột ngột lên 200 VU (ramp-up cực nhanh trong 2 giây) và giữ mốc 200 VU này trong 5 giây.
- Giai đoạn 3 (Baseline sau bão & Recovery): Lập tức tụt về lại mức 10 VU và tiếp tục giữ đều 10 VU này trong 120 giây tiếp theo để quan sát tiêu chí recovery (phục hồi trong tối đa 1 phút).

Mọi thông số CSV đã được bảo mật. hãy sinh 4 file JMX (mã code XML) với tên convention `23127104_{Scenario}_{YYYYMMDD}.jmx` để tôi lưu lại và chạy thực tế.
```
- AI Output:
```
Cấu hình scheduler làm thay đổi workload shape của Stress và Spike, nên Profile Matrix r1.0 bị thay thế bằng revision r1.1 đang chờ phê duyệt lại. Chưa sinh JMX, workload number mới chỉ là CANDIDATE — CHƯA ĐO.
```

# Prompt 14:
- Name of the AI tool: OpenAI Codex
- Date/time: 2026-08-30T11:55:33.8837580+07:00
- Prompt:
```
# Context from my IDE setup:

## Active file: .gitignore

## Open tabs:
- .gitignore: .gitignore
- hw05.md: docs/hw05.md
- 04_HuongDanChiTiet.md: docs/04_HuongDanChiTiet.md
- test-design.md: agent-skill-kit/hw05-performance-testing/references/test-design.md
- execution-evidence.md: agent-skill-kit/hw05-performance-testing/references/execution-evidence.md

## My request:
[$ai-audit-logger](C:\Users\cpshc\Y3\SoftwareTesting\SoftwareTesting-HW05\SoftwareTesting-HW05-23127104\\.agents\skills\ai-audit-logger\SKILL.md) Duyệt Profile Matrix r1.1 và các CANDIDATE — CHƯA ĐO  
```
- AI Output:
```
Profile Matrix r1.1 đã được user duyệt rõ ràng. STEP_3_PROFILE_APPROVED=true và audit này được append thành công, nên STEP_3_AUDIT_LOGGED=true. Chưa sinh JMX vì approval không tự động là yêu cầu tạo file.
```

# Prompt 15:
- Name of the AI tool: OpenAI Codex
- Date/time: 2026-08-30T11:58:59.6609879+07:00
- Prompt:
```
# Context from my IDE setup:

## Active file: report/AI_AUDIT_REPORT.md

## Open tabs:
- AI_AUDIT_REPORT.md: report/AI_AUDIT_REPORT.md
- admin_credentials.csv: test-data/admin_credentials.csv
- .gitignore: .gitignore
- hw05.md: docs/hw05.md
- 04_HuongDanChiTiet.md: docs/04_HuongDanChiTiet.md

## My request:
[$ai-audit-logger](C:\Users\cpshc\Y3\SoftwareTesting\SoftwareTesting-HW05\SoftwareTesting-HW05-23127104\\.agents\skills\ai-audit-logger\SKILL.md) Sinh 4 file JMX theo Profile Matrix r1.1.  
```
- AI Output:
```
Đã sinh bốn JMX Load, Stress, Spike và Soak theo Profile Matrix r1.1, cùng fragment workflow dùng chung để giữ cùng request contract, correlation và data handling. Chưa có execution evidence hoặc measured threshold.
```

