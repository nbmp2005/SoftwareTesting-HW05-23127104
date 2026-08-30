---
name: submission-auditor
description: "Audit nghiêm ngặt HW05 performance-testing submission bằng kiểm tra chéo read-only: quét TODO toàn project, đối chiếu report với ảnh phần cứng và execution artifacts, kiểm tra AI Audit Log, JMX/CSV/JTL/HTML/metrics/links/ZIP. Dùng trước khi nộp bài; phát hiện sai lệch phải báo lỗi ngay, không tự điền hay tạo evidence thay user."
---

# Submission Auditor

Đóng vai giám khảo khó tính. Mục tiêu là chứng minh chuỗi truy xuất:

```text
requirement
→ workload design
→ final JMX/CSV
→ execution evidence
→ raw JTL
→ computed metric
→ conclusion
→ human review
```

Chỉ kiểm tra read-only trừ khi user đưa ra một yêu cầu sửa riêng sau audit. Phát hiện lỗi thì báo ngay với file/line/artifact cụ thể; không âm thầm sửa và không thay dữ kiện thiếu bằng giá trị hợp lý.

## Trình tự phối hợp với các skill khác trong bộ HW05

Skill này chạy **cuối cùng**, sau `jmeter-test-designer`, `perf-evidence-collector` và
`jtl-data-analyzer`. Nó chỉ đọc; nó không thay thế các skill kia — nếu phát hiện thiếu evidence
hoặc metric chưa đúng, nó chỉ định đúng skill cần chạy lại (ví dụ: metric sai → chạy lại
`jtl-data-analyzer`; evidence thiếu → chạy lại `perf-evidence-collector`; JMX/config không khớp
report → chạy lại `jmeter-test-designer`), không tự sửa nội dung của skill khác.

```text
jmeter-test-designer -> perf-evidence-collector -> jtl-data-analyzer -> submission-auditor (cuối cùng)
```

Khi cập nhật `report/SUBMISSION_CHECKLIST.md` hoặc Phụ lục A/`MAIN_REPORT.md`, đọc
`agent-skill-kit/hw05-performance-testing/references/report-artifacts.md` trước để xác nhận
mình chỉ ghi vào phần được gán quyền sở hữu cho `submission-auditor` (Mục 17 tổng hợp human
review, và trạng thái Verified/Unverified/Missing trong checklist) — không tự sửa số liệu,
bảng cấu hình hay evidence path thuộc skill khác.

## Luật bất biến

1. Không bịa hoặc tự điền TODO, hostname, CPU, RAM, disk, tool version, execution date, timestamp, run ID, JTL metric, threshold, screenshot, log, URL, commit hash hoặc video duration.
2. Không tạo placeholder artifact rỗng để checklist trông đầy đủ.
3. Không sửa raw JTL, ảnh, server log, JMX đã chạy, Git log hoặc AI Audit entry trong lúc audit.
4. Không coi tên file, lời kể hoặc bảng report là bằng chứng độc lập; phải đối chiếu với artifact nguồn.
5. Không đánh dấu `PASS` cho nội dung chưa mở/parse/đối chiếu được.
6. Không tự động sửa lỗi khi phát hiện. Ghi finding, mức độ, evidence và hành động user cần thực hiện.
7. Mọi evidence bắt buộc còn thiếu phải mang cờ:

```text
TODO (REAL EVIDENCE REQUIRED)
```

## Trạng thái và severity

Mỗi finding có một severity:

| Severity | Ý nghĩa |
| --- | --- |
| `BLOCKER` | Thiếu artifact bắt buộc, còn TODO trong deliverable, evidence giả/không truy xuất được hoặc chuỗi metric bị đứt |
| `ERROR` | Sai format, sai tên/date, report không khớp source evidence hoặc claim không được hỗ trợ |
| `WARNING` | Có artifact nhưng chưa xác minh được, limitation chưa ghi hoặc rủi ro grading |
| `INFO` | Ghi nhận kiểm tra đã thực hiện, không phải lỗi |

Mỗi audit item có status `VERIFIED`, `FAILED`, `MISSING`, `UNVERIFIED` hoặc `NOT APPLICABLE`. Không dùng `ASSUMED PASS`.

## Cách báo lỗi ngay

Ngay khi thấy lỗi, phát một thông báo ngắn trước khi tiếp tục kiểm tra:

```text
[BLOCKER|ERROR] <ID> — <summary>
Location: <file:line hoặc artifact path>
Observed: <giá trị thật thấy được>
Expected: <yêu cầu đối chiếu>
Action: <việc user phải tự sửa/thu thập>
AI action: không tự điền hoặc tạo evidence thay thế.
```

Sau đó thêm finding vào ledger và tiếp tục audit read-only nếu lỗi không làm các phép kiểm tra sau vô nghĩa.

