# HW05 Submission Checklist

## A. Nội dung học thuật

- [x] Cùng một Workflow 5 xuất hiện trong Load, Stress và Spike.
- [x] Auth-heavy, read-heavy và transactional được map rõ.
- [x] Workload, ramp-up, duration, think time và lý do được ghi.
- [ ] CSV data-driven, correlation JWT/category ID và unique mutation data được chứng minh.
- [x] Ba listener/report type khác nhau, không lặp; Spike View Results Tree đã disable trong JMX hiện tại để rerun non-GUI.
- [x] Human review ghi AI sai/thiếu gì, sửa gì và vì sao.
- [ ] Stress threshold và soak 10–15 phút có số liệu thật.
- [x] Task 2 có AI claim, raw JTL value và correction.
- [x] Optimization được phân loại bằng evidence.
- [x] Continuous-testing proposal có flowchart, p95 gate, cost và false alarms.
- [x] AI Critique hoàn chỉnh 200–300 từ.

## B. Artifact bắt buộc

- [x] `23127104_Load_20260830.jmx` với ngày chạy thật.
- [x] `23127104_Stress_20260830.jmx` với ngày chạy thật.
- [x] `23127104_Spike_20260830.jmx` với ngày chạy thật.
- [x] Ba raw JTL đầy đủ, không chỉ summary.
- [x] Ba HTML report folders.
- [x] CSV input file tồn tại cục bộ; file thật bị Git ignore, có `admin_credentials.example.csv` cho cấu trúc public.
- [ ] Screenshot tool và backend resource usage cho từng run.
- [x] dxdiag screenshot + hardware table có hostname phù hợp.
- [x] Soak raw result và một resource snapshot; vẫn thiếu trend đầu/giữa/cuối để công bố threshold.
- [ ] Main report Markdown + PDF.
- [ ] AI Critique Markdown + PDF.
- [ ] AI Audit Report Markdown + PDF.
- [ ] Git commit log dạng text.
- [x] README có self-assessment và test summary.
- [x] Public GitHub repository URL.
- [x] GitHub Issue links/screenshots cho lỗi thật, hoặc ghi rõ không quan sát thấy issue.
- [x] Local `report/BUG_REPORT.md` có BUG-SPIKE-001 và BUG-STRESS-001; đã bổ sung link GitHub Issue.
- [ ] YouTube unlisted >=6 phút, tiếng Việt, tool + resource monitor cùng frame.
- [ ] Video demo Agent Skill end-to-end trên một endpoint group.

## C. Audit chống bịa evidence

- [ ] Mọi timestamp đến từ clock/log thật.
- [x] Mọi metric đang công bố truy được về raw JTL + label + window.
- [x] Hardware/hostname đến từ ảnh/report thật.
- [ ] Video/issue/repository URL mở được.
- [x] Không còn placeholder `TODO` trong README/main report/AI Critique/bug report; các mục thiếu được ghi rõ trạng thái thay vì điền giả.
- [x] Không dùng số workload gợi ý như measured threshold.
- [x] Lỗi data collision/script được tách khỏi capacity failure.

## D. Git và đóng gói

- [ ] Có commit riêng cho từng bước/scenario/analysis/proposal.
- [ ] Export log sau commit cuối: `git log --date=iso-strict --pretty=format:"%h%x09%ad%x09%s"`.
- [ ] Self-AssessedGrade là 3 chữ số trong `[000,100]` và khớp bảng README.
- [ ] ZIP tên `23127104_HW05_AI_Performance_NNN.zip`.
- [ ] Mở ZIP kiểm tra lại toàn bộ nội dung trước khi upload Moodle.

## E. Oral defense

- [ ] Có thể giải thích p95 khác max/mean thế nào.
- [ ] Có thể giải thích vì sao error rate không tự động là overload.
- [ ] Có thể chỉ raw JTL row/label hỗ trợ correction.
- [ ] Có thể giải thích threshold được chọn từ stress/soak thế nào.
- [ ] Có thể demo correlation, CSV uniqueness và assertion.
- [ ] Có thể bảo vệ classification của từng optimization.
