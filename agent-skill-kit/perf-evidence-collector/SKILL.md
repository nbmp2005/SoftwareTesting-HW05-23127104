---
name: perf-evidence-collector
description: "Thu thập và audit bằng chứng performance test bằng checklist tuần tự bắt buộc. Dùng khi kiểm kê JMX, CSV, raw JTL, HTML report, ảnh Task Manager/phần cứng, run notes và server log; mọi artifact thiếu hoặc chưa kiểm chứng phải giữ cờ TODO (REAL EVIDENCE REQUIRED), không được suy diễn hay chế tạo evidence."
---

# Performance Evidence Collector

Thu thập evidence theo từng mục và chỉ công nhận thứ có thể kiểm tra. Đây là evidence gate, không phải công cụ tạo dữ liệu còn thiếu.

## Trình tự phối hợp với các skill khác trong bộ HW05

Skill này chạy **sau khi test đã được chạy thật** (sau `jmeter-test-designer` sinh JMX và sau khi
user tự chạy JMeter thủ công), và **trước** `jtl-data-analyzer` (JTL nên được audit ở đây trước
khi đưa vào phân tích) cũng như trước `submission-auditor` (audit cuối chỉ nên chạy khi evidence
ledger ở đây đã ở trạng thái ổn định).

```text
jmeter-test-designer -> (chạy test thủ công) -> perf-evidence-collector -> jtl-data-analyzer -> submission-auditor
```

Trước khi cập nhật `report/MAIN_REPORT.md`, `README.md` hoặc `report/SUBMISSION_CHECKLIST.md`,
đọc `agent-skill-kit/hw05-performance-testing/references/report-artifacts.md` để biết đúng heading
mình sở hữu (Mục 4 môi trường; phần evidence path trong Mục 7.3/8.2/9.2; Mục 10 lockout; phần
evidence CPU/RAM của Mục 11 Soak; Mục 13 bugs; Phụ lục A). Không tự điền số liệu đo được
(RPS/p95/error rate) — đó là quyền của `jtl-data-analyzer`; skill này chỉ xác nhận evidence
path/screenshot có tồn tại và hợp lệ.

## Quy tắc tuyệt đối

1. Không bịa thông số phần cứng, hostname, CPU, RAM, disk, tool version hoặc topology.
2. Không tự tạo, mô phỏng, bổ sung hay “làm mẫu” raw JTL, server log, screenshot, HTML report, Git commit, issue link, video timestamp hoặc execution timestamp.
3. Không đổi tên artifact để giả vờ nó được chạy vào ngày khác.
4. Không dùng giá trị thiết kế, tên file hoặc lời kể của user như bằng chứng kết quả thực thi.
5. Không sửa raw JTL, ảnh gốc hoặc log gốc. Chỉ đọc; nếu cần phân tích, tạo output riêng và ghi rõ input.
6. Không đánh dấu hoàn thành chỉ vì user trả lời “có”. Phải nhận path/attachment/link có thể kiểm tra hoặc giữ trạng thái chưa xác minh.
7. Không lấy timestamp từ trí nhớ hoặc tự điền thời gian hợp lý. Timestamp chỉ được lấy từ clock/tool thật, metadata, JTL, log hoặc ảnh có thời gian nhìn thấy được.
8. Khi thiếu hoặc không kiểm chứng được evidence, phải cảnh báo và gắn đúng chuỗi:

```text
TODO (REAL EVIDENCE REQUIRED)
```

## Trạng thái duy nhất được phép

Giữ một `Evidence Ledger` trong suốt phiên. Mỗi mục chỉ có một trạng thái:

| Status | Khi nào dùng | Có được coi là hoàn thành? |
| --- | --- | --- |
| `VERIFIED` | Artifact tồn tại, đọc/mở được và nội dung phù hợp mục đích | Có |
| `PRESENT — UNVERIFIED` | User nói có hoặc cung cấp path/link nhưng chưa thể kiểm tra | Không |
| `MISSING — TODO (REAL EVIDENCE REQUIRED)` | Chưa có artifact | Không |
| `INVALID — TODO (REAL EVIDENCE REQUIRED)` | Artifact rỗng, sai loại, sai scenario/date hoặc không chứng minh claim | Không |
| `NOT APPLICABLE` | Yêu cầu thật sự không áp dụng và đã ghi lý do | Có, chỉ cho mục không bắt buộc |

Không có trạng thái `ASSUMED`, `LIKELY`, `GENERATED` hoặc `PASS` không kèm verification.

## Cách hỏi bắt buộc

Hỏi **một mục trong mỗi lượt**, theo thứ tự checklist. Không gửi toàn bộ bảng câu hỏi rồi để user tự chọn.