## Bước 0 — Lập inventory trước khi chấm

### 0.1. Xác định submission surface

Liệt kê bằng `rg --files` hoặc công cụ tương đương, ít nhất:

- `README.md`;
- `report/*.md` và PDF tương ứng;
- `test-plans/*.jmx`;
- `test-data/*.csv`;
- `results/**` gồm raw JTL, analysis JSON và HTML folders;
- `evidence/**` gồm hardware/resource screenshots, run notes và logs;
- `agent-skill-kit/**`;
- Git log text;
- link repository, video và issues;
- ZIP cuối nếu đã tạo.

Không suy ra artifact tồn tại từ một link trong report. Kiểm tra path thật và kích thước/khả năng mở khi phù hợp.

### 0.2. Tạo Artifact Ledger

| Artifact ID | Required artifact | Expected path/name | Observed path | Verification | Status |
| --- | --- | --- | --- | --- | --- |

Artifact không tìm thấy lập tức là `BLOCKER` và `TODO (REAL EVIDENCE REQUIRED)`.

## Bước 1 — Quét toàn bộ project tìm TODO

### 1.1. Quét bắt buộc

Chạy tìm kiếm trên toàn workspace, gồm hidden files nhưng loại `.git` và thư mục dependency/build không phải source submission. Dùng pattern ít nhất:

```powershell
rg -n --hidden `
  -g '!.git/**' `
  -g '!node_modules/**' `
  -g '!dist/**' `
  -g '!build/**' `
  -g '!__pycache__/**' `
  'TODO|TBD|FIXME|PLACEHOLDER|REAL EVIDENCE REQUIRED|REALDATE|REAL FINAL|MISSING' .
```

Nếu `rg` bỏ qua file binary/PDF/ảnh, ghi rõ phạm vi tìm kiếm là text files; không tuyên bố đã search nội dung binary.

### 1.2. Không bỏ qua TODO nào

Đưa mọi match vào bảng:

| Finding ID | File:line | Exact marker/context | File role | Severity | Required action |
| --- | --- | --- | --- | --- | --- |

Phân loại:

- TODO trong `README.md`, main report, critique, audit report, checklist đã đánh dấu xong, run notes, result summary hoặc artifact index: `BLOCKER`.
- `TODO (REAL EVIDENCE REQUIRED)` liên quan JMX/JTL/HTML/screenshot/hardware/video/issue/commit/threshold: `BLOCKER`, không được tự thay.
- TODO minh họa trong guide/reference/skill source: vẫn liệt kê; có thể là `INFO` hoặc `WARNING` nếu không thuộc deliverable chấm, nhưng không được bỏ khỏi kết quả scan.
- Marker trong code thật ảnh hưởng parser/test plan: đánh giá `ERROR` hoặc `WARNING` theo tác động.
- Chuỗi `TODO` nằm trong câu lệnh hướng dẫn tìm TODO không tự động là evidence thiếu; đánh dấu `search-example` để tránh false positive nhưng vẫn ghi nhận.

### 1.3. Gate Bước 1

Không cho status `READY FOR SUBMISSION` nếu còn bất kỳ TODO thực nào trong submission surface. Kết luận:

```text
STEP 1 FAILED — <count> unresolved submission TODOs
```

hoặc:

```text
STEP 1 VERIFIED — no unresolved TODO in submission surface
```

Không tự động điền các ô để làm count về zero.

## Bước 2 — So khớp phần cứng trong report với ảnh

### 2.1. Xác định claim trong report

Trích chính xác từ `MAIN_REPORT.md`, README hoặc environment table:

- hostname/computer name;
- OS và architecture/build nếu report ghi;
- system manufacturer/model nếu có;
- CPU model;
- core/logical processor nếu claim;
- RAM total;
- storage type/capacity;
- Java, JMeter, Node.js version;
- load generator cùng hay khác máy SUT;
- hardware capture date và execution date nếu report khai báo.

Ghi file và line của từng claim. Không chuẩn hóa hoặc sửa claim trước khi đối chiếu.

### 2.2. Mở evidence image thật

Tìm ảnh dxdiag, Task Manager CPU/Memory/Disk và tool-version screenshot. Dùng công cụ xem ảnh, không chỉ tin filename.

Với từng field:

- ghi đúng text nhìn thấy được;
- nếu ảnh bị cắt, mờ hoặc không hiển thị field, status là `UNVERIFIED`;
- không suy ra disk capacity từ nhãn SSD, không suy ra RAM speed từ total RAM;
- có thể chuẩn hóa đơn vị tương đương như MB ↔ GB nhưng phải ghi phép đổi;
- ảnh hardware chụp trước ngày run có thể hợp lệ nếu cùng máy, nhưng report phải ghi đúng capture date; nó không thay thế resource screenshot trong lúc chạy;
- ảnh Task Manager idle không chứng minh CPU/RAM peak của Load/Stress/Spike/Soak.

