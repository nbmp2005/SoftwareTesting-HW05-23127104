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
| Stress | `23127104_Stress_20260830.jmx` | 10→20→30→40→50 VU; whole-run 15.445 samples | Aggregate + HTML | 14 ms (whole-run) | 10,8773% | 22,1151 samples/s | Invalid for capacity: 1.680 coupon HTTP 500 do stage data collision |
| Spike | `23127104_Spike_20260830.jmx` | 8 VU pre → 40 VU burst → 8 VU recovery; whole-run 2.332 samples | HTML report | 16 ms (whole-run) | 5,4031% | 12,8737 samples/s | Failed: 126 HTTP 500 ở create coupon; cần stage analysis |
| Soak | `23127104_Soak_20260830.jmx` | 10 VU, khoảng 12 phút; 5.634 samples | HTML report | 17 ms | 0% | 7,8395 samples/s | JTL ổn định; thiếu resource trend để công bố threshold |

**Endpoint groups covered:** auth-heavy, read-heavy, transactional trong cùng workflow.

**Endurance/soak result:** candidate 10 VU có 0% error, p95 17 ms và throughput 7,8395 samples/s trong khoảng 12 phút. Đây là mức ổn định theo HTTP/JTL, chưa phải endurance threshold hoàn chỉnh vì chỉ có một ảnh resource snapshot, không có trend đầu/giữa/cuối.

**Bugs/performance issues:** 2 scenario findings trong [BUG_REPORT.md](report/BUG_REPORT.md): Spike có 126 coupon HTTP 500; Stress có 1.680 coupon HTTP 500 với pattern xác nhận stage data collision. Load và Soak không ghi nhận issue trong raw JTL.

**Demo video:** Chưa quay. Kịch bản quay và checklist hậu kỳ: [docs/05_KICH_BAN_VIDEO_DEMO.md](docs/05_KICH_BAN_VIDEO_DEMO.md). Sau khi upload, thay dòng này bằng URL YouTube unlisted thật.

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
- [Kịch bản hai video demo](docs/05_KICH_BAN_VIDEO_DEMO.md)
- [Main report](report/MAIN_REPORT.md)
- [AI Critique](report/AI_CRITIQUE.md)
- [AI Audit Report](report/AI_AUDIT_REPORT.md)
- [Submission checklist](report/SUBMISSION_CHECKLIST.md)

## Trạng thái hiện tại

Đã có bốn JMX, bốn raw JTL, bốn HTML report, JSON analysis, ảnh hardware/resource snapshot và hai GitHub Issue. Stress/Spike hiện là run chẩn đoán không hợp lệ để suy capacity vì coupon code bị trùng giữa các Thread Group trong phiên bản đã chạy; JMX hiện tại đã đổi sang UUID nhưng chưa rerun. Các blocker còn lại trước khi nộp là: quay/upload hai video, xuất PDF, ghi resource trend đầu/giữa/cuối nếu muốn công bố endurance threshold, rerun Stress/Spike với JMX đã sửa, và cập nhật Git commit log sau commit cuối.
