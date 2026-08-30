# AI Critique (Mandatory, 200–300 words)

> **Trạng thái:** Đã hoàn thành (Dựa trên lỗi claim C-001 từ phân tích JTL).

AI claim [C-001] rằng "Thời gian phản hồi p95 tổng thể là 25.5ms và nút thắt cổ chai nằm ở API GET coupons với Max là 34ms, chậm nhất hệ thống".
Trong file `results/23127104_Load_20260830.jtl`, label `__overall__` và các label endpoint, parser JSON tại `load_stats.json` cho giá trị đúng của p95 tổng thể là 17.0ms. Chênh lệch là 8.5ms (tương đối 50%). Đồng thời, API có thời gian Max cao nhất thực tế là `Login admin` (102.0ms), và xét theo trung vị/p95 thì `POST create category` (19.0ms) mới là endpoint tốn tải nhất chứ không phải `GET coupons` (p95 chỉ 9.0ms).
Sai lệch này xảy ra vì AI đã có xu hướng "hallucinate" (bịa số) khi không được cung cấp công cụ đọc file CSV thô, dẫn đến việc lấy trung bình cộng sai cách hoặc tự đoán mò số liệu từ tên API. Hơn nữa, AI đã overreach (kết luận vội) nút thắt cổ chai chỉ dựa vào 1 chỉ số Max đơn lẻ mà bỏ qua p95 và phân bố chung.
Correction là: p95 thực tế của hệ thống ở Load Test đạt 17.0ms rất xuất sắc, nút thắt nhẹ nằm ở các tác vụ Write (POST) như tạo Category/Coupon.
Bài học human review rút ra là: Không bao giờ tin tưởng hoàn toàn vào năng lực xử lý toán học hay đọc file log thô của LLM. Mọi phân tích phải được trích xuất từ một parser script trung gian có output JSON rõ ràng, và người kỹ sư phải tự mình đối chiếu chéo các metric quan trọng (như p95, Error rate) trước khi đưa ra kết luận.

Sau khi thay placeholder, kiểm tra độ dài bằng công cụ đếm từ và ghi số từ cuối cùng: `271 words`.
