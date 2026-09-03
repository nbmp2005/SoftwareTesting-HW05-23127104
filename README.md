# 23127104 – HW05 AI Performance Testing

Repository cho HW05 – Performance Testing, Workflow 5: **Admin Catalog & Promo Operations**.

## Workflow được chọn

`POST /api/login` → `GET /api/admin/users` → `GET /api/coupons` → `POST /api/categories` → `POST /api/products` hoặc `POST /api/admin/import-products` → `POST /api/admin/coupons`.

| Nhóm endpoint | Endpoint |
| --- | --- |
| Auth-heavy | `POST /api/login` |
| Read-heavy | `GET /api/admin/users`, `GET /api/coupons` |
| Transactional | Tạo category → product/import → coupon |

## Test summary

> Không thay các ô dưới đây bằng số ước lượng. Chỉ điền từ lần chạy thật và raw JTL.

| Scenario | Plan | Workload thực tế | Report view | p95 | Error rate | Throughput | Trạng thái |
| --- | --- | --- | --- | ---: | ---: | ---: | --- |
| Load | `23127104_Load_20260830.jmx` | 10 VU, ramp 30s, total duration 330s; 2.516 samples | Summary Report + HTML | 17 ms | 0% | 7,6773 samples/s | Ổn định theo HTTP/JTL; chưa phải capacity threshold |
| Stress | `23127104_Stress_20260830.jmx` | UUID rerun 10→20→30→40→50 VU; 15.397 samples | Aggregate + HTML | 24 ms (whole-run) | 0% | 22,0486 samples/s | Không có error breakpoint đến 50 VU; Stage 5 đạt 36,8904 samples/s, p95 31 ms |
| Spike | `23127104_Spike_20260830.jmx` | UUID rerun 8 VU pre → 40 VU burst → 8 VU recovery; 2.330 samples | HTML report | 15 ms (whole-run) | 0% | 12,8438 samples/s | Burst 0 lỗi; recovery 0 lỗi, p95 20 ms và throughput trở về baseline |
| Soak | `23127104_Soak_20260830.jmx` | 10 VU, khoảng 12 phút; 5.634 samples | HTML report | 17 ms | 0% | 7,8395 samples/s | JTL ổn định; thiếu resource trend để công bố threshold |

**Endpoint groups covered:** auth-heavy, read-heavy, transactional trong cùng workflow.

**Endurance/soak result:** candidate 10 VU có 0% error, p95 17 ms và throughput 7,8395 samples/s trong khoảng 12 phút. Đây là mức ổn định theo HTTP/JTL, chưa phải endurance threshold hoàn chỉnh vì chỉ có một ảnh resource snapshot, không có trend đầu/giữa/cuối.

**Bugs/performance issues:** 2 test-data findings trong [BUG_REPORT.md](report/BUG_REPORT.md) được xác minh đã sửa. Pre-fix Spike/Stress có 126/1.680 coupon HTTP 500 do counter collision; UUID rerun tương ứng có 0/2.330 và 0/15.397 failures. Không ghi nhận HTTP error trong bốn kết quả canonical Load, Stress, Spike và Soak.

**Video demo performance testing:** [YouTube – Video demo HW05](https://youtu.be/6lmRExvkqj4) (6 phút 31 giây; metadata YouTube đã xác minh ngày 03/09/2026).

**Video demo Agent Skill:** [YouTube – Video demo Agent Skill HW05](https://youtu.be/j8wR1m32oiw) (9 phút 09 giây; metadata YouTube đã xác minh ngày 03/09/2026).

**Public repository:** `https://github.com/nbmp2005/SoftwareTesting-HW05-23127104`.

**Test data:** JMX dùng `test-data/admin_credentials.csv` ở máy chạy; file này bị ignore để không public password. Cấu trúc không chứa secret được cung cấp tại `test-data/admin_credentials.example.csv`; bản ZIP nộp bài cần chứa CSV chạy thật theo quy định môn học và phải được xử lý theo phạm vi chia sẻ của lớp.

## Self-assessment

| No. | Criteria | Grade | Self-Assessed Grade |
| --- | --- | ---: | ---: |
| 1 | Task 1 – Load testing | 30 | 30 |
| 2 | Task 1 – Stress testing | 20 | 20 |
| 3 | Task 1 – Spike testing | 20 | 20 |
| 4 | Task 2 – AI analysis + misinterpretation hunt | 10 | 10 |
| 5 | Task 3 – Continuous Performance Testing proposal | 10 | 10 |
| 6 | Agent Skills | 10 | 10 |
| **Total** | | **100** | **100** |

## Tài liệu

- [Kiến thức performance testing](docs/01_KIEN_THUC_PERFORMANCE_TESTING.md)
- [Workflow thực hiện](docs/02_WORKFLOW_THUC_HIEN.md)
- [Hướng dẫn Agent Skill Kit](docs/03_HUONG_DAN_AGENT_SKILL_KIT.md)
- [Kịch bản video performance testing](docs/05_KICH_BAN_VIDEO_DEMO.md)
- [Kịch bản video Agent Skill](docs/06_KICH_BAN_VIDEO_AGENT_SKILL.md)
- [Main report](report/MAIN_REPORT.md)
- [AI Critique](report/AI_CRITIQUE.md)
- [AI Audit Report](report/AI_AUDIT_REPORT.md)
- [Submission checklist](report/SUBMISSION_CHECKLIST.md)

## Trạng thái hiện tại

Đã có bốn JMX, raw JTL/HTML/JSON canonical, evidence pre-fix, ảnh hardware/resource snapshot, hai GitHub Issue và hai video demo. Stress/Spike đã rerun thành công bằng UUID: cả hai có 0% lỗi; pre-fix result được giữ riêng để chứng minh human diagnosis và hiệu quả fix. Các việc còn lại trước khi nộp là: xác nhận thủ công video ở chế độ **Unlisted** và nội dung/audio đúng yêu cầu; xuất ba PDF; commit thay đổi cuối và export lại `report/GIT_COMMIT_LOG.txt`; cập nhật trạng thái hai GitHub Issue; tạo ZIP `23127104_HW05_AI_Performance_100.zip` rồi mở kiểm tra trước khi upload Moodle. Resource trend mới không được thu, nên chỉ công bố Stress lower bound 50 VU, không gọi đó là capacity tối đa tuyệt đối.
