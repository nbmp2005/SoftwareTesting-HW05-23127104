---
name: jtl-data-analyzer
description: "Phân tích raw JMeter JTL theo quy trình script-first: bắt buộc chạy scripts/analyze_jtl.py trên log thật, chỉ suy luận từ JSON đã xác minh, đối chiếu metric và tự săn sai lệch định lượng để viết AI Critique. Dùng cho JTL metrics, threshold review và misinterpretation hunt; không dùng mắt đọc log để thay parser hoặc bịa số liệu còn thiếu."
---

# JTL Data Analyzer

Phân tích theo pipeline có gate. Raw JTL là evidence bất biến; JSON do parser sinh ra là nguồn duy nhất cho các con số AI dùng ở lần phân tích đầu tiên.

## Trình tự phối hợp với các skill khác trong bộ HW05

Skill này chạy **sau** `jmeter-test-designer` (thiết kế + JMX) và **sau** `perf-evidence-collector`
(xác minh raw JTL là evidence thật, không phải summary đổi đuôi hay file demo). Không phân tích
một JTL chưa được `perf-evidence-collector` đánh dấu `VERIFIED` hoặc ít nhất `PRESENT —
UNVERIFIED` với path xác định; nếu user đưa thẳng một file chưa qua bước đó, vẫn chạy Gate 1 của
skill này như bình thường (Gate 1 tự kiểm tra input độc lập), nhưng nhắc user rằng evidence
ledger toàn cục nên được cập nhật qua `perf-evidence-collector` để tránh hai nguồn trạng thái
khác nhau cho cùng một file.

Trước khi ghi vào `report/MAIN_REPORT.md` hoặc `README.md`, đọc
`agent-skill-kit/hw05-performance-testing/references/report-artifacts.md` để biết đúng heading
mình được sở hữu (Mục 12 toàn bộ; phần số liệu đo được trong Mục 7.3/8.2/9.2 và Mục 11; AI
Critique). Không sửa các heading thuộc quyền `jmeter-test-designer` hoặc `perf-evidence-collector`
(ví dụ bảng cấu hình `CANDIDATE`, đường dẫn evidence, ảnh hardware) — nếu cần sửa, báo user chạy
đúng skill sở hữu.

## Trạng thái bắt buộc

Theo dõi các cờ sau trong phiên:

```text
REAL_JTL_VERIFIED = false
SCRIPT_RUN_SUCCEEDED = false
JSON_OUTPUT_VERIFIED = false
INFERENCE_ALLOWED = false
CROSS_CHECK_COMPLETED = false
MISINTERPRETATION_HUNT_COMPLETED = false
CRITIQUE_READY = false
```

Không suy đoán trạng thái từ tên file. Chỉ đổi cờ khi đã thực hiện và kiểm tra bước tương ứng trong phiên hiện tại hoặc có provenance kiểm chứng được.

## Hard gates

### Gate 1 — cấm phân tích bằng mắt thay parser

Khi `SCRIPT_RUN_SUCCEEDED = false` hoặc `JSON_OUTPUT_VERIFIED = false`, tuyệt đối không được:

- đọc vài dòng JTL rồi tự tính sample count, error rate, throughput, mean hoặc percentile;
- dùng spreadsheet, regex, phỏng đoán hoặc số trong screenshot để thay kết quả script bắt buộc;
- đưa ra bảng metric, threshold, bottleneck, optimization hoặc kết luận pass/fail;
- tạo JSON giả, sửa JTL cho parser chạy được hoặc tự điền field còn thiếu;
- dùng output từ một JTL khác có tên tương tự.

Nếu script không tồn tại, không chạy được, JTL không phải CSV hợp lệ hoặc thiếu cột bắt buộc, dừng ở Bước 1. Báo lỗi cụ thể và đặt:

```text
TODO (REAL PARSE OUTPUT REQUIRED)
```

Không fallback sang “đọc bằng mắt”.

### Gate 2 — chỉ suy luận từ JSON đã xác minh

Chỉ khi tất cả điều kiện sau đúng mới đặt `INFERENCE_ALLOWED = true`:

```text
REAL_JTL_VERIFIED = true
SCRIPT_RUN_SUCCEEDED = true
JSON_OUTPUT_VERIFIED = true
```

Sau khi gate mở, mọi con số trong claim phải truy được tới JSON path cụ thể. Dữ kiện không có trong JSON phải ghi `NOT AVAILABLE IN PARSER OUTPUT`, không được suy ra ngầm từ tên scenario hoặc ảnh.

## Bước 1 — Chạy parser bắt buộc trên raw JTL thật

### 1.1. Nhận và xác minh input

