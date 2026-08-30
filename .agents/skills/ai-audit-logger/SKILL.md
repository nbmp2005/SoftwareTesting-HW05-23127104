---
name: ai-audit-logger
description: Trích xuất và định dạng lại lịch sử tương tác AI (tool, thời gian, prompt, output) thành các entry cho AI Audit Report theo đúng format đề bài HW04. Dùng cuối mỗi phiên làm việc với AI.
---

# AI Audit Logger

## Format entry bắt buộc (theo đề)
Mỗi entry báo cáo phải tuân thủ chính xác định dạng sau (sử dụng định dạng danh sách của markdown):

- Name of the AI tool: <tên AI, ví dụ: Gemini 3.1 Pro>
- Date/time: <ISO timestamp thật, không bịa, ví dụ: 2026-08-25T20:23:19+07:00>
- Prompt: 
```
<giữ NGUYÊN VĂN 100% prompt người dùng đã gõ, tuyệt đối không tự ý tóm tắt hay thêm bớt chữ>
```
- AI Output: 
```
<tóm tắt hoặc trích xuất ngắn gọn output AI đã sinh ra>
```

## Quy trình
Khi được người dùng gọi, Agent phải thực hiện các bước sau:
1. **Thu thập**: Tổng hợp lại các prompt/output quan trọng trong phiên làm việc hiện tại (từ transcript hoặc context hiện tại).
2. **Ghi log**: Định dạng các mục này theo Format bắt buộc ở trên và **chèn nối tiếp** (append) vào file `report/AI_AUDIT_REPORT.md`.
3. **Cảnh báo**: Sau khi ghi xong, LUÔN nhắc nhở người dùng: "KHÔNG được để AI tự bịa timestamp — phải đảm bảo thời gian ghi nhận là thời gian thật của phiên làm việc."
4. **Lưu ý**: Chỉ dùng skill /ai-audit-logger khi được người dùng gọi trong câu lệnh, không tự ý thêm các câu chat không được gọi skill này vào.
