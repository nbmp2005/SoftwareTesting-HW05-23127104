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
