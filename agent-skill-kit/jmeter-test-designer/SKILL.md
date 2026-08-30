---
name: jmeter-test-designer
description: "Thiết kế JMeter Load, Stress, Spike và Soak/Endurance theo workflow phê duyệt bắt buộc: phỏng vấn SUT, chốt ma trận dữ liệu, rồi mới xác định workload và ngưỡng. Dùng khi cần thiết kế hoặc review test plan JMeter có kiểm soát; không sinh JMX hay con số tải trước khi user duyệt context và data matrix."
---

# JMeter Test Designer

Thiết kế test plan bằng một state machine có approval gate. Không thay thế dữ kiện còn thiếu bằng giả định ngầm và không biến giá trị gợi ý thành kết quả đo.

## Trình tự phối hợp với các skill khác trong bộ HW05

Skill này chỉ phụ trách **thiết kế và sinh JMX** (Bước 1–3 dưới đây). Nó không thu thập evidence
thực thi, không phân tích JTL, và không audit bản nộp cuối. Thứ tự dùng đúng trong bộ 4 skill:

```text
1. jmeter-test-designer   -> chốt context, data matrix, profile, sinh JMX (skill này)
2. (chạy test thủ công trong JMeter, ngoài phạm vi mọi skill)
3. perf-evidence-collector -> audit evidence thực thi (JTL/screenshot/log) sau khi chạy
4. jtl-data-analyzer        -> phân tích JTL đã được xác minh, viết AI Critique
5. submission-auditor       -> audit toàn bộ trước khi nộp
```

Bốn skill dùng chung `agent-skill-kit/hw05-performance-testing/references/report-artifacts.md`
làm bản đồ heading trong `report/MAIN_REPORT.md`/`README.md`. Skill này chỉ được sửa các heading
được gán quyền sở hữu cho `jmeter-test-designer` trong file đó (scope/endpoint mapping, data &
correlation, bảng cấu hình Load/Stress/Spike/Soak, human review thiết kế). Nếu heading cần sửa
không thuộc quyền sở hữu của skill này, dừng lại và báo cho user thay vì tự ghi đè.

## Trạng thái bắt buộc

Theo dõi trạng thái trong suốt phiên:

```text
STEP_1_CONTEXT_APPROVED = false
STEP_1_AUDIT_LOGGED = false
STEP_2_DATA_APPROVED = false
STEP_2_AUDIT_LOGGED = false
STEP_3_PROFILE_APPROVED = false
STEP_3_AUDIT_LOGGED = false
```

Chỉ coi một bước được duyệt khi user xác nhận rõ ràng như “duyệt”, “đồng ý cấu hình này” hoặc cung cấp bản sửa và xác nhận bản sửa là cuối cùng. Im lặng, trả lời một phần, hoặc chuyển chủ đề không phải approval.

Ở đầu mỗi phản hồi trong workflow, nêu ngắn gọn bước hiện tại, dữ kiện còn thiếu và gate tiếp theo. Không tự nhảy bước.

## Hard gates

### Gate A — trước khi Bước 1 và Bước 2 đều được duyệt

Khi `STEP_1_CONTEXT_APPROVED` hoặc `STEP_2_DATA_APPROVED` còn `false`, tuyệt đối không được:

- sinh nội dung XML/JMX, file `.jmx`, đoạn code tạo JMX hoặc lệnh chạy một test plan chưa được duyệt;
- đưa ra bất kỳ con số workload hay ngưỡng định lượng nào, gồm VU/thread, iteration, ramp-up, duration, stage, RPS, throughput, think time, percentile target, error-rate target hoặc stop threshold;
- sao chép các workload mẫu từ tài liệu tham khảo như thể chúng phù hợp với SUT;
- tuyên bố một threshold, capacity, bottleneck hoặc kết quả hiệu năng;
- âm thầm chọn endpoint, success code, extractor, dữ liệu seed, cơ chế reset hoặc listener thay user.

Khi bị yêu cầu sinh JMX hoặc con số quá sớm, từ chối phần đó trong một câu, chỉ ra gate chưa đạt, rồi tiếp tục đúng câu hỏi của bước hiện tại.

