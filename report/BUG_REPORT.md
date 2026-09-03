# BUG-SPIKE-001 – POST create coupon trả HTTP 500 trong Spike run

## Tóm tắt

Trong Spike run `23127104_Spike_20260830`, sampler `6 - POST create coupon` ghi nhận 126/367 request thất bại (34,3324%), tất cả có response code `500 Internal Server Error`. Toàn run có 126/2.332 failures (5,4031%). Hiện tượng được xác nhận; root cause chưa được xác nhận.

## Phân loại

| Thuộc tính | Giá trị |
| --- | --- |
| ID | [BUG-SPIKE-001](https://github.com/nbmp2005/SoftwareTesting-HW05-23127104/issues/1) |
| Loại | Performance test-script/test-data defect; SUT error-handling finding còn conditional |
| Severity | High đối với kết quả run vì hơn một phần ba thao tác tạo coupon thất bại |
| Priority | High cho triage trước khi dùng run để kết luận capacity |
| Trạng thái | Test-script fix verified ngày 03/09/2026; GitHub Issue cần cập nhật/đóng thủ công; duplicate error contract vẫn ngoài phạm vi |
| Scenario | Spike: pre-baseline 8 VU → burst 40 VU → recovery 8 VU |
| Endpoint | `POST http://localhost:3000/api/admin/coupons` |

## Điều kiện và bước tái hiện

1. Khởi động EShop backend tại `http://localhost:3000` và chuẩn bị credential admin hợp lệ.
2. Chạy `jmeter/23127104_Spike_20260830.jmx` với cùng một `run_id`, ví dụ `SP1`, và ghi raw JTL.
3. Cho test chạy hết ba Thread Group pre-baseline, burst và recovery.
4. Lọc raw JTL theo label `6 - POST create coupon` và kiểm tra `success`, `responseCode`, `responseMessage`.

## Kết quả mong đợi

Response Assertion trong JMX kỳ vọng HTTP 200 cho coupon code mới. Với payload trùng code, response đúng phải theo API contract; evidence hiện tại chưa đủ để khẳng định phải là một mã 4xx cụ thể.

## Kết quả thực tế

- JSON path `6 - POST create coupon.samples`: 367.
- JSON path `6 - POST create coupon.failures`: 126.
- JSON path `6 - POST create coupon.error_rate_percent`: 34,3324%.
- JSON path `6 - POST create coupon.response_codes`: HTTP 200 = 241, HTTP 500 = 126.
- JSON path `__overall__.failures`: 126; `__overall__.error_rate_percent`: 5,4031%.
- Phase pre-spike: 393 samples, 0 failures; 63 coupon samples, 0 failures.
- Phase burst: 1.545 samples, 63 failures; 63/241 coupon failures.
- Phase recovery: 394 samples, 63 failures; 63/63 coupon failures.
- Failed raw rows có `responseMessage = Internal Server Error` và assertion nhận 500 thay vì 200.

## Evidence

- Raw JTL: `results/23127104_Spike_20260830.jtl` (439.607 byte; SHA-256 `0DCF49DEDEF899ED570B545543F483535023DAEC89A23FE3127A8A2C1B7B3A23`).
- Parser JSON: `results/23127104_Spike_20260830_analysis.json`.
- Phase JSON: `results/spike-phase-analysis/pre-spike_analysis.json`, `spike_analysis.json`, `recovery_analysis.json`.
- JMeter HTML cross-check: `results/spike-report/statistics.json`.
- Screenshot cuối run: `evidence/23127104_Spike_Evidence_20260830.png` hiển thị 2.332 samples và 126 errors.
- Executed pre-fix JMX: phiên bản ở commit `8897078` dùng `CPN${run_id}${__counter(FALSE,seq)}` trong cả ba phase. JMX hiện tại dùng `CPN${run_id}_${__UUID()}` và đã được rerun ngày 03/09/2026.

Cross-check JMeter HTML khớp parser ở overall sample count (delta 0), failure count (delta 0) và p95 elapsed 16 ms (delta 0). Coupon p95 là 17,0 ms theo nội suy tuyến tính của parser và khoảng 17,6 ms theo JMeter; chênh lệch 0,6 ms là khác phương pháp percentile/làm tròn, không liên quan đến 126 failures.

## Phân tích nguyên nhân và giới hạn

Raw JTL chứng minh HTTP 500 nhưng không lưu response body hoặc server stack trace, nên không chứng minh database, CPU hay overload là root cause. Burst thất bại đúng 63 coupon — bằng số coupon pre-spike — và recovery thất bại toàn bộ 63 coupon khi ba Thread Group của executed JMX dùng lại `CPN${run_id}${__counter(FALSE,seq)}`. Pattern xác nhận test-data/counter collision với độ tin cậy cao. Server-side exception và cách API phải xử lý duplicate vẫn cần contract/server log để xác nhận.

## Đề xuất xác minh/fix

1. Dùng JMX hiện tại đã đổi coupon code sang UUID, dọn dữ liệu test và rerun với `run_id` mới.
2. Bật lưu response body cho failed samples trong một run chẩn đoán nhỏ và thu server log/DB constraint error cùng timestamp.
3. Nếu 500 biến mất, phân loại finding là test-script/data defect và sửa generator.
4. Nếu 500 vẫn xuất hiện với payload duy nhất, mở SUT defect cho concurrent coupon creation kèm server trace.
5. Nếu nguyên nhân là duplicate code, kiểm tra API contract; chỉ báo lỗi xử lý exception nếu contract yêu cầu validation response thay vì generic 500.

## Acceptance criteria

- Run chẩn đoán với payload coupon duy nhất không còn HTTP 500 do collision; hoặc
- SUT xử lý concurrent create đúng contract, không trả unhandled HTTP 500; và
- Spike run được chạy lại, raw JTL mới có provenance riêng trước khi kết luận capacity/recovery.

## Xác minh sau fix – 03/09/2026

Rerun `run_id=SPIKE_UUID_20260903_01` đáp ứng acceptance criteria của phần test-script:

- Raw JTL: `results/rerun-uuid-20260903/spike/23127104_Spike_UUID_20260903.jtl` (423.651 byte; SHA-256 `FE98B24EC73AE84E37DD07C23CE7F375DD5745B4FFBB2A078950BB273B9A0D92`).
- Whole-run: 2.330 samples, 0 failures, 0% error, p95 15 ms, 12,8438 samples/s; toàn bộ response HTTP 200.
- Coupon: 366 samples, 0 failures, p95 19 ms.
- Pre-spike/burst/recovery: lần lượt 393/1.537/400 samples, đều 0 failures; p95 15/13/20 ms.
- HTML cross-check tại `results/rerun-uuid-20260903/spike/html-report/statistics.json` khớp sample count, failure count và p95 whole-run (delta 0).

Kết luận: UUID loại bỏ collision; recovery đạt candidate criteria 0% lỗi và p95 <2.000 ms. Finding test-script được xác minh đã sửa. Kết quả HTTP 500 pre-fix vẫn có giá trị minh họa duplicate handling, nhưng không còn được dùng để đánh giá Spike performance.

---

# BUG-STRESS-001 – Coupon code bị tái sử dụng giữa các Stress stage, tạo HTTP 500 giả capacity failure

## Tóm tắt

Trong Stress run `23127104_Stress_20260830`, sampler `6 - POST create coupon` có 1.680/2.519 failures (66,6931%), đều là HTTP 500. Toàn run có 1.680/15.445 failures (10,8773%). Phân tích từng stage cho thấy failure bắt đầu từ Stage 2 và số failure coupon ở mỗi stage sau bằng đúng số coupon samples của stage ngay trước: 167, 338, 504 và 671. Executed JMX ở commit `8897078` dùng lại `CPN${run_id}${__counter(FALSE,seq)}` trong mỗi Thread Group; pattern này xác nhận lỗi thiết kế test-data/counter giữa các stage với độ tin cậy cao và không chứng minh SUT saturation.

## Phân loại

| Thuộc tính | Giá trị |
| --- | --- |
| ID | [BUG-STRESS-001](https://github.com/nbmp2005/SoftwareTesting-HW05-23127104/issues/2) |
| Loại | Performance test-script / test-data defect; có conditional SUT error-handling finding |
| Severity | Critical đối với tính hợp lệ của Stress threshold; High đối với tỷ lệ request coupon thất bại |
| Priority | P1 – phải sửa và rerun trước khi kết luận capacity |
| Trạng thái | Test-script fix verified ngày 03/09/2026; GitHub Issue cần cập nhật/đóng thủ công; SUT duplicate error contract vẫn ngoài phạm vi |
| Scenario | Stress 10 → 20 → 30 → 40 → 50 VU, mỗi stage 140 giây theo JMX |
| Endpoint | `POST http://localhost:3000/api/admin/coupons` |

## Bước tái hiện

1. Khởi động EShop backend tại `http://localhost:3000`, dùng credential admin hợp lệ và một `run_id` cố định, ví dụ `S1`.
2. Chạy `jmeter/23127104_Stress_20260830.jmx` và lưu raw JTL.
3. Để cả năm Thread Group chạy tuần tự.
4. Tách JTL theo prefix `threadName` của từng `Stress stage N`, chạy parser canonical và kiểm tra label `6 - POST create coupon`.

## Kết quả mong đợi

Mỗi request hợp lệ dùng coupon code duy nhất và trả HTTP 200 theo Response Assertion. Dữ liệu của stage sau không được trùng stage trước. Stress threshold phải phản ánh capacity của SUT, không bị nhiễu bởi constraint collision do script.

## Kết quả thực tế

| Stage JSON | VU | Coupon samples | Coupon failures | Coupon error rate | Response codes |
| --- | ---: | ---: | ---: | ---: | --- |
| `results/stress-stage-analysis/stage-1_analysis.json` | 10 | 167 | 0 | 0% | 200: 167 |
| `results/stress-stage-analysis/stage-2_analysis.json` | 20 | 338 | 167 | 49,4083% | 200: 171; 500: 167 |
| `results/stress-stage-analysis/stage-3_analysis.json` | 30 | 504 | 338 | 67,0635% | 200: 166; 500: 338 |
| `results/stress-stage-analysis/stage-4_analysis.json` | 40 | 671 | 504 | 75,1118% | 200: 167; 500: 504 |
| `results/stress-stage-analysis/stage-5_analysis.json` | 50 | 839 | 671 | 79,9762% | 200: 168; 500: 671 |

Số failure ở Stage 2–5 lần lượt bằng coupon sample count của Stage 1–4. Mỗi stage vẫn tạo thành công khoảng 166–171 coupon mới sau khi vượt qua dải code đã tồn tại, phù hợp với counter bị khởi tạo lại trong từng Thread Group.

## Evidence và cross-check

- Raw JTL: `results/23127104_Stress_20260830.jtl` (3.058.854 byte; SHA-256 `DF6EC49CCCEB4DBBF3AE6F9E0B6981B9EE27B2C3C5FE0AF7A4DF46567E4898DA`).
- Whole-run JSON: `results/23127104_Stress_20260830_analysis.json`.
- Stage inputs/JSON: `results/stress-stage-analysis/`.
- JMeter HTML: `results/stress-report/statistics.json`.
- Executed pre-fix JMX: phiên bản ở commit `8897078` dùng counter cục bộ; JMX hiện tại dùng `CPN${run_id}_${__UUID()}` và đã được rerun ngày 03/09/2026.
- Raw failed rows có label `6 - POST create coupon`, response `500 Internal Server Error` và assertion nhận 500 thay vì 200.

JMeter HTML khớp whole-run parser ở sample count 15.445, failure count 1.680 và p95 elapsed 14 ms; absolute delta của cả ba bằng 0. Tổng samples/failures của năm stage JSON cũng lần lượt bằng whole-run JSON: 15.445 và 1.680.

## Ảnh hưởng

- Làm Stress run fail từ Stage 2 và khiến việc chọn breakpoint/capacity threshold không hợp lệ.
- Error responses nhanh làm p95 aggregate không tăng tương ứng; nếu chỉ nhìn latency có thể kết luận sai rằng stage cao hơn vẫn tốt.
- HTTP 500 khi dữ liệu trùng có thể là một finding về error handling, nhưng cần API contract, response body và server log trước khi xác nhận SUT defect.

## Đề xuất fix và xác minh

1. Dùng JMX hiện tại đã sinh coupon code UUID duy nhất, dọn/seed database và đặt `run_id` mới.
2. Dọn/seed database có kiểm soát và dùng `run_id` mới cho mỗi attempt.
3. Lưu response body của failed samples trong diagnostic run nhỏ và thu server log cùng timestamp.
4. Rerun toàn bộ Stress scenario; chỉ dùng run mới để xác định first sustained capacity breach.
5. Nếu payload duy nhất vẫn trả 500, mở SUT defect riêng cho concurrent coupon creation.

## Acceptance criteria

- Không có duplicate coupon code giữa các stage trong payload đã ghi nhận.
- Không còn HTTP 500 do coupon collision.
- Stage metrics của rerun có error rate phản ánh SUT behavior thay vì test-data defect.
- Stress threshold chỉ được công bố từ rerun mới cùng resource evidence theo stage.

## Xác minh sau fix – 03/09/2026

Rerun `run_id=STRESS_UUID_20260903_01` xác nhận UUID loại bỏ defect:

- Raw JTL: `results/rerun-uuid-20260903/stress/23127104_Stress_UUID_20260903.jtl` (2.851.178 byte; SHA-256 `AA5EFC02BBD57F379D8DB1E0E145646D9079323B134EB2DD059DBA33631DAB97`).
- Whole-run: 15.397 samples, 0 failures, 0% error, p95 24 ms, 22,0486 samples/s; toàn bộ response HTTP 200.
- Coupon: 2.503 samples, 0 failures, p95 19 ms.
- Stage 1→5 đều 0 failures; throughput 7,4394→14,9190→22,2335→29,5590→36,8904 samples/s; p95 17→15→19→21→31 ms.
- HTML cross-check tại `results/rerun-uuid-20260903/stress/html-report/statistics.json` khớp sample count, failure count và p95 whole-run (delta 0).

Kết luận: finding test-script được xác minh đã sửa. Không quan sát error-based breakpoint đến 50 VU; đây là lower bound trong phạm vi test, không phải capacity tối đa vì không có stage trên 50 VU hoặc resource trend mới.