Yêu cầu user cung cấp path của raw JTL. Kiểm tra read-only:

- file tồn tại, không rỗng và là JTL dạng CSV;
- header có tối thiểu `timeStamp`, `elapsed`, `label`, `responseCode`, `success`;
- file là raw sample log, không phải Summary Report/HTML/table được đổi đuôi;
- scenario, run date và attempt có provenance từ run notes/JMX/evidence;
- raw file không bị sửa trong quá trình phân tích.

Ghi `input_path`, kích thước file và, khi công cụ có sẵn, checksum SHA-256. Checksum chỉ chứng minh đúng input đã phân tích; không tự chứng minh run là thật.

Nếu không xác minh được log thật, giữ `REAL_JTL_VERIFIED = false`, cảnh báo và không chạy tiếp như thể input hợp lệ.

### 1.2. Resolve script

Parser bắt buộc là `scripts/analyze_jtl.py` thuộc bộ `hw05-performance-testing`. Trong repository này, đường dẫn canonical là:

```text
agent-skill-kit/hw05-performance-testing/scripts/analyze_jtl.py
```

Nếu skill được đóng gói cùng bản script ở `scripts/analyze_jtl.py`, có thể dùng bản đó sau khi xác nhận cùng giao diện. Không tự viết một parser tạm để bỏ qua yêu cầu. Nếu không tìm thấy script, dừng và yêu cầu user cung cấp/cài đúng script.

### 1.3. Gọi script — không được bỏ qua

Chọn output JSON mới, không ghi đè một analysis không cùng provenance. Chạy lệnh tương đương:

```powershell
python -X utf8 agent-skill-kit/hw05-performance-testing/scripts/analyze_jtl.py `
  <real-input.jtl> `
  --output <analysis-output.json>
```

Phải thực sự gọi tool/terminal; chỉ in lệnh cho user không được tính là đã chạy. Ghi lại:

- command thực;
- input path;
- output path;
- exit code;
- stdout/stderr liên quan;
- thời điểm phân tích thật nếu cần provenance, không giả làm execution time.

Script phải chạy thành công với exit code zero trước khi đặt `SCRIPT_RUN_SUCCEEDED = true`.

### 1.4. Xác minh JSON output

Mở JSON và kiểm tra:

- parse được, không rỗng;
- có group theo sampler label và `__overall__`;
- mỗi group có `samples`, `failures`, `error_rate_percent`, `throughput_samples_per_second`, `duration_seconds`;
- `elapsed_ms` có `mean`, `min`, `median`, `p90`, `p95`, `p99`, `max`;
- có `response_codes`;
- labels phù hợp input/scenario;
- output mới thật sự được sinh từ input và command vừa ghi.

Chỉ sau kiểm tra này đặt:

```text
JSON_OUTPUT_VERIFIED = true
INFERENCE_ALLOWED = true
```

Kết thúc Bước 1 bằng một `Parse Receipt`:

| Field | Verified value |
| --- | --- |
| Raw JTL | path |
| Raw checksum/size | value hoặc unavailable |
| Parser | exact path |
| Command/exit code | value |
| JSON output | path |
| Labels found | từ JSON |
| Gate status | OPEN/BLOCKED |

## Bước 2 — Suy luận chỉ từ JSON

### 2.1. Lập metric table có provenance

Với mỗi label, đọc từ JSON và xuất:

| Label | JSON path | Samples | Failures | Error rate | Throughput | Mean | Median | p90 | p95 | p99 | Max | Response codes |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |

Không chép số mà không kèm label và JSON path. Đơn vị elapsed là millisecond; throughput là samples/second theo observation duration do script tính.

### 2.2. Hiểu đúng phép tính của script

Khi diễn giải, giữ các quy tắc:

- error rate = `failures / samples × 100`;
- throughput = completed samples chia observation duration, không phải concurrent users;
- percentile được tính từ từng giá trị `elapsed`, không lấy trung bình percentile của label con;
- script dùng nội suy tuyến tính với vị trí `(n - 1) × percentile / 100` và làm tròn một số output;
- `p95` không phải request chậm nhất; `max` mới là giá trị lớn nhất trong group;
- elapsed, latency và connect time không đồng nghĩa. Parser hiện chỉ tổng hợp `elapsed`;
- error response nhanh không chứng minh hệ thống tốt;
- correlation không đồng nghĩa causation: JTL không tự chứng minh database, CPU hoặc network là root cause.

### 2.3. Kiểm tra tính hợp lệ của overall

Không mặc định `__overall__` luôn có ý nghĩa. Trước khi dùng:

- kiểm tra có Transaction Controller samples hoặc synthetic parent labels trong JTL không;
- xác định overall có đếm cả parent và child, làm double-count workload hay không;
- xác định các label có cùng observation window và cùng meaning không.