Mỗi câu hỏi phải có bốn phần:

1. câu hỏi yes/no rõ ràng;
2. artifact/path cần user cung cấp;
3. điều kiện để đánh dấu `VERIFIED`;
4. trạng thái hiện tại nếu user chưa cung cấp.

Mẫu:

```text
Mục <ID> — <tên evidence>
Bạn đã có <evidence> chưa?
Nếu có, hãy gửi attachment hoặc path/link thật: <expected path/type>.
Tôi chỉ đánh dấu VERIFIED sau khi kiểm tra <verification conditions>.
Hiện tại: MISSING — TODO (REAL EVIDENCE REQUIRED).
```

Nếu user trả lời “chưa”, giữ TODO, hướng dẫn ngắn gọn cách thu thập thật, rồi hỏi mục tiếp theo. Nếu user trả lời “có” nhưng không cung cấp artifact/path, đặt `PRESENT — UNVERIFIED`, yêu cầu path và chưa chuyển mục. Nếu artifact được cung cấp, kiểm tra read-only, cập nhật ledger, rồi mới hỏi mục tiếp theo.

## Bước 0 — Chốt scope kiểm kê

Xác định scope từ yêu cầu và repository trước khi hỏi evidence:

- scenario cần kiểm kê: Load, Stress, Spike, Soak hoặc toàn bộ;
- student ID và quy tắc tên file;
- workspace/report đích;
- ngày chạy user tuyên bố;
- SUT repository và commit dự kiến.

Các dữ kiện này chỉ dùng để đối chiếu, chưa phải evidence. Nếu user không chỉ định scenario, audit theo thứ tự: Global → Load → Stress → Spike → Soak → Video/report links.

## Checklist G — Evidence toàn cục

Hỏi tuần tự từng mục.

### G1 — SUT identity

Hỏi:

```text
Bạn đã có repository URL và commit SHA thật của SUT được dùng khi chạy chưa?
```

Xác minh SHA có định dạng hợp lệ và, khi repository local có sẵn, đối chiếu bằng Git read-only. Không tự chọn commit hiện tại thay cho commit user đã test.

### G2 — Ảnh dxdiag/hardware có hostname

Hỏi:

```text
Bạn đã có ảnh dxdiag hoặc hardware report hiển thị hostname, OS, CPU và RAM chưa?
```

Yêu cầu attachment/path. Mở ảnh và kiểm tra các trường nhìn thấy được. Không suy ra model/dung lượng bị cắt khỏi ảnh. Storage thiếu thì hỏi riêng evidence storage và giữ TODO cho trường đó.

### G3 — Phiên bản công cụ

Hỏi:

```text
Bạn đã có ảnh hoặc output thật của Java, JMeter và Node.js version chưa?
```

Chỉ ghi version nhìn thấy trong output/file thật. Không lấy version từ tài liệu cài đặt hay tên thư mục nếu chưa xác minh.

### G4 — Clock/timezone và run identity

Hỏi:

```text
Bạn đã có bằng chứng clock/timezone thật và run ID dùng cho lần chạy chưa?
```

Không tự tạo run ID hoặc timestamp quá khứ. Nếu lấy thời gian hiện tại bằng tool, phải nói rõ đó là thời gian kiểm kê, không phải thời gian execution trước đó.

### G5 — Smoke test

Hỏi:

```text
Bạn đã có evidence smoke test một user/một iteration với mọi response và assertion được kiểm tra chưa?
```

Ảnh listener đơn lẻ chỉ chứng minh phần nhìn thấy. Nếu claim cần raw result hoặc server state mà ảnh không thể hiện, giữ phần đó unverified.

## Checklist S — Lặp cho từng scenario

Với từng scenario trong scope, tạo prefix `LOAD`, `STRESS`, `SPIKE` hoặc `SOAK`, rồi hỏi các mục sau đúng thứ tự.

### S1 — Ảnh Task Manager cùng frame

Phải hỏi nguyên ý:

```text
Bạn đã có ảnh chụp Task Manager trong lúc <scenario> đang chạy chưa?
```

Yêu cầu ảnh cho thấy, trong cùng frame khi đề bài yêu cầu:

- terminal/JMeter đang chạy;
- Task Manager hoặc resource monitor;
- CPU/RAM và, nếu có thể, process backend;
- context đủ để biết scenario nào đang chạy.

Ảnh Task Manager chụp ngày khác ở trạng thái idle chỉ là hardware/baseline evidence, không thay thế resource evidence của run. Không suy ra peak/range từ một ảnh tức thời.

### S2 — CSV input

Phải hỏi nguyên ý:

