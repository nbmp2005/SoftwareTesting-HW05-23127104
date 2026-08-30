# Hướng dẫn sử dụng Agent Skill Kit HW05

## 1. Skill kit giải quyết việc gì?

Gói [hw05-performance-testing](../agent-skill-kit/hw05-performance-testing/SKILL.md) đóng vai trò điều phối bốn công việc tái sử dụng:

1. thiết kế/review JMeter plan;
2. chạy test và thu thập evidence;
3. phân tích JTL, tìm AI misinterpretation và đánh giá optimization;
4. viết/audit report và submission.

Skill không tự tạo bằng chứng. Đây là ranh giới quan trọng nhất vì đề cấm bịa JTL, screenshot, video, hardware, timestamp và kết quả.

## 2. Cấu trúc

```text
hw05-performance-testing/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── test-design.md
│   ├── execution-evidence.md
│   ├── result-analysis.md
│   └── report-submission.md
└── scripts/
    └── analyze_jtl.py
```

`SKILL.md` chứa quy tắc cốt lõi và router. Agent chỉ đọc reference phù hợp với mode, giúp giảm context nhưng vẫn giữ các invariant. Script phân tích JTL dùng standard library, không sửa raw input.

## 3. Cài đặt

Trong repository này, `.agents/skills` đang bị môi trường hiện tại đặt read-only, nên kit được tạo trong `agent-skill-kit/` để có thể nộp và review. Khi chạy trên máy của bạn, copy nguyên thư mục:

```text
agent-skill-kit/hw05-performance-testing
```

vào một trong các vị trí skill mà Codex của bạn quét, ưu tiên:

```text
.agents/skills/hw05-performance-testing
```

hoặc thư mục skills cá nhân của Codex. Không chỉ copy `SKILL.md`; giữ cả `references`, `scripts` và `agents/openai.yaml`.

Sau khi cài, khởi động lại/reload phiên nếu UI chưa nhận skill. Kiểm tra tên `$hw05-performance-testing` xuất hiện trong danh sách skill.

## 4. Cách gọi theo từng giai đoạn

### Thiết kế

```text
$hw05-performance-testing Hãy review kế hoạch JMeter Workflow 5 của tôi. Kiểm tra correlation token/category ID, CSV uniqueness, assertions, workload shape và listener không trùng. Chưa được tạo hoặc tuyên bố bất kỳ kết quả chạy nào.
```

Đầu vào nên kèm JMX/CSV hiện có, hardware dự kiến và workload mục tiêu. Output mong đợi là review có lỗi, lý do, thay đổi đề xuất và danh sách điểm cần smoke test.

### Execution/evidence

```text
$hw05-performance-testing Hãy lập runbook cho plan Load này và audit evidence sau khi tôi chạy. Mọi số liệu thiếu phải ghi TODO (REAL EVIDENCE REQUIRED).
```

Agent phải đọc `execution-evidence.md`, không được chạy/ghi đè artifact ngoài phạm vi được phép và không được đánh dấu pass nếu chưa có JTL thật.

### JTL analysis

```text
$hw05-performance-testing Phân tích file results/load/<real-file>.jtl theo label; báo sample count, error rate, throughput, mean, p50, p90, p95, p99, max và response codes. Sau đó liệt kê các kết luận cần human review.
```

Chạy script:

```powershell
python agent-skill-kit/hw05-performance-testing/scripts/analyze_jtl.py results/load/<real-file>.jtl --output results/load/analysis.json
```

Đối chiếu ít nhất sample count, error count và p95 bằng JMeter report hoặc cách tính thứ hai. Script dùng linear interpolation; JMeter có thể làm tròn hoặc dùng phương pháp rank khác nên cần ghi phương pháp khi số lẻ khác nhau.

### Submission audit

```text
$hw05-performance-testing Hãy audit repository theo checklist HW05. Phân loại Ready, Missing real evidence, Invalid naming và Needs human review. Không tự tạo placeholder artifact.
```

## 5. Prompt chain AI-first đề xuất

Không gửi một prompt kiểu “hãy làm toàn bộ bài”. Dùng chuỗi có checkpoint:

1. **Understand**: AI map đề bài → deliverable và nêu chỗ chưa biết.
2. **Design workflow**: AI map endpoint, payload, dependency và data uniqueness.
3. **Design Load**: đề xuất parameter + lý do → sinh viên chỉnh.
4. **Design Stress**: stage + stop criteria → sinh viên chỉnh.
5. **Design Spike**: baseline/spike/recovery → sinh viên chỉnh.
6. **Review JMX/CSV**: AI kiểm correlation/assertion/listener → chạy smoke thật.
7. **Analyze JTL**: AI tính metric → sinh viên đối chiếu raw/JMeter.
8. **Optimization**: AI đề xuất → sinh viên kiểm source/resource evidence.
9. **Report audit**: AI chỉ ra thiếu sót → sinh viên bổ sung evidence.
10. **AI audit logger**: ghi prompt/output/timestamp thật của các phiên được yêu cầu log.

Mỗi bước nên lưu prompt và output ngay, không đợi cuối bài mới nhớ lại.

## 6. Cách mở rộng skill

Khi đổi endpoint group, chỉ cập nhật facts/reference riêng cho workflow; không biến một lỗi quan sát được thành quy luật chung. Khi script có bug, thêm fixture JTL tối thiểu và test bất biến (count, errors, percentile), không test chuỗi output trang trí.

Có thể bổ sung sau khi đã có artifact thật:

- parser chia stage theo timestamp cho Stress/Spike;
- detector regression so baseline/candidate với cùng workload;
- validator cây submission và filename/date;
- report table generator từ JSON analysis.

Mỗi tự động hóa phải giữ raw JTL bất biến và in rõ input, phương pháp, timezone, window.

## 7. Demo skill trong video

Để đáp ứng phần Agent Skill, demo end-to-end một endpoint group, ví dụ transactional:

1. gọi skill review category → product → coupon;
2. cho thấy skill phát hiện cần token/category correlation và coupon unique;
3. chạy smoke/thử nghiệm thật;
4. dùng script đọc JTL thật;
5. đối chiếu một metric thủ công;
6. cho thấy skill không điền evidence khi chưa có.

Video vẫn phải có giọng thuyết minh tiếng Việt của bạn và, khi trình bày scenario, tool cùng resource monitor trong cùng frame.