Nếu aggregation không có ý nghĩa, không dùng `__overall__` để kết luận capacity. Báo theo endpoint/transaction label phù hợp.

### 2.4. Stress/Spike/Soak window gate

JSON của parser hiện tổng hợp theo label, không tự chia stage/time window. Vì vậy:

- không được suy ra stage threshold từ một JSON aggregate nếu chưa có stage boundaries thật;
- không được so pre-spike, spike và recovery nếu chưa có time windows tương ứng;
- không được kết luận memory leak vì JSON không chứa resource trend;
- không được gọi một workload candidate là endurance threshold;
- với Soak cụ thể, endurance threshold chỉ được ghi là `MEASURED THRESHOLD` khi có: JSON của
  toàn bộ raw JTL run Soak (không phải Load/Stress), và resource evidence tối thiểu ba mốc
  đầu/giữa/cuối do `perf-evidence-collector` xác minh; nếu thiếu một trong hai, giữ
  `TODO (REAL STAGE-WINDOW ANALYSIS REQUIRED)` cho phần threshold đó.

Nếu cần stage analysis, yêu cầu run notes/timestamps thật và một phép chia cửa sổ có thể tái hiện. Mỗi stage-specific metric vẫn phải được tạo bằng deterministic parsing trên dữ liệu thật, không đọc thủ công bằng mắt. Nếu chưa có, đặt:

```text
TODO (REAL STAGE-WINDOW ANALYSIS REQUIRED)
```

### 2.5. Claim ledger

Trước khi viết prose, đăng ký mọi nhận định:

| Claim ID | Exact claim | JSON label/path | Numeric evidence | Type | Confidence | Needed external evidence |
| --- | --- | --- | --- | --- | --- | --- |
| C-... | ... | ... | ... | Measured fact/Inference/Recommendation | ... | ... |

Không viết claim ngoài ledger. Root-cause và optimization luôn cần source/resource/server evidence ngoài JSON.

## Bước 3 — Cross-check bắt buộc

Sau metric table nhưng trước kết luận cuối, đối chiếu tối thiểu:

1. một sample count;
2. một failure/error count;
3. một p95.

Dùng JMeter report hoặc cách tính thứ hai có thể tái hiện. Không sửa JSON để ép khớp. Ghi rõ:

- file/label/window;
- tool/phương pháp thứ hai;
- percentile method;
- parser value;
- cross-check value;
- absolute delta;
- relative delta khi mẫu số có ý nghĩa;
- verdict và lý do chênh nếu biết.

Sai khác làm tròn hoặc percentile rank vẫn phải được ghi; không gọi là lỗi AI nếu chỉ là khác phương pháp đã giải thích chính xác.

Chỉ đặt `CROSS_CHECK_COMPLETED = true` khi cả ba loại kiểm tra có evidence.

## Bước 4 — Misinterpretation hunt: AI tự soi lại chính mình

### 4.1. Freeze output cần audit

Giữ nguyên metric table, claim ledger và prose AI đã viết ở Bước 2. Không âm thầm sửa câu cũ trước khi audit. Gán Claim ID để có thể trích nguyên văn.

### 4.2. Audit từng claim

Với mỗi claim, tự hỏi:

- Con số có khớp đúng JSON label/path không?
- Đơn vị có đúng không?
- Có nhầm mean, median, p95, max, latency, connect hoặc elapsed không?
- Có so hai window/workload không tương đương không?
- Có gọi application/data/assertion error là overload không?
- Có suy ra memory leak từ một điểm hoặc database bottleneck chỉ từ JTL không?
- Có gọi fastest run là tốt nhất dù failures cao không?
- Có dùng overall bị double-count không?

### 4.3. Bảng chênh lệch bắt buộc

Không được viết “AI có thể đã nhầm” chung chung. Mỗi finding phải có:

| Claim ID | Nguyên văn claim AI | File/label/window | AI stated value | Correct reference value | Absolute delta | Relative delta | Verdict | Correction |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| ... | ... | ... | ... | ... | ... | ... | Wrong/Incomplete/Unsupported/Correct | ... |

Cách tính:

```text
absolute delta = AI stated value - correct reference value
relative delta (%) = absolute delta / correct reference value × 100
```

Nếu correct reference bằng zero, relative delta là `N/A`, không chia cho zero.

Finding chỉ hợp lệ khi có con số thật từ JSON và nguồn đối chiếu thật. Không chế tạo một lỗi AI để đủ bài.

### 4.4. Gate cho misinterpretation thật

Chỉ đặt `MISINTERPRETATION_HUNT_COMPLETED = true` khi:

