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
| Load | `TODO (REAL EXECUTION DATE)` | `TODO (REAL EVIDENCE REQUIRED)` | Summary Report | TODO | TODO | TODO | Chưa chạy |
| Stress | `TODO (REAL EXECUTION DATE)` | `TODO (REAL EVIDENCE REQUIRED)` | Aggregate Report | TODO | TODO | TODO | Chưa chạy |
| Spike | `TODO (REAL EXECUTION DATE)` | `TODO (REAL EVIDENCE REQUIRED)` | View Results Tree (debug; disabled for full load nếu áp dụng) | TODO | TODO | TODO | Chưa chạy |

**Endpoint groups covered:** auth-heavy, read-heavy, transactional trong cùng workflow.

**Endurance threshold:** `TODO (REAL 10–15 MINUTE SOAK EVIDENCE REQUIRED)`.

**Bugs/performance issues:** `TODO (REAL OBSERVATIONS AND GITHUB ISSUE LINKS REQUIRED)`.

**Demo video:** `TODO (REAL UNLISTED YOUTUBE URL REQUIRED)`.

**Public repository:** `TODO (REAL PUBLIC GITHUB URL REQUIRED)`.

## Self-assessment

| No. | Criteria | Grade | Self-Assessed Grade |
| --- | --- | ---: | ---: |
| 1 | Task 1 – Load testing | 30 | TODO |
| 2 | Task 1 – Stress testing | 20 | TODO |
| 3 | Task 1 – Spike testing | 20 | TODO |
| 4 | Task 2 – AI analysis + misinterpretation hunt | 10 | TODO |
| 5 | Task 3 – Continuous Performance Testing proposal | 10 | TODO |
| 6 | Agent Skills | 10 | TODO |
| **Total** | | **100** | **TODO** |

## Tài liệu

- [Kiến thức performance testing](docs/01_KIEN_THUC_PERFORMANCE_TESTING.md)
- [Workflow thực hiện](docs/02_WORKFLOW_THUC_HIEN.md)
- [Hướng dẫn Agent Skill Kit](docs/03_HUONG_DAN_AGENT_SKILL_KIT.md)
- [Main report](report/MAIN_REPORT.md)
- [AI Critique](report/AI_CRITIQUE.md)
- [AI Audit Report](report/AI_AUDIT_REPORT.md)
- [Submission checklist](report/SUBMISSION_CHECKLIST.md)

## Trạng thái hiện tại

Khung tài liệu và Agent Skill Kit đã được chuẩn bị. Các artifact chống gian lận của đề — JMX có ngày chạy thật, raw JTL, HTML reports, screenshots, hardware report, video, issue links, commit hashes và measured threshold — chưa được tạo hoặc tuyên bố trong repository này.