### Gate B — sau khi Bước 1 và Bước 2 được duyệt

Chỉ khi cả bốn cờ sau đều `true` mới được bắt đầu Bước 3 và đưa ra con số hiệu chỉnh:

```text
STEP_1_CONTEXT_APPROVED
STEP_1_AUDIT_LOGGED
STEP_2_DATA_APPROVED
STEP_2_AUDIT_LOGGED
```

Mọi con số ở Bước 3 phải được gắn nhãn `CANDIDATE — CHƯA ĐO`, kèm căn cứ và điều kiện hiệu chỉnh. Không gọi chúng là measured threshold.

### Gate C — trước khi sinh JMX

Chỉ được sinh hoặc chỉnh JMX khi:

```text
STEP_3_PROFILE_APPROVED = true
STEP_3_AUDIT_LOGGED = true
```

Ngoài hai điều kiện trên, user còn phải yêu cầu rõ ràng việc sinh/chỉnh JMX. Approval profile không tự động là quyền tạo file.

## Bước 1 — Phỏng vấn lấy SUT context

### Mục tiêu

Chốt một `SUT Context Record` đủ để biết chính xác test cái gì, theo thứ tự nào, trong môi trường nào và success được xác định ra sao. Chưa thiết kế workload và chưa đưa ra con số.

### Cách phỏng vấn

Không hỏi một danh sách dài nếu repository hoặc tài liệu đã trả lời được. Trước hết đọc các tài liệu/source user đặt trong scope, trích dẫn file hoặc endpoint làm căn cứ, rồi chỉ hỏi phần còn thiếu hoặc mâu thuẫn.

Thu thập bắt buộc:

1. **Identity**: tên SUT, repository, commit/version thực sự sẽ test, môi trường và base URL.
2. **Business transaction**: chuỗi endpoint theo đúng thứ tự; endpoint nào là auth-heavy, read-heavy và transactional.
3. **Request contract**: method, path, content type, body/query/header cần thiết và success code thực tế của từng request.
4. **Dependencies/correlation**: giá trị nào sinh từ response trước, JSONPath/regex dự kiến và request nào tiêu thụ nó; tối thiểu xem xét JWT và ID của entity vừa tạo.
5. **Authentication/state**: loại credential, role, token lifetime, lockout, session/cookie và điều kiện reset tài khoản.
6. **Environment topology**: load generator cùng hay khác máy SUT, database, network path, resource monitor và giới hạn máy có thể ảnh hưởng phép đo.
7. **State lifecycle**: seed trước run, mutation trong run, cleanup/reset sau run và tác động của restart.
8. **Success oracle**: response code, trường JSON/message bắt buộc, assertion lỗi và cách xử lý dependency failure.
9. **Measurement output**: các trường JTL cần giữ, cách phân biệt sampler/transaction và report/listener bắt buộc nếu có.

### Đầu ra bắt buộc

Xuất đúng hai bảng, không có workload number:

| Context field | Confirmed value | Evidence/source | Status |
| --- | --- | --- | --- |
| SUT/version/environment | ... | ... | Confirmed/Missing/Conflict |
| Ordered workflow | ... | ... | Confirmed/Missing/Conflict |
| Auth and state | ... | ... | Confirmed/Missing/Conflict |
| Topology/resources | ... | ... | Confirmed/Missing/Conflict |
| Reset/cleanup | ... | ... | Confirmed/Missing/Conflict |

| Request label | Method/path | Input contract | Correlation produced/consumed | Success oracle | Evidence |
| --- | --- | --- | --- | --- | --- |
| ... | ... | ... | ... | ... | ... |

Không điền giá trị đoán. Dùng `MISSING — USER INPUT REQUIRED` hoặc `CONFLICT — USER DECISION REQUIRED`.

### Approval gate của Bước 1

Kết thúc bằng yêu cầu user:

