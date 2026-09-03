# HW05 Submission Checklist

## A. Nội dung học thuật

- [x] Cùng một Workflow 5 xuất hiện trong Load, Stress và Spike.
- [x] Auth-heavy, read-heavy và transactional được map rõ.
- [x] Workload, ramp-up, duration, think time và lý do được ghi.
- [x] CSV data-driven và correlation JWT/category ID được chứng minh; UUID rerun xác nhận mutation coupon không còn collision.
- [x] Ba listener/report type khác nhau, không lặp; Spike View Results Tree đã disable trong JMX hiện tại để rerun non-GUI.
- [x] Human review ghi AI sai/thiếu gì, sửa gì và vì sao.
- [x] Soak khoảng 12 phút có raw JTL, whole-run/window metrics thật.
- [x] Stress UUID rerun có năm stage 0% lỗi; công bố lower bound 50 VU, không công bố capacity tối đa do chưa test cao hơn/thiếu resource trend.
- [x] Task 2 có AI claim, raw JTL value và correction.
- [x] Optimization được phân loại bằng evidence.
- [x] Continuous-testing proposal có flowchart, p95 gate, cost và false alarms.
- [x] AI Critique hoàn chỉnh 200–300 từ.

## B. Artifact bắt buộc

- [x] `23127104_Load_20260830.jmx` với ngày chạy thật.
- [x] `23127104_Stress_20260830.jmx` với ngày chạy thật.
- [x] `23127104_Spike_20260830.jmx` với ngày chạy thật.
- [x] Ba raw JTL canonical đầy đủ, không chỉ summary; giữ thêm Stress/Spike pre-fix làm evidence.
- [x] Ba HTML report canonical; giữ thêm Stress/Spike pre-fix report.
- [x] CSV input file tồn tại cục bộ; file thật bị Git ignore, có `admin_credentials.example.csv` cho cấu trúc public.
- [x] Có screenshot terminal/JMeter và Task Manager cùng frame cho Load, Stress, Spike và Soak.
- [x] Stress/Spike rerun không có ảnh mới; báo cáo ghi rõ giới hạn, không gán ảnh pre-fix cho rerun.
- [x] dxdiag screenshot + hardware table có hostname phù hợp.
- [x] Soak raw result và một resource snapshot; vẫn thiếu trend đầu/giữa/cuối để công bố threshold.
- [ ] Main report Markdown + PDF (Markdown đã có; PDF cần build/kiểm tra sau lần sửa cuối).
- [ ] AI Critique Markdown + PDF (Markdown đã có; PDF cần build/kiểm tra sau lần sửa cuối).
- [ ] AI Audit Report Markdown + PDF (Markdown đã có; PDF cần build/kiểm tra sau lần sửa cuối).
- [x] Có `report/GIT_COMMIT_LOG.txt` dạng text; phải export lại sau commit cuối.
- [x] README có self-assessment và test summary.
- [x] Public GitHub repository URL.
- [x] GitHub Issue links/screenshots cho lỗi thật, hoặc ghi rõ không quan sát thấy issue.
- [x] Local `report/BUG_REPORT.md` có BUG-SPIKE-001 và BUG-STRESS-001; đã bổ sung link GitHub Issue.
- [x] URL video performance mở được và metadata xác nhận 6:31: <https://youtu.be/6lmRExvkqj4>.
- [x] URL video Agent Skill mở được và metadata xác nhận khoảng 9:09: <https://youtu.be/j8wR1m32oiw>.
- [ ] Human review bằng cửa sổ ẩn danh: cả hai video là Unlisted; video performance có tiếng Việt và tool + resource monitor cùng frame; video skill thể hiện end-to-end trên endpoint group.

## C. Audit chống bịa evidence

- [x] Timestamp metric lấy từ raw JTL; ngày/giờ hardware và scenario evidence hiển thị trong ảnh thật.
- [x] Mọi metric đang công bố truy được về raw JTL + label + window.
- [x] Hardware/hostname đến từ ảnh/report thật.
- [x] Hai video trả metadata YouTube; repository có nhánh `main`; hai GitHub Issue trả HTTP 200 (xác minh 03/09/2026).
- [x] Không còn placeholder `TODO` trong README/main report/AI Critique/bug report; các mục thiếu được ghi rõ trạng thái thay vì điền giả.
- [x] Không dùng số workload gợi ý như measured threshold.
- [x] Lỗi data collision/script được tách khỏi capacity failure.
- [x] A/B rerun xác nhận UUID loại bỏ collision: Stress 1.680→0 failures, Spike 126→0 failures.

## D. Git và đóng gói

- [x] Lịch sử hiện có commit riêng cho Agent Skill, test-plan generation, execution/artifacts, analysis và report review; proposal nằm trong chuỗi cập nhật report.
- [ ] Sau commit cuối, export lại: `git log --date=iso-strict --pretty=format:"%h%x09%ad%x09%s"`.
- [x] Self-AssessedGrade chốt là `100`, thuộc `[000,100]` và khớp bảng README.
- [ ] ZIP tên `23127104_HW05_AI_Performance_NNN.zip`.
- [ ] Mở ZIP kiểm tra lại toàn bộ nội dung trước khi upload Moodle.

## E. Oral defense

- [ ] Có thể giải thích p95 khác max/mean thế nào.
- [ ] Có thể giải thích vì sao error rate không tự động là overload.
- [ ] Có thể chỉ raw JTL row/label hỗ trợ correction.
- [ ] Có thể giải thích threshold được chọn từ stress/soak thế nào.
- [ ] Có thể demo correlation, CSV uniqueness và assertion.
- [ ] Có thể bảo vệ classification của từng optimization.