```text
Bạn đã có file CSV đầu vào thật cho <scenario> chưa?
```

Yêu cầu path/file. Kiểm tra read-only:

- file tồn tại, không rỗng và đọc được;
- header khớp biến mà JMX tham chiếu khi JMX có sẵn;
- quy tắc recycle/EOF phù hợp consumption model;
- mutation data có cơ chế unique;
- không vô tình công khai production secret;
- run ID/data phù hợp scenario được khai báo.

Không tự sinh CSV để lấp mục evidence. Có thể hướng dẫn user tạo lại, nhưng mục vẫn là TODO cho đến khi file thật được cung cấp và kiểm tra.

### S3 — Raw JTL

Phải hỏi nguyên ý:

```text
Bạn đã có raw JTL nguyên vẹn của <scenario> chưa?
```

Yêu cầu path/file. Kiểm tra read-only:

- file tồn tại, có kích thước lớn hơn zero và parse được;
- có header/cấu trúc JTL hợp lệ;
- có timestamp, elapsed, label, response code/message, success và các trường đo cần thiết nếu cấu hình đã yêu cầu;
- timestamp range phù hợp run notes/date khai báo;
- label phù hợp workflow/scenario;
- không phải bảng summary được đổi đuôi thành `.jtl`;
- không có dấu hiệu file demo/synthetic được dùng thay run thật.

Không tự viết dòng JTL, không ghép các attempt, không sửa response code và không tạo log giả để parser chạy được. Nếu JTL thiếu, mọi metric từ scenario phải giữ `TODO (REAL EVIDENCE REQUIRED)`.

### S4 — JMX đúng tên và ngày thật

Hỏi:

```text
Bạn đã có file JMX thực sự được dùng cho <scenario> chưa?
```

Kiểm tra:

- file tồn tại và parse được;
- tên đúng convention, ví dụ `<StudentID>_<Scenario>_<YYYYMMDD>.jmx`;
- ngày trong tên khớp ngày execution có evidence;
- CSV path, workload, listener và output configuration phù hợp run notes/JTL;
- không lấy một plan chưa chạy rồi tuyên bố đó là plan đã tạo JTL.

### S5 — HTML report

Hỏi:

```text
Bạn đã có thư mục HTML report sinh từ raw JTL của <scenario> chưa?
```

Kiểm tra thư mục có `index.html` và assets cần thiết; khi có thể, đối chiếu sample/error/time range với raw JTL. Một screenshot dashboard không thay thế toàn bộ report folder.

### S6 — Run notes và thời gian thật

Hỏi:

```text
Bạn đã có run notes ghi start time, end time, workload, run ID và observations thật của <scenario> chưa?
```

Không điền timestamp còn thiếu. Đối chiếu notes với timestamp JTL, ảnh, terminal hoặc log. Nếu chỉ có mốc từ trí nhớ, đánh dấu unverified.

### S7 — Server log thật

Hỏi:

```text
Bạn đã lưu server log thật tương ứng cửa sổ chạy <scenario> chưa?
```

Kiểm tra file/log capture có timestamp hoặc context đối chiếu được với run. Không tự mô phỏng log Node.js, SQLite error, lockout, timeout hoặc recovery. Nếu server không phát log cần thiết, ghi đúng “không có server log được thu thập” và giữ TODO nếu log là evidence bắt buộc cho claim.

### S8 — Response/error classification

Hỏi:

```text
Bạn đã có evidence phân bố response code và phân loại lỗi của <scenario> chưa?
```

Phân loại dựa trên JTL/HTML/server log thật:

- application/functional error;
- auth/lockout error;
- data collision hoặc CSV EOF;
- assertion/test-script error;
- suspected capacity/resource failure;
- unknown — insufficient evidence.

Không gọi duplicate coupon, extractor sentinel, CSV EOF hoặc assertion sai là overload.

### S9 — Không ghi đè và attempt lineage

Hỏi:

```text
Bạn đã lưu riêng từng attempt và xác định attempt nào là kết quả chính chưa?
```

Không cho phép JTL/report mới ghi đè artifact cũ. Nếu nhiều attempt, lập mapping giữa JMX, CSV, JTL, HTML, screenshot, notes và log của cùng attempt.

## Checklist Soak bổ sung

Sau checklist S cho Soak, hỏi thêm từng mục:

1. Ảnh resource lúc bắt đầu.
2. Ảnh resource ở giữa run.
3. Ảnh resource lúc kết thúc.
4. Raw JTL của toàn cửa sổ soak.
5. Evidence CPU range/peak, memory start/peak/end và disk observation.
6. Tiêu chí ổn định được khai báo trước khi kết luận threshold.

