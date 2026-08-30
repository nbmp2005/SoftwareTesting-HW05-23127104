# HW05 Submission Checklist

## A. Nội dung học thuật

- [ ] Cùng một Workflow 5 xuất hiện trong Load, Stress và Spike.
- [ ] Auth-heavy, read-heavy và transactional được map rõ.
- [ ] Workload, ramp-up, duration, think time và lý do được ghi.
- [ ] CSV data-driven, correlation JWT/category ID và unique mutation data được chứng minh.
- [ ] Ba listener/report type khác nhau, không lặp.
- [ ] Human review ghi AI sai/thiếu gì, sửa gì và vì sao.
- [ ] Stress threshold và soak 10–15 phút có số liệu thật.
- [ ] Task 2 có AI claim, raw JTL value và correction.
- [ ] Optimization được phân loại bằng evidence.
- [ ] Continuous-testing proposal có flowchart, p95 gate, cost và false alarms.
- [ ] AI Critique hoàn chỉnh 200–300 words.

## B. Artifact bắt buộc

- [ ] `23127104_Load_YYYYMMDD.jmx` với ngày chạy thật.
- [ ] `23127104_Stress_YYYYMMDD.jmx` với ngày chạy thật.
- [ ] `23127104_Spike_YYYYMMDD.jmx` với ngày chạy thật.
- [ ] Ba raw JTL đầy đủ, không chỉ summary.
- [ ] Ba HTML report folders.
- [ ] CSV input files.
- [ ] Screenshot tool và backend resource usage cho từng run.
- [ ] dxdiag/screenfetch screenshot + hardware table có hostname phù hợp.
- [ ] Soak raw result/resource evidence.
- [ ] Main report Markdown + PDF.
- [ ] AI Critique Markdown + PDF.
- [ ] AI Audit Report Markdown + PDF.
- [ ] Git commit log dạng text.
- [ ] README có self-assessment và test summary.
- [ ] Public GitHub repository URL.
- [ ] GitHub Issue links/screenshots cho lỗi thật, hoặc ghi rõ không quan sát thấy issue.
- [ ] YouTube unlisted >=6 phút, tiếng Việt, tool + resource monitor cùng frame.
- [ ] Video demo Agent Skill end-to-end trên một endpoint group.

## C. Audit chống bịa evidence

- [ ] Mọi timestamp đến từ clock/log thật.
- [ ] Mọi metric truy được về raw JTL + label + window.
- [ ] Hardware/hostname đến từ ảnh/report thật.
- [ ] Video/issue/repository URL mở được.
- [ ] Không có placeholder `TODO` trong bản nộp cuối.
- [ ] Không dùng số workload gợi ý như measured threshold.
- [ ] Lỗi data collision/script được tách khỏi capacity failure.

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