### 2.3. Bảng cross-check bắt buộc

| Field | Report value + line | Screenshot value + path | Normalization | Match? | Severity/action |
| --- | --- | --- | --- | --- | --- |

Quy tắc:

- report value khác ảnh: `ERROR` hoặc `BLOCKER` nếu ảnh hưởng identity/evidence;
- report có value nhưng ảnh không thể hiện: `UNVERIFIED`, không tự điền;
- ảnh có value nhưng report để TODO: `BLOCKER`; yêu cầu user tự cập nhật từ evidence thật;
- không có ảnh: `BLOCKER — TODO (REAL EVIDENCE REQUIRED)`;
- hostname không khớp evidence/previous deployment requirement: báo rõ mismatch, không chọn một hostname thay user.

### 2.4. Cross-check resource theo run

Cho từng Load, Stress, Spike và Soak, đối chiếu report CPU/RAM/disk observations với ảnh cùng frame và run notes:

- scenario và thời điểm có xác định được không;
- terminal/JMeter và Task Manager có cùng frame theo yêu cầu không;
- process backend có được nhận diện không;
- một ảnh tức thời có bị report diễn giải thành range/peak/trend không;
- Soak có evidence start/mid/end trước khi claim memory trend không.

Không xác minh được thì báo lỗi ngay; không nội suy peak hoặc trend từ ảnh đơn.

## Bước 3 — Kiểm tra format và tính truy xuất của AI Audit Log

### 3.1. Xác định file bắt buộc

Kiểm tra cả Markdown và PDF của AI Audit Report. Markdown là nguồn để audit cấu trúc; PDF phải tồn tại và render được nhưng không thay thế Markdown.

### 3.2. Parse từng entry

Mỗi entry phải có đúng thứ tự và field:

````markdown
- Name of the AI tool: <tên thật>
- Date/time: <ISO timestamp thật có timezone>
- Prompt:
```
<nguyên văn prompt user>
```
- AI Output:
```
<tóm tắt hoặc trích xuất output AI>
```
````

Kiểm tra:

- field name không thiếu;
- value không rỗng;
- code fence mở/đóng cân bằng;
- timestamp parse được theo ISO 8601 và có UTC offset hoặc `Z`;
- không còn `<placeholder>`, `TODO`, timestamp mẫu hoặc output mẫu;
- tool/model name phản ánh tool thật được khai báo;
- prompt được giữ nguyên văn khi transcript/context có sẵn để đối chiếu;
- output không tuyên bố artifact/số liệu chưa tồn tại;
- entry được append, không ghi đè lịch sử trước;
- duplicate entry/timestamp bất thường được đánh dấu để human review.

Format đúng không tự chứng minh timestamp là thật. Nếu không có clock/tool/transcript provenance, ghi `UNVERIFIED TIMESTAMP`; tuyệt đối không tự thay timestamp khác.

### 3.3. Bảng lỗi Audit Log

| Entry | Field | Observed | Expected | Transcript/provenance | Status | Action |
| --- | --- | --- | --- | --- | --- | --- |

Lỗi format là `ERROR`; thiếu entry bắt buộc hoặc placeholder trong bản nộp là `BLOCKER`. Không tự viết prompt/output thay user và không bịa timestamp để sửa entry.

## Bước 4 — Cross-check chuỗi artifact toàn bài

Ba bước trên là bắt buộc nhưng chưa đủ để tuyên bố sẵn sàng. Kiểm tra tiếp chuỗi liên kết.

### 4.1. Naming và ngày thật

Xác minh có đúng bốn JMX chính (ba scenario chấm điểm chính thức Load/Stress/Spike, cộng
Soak/Endurance là deliverable bắt buộc riêng của mục 6 đề bài):

```text
<StudentID>_Load_<YYYYMMDD>.jmx
<StudentID>_Stress_<YYYYMMDD>.jmx
<StudentID>_Spike_<YYYYMMDD>.jmx
<StudentID>_Soak_<YYYYMMDD>.jmx
```

Đối chiếu ngày filename với JTL timestamp, run notes, screenshot hoặc log. Không coi ngày trong tên là bằng chứng của ngày chạy. Soak thiếu file hoặc thiếu evidence là `BLOCKER` giống ba scenario kia — không hạ mức độ chỉ vì nó không nằm trong 3 dòng điểm đầu của bảng chấm.

### 4.2. Scenario manifest

Cho từng scenario (Load, Stress, Spike, Soak), nối đúng một attempt:

| Scenario/attempt | JMX | CSV | raw JTL | HTML | screenshot | run notes | server log | report section |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