```text
Hãy sửa các ô Missing/Conflict và xác nhận rõ “Duyệt SUT Context Bước 1”.
Tôi chưa được phép lập workload number hoặc sinh JMX.
```

Khi user duyệt, đặt `STEP_1_CONTEXT_APPROVED = true`, khóa bản context đã duyệt bằng một revision label, rồi thực hiện AI Audit trước khi sang Bước 2.

## Bước 2 — Lập và duyệt ma trận data

### Tiền điều kiện

Chỉ bắt đầu khi:

```text
STEP_1_CONTEXT_APPROVED = true
STEP_1_AUDIT_LOGGED = true
```

Nếu context thay đổi trong Bước 2, quay lại Bước 1, tạo revision mới và yêu cầu duyệt lại phần bị ảnh hưởng.

### Mục tiêu

Chứng minh mỗi request lấy dữ liệu từ đâu, dữ liệu nào phải unique, dữ liệu nào được correlate và state được reset thế nào. Vẫn chưa được đưa ra workload number hoặc sinh JMX.

### Ma trận bắt buộc

Lập một dòng cho từng field thực sự được request hoặc assertion sử dụng:

| Request label | Field/variable | Source | Producer | Consumer | Scope/lifetime | Unique rule | Secret? | Validation/assertion | Reset/cleanup | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ... | ... | CSV/constant/extracted/generated | ... | ... | run/VU/iteration | ... | Yes/No | ... | ... | Confirmed/Missing |

Áp dụng các invariant sau khi phù hợp với SUT đã duyệt:

- CSV column phải khớp chính xác tên biến được dùng.
- Credential test không được đưa vào log công khai nếu là secret; không dùng password sai trong concurrent workload trừ khi mục tiêu đã duyệt là lockout.
- Token và ID động phải được extract từ response, có default sentinel và có assertion không rỗng trước khi request phụ thuộc chạy.
- Dữ liệu mutation phải unique nhưng tái hiện được. Ưu tiên kết hợp `run_id`, seed của VU/row và iteration; ghi lại run ID thật.
- Coupon/code có ràng buộc unique phải dùng định dạng hợp lệ và không trùng giữa các rerun.
- Nếu dùng CSV không recycle, chứng minh dữ liệu đủ cho consumption model; nếu recycle, chứng minh unique suffix ngăn collision.
- Response code phải theo contract thực tế, không mặc định create luôn trả `201`.
- Assertion thời gian chỉ là SLO, không thay cho assertion chức năng.
- Error do duplicate, CSV EOF, extractor sentinel hoặc assertion sai là test-data/script failure, không phải capacity failure.
- Setup, mutation, cleanup và hậu quả của reset phải được mô tả rõ.

### Data-flow review

Sau ma trận, xuất sơ đồ text ngắn theo dữ liệu phụ thuộc, ví dụ ở mức ký hiệu, không điền giá trị giả:

```text
credential → login → token → protected requests
category payload → create category → category_id → product payload
run identity + row/VU/iteration identity → unique mutation fields
```

Liệt kê riêng:

- collision risks;
- data exhaustion risks;
- secret exposure risks;
- missing extractor/assertion risks;
- cleanup/reset risks.

### Approval gate của Bước 2

Kết thúc bằng yêu cầu user:

```text
Hãy sửa các dòng Missing/risk chưa chấp nhận và xác nhận rõ “Duyệt Data Matrix Bước 2”.
Cho đến lúc đó tôi vẫn không được phép đưa ra workload number hoặc sinh JMX.
```

Khi user duyệt, đặt `STEP_2_DATA_APPROVED = true`, khóa data-matrix revision, rồi thực hiện AI Audit trước khi sang Bước 3.

## Bước 3 — Xác định cấu hình và ngưỡng Load/Stress/Spike/Soak

### Tiền điều kiện

Không bắt đầu nếu Gate B chưa đạt. Nếu user thay đổi workflow, correlation, data capacity, uniqueness hoặc reset strategy, hủy approval liên quan và quay lại bước trước.

### Phân biệt bắt buộc

Không trộn ba loại giá trị:

1. `OBSERVED`: số lấy từ traffic/hardware/JTL thật, kèm nguồn.
2. `CANDIDATE — CHƯA ĐO`: cấu hình ban đầu để chạy thử, không phải capacity.
3. `MEASURED THRESHOLD`: chỉ được dùng sau execution thật, raw JTL và resource evidence.

Nếu chưa có baseline thực, chỉ được đề xuất `CANDIDATE — CHƯA ĐO`. Không được gọi candidate là threshold của hệ thống.

### Thu thập căn cứ định lượng

Trước khi đề xuất con số, yêu cầu và kiểm tra:

- traffic/concurrency/RPS quan sát được hoặc mục tiêu nghiệp vụ;
- hardware và việc load generator có dùng chung máy SUT hay không;
- kết quả smoke/baseline nếu đã có;
- SLO p95/error rate hoặc tiêu chí ổn định do user chịu trách nhiệm;
- think time/pacing phù hợp hành vi;
- giới hạn data capacity từ Bước 2;
- thời lượng khả dụng và stop/safety condition;
- listener/report requirement.

Thiếu căn cứ nào thì ghi rõ assumption và xin user duyệt assumption trước khi dùng nó để tính số.

### Ma trận profile bắt buộc

Đề xuất bốn profile trong một bảng: Load, Stress, Spike, và Soak/Endurance. Mọi ô số phải mang nhãn `CANDIDATE — CHƯA ĐO` cho đến khi có execution evidence:

| Scenario | Business purpose | Start/baseline load | Ramp/stages | Hold | Think time/pacing | Acceptance/stop criteria | Recovery check | Distinct report view | Rationale/evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Load | Expected stable behavior | ... | ... | ... | ... | ... | ... | ... | ... |
| Stress | First sustained breach and highest stable stage | ... | ... | ... | ... | ... | ... | ... | ... |
| Spike | Burst impact and return to baseline | ... | ... | ... | ... | ... | ... | ... | ... |
| Soak | Sustained load 10–15 phút để tìm ngưỡng ổn định phần cứng (endurance) | ... | ... | ... | ... | ... | ... | ... | ... |

Quy tắc thiết kế:

- Cả bốn profile dùng cùng ordered workflow và data contract đã duyệt.
- Load kiểm tra concurrency dự kiến ổn định; Stress tăng theo stage có cửa sổ đủ để đánh giá; Spike có baseline, rise, hold và recovery rõ ràng; Soak giữ **một mức tải không đổi** (không ramp theo stage như Stress, không burst như Spike) trong toàn bộ 10–15 phút.
- Soak phải có: baseline load ổn định đã được Load/Stress xác nhận là an toàn để giữ liên tục, tổng duration nằm trong khoảng 10–15 phút, và các mốc quan sát bắt buộc ở đầu/giữa/cuối run cho CPU/RAM (không chỉ 1 điểm ảnh).
- Không dùng cùng listener/report type cho nhiều plan nếu yêu cầu bài cấm lặp.
- View Results Tree chỉ dùng cho debug nhỏ; full measurement chạy non-GUI và sinh HTML từ raw JTL.
- Stress threshold là stage cao nhất thỏa tiêu chí trong toàn cửa sổ, không đơn giản là stage có RPS cao nhất.
- Soak threshold (endurance threshold) chỉ được tuyên bố là `MEASURED THRESHOLD` sau khi có raw JTL và resource trend đủ ba mốc của chính run Soak; không được suy ra ngưỡng này từ cấu hình Stress hoặc từ candidate chưa chạy.
- Error từ data/script không được tính là saturation trước khi phân loại response và failure cause.
- Mọi revision sau smoke/hardware observation phải được ghi lý do.

### Approval gate của Bước 3

Trình bày assumptions, profile matrix (bốn scenario) và danh sách rủi ro. Yêu cầu user xác nhận rõ:

```text
Duyệt Profile Matrix Bước 3 (Load/Stress/Spike/Soak) và các CANDIDATE — CHƯA ĐO.
```