Không kết luận memory leak từ hai điểm ảnh và không gọi VU candidate là endurance threshold. Threshold chỉ được điền từ run thật có JTL và resource trend tương ứng.

## Account lockout và recovery evidence

Nếu có 401/403 hoặc user nói tài khoản bị khóa, chuyển sang checklist phụ, hỏi từng mục:

1. Có response 401/403 thật và timestamp không?
2. Run đã dừng để tránh làm bẩn kết quả chưa?
3. Có evidence thời gian chờ hoặc lệnh reset database thật không?
4. Việc reset đã xóa dữ liệu gì và có được ghi lại không?
5. Có smoke test sau recovery trước khi chạy lại không?

Không tự điền lock interval từ tài liệu như observed behavior. Tách discrepancy chức năng khỏi performance result.

## Cách xác minh artifact

Ưu tiên kiểm tra read-only trong workspace:

- tìm file bằng tên/path cụ thể;
- kiểm tra tồn tại, kích thước và định dạng;
- mở ảnh bằng công cụ xem ảnh;
- đọc header/sample tối thiểu của CSV/JTL/log mà không sửa file;
- đối chiếu date, scenario, run ID, labels và time window;
- kiểm tra link thật mở được nếu công cụ truy cập được.

Không thực hiện external mutation, upload, issue creation, video publication, test execution hoặc reset database chỉ vì đang audit evidence. Những hành động đó cần yêu cầu riêng của user.

## Evidence Ledger bắt buộc sau mỗi câu trả lời

Sau khi xử lý một artifact, cập nhật ledger ngắn gọn:

| ID | Scenario | Artifact/claim | Path/source | Verification performed | Status | Missing action |
| --- | --- | --- | --- | --- | --- | --- |
| ... | ... | ... | ... | ... | ... | ... |

Nếu một claim chỉ được hỗ trợ một phần, tách thành nhiều dòng. Ví dụ ảnh có CPU nhưng không có hostname: CPU có thể `VERIFIED`, hostname vẫn `MISSING — TODO (REAL EVIDENCE REQUIRED)`.

Sau ledger, hỏi đúng một mục kế tiếp.

## Báo cáo tổng kết

Chỉ xuất tổng kết khi đã hỏi hết checklist hoặc user yêu cầu dừng. Chia thành bốn nhóm:

### Verified

Liệt kê artifact đã kiểm tra, path, scenario và claim được hỗ trợ.

### Present but unverified

Liệt kê lời khai/path/link chưa mở hoặc chưa đối chiếu được. Không dùng chúng để điền metric.

### Missing real evidence

Mỗi mục phải có đúng cờ:

```text
TODO (REAL EVIDENCE REQUIRED)
```

Kèm một hành động cụ thể để user tự thu thập evidence thật.

### Invalid or mismatched

Nêu lý do: rỗng, sai date, sai scenario, screenshot không cùng frame, summary thay raw JTL, report không khớp JTL, hoặc timestamp không truy xuất được.

## Đồng bộ Markdown evidence

Khi user yêu cầu tạo/cập nhật report, đọc `agent-skill-kit/hw05-performance-testing/references/report-artifacts.md`. Chỉ sau khi mở và xác minh artifact, cập nhật theo nguồn: evidence path và trạng thái trong Phụ lục A của `report/MAIN_REPORT.md`, cấu hình/evidence theo scenario ở phần Load/Stress/Spike/Soak, và trạng thái thiếu/đã xác minh trong `report/SUBMISSION_CHECKLIST.md`. Cập nhật `README.md` chỉ với summary ngắn đã có provenance. Không điền CPU/RAM/metric từ lời khai; ghi TODO cụ thể cho bất kỳ evidence nào chưa xác minh. Giữ mỗi attempt riêng và báo lại các file/heading đã sửa. Chỉ sửa heading mà `report-artifacts.md` gán quyền sở hữu cho `perf-evidence-collector`; không tự điền số liệu đo được (RPS/error rate/percentile) — đó là quyền của `jtl-data-analyzer`.

## Completion gate

Không tuyên bố evidence package hoàn tất nếu còn bất kỳ artifact bắt buộc nào ở trạng thái `PRESENT — UNVERIFIED`, `MISSING` hoặc `INVALID`.

Đặc biệt, luôn kiểm tra ba câu hỏi trước khi kết luận:

```text
Đã có và xác minh ảnh Task Manager của từng run chưa?
Đã có và xác minh CSV của từng scenario chưa?
Đã có và xác minh raw JTL nguyên vẹn của từng scenario chưa?
```

Nếu bất kỳ câu trả lời nào là chưa, kết luận phải chứa `TODO (REAL EVIDENCE REQUIRED)` và không được sinh metric thay thế.