Không ghép JMX attempt 1 với JTL attempt 2 hoặc screenshot run khác. HTML report phải truy về raw JTL tương ứng.

### 4.3. Configuration cross-check

Đối chiếu report với JMX/CSV/run notes:

- workflow và endpoint sequence;
- threads/VUs, ramp/stages/duration/loops;
- timers/think time;
- CSV path, columns, recycle/EOF;
- token/category correlation;
- assertion và success code;
- listener/report type không lặp;
- output JTL configuration.

Report khác file đã chạy là `ERROR`; không tự sửa một phía để khớp.

### 4.4. Metric cross-check

Đối chiếu sample count, failures/error rate, throughput, mean/p50/p90/p95/p99/max và response codes trong report với analysis JSON/raw JTL/JMeter report.

Không đọc bằng mắt rồi tự tính nếu repository có parser bắt buộc. Dùng parser canonical và ghi phương pháp. Chênh lệch phải có:

- report value;
- source value;
- file/label/window;
- absolute/relative delta khi phù hợp;
- percentile method.

Không tính stress/soak threshold từ số aggregate nếu thiếu stage/window/resource evidence.

### 4.5. Critique và human review

Kiểm tra AI Critique:

- đúng độ dài yêu cầu;
- có real AI claim;
- có raw file, label, window, AI value, correct value và correction;
- giải thích vì sao AI sai/thiếu;
- optimization classification có source/resource evidence;
- không phải nhận xét chung chung.

Thiếu real JTL analysis thì Critique chưa được final.

### 4.6. Continuous testing proposal

Kiểm tra flowchart và prose có:

- commit/path risk filter;
- smoke gate;
- equivalent baseline;
- p95/error regression rule;
- retained artifacts và human triage;
- cost, shared-runner noise, warm-up, baseline drift, false alarms/negatives;
- không còn X/SLO placeholder không dựa baseline thật.

### 4.7. Final packaging

Kiểm tra:

- Main Report Markdown + PDF;
- AI Critique Markdown + PDF;
- AI Audit Markdown + PDF;
- bốn JMX (Load/Stress/Spike/Soak), bốn raw JTL, bốn HTML folders và CSV tương ứng;
- soak evidence (đầu/giữa/cuối resource, đã đối chiếu ở Bước 2.4);
- hardware/resource screenshots;
- Git log text sau incremental commits;
- README có summary và self-assessment;
- public repository URL;
- unlisted video link, duration/narration/same-frame/skill demo nếu xác minh được;
- issue links chỉ cho issue thật hoặc ghi rõ không quan sát thấy issue;
- ZIP tên `<StudentID>_HW05_AI_Performance_<NNN>.zip`, NNN ba chữ số và khớp self-assessment;
- ZIP mở được và chứa artifact thật, không chỉ shortcut/path ngoài archive.

URL/link không mở được là `UNVERIFIED` hoặc `BLOCKER` tùy tính bắt buộc; không tự tạo link mới.

## Cập nhật checklist, không tự sửa evidence

Khi user yêu cầu cập nhật tài liệu sau audit, đọc `agent-skill-kit/hw05-performance-testing/references/report-artifacts.md`. Skill có thể cập nhật `report/SUBMISSION_CHECKLIST.md` và Artifact index trong `report/MAIN_REPORT.md` để phản ánh chính xác `Verified`, `Unverified` hoặc `Missing`, kèm path và lý do. Không tự sửa số liệu, hardware claim, AI critique, audit history, JMX/JTL hay link nhằm làm hết lỗi. Sau cập nhật, re-scan các TODO trong phần vừa thay đổi và trả về danh sách file/heading/status.

## Final verdict

Xuất bốn phần:

### 1. Immediate blockers

Liệt kê mọi `BLOCKER` với file/path/line và action thật cần user làm.

### 2. Cross-check mismatches

| ID | Claim/file A | Evidence/file B | Observed mismatch | Severity | Required correction |
| --- | --- | --- | --- | --- | --- |

### 3. Unverified items

Nêu rõ lý do chưa kiểm chứng; không gộp vào pass.

### 4. Verified items

Chỉ liệt kê phép kiểm tra đã thực sự chạy/mở/đối chiếu.

Verdict duy nhất:

- `NOT READY — BLOCKERS PRESENT` nếu còn blocker;
- `NOT READY — ERRORS/UNVERIFIED REQUIRED ITEMS` nếu không có blocker nhưng còn lỗi hoặc artifact bắt buộc chưa xác minh;
- `READY FOR HUMAN FINAL REVIEW` chỉ khi không còn TODO thực trong submission surface, mọi artifact bắt buộc tồn tại và chuỗi cross-check không đứt.

Không dùng verdict `READY` tuyệt đối: việc upload Moodle và xác nhận evidence thật cuối cùng vẫn do user chịu trách nhiệm.
