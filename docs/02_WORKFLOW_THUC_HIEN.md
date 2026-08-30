# Workflow thực hiện HW05 cho Workflow 5

## 1. Kết quả đầu ra cần đạt

Bạn cần tạo ba JMeter plan dùng cùng chuỗi nghiệp vụ admin, ba CSV/JTL/report tương ứng, một soak run 10–15 phút, evidence phần cứng/tài nguyên, video tối thiểu 6 phút, AI analysis có human correction, đề xuất continuous testing, AI audit, Git log, README và bản PDF của các tài liệu bắt buộc.

Các mục có nhãn `TODO (REAL EVIDENCE REQUIRED)` chỉ được thay bằng dữ liệu bạn tự chạy/ghi nhận.

## 2. Cấu trúc artifact đề xuất

```text
test-plans/
  23127104_Load_YYYYMMDD.jmx
  23127104_Stress_YYYYMMDD.jmx
  23127104_Spike_YYYYMMDD.jmx
test-data/
  admin_workflow_load.csv
  admin_workflow_stress.csv
  admin_workflow_spike.csv
results/
  load/<raw.jtl + html-report/>
  stress/<raw.jtl + html-report/>
  spike/<raw.jtl + html-report/>
  soak/<raw.jtl + analysis/>
evidence/
  hardware/
  load/
  stress/
  spike/
  soak/
report/
```

Không tạo file/folder evidence giả chỉ để đủ cây thư mục.

## 3. Phase A – Chốt scope và baseline

1. Xác nhận với nhóm rằng không ai trùng Workflow 5.
2. Ghi URL repository SUT và commit SHA bạn thực sự test.
3. Cài Node.js >=18, JDK phù hợp và JMeter; ghi version.
4. Khởi tạo database theo hướng dẫn SUT, chạy backend ở port 3000.
5. Dùng Postman/curl hoặc một-thread JMeter xác nhận từng endpoint và payload.
6. Chụp hardware report có hostname và lập bảng CPU/RAM/OS/storage.
7. Ghi giả định: localhost, frontend không thuộc tải chính, máy tạo tải có cùng/khác máy SUT.

Exit criteria: một vòng workflow chạy thành công, token/category ID được correlate và không có dữ liệu trùng.

## 4. Phase B – Chuẩn bị CSV

Header gợi ý:

```csv
email,password,run_id,row_seed,category_name,product_name,price,description,image_url,coupon_code,coupon_type,discount_value,min_order_amount,expired_at,max_uses_per_user
```

Mỗi dòng dùng `row_seed` khác nhau. `category_name` và `coupon_code` cần kết hợp `run_id`/seed. Không commit credential production. Với tài khoản admin seed dùng chung, nhiều thread login đúng là hợp lệ; tuyệt đối không tạo dữ liệu password sai trong test chính.

Nếu dùng import endpoint, JSON body là `{ "products": [...] }`, không phải upload multipart trực tiếp vì frontend parse CSV rồi gửi mảng JSON.

## 5. Phase C – Xây Test Plan gốc

Tạo cấu trúc:

1. Test Plan/User Defined Variables: `base_url=http://localhost:3000`.
2. HTTP Request Defaults và HTTP Header Manager cho JSON.
3. CSV Data Set Config.
4. Thread Group.
5. Transaction Controller cho toàn workflow và từng nhóm.
6. Login sampler + response-code assertion + JSON Extractor `$.token`.
7. Header `Authorization: Bearer ${token}` cho request sau.
8. Hai GET read-heavy với assertions.
9. Tạo category + JSON Extractor `$.id`.
10. Tạo product dùng category ID hoặc import product array.
11. Tạo coupon với code duy nhất.
12. Timers/think time.
13. Listener riêng của scenario và Simple Data Writer/JTL configuration.

Chạy 1 VU × 1 iteration trong GUI. Chỉ chuyển sang tải khi mọi assertion pass và dữ liệu database đúng.

## 6. Phase D – Tách ba profile

Các số sau là điểm bắt đầu phải hiệu chỉnh, không phải kết quả đo:

| Plan | Profile ban đầu | Listener/report không lặp |
| --- | --- | --- |
| Load | 20 VU, ramp-up 120 s, giữ 8 phút | Summary Report |
| Stress | 10→20→40→60 VU, mỗi bậc 2 phút | Aggregate Report |
| Spike | 10 VU baseline, nhảy 80 VU trong <=10 s, giữ 60 s, về 10 VU trong 2 phút | View Results Tree chỉ bật khi debug |

Đặt tên bằng ngày chạy thật: `23127104_{Load|Stress|Spike}_YYYYMMDD.jmx`. Không coi việc đổi Thread Group và Save As là đủ: kiểm tra lại timer, scheduler, stage shape, listener và data capacity.

## 7. Phase E – Chạy và lấy evidence

Cho từng scenario:

1. Reset/chuẩn bị dữ liệu theo run ID mới.
2. Smoke test 1 VU.
3. Mở Task Manager tab Performance/Details, hiển thị backend Node process.
4. Chạy non-GUI và ghi start/end time.
5. Quay/chụp tool và resource monitor trong cùng frame.
6. Theo dõi CPU, RAM, disk và server log.
7. Lưu raw JTL, HTML report và run notes ngay sau khi kết thúc.
8. Kiểm tra response-code distribution trước khi gọi run “hợp lệ”.

Nếu 401/403 xuất hiện, dừng để kiểm token/lockout. Nếu coupon duplicate hoặc CSV EOF, sửa test data rồi chạy lại; không gộp run lỗi script vào kết quả capacity.

## 8. Phase F – Stress threshold và soak

Từ stress test, tìm bậc cao nhất vẫn đáp ứng tiêu chí được khai báo trước. Chọn tải soak thấp hơn hoặc bằng bậc ổn định cuối, chạy 10–15 phút. Báo:

- stable RPS;
- p95 và error rate;
- CPU range/peak;
- memory start/peak/end và xu hướng;
- dấu hiệu disk/SQLite contention;
- tiêu chí khiến tải cao hơn không còn ổn định.

Đây mới là endurance threshold trên phần cứng của bạn. Không lấy con số profile gợi ý làm threshold.

## 9. Phase G – AI analysis và human review

1. Giữ raw JTL nguyên vẹn và đưa bản sao/dữ liệu cần thiết cho AI.
2. Yêu cầu AI nêu công thức, cửa sổ thời gian, kết quả theo label và response code.
3. Chạy `analyze_jtl.py` hoặc JMeter report làm phép đối chiếu.
4. Lập bảng AI claim → raw value → verdict → correction.
5. Yêu cầu AI đề xuất optimization.
6. Phân loại feasible/conditional/unsupported/hallucinated dựa trên source và resource evidence.
7. Viết critique 200–300 từ sau khi đã có ít nhất một sai lệch thật.

## 10. Phase H – Bug/issue và video

Chỉ tạo GitHub Issue cho lỗi thật, có bước tái hiện, expected/actual, environment, evidence và tác động. Tách lỗi chức năng/authorization đã phát hiện trong source khỏi performance issue đo được.

Video tối thiểu 6 phút, narration tiếng Việt, nên có:

- scope/workflow và test data;
- cấu hình từng profile;
- tool + resource monitor cùng frame khi chạy;
- kết quả và threshold;
- AI misinterpretation + correction;
- demo skill trên một endpoint group.

## 11. Phase I – Continuous testing và đóng gói

Viết flowchart quyết định từ commit/PR, filter thay đổi, smoke, performance baseline, so p95 và flag regression. Trình bày cost/false alarms và human triage.

Sau mỗi bước logic, tạo một commit thật. Cuối cùng xuất `git log` ra file text, render Markdown sang PDF, chạy checklist, rồi tạo ZIP `23127104_HW05_AI_Performance_NNN.zip` với NNN là điểm tự đánh giá 000–100.

## 12. Thứ tự commit đề xuất

1. `docs: define workflow 5 scope and environment`
2. `test(load): add data-driven admin workflow plan`
3. `test(stress): add staged stress plan`
4. `test(spike): add spike and recovery plan`
5. `results: add raw reports and hardware evidence`
6. `analysis: add AI review and JTL corrections`
7. `docs: add continuous performance proposal`
8. `skill: add reusable HW05 performance skill`
9. `docs: finalize report and submission checklist`

Chỉ commit artifact thực sự đã tạo ở bước tương ứng; không bịa commit hash trong report.