Khi user duyệt, đặt `STEP_3_PROFILE_APPROVED = true`, khóa profile revision và ghi AI Audit. Chỉ sau đó mới có thể nhận một yêu cầu riêng để sinh/chỉnh JMX.

## AI Audit bắt buộc sau mỗi bước

Sau khi user duyệt một bước, phải ghi audit trước khi bắt đầu bước kế tiếp.

1. Lấy timestamp thật từ clock/tool ở thời điểm ghi; không suy đoán hoặc tái tạo về sau.
2. Append vào `report/AI_AUDIT_REPORT.md`; không ghi đè entry cũ.
3. Giữ nguyên văn 100% prompt user dẫn đến output của bước, kể cả khoảng trắng/nội dung quan trọng. Không tóm tắt phần Prompt.
4. AI Output chỉ tóm tắt ngắn gọn output, revision đã duyệt, quyết định của user và gate được mở.
5. Nếu không thể ghi file, xuất block sẵn để user lưu và giữ cờ `*_AUDIT_LOGGED = false`; không chuyển bước cho đến khi audit được lưu thật.
6. Không bịa timestamp, artifact, approval hoặc user decision.

Định dạng bắt buộc:

````markdown
- Name of the AI tool: <tên tool/model thật>
- Date/time: <ISO timestamp thật có timezone>
- Prompt:
```
<nguyên văn 100% prompt user>
```
- AI Output:
```
<tóm tắt output, revision được duyệt và trạng thái gate>
```
````

Sau khi append thành công, đặt cờ `STEP_N_AUDIT_LOGGED = true` và báo đường dẫn entry cho user.

## Khi user quay lại giữa workflow

- Tóm tắt revision đã duyệt và các cờ trạng thái dựa trên transcript/audit thật; không đoán approval.
- Nếu không chứng minh được approval hoặc audit entry, coi gate tương ứng là `false`.
- Thay đổi request contract, workflow hoặc environment làm mất hiệu lực approval Bước 1.
- Thay đổi correlation, CSV schema, unique rule hoặc reset strategy làm mất hiệu lực approval Bước 2.
- Thay đổi SLO, hardware, workload shape hoặc data capacity làm mất hiệu lực approval Bước 3.

## Điều kiện hoàn tất thiết kế

Chỉ tuyên bố thiết kế sẵn sàng sinh JMX khi:

- ba revision đã được user duyệt rõ ràng (Bước 1, Bước 2, Bước 3 — Bước 3 bao gồm cả bốn scenario Load/Stress/Spike/Soak trong cùng một revision);
- ba audit entry đã được append với timestamp thật;
- không còn `Missing/Conflict` ảnh hưởng request contract, correlation, data uniqueness hoặc workload safety;
- profile number vẫn được phân biệt rõ với measured threshold;
- user đã yêu cầu riêng việc sinh/chỉnh JMX.

## Cập nhật tài liệu thiết kế

Khi user yêu cầu tạo hoặc cập nhật report cùng với thiết kế, đọc `agent-skill-kit/hw05-performance-testing/references/report-artifacts.md` trước khi sửa file. Sau mỗi bước được duyệt, cập nhật đúng phần liên quan của `report/MAIN_REPORT.md`: scope/endpoint mapping (Bước 1), data & correlation (Bước 2), hoặc bảng cấu hình Load/Stress/Spike/Soak và human review (Bước 3). Các workload chưa chạy phải giữ nhãn `CANDIDATE — CHƯA ĐO`; không điền metric, threshold hay evidence path. Cập nhật `README.md` chỉ với tóm tắt đã được xác minh, và cập nhật checklist nếu artifact được tạo/thiếu. Mỗi lần sửa phải nêu file, heading và nguồn của từng fact mới. Chỉ sửa các heading mà `report-artifacts.md` gán quyền sở hữu cho `jmeter-test-designer`; nếu một heading thuộc quyền của skill khác (vd metric/threshold đo được thuộc `jtl-data-analyzer`, evidence path thuộc `perf-evidence-collector`), không ghi đè — báo cho user biết cần chạy skill tương ứng.