- đã audit mọi claim định lượng;
- có ít nhất một claim sai/thiếu/unsupported được chứng minh;
- finding ghi rõ file, label, window, hai giá trị và delta;
- correction không mâu thuẫn parser/cross-check.

Nếu AI không có sai lệch định lượng thật, không bịa. Giữ:

```text
TODO (REAL AI MISINTERPRETATION WITH NUMERIC EVIDENCE REQUIRED)
```

Sau đó mở rộng kiểm tra sang stage window, overall double-count hoặc claim causal đã thực sự được AI viết. Nếu vẫn không có sai lệch thật, báo chưa đủ evidence để hoàn tất Critique theo yêu cầu này.

## Bước 5 — Viết AI Critique từ finding thật

Chỉ đặt `CRITIQUE_READY = true` và viết Critique khi:

```text
CROSS_CHECK_COMPLETED = true
MISINTERPRETATION_HUNT_COMPLETED = true
```

Đoạn Critique phải:

- dài theo yêu cầu bài, thường 200–300 từ nếu đề quy định;
- trích hoặc paraphrase sát một claim AI cụ thể có Claim ID;
- nêu raw JTL filename, label và time window;
- ghi AI stated value, correct value, absolute/relative delta và đơn vị;
- nêu phương pháp/parser/cross-check tạo giá trị đúng;
- giải thích vì sao AI sai: prompt thiếu window/method, nhầm metric, aggregation hoặc causal overreach;
- sửa kết luận bằng evidence;
- phân loại recommendation là feasible, conditional, unsupported hoặc hallucinated với source/resource evidence;
- rút ra một nguyên tắc human review cụ thể.

Cấm các câu Critique không có evidence như “AI đôi khi chưa chính xác”, “cần kiểm tra lại AI” hoặc “AI có thể hallucinate” nếu không gắn với claim và chênh lệch cụ thể.

Khung bắt buộc:

```text
AI claim [Claim ID] rằng [claim + value].
Trong [JTL file], label [label], window [window], parser JSON tại [path]
và phép đối chiếu [method] cho giá trị đúng [value + unit].
Chênh lệch là [absolute delta] ([relative delta]).
Sai lệch xảy ra vì [specific reason].
Correction là [evidence-backed correction].
Recommendation [name] được phân loại [class] vì [source/resource evidence].
Bài học human review là [specific reproducible principle].
```

Không thay placeholder bằng số ước lượng. Nếu thiếu bất kỳ trường nào, giữ `TODO (REAL EVIDENCE REQUIRED)` và không tuyên bố Critique hoàn tất.

## Optimization judgement

Sau misinterpretation hunt, đánh giá từng recommendation:

| Recommendation | Classification | JTL/JSON signal | Required source/resource evidence | A/B verification | Verdict |
| --- | --- | --- | --- | --- | --- |

Không khẳng định index, WAL, batching, serialization hoặc connection pool sẽ cải thiện chỉ vì đó là lời khuyên phổ biến. JTL có thể gợi ý nơi điều tra, không tự chứng minh database causality.

## Đồng bộ Markdown analysis

Khi được yêu cầu tạo/cập nhật tài liệu, đọc `agent-skill-kit/hw05-performance-testing/references/report-artifacts.md`. Sau khi các gate tương ứng mở, cập nhật phần kết quả của scenario trong `report/MAIN_REPORT.md` từ JSON có provenance; ghi parser command, JTL/JSON path và method. Chỉ cập nhật `report/AI_CRITIQUE.md` khi có finding misinterpretation thật theo Bước 4; nếu chưa có thì giữ TODO, không tạo critique giả. Đồng bộ summary đo được sang `README.md` và checklist/artifact index. Mỗi cập nhật phải chỉ rõ JSON path hoặc evidence dùng cho từng giá trị. Chỉ sửa các heading mà `report-artifacts.md` gán quyền sở hữu cho `jtl-data-analyzer`; không sửa bảng cấu hình `CANDIDATE` hay đường dẫn evidence thô — đó là quyền của `jmeter-test-designer`/`perf-evidence-collector`.

## Output package

Một analysis hoàn chỉnh phải chỉ ra:

- raw JTL path và checksum/size;
- exact parser command và exit code;
- JSON output path;
- metric table theo label;
- response-code distribution;
- claim ledger;
- cross-check table cho count, failures và p95;
- misinterpretation table có delta cụ thể;
- Critique dựa trên finding thật;
- optimization judgement;
- danh sách evidence còn thiếu với `TODO (REAL EVIDENCE REQUIRED)`.

Không tuyên bố hoàn tất nếu bất kỳ hard gate nào chưa đạt.
