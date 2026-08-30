# Hướng dẫn chi tiết thực hiện HW05 – Performance Testing

Bạn có thể hiểu bài này như sau:

> Dùng JMeter giả lập nhiều admin cùng thực hiện một chuỗi API, chạy chuỗi đó theo ba kiểu tải khác nhau, thu bằng chứng thật, nhờ AI phân tích kết quả, sau đó tự kiểm tra và sửa nhận định của AI.

Hiện repository mới có khung báo cáo và hướng dẫn; các file chạy thật như JMX, JTL, HTML report, ảnh và video vẫn phải được tạo từ quá trình thực hiện thật.

## 1. Cuối bài phải có những gì?

Bạn cần tạo tối thiểu:

| Nội dung | Kết quả phải nộp |
| --- | --- |
| Load test | 1 JMX + CSV + raw JTL + HTML report + ảnh |
| Stress test | 1 JMX + CSV + raw JTL + HTML report + ảnh |
| Spike test | 1 JMX + CSV + raw JTL + HTML report + ảnh |
| Soak test | Kết quả chạy thật 10–15 phút + JTL + ảnh tài nguyên |
| Phần cứng | Ảnh dxdiag có hostname + bảng CPU/RAM/OS |
| AI analysis | Prompt, output và bảng sửa lỗi AI |
| AI Critique | Đoạn 200–300 từ |
| Continuous testing | Flowchart và phần phân tích chi phí/false alarm |
| Agent Skill | Skill trong repo + đoạn demo sử dụng |
| Video | YouTube Unlisted, ít nhất 6 phút, nói tiếng Việt |
| Git | Nhiều commit theo từng bước + file git log |
| Báo cáo | Markdown và PDF |
| Đóng gói | `23127104_HW05_AI_Performance_NNN.zip` |

Checklist hoàn chỉnh nằm ở [SUBMISSION_CHECKLIST.md](../report/SUBMISSION_CHECKLIST.md).

## 2. Workflow đang kiểm thử là gì?

Bạn đang làm Workflow 5 – Admin Catalog & Promo Operations:

```text
Đăng nhập admin
→ Xem danh sách user
→ Xem danh sách coupon
→ Tạo category
→ Tạo product thuộc category vừa tạo
→ Tạo coupon
```

Ánh xạ theo yêu cầu:

| Nhóm | API |
| --- | --- |
| Auth-heavy | `POST /api/login` |
| Read-heavy | `GET /api/admin/users` |
| Read-heavy | `GET /api/coupons` |
| Transactional | `POST /api/categories` |
| Transactional | `POST /api/products` |
| Transactional | `POST /api/admin/coupons` |

Cả Load, Stress và Spike đều phải chạy đúng chuỗi trên, đúng thứ tự. Không được cho Load chạy workflow A còn Stress chạy workflow B.

API chính thức dùng base URL `http://localhost:3000`; tài liệu API cũng mô tả payload cho product, category, import và coupon: [Đặc tả API EShop](https://github.com/ttbhanh/eshop-sut/blob/main/api_specification.md).

## 3. Hiểu nhanh bốn kiểu kiểm thử

### 3.1. Load test

Giả lập mức tải bình thường trong một khoảng thời gian.

Ví dụ ban đầu:

```text
20 người dùng ảo
tăng từ 0 lên 20 trong 120 giây
giữ 20 VU trong 8 phút
```

Mục tiêu: xem hệ thống có ổn định khi hoạt động bình thường không.

### 3.2. Stress test

Tăng tải từng bậc cho đến khi hệ thống bắt đầu không đáp ứng tiêu chí.

Ví dụ:

```text
10 VU → 20 VU → 40 VU → 60 VU
mỗi mức khoảng 2 phút
```

Mục tiêu: tìm mức tải cao nhất vẫn ổn định và mức đầu tiên bắt đầu suy giảm.

### 3.3. Spike test

Tải đang thấp rồi tăng cực nhanh.

Ví dụ:

```text
10 VU bình thường
→ nhảy lên 80 VU trong 10 giây
→ giữ 60 giây
→ trở lại 10 VU
```

Mục tiêu: xem hệ thống có chịu được cú tăng đột ngột và phục hồi được không.

### 3.4. Soak test

Giữ một mức tải ổn định trong 10–15 phút.

Mục tiêu: tìm dấu hiệu tăng bộ nhớ liên tục, latency tăng dần hoặc lỗi xuất hiện sau khi chạy lâu.

Các con số trên chỉ là điểm bắt đầu. Không được viết “hệ thống chịu được 60 VU” nếu bạn chưa thực sự chạy và đo.

## 4. Bước 1 – Cài công cụ

### 4.1. Cài Java và JMeter

JMeter được phát hành dưới dạng ZIP, chỉ cần giải nén rồi chạy. Apache yêu cầu Java 8+, nhưng nên dùng một JDK hiện đại ổn định: [Apache JMeter Download](https://jmeter.apache.org/download_jmeter.cgi).

Sau khi cài Java, mở PowerShell:

```powershell
java -version
```

Tải JMeter ZIP, giải nén vào đường dẫn không có khoảng trắng, ví dụ:

```text
C:\tools\apache-jmeter-5.6.3
```

Mở GUI:

```powershell
C:\tools\apache-jmeter-5.6.3\bin\jmeter.bat
```

Kiểm tra phiên bản:

```powershell
C:\tools\apache-jmeter-5.6.3\bin\jmeter.bat -v
```

JMeter GUI chỉ dùng để xây và debug test plan. Khi đo hiệu năng thật phải chạy CLI/non-GUI vì GUI và listener nặng có thể làm sai kết quả. Đây cũng là khuyến nghị chính thức của JMeter: [JMeter Getting Started](https://jmeter.apache.org/usermanual/get-started.html).

### 4.2. Công cụ khác

Bạn cần thêm:

- Node.js từ 18 trở lên.
- Git.
- Task Manager của Windows.
- `dxdiag`.
- Phần mềm quay màn hình, ví dụ OBS Studio hoặc Xbox Game Bar.
- Một AI tool, ví dụ ChatGPT/Codex.
- Công cụ xuất Markdown sang PDF, ví dụ VS Code Markdown PDF hoặc Pandoc.

Chụp ảnh terminal hiển thị:

```powershell
node --version
npm --version
java -version
C:\tools\apache-jmeter-5.6.3\bin\jmeter.bat -v
git --version
```

Lưu ví dụ:

```text
evidence/hardware/01_tool_versions_YYYYMMDD.png
```

## 5. Bước 2 – Chuẩn bị và chạy SUT

Clone SUT vào một thư mục riêng:

```powershell
git clone https://github.com/ttbhanh/eshop-sut.git
cd eshop-sut
git rev-parse HEAD
cd backend
npm install
node database.js
node server.js
```

Giữ terminal chạy backend trong suốt bài test. Khi thành công sẽ thấy:

```text
Server is running on http://localhost:3000
```

Theo source hiện tại, tài khoản seed thật là:

```text
Email: admin@eshop.com
Password: Admin123!
```

Tài liệu setup cũ ghi `admin123`, nhưng file database hiện tại seed `Admin123!`. Vì vậy phải dùng `Admin123!` và xác nhận bằng request thật: [Database seed hiện tại](https://github.com/ttbhanh/eshop-sut/blob/main/backend/database.js).

Một lưu ý rất quan trọng: `server.js` import `database.js`, còn `database.js` chạy `initDatabase()`. Vì vậy việc khởi động backend hiện tại có thể reset database. Phải ghi lại mỗi lần backend được restart/reset: [Source backend hiện tại](https://github.com/ttbhanh/eshop-sut/blob/main/backend/server.js).

Ghi vào báo cáo:

```text
SUT repository: https://github.com/ttbhanh/eshop-sut
SUT commit SHA: kết quả của git rev-parse HEAD
Backend URL: http://localhost:3000
Load generator: cùng máy với backend
Frontend traffic: không nằm trong workload đo chính
```

## 6. Bước 3 – Chụp bằng chứng phần cứng

### 6.1. Ảnh dxdiag

Nhấn `Win + R`, nhập:

```text
dxdiag
```

Trong tab System, chụp sao cho thấy:

- Computer Name/hostname.
- Operating System.
- Processor.
- Memory.
- DirectX version nếu có.

Lưu:

```text
evidence/hardware/01_dxdiag_system_YYYYMMDD.png
```

Nếu thông tin CPU/RAM không nằm gọn một ảnh, chụp thêm:

```text
evidence/hardware/02_task_manager_cpu_YYYYMMDD.png
evidence/hardware/03_task_manager_memory_YYYYMMDD.png
evidence/hardware/04_task_manager_disk_YYYYMMDD.png
```

Ảnh cấu hình phần cứng có thể được chụp trước ngày chạy nếu vẫn dùng đúng máy và phần cứng không thay đổi. Tuy nhiên, ảnh mức sử dụng CPU/RAM/Disk phải được chụp lại trong từng lần chạy Load, Stress, Spike và Soak.

### 6.2. Bảng phần cứng trong report

Điền vào [MAIN_REPORT.md](../report/MAIN_REPORT.md):

| Thành phần | Giá trị thật |
| --- | --- |
| Hostname | Từ dxdiag |
| OS | Windows… |
| CPU | Tên CPU |
| RAM | Tổng dung lượng |
| Storage | SSD/HDD và dung lượng |
| Java | Kết quả `java -version` |
| JMeter | Kết quả `jmeter -v` |
| Node.js | Kết quả `node -v` |

Hostname phải khớp máy bạn đã dùng ở bài trước theo yêu cầu chống bịa evidence.

## 7. Bước 4 – Kiểm tra API thủ công trước khi dùng JMeter

Trước tiên hãy dùng Postman hoặc một JMeter thread để xác nhận payload thật.

### Request 1: Login

```http
POST http://localhost:3000/api/login
Content-Type: application/json
```

```json
{
  "email": "admin@eshop.com",
  "password": "Admin123!"
}
```

Kết quả mong đợi: HTTP `200`, JSON có `token`.

### Request 2: Users

```http
GET http://localhost:3000/api/admin/users
Authorization: Bearer <token>
```

Mong đợi: HTTP `200`, trả về mảng user.

### Request 3: Coupons

```http
GET http://localhost:3000/api/coupons
Authorization: Bearer <token>
```

Mong đợi: HTTP `200`, trả về mảng coupon.

### Request 4: Create category

```http
POST http://localhost:3000/api/categories
Content-Type: application/json
Authorization: Bearer <token>
```

```json
{
  "name": "HW05_TEST_CATEGORY_001"
}
```

Mong đợi: HTTP `200`, JSON có `id`.

### Request 5: Create product

```http
POST http://localhost:3000/api/products
Content-Type: application/json
Authorization: Bearer <token>
```

```json
{
  "name": "HW05_TEST_PRODUCT_001",
  "price": 100000,
  "description": "San pham performance test",
  "imageUrl": "https://placehold.co/300x300",
  "category_id": 4
}
```

`category_id` phải lấy từ response của request Create category, không được ghi cứng `4`.

### Request 6: Create coupon

```http
POST http://localhost:3000/api/admin/coupons
Content-Type: application/json
Authorization: Bearer <token>
```

```json
{
  "code": "HW05COUPON001",
  "type": "percent",
  "discount_value": 10,
  "min_order_amount": 100000,
  "expired_at": "2099-12-31",
  "max_uses_per_user": 1
}
```

Coupon code phải duy nhất. Code trùng sẽ gây lỗi SQLite `UNIQUE constraint`, nhưng đó là lỗi dữ liệu test, không phải bằng chứng server quá tải.

## 8. Bước 5 – Chuẩn bị CSV

Tạo ba file:

```text
test-data/admin_workflow_load.csv
test-data/admin_workflow_stress.csv
test-data/admin_workflow_spike.csv
```

Ví dụ:

```csv
email,password,run_id,category_prefix,product_prefix,price,description,image_url,coupon_prefix,coupon_type,discount_value,min_order_amount,expired_at,max_uses_per_user
admin@eshop.com,Admin123!,LOAD20260829,LDCAT,LDPROD,100000,Load test product,https://placehold.co/300x300,LDCP,percent,10,100000,2099-12-31,1
```

Đổi `LOAD20260829` thành ngày/run ID thật.

Trong JMeter, tạo một Counter tên `iteration_no`, sau đó tạo giá trị duy nhất:

```text
Category:
${category_prefix}_${run_id}_${__threadNum}_${iteration_no}

Product:
${product_prefix}_${run_id}_${__threadNum}_${iteration_no}

Coupon:
${coupon_prefix}${run_id}${__threadNum}${iteration_no}
```

Coupon nên dùng chữ hoa và số, tránh dấu cách.

Do file CSV chỉ có một credential chung, bạn có thể đặt:

```text
Recycle on EOF: True
Stop thread on EOF: False
Sharing mode: All threads
```

Tính duy nhất không phụ thuộc vào việc CSV có một dòng, vì đã kết hợp thêm `run_id`, thread number và counter.

Nếu chọn `Recycle on EOF = False`, CSV phải đủ dòng cho toàn bộ số iteration, không chỉ đủ số thread.

## 9. Bước 6 – Tạo test plan gốc trong JMeter

Mở:

```text
C:\tools\apache-jmeter-5.6.3\bin\jmeter.bat
```

### 9.1. Tạo Test Plan và biến chung

Chuột phải `Test Plan`:

```text
Add
→ Config Element
→ User Defined Variables
```

Thêm:

| Name | Value |
| --- | --- |
| protocol | http |
| host | localhost |
| port | 3000 |

### 9.2. HTTP Request Defaults

Chuột phải `Test Plan`:

```text
Add
→ Config Element
→ HTTP Request Defaults
```

Điền:

```text
Protocol: ${protocol}
Server Name or IP: ${host}
Port Number: ${port}
Implementation: HttpClient4
```

### 9.3. HTTP Header Manager

```text
Add
→ Config Element
→ HTTP Header Manager
```

Thêm:

| Name | Value |
| --- | --- |
| Content-Type | application/json |
| Accept | application/json |

Authorization nên thêm vào từng request cần token:

| Name | Value |
| --- | --- |
| Authorization | `Bearer ${token}` |

### 9.4. CSV Data Set Config

Chuột phải Thread Group:

```text
Add
→ Config Element
→ CSV Data Set Config
```

Điền:

```text
Filename: đường dẫn tuyệt đối đến CSV
File encoding: UTF-8
Variable Names: để trống nếu file có header
Delimiter: ,
Allow quoted data: True
Recycle on EOF: True
Stop thread on EOF: False
Sharing mode: All threads
```

### 9.5. Counter

```text
Add
→ Config Element
→ Counter
```

Điền:

```text
Starting value: 1
Increment: 1
Reference Name: iteration_no
Track counter independently for each user: chọn
Reset counter on each Thread Group iteration: không chọn
```

### 9.6. Thread Group

```text
Test Plan
→ Add
→ Threads (Users)
→ Thread Group
```

Khi smoke test:

```text
Number of Threads: 1
Ramp-up: 1
Loop Count: 1
```

Bật:

```text
Action to be taken after a Sampler error: Stop Thread
```

## 10. Bước 7 – Thêm sáu HTTP Request

Nên tạo cấu trúc:

```text
Thread Group
└── Transaction Controller: TC_Entire_Admin_Workflow
    ├── Transaction Controller: TC_Auth
    │   └── 01_Login
    ├── Transaction Controller: TC_Reads
    │   ├── 02_Get_Admin_Users
    │   └── 03_Get_Coupons
    └── Transaction Controller: TC_Mutations
        ├── 04_Create_Category
        ├── 05_Create_Product
        └── 06_Create_Coupon
```

Chuột phải Thread Group:

```text
Add
→ Logic Controller
→ Transaction Controller
```

Không chọn `Generate parent sample` nếu bạn muốn giữ rõ từng sampler. Khi phân tích, phải phân biệt các dòng `TC_*` với request thật để tránh đếm trùng.

### 10.1. 01_Login

```text
Add
→ Sampler
→ HTTP Request
```

Điền:

```text
Name: 01_Login
Method: POST
Path: /api/login
Body Data:
```

```json
{
  "email": "${email}",
  "password": "${password}"
}
```

Thêm Response Assertion:

```text
01_Login
→ Add
→ Assertions
→ Response Assertion
```

Chọn:

```text
Field to Test: Response Code
Pattern Matching Rules: Equals
Patterns to Test: 200
```

Thêm assertion thứ hai kiểm tra response chứa `"token"`.

Thêm JSON Extractor:

```text
01_Login
→ Add
→ Post Processors
→ JSON Extractor
```

Điền:

```text
Names of created variables: token
JSON Path Expressions: $.token
Match No.: 1
Default Values: TOKEN_NOT_FOUND
```

### 10.2. 02_Get_Admin_Users

```text
Method: GET
Path: /api/admin/users
```

Thêm Header Manager riêng:

```text
Authorization: Bearer ${token}
```

Assertion:

```text
Response Code Equals 200
```

### 10.3. 03_Get_Coupons

```text
Method: GET
Path: /api/coupons
Authorization: Bearer ${token}
```

Assertion:

```text
Response Code Equals 200
```

### 10.4. 04_Create_Category

```text
Method: POST
Path: /api/categories
Authorization: Bearer ${token}
```

Body:

```json
{
  "name": "${category_prefix}_${run_id}_${__threadNum}_${iteration_no}"
}
```

Assertion response code `200`.

Thêm JSON Extractor:

```text
Variable: category_id
JSONPath: $.id
Default: CATEGORY_ID_NOT_FOUND
```

Đây gọi là correlation: request sau dùng ID sinh ra từ request trước.

### 10.5. 05_Create_Product

```text
Method: POST
Path: /api/products
Authorization: Bearer ${token}
```

Body:

```json
{
  "name": "${product_prefix}_${run_id}_${__threadNum}_${iteration_no}",
  "price": ${price},
  "description": "${description}",
  "imageUrl": "${image_url}",
  "category_id": ${category_id}
}
```

Assertion:

```text
Response Code Equals 200
Response body contains "id"
```

Source hiện tại trả `200`, không phải `201`. Đây là một điểm bạn có thể ghi vào Human Review nếu AI mặc định đề xuất `201`: [Các endpoint trong server hiện tại](https://github.com/ttbhanh/eshop-sut/blob/main/backend/server.js).

### 10.6. 06_Create_Coupon

```text
Method: POST
Path: /api/admin/coupons
Authorization: Bearer ${token}
```

Body:

```json
{
  "code": "${coupon_prefix}${run_id}${__threadNum}${iteration_no}",
  "type": "${coupon_type}",
  "discount_value": ${discount_value},
  "min_order_amount": ${min_order_amount},
  "expired_at": "${expired_at}",
  "max_uses_per_user": ${max_uses_per_user}
}
```

Assertion:

```text
Response Code Equals 200
Response body contains "id"
```

## 11. Bước 8 – Thêm think time

Không nên để các request chạy dồn dập với zero delay trong Load test.

Chuột phải các Transaction Controller:

```text
Add
→ Timer
→ Uniform Random Timer
```

Ví dụ ban đầu:

```text
Random Delay Maximum: 500 ms
Constant Delay Offset: 500 ms
```

Mỗi lần nghỉ khoảng 0.5–1 giây.

Bạn có thể dùng:

- Load: 500–1000 ms.
- Stress: 200–500 ms.
- Spike: 100–300 ms.

Đây là cấu hình thiết kế, không phải kết quả đo. Ghi lý do: admin cần thời gian đọc/chuyển thao tác, nhưng Stress và Spike cố ý giảm think time để tạo tải cao hơn.

## 12. Bước 9 – Chạy smoke test

Thêm:

```text
Thread Group
→ Add
→ Listener
→ View Results Tree
```

Cấu hình:

```text
Threads: 1
Ramp-up: 1
Loop: 1
```

Nhấn nút Start.

Kiểm tra lần lượt:

- `01_Login` xanh và có token.
- `02_Get_Admin_Users` trả 200.
- `03_Get_Coupons` trả 200.
- `04_Create_Category` có ID.
- `05_Create_Product` dùng đúng category ID.
- `06_Create_Coupon` có ID.
- Không request nào dùng `TOKEN_NOT_FOUND`.
- Không request nào dùng `CATEGORY_ID_NOT_FOUND`.
- Database thật có category/product/coupon vừa tạo.

Chụp ảnh:

```text
evidence/smoke/01_all_requests_green.png
evidence/smoke/02_login_token_extracted.png
evidence/smoke/03_category_id_extracted.png
```

Không cần để lộ toàn bộ JWT trong báo cáo; có thể che phần giữa token, nhưng ảnh gốc nên được giữ.

Nếu smoke chưa pass thì tuyệt đối chưa chạy 20–80 VU.

## 13. Bước 10 – Human review kế hoạch do AI đề xuất

Bạn cần chứng minh không chấp nhận kế hoạch AI một cách máy móc.

Có thể ghi bảng:

| AI đề xuất/thiếu sót | Đánh giá của bạn | Cách sửa |
| --- | --- | --- |
| Dùng status `201` cho create | Sai với implementation hiện tại | Đổi assertion thành `200` |
| Ghi cứng category ID | Sai | Extract `$.id` thành `${category_id}` |
| Dùng một coupon code cho mọi thread | Sai | Ghép run ID + thread + counter |
| Dùng password sai để tạo auth load | Nguy hiểm | Chỉ dùng password đúng |
| Bật View Results Tree khi chạy 80 VU | Không phù hợp | Chỉ bật khi debug, disable khi full run |
| Không có think time | Không thực tế cho Load | Thêm Uniform Random Timer |
| Gọi lỗi coupon duplicate là overload | Sai nguyên nhân | Loại run lỗi dữ liệu khỏi capacity result |

Prompt nên dùng:

```text
Bạn là trợ lý review kế hoạch JMeter, không được tự tạo kết quả chạy.

Workflow bắt buộc của tôi là:
POST /api/login
→ GET /api/admin/users
→ GET /api/coupons
→ POST /api/categories
→ POST /api/products
→ POST /api/admin/coupons.

Hãy review kế hoạch theo các tiêu chí:
1. JWT correlation từ $.token.
2. Category ID correlation từ $.id.
3. Dữ liệu category/product/coupon duy nhất theo run, thread và iteration.
4. Assertions cho response code và nội dung.
5. Không dùng password sai trong workload chính.
6. Think time hợp lý.
7. Listener không lặp giữa Load, Stress và Spike.
8. Không được tuyên bố bất kỳ số liệu performance nào khi chưa có JTL thật.

Hãy trả về bảng: vấn đề, mức nghiêm trọng, lý do và cách sửa.
```

Hãy sửa prompt theo cách diễn đạt của bạn và ghi nguyên văn prompt thực vào AI Audit. Đề cấm sao chép prompt giữa sinh viên.

## 14. Bước 11 – Tạo ba test plan

Sau khi smoke pass, dùng `Save As`.

Nếu chạy ngày 29/08/2026:

```text
test-plans/23127104_Load_20260829.jmx
test-plans/23127104_Stress_20260829.jmx
test-plans/23127104_Spike_20260829.jmx
```

Ngày trong tên phải là ngày chạy thật, không phải ngày dự kiến.

### Load

Điểm bắt đầu:

```text
20 VU
Ramp-up: 120 giây
Steady: 8 phút
Ramp-down: 60 giây
Listener: Summary Report
```

### Stress

Điểm bắt đầu:

```text
10 VU: 2 phút
20 VU: 2 phút
40 VU: 2 phút
60 VU: 2 phút
sau đó recovery
Listener: Aggregate Report
```

### Spike

Điểm bắt đầu:

```text
10 VU baseline
nhảy lên 80 VU trong tối đa 10 giây
giữ 80 VU trong 60 giây
trở lại 10 VU trong 2 phút
Listener: View Results Tree chỉ dùng cho debug
```

Để tạo shape chính xác, cách dễ hơn là cài JMeter Plugins Manager rồi dùng Ultimate Thread Group. Nếu chưa cài plugin, bạn có thể dùng nhiều built-in Thread Group cho từng stage, nhưng việc cấu hình và đọc kết quả sẽ khó hơn: [JMeter Plugins Manager](https://jmeter-plugins.org/install/Install/).

Quan trọng: View Results Tree phải disable khi chạy Spike full load. Bạn vẫn giữ nó trong plan và chụp bằng chứng debug, nhưng không bật khi đo 80 VU.

## 15. Bước 12 – Đặt tiêu chí trước khi chạy

Bạn cần tuyên bố trước thế nào là “ổn định”.

Ví dụ tiêu chí ban đầu:

```text
Error rate ≤ 1%
p95 ≤ 1000 ms
Không có 5xx kéo dài
CPU backend không nằm ở mức 90–100% liên tục
RAM không tăng liên tục mà không quay lại
Throughput không bị giảm mạnh khi số VU tăng
```

Đây chỉ là SLO/acceptance criteria do bạn chọn trước khi chạy, không phải kết quả.

Đối với Stress, có thể định nghĩa “first sustained breach” là một stage vi phạm tiêu chí liên tục ít nhất 30–60 giây.

## 16. Bước 13 – Chạy full test đúng cách

Không chạy full load bằng GUI.

Ví dụ PowerShell cho Load:

```powershell
C:\tools\apache-jmeter-5.6.3\bin\jmeter.bat `
  -n `
  -t test-plans\23127104_Load_20260829.jmx `
  -l results\load\23127104_Load_20260829_raw.jtl `
  -e `
  -o results\load\html-report
```

Stress:

```powershell
C:\tools\apache-jmeter-5.6.3\bin\jmeter.bat `
  -n `
  -t test-plans\23127104_Stress_20260829.jmx `
  -l results\stress\23127104_Stress_20260829_raw.jtl `
  -e `
  -o results\stress\html-report
```

Spike:

```powershell
C:\tools\apache-jmeter-5.6.3\bin\jmeter.bat `
  -n `
  -t test-plans\23127104_Spike_20260829.jmx `
  -l results\spike\23127104_Spike_20260829_raw.jtl `
  -e `
  -o results\spike\html-report
```

Mỗi lần chạy:

- JTL chưa được tồn tại.
- HTML output phải là thư mục mới hoặc rỗng.
- Không ghi đè kết quả cũ.
- Nếu chạy lại, dùng thư mục `attempt-02`.
- Giữ raw JTL nguyên vẹn.
- Ghi start time và end time thật.

## 17. Chính xác cần chụp màn hình gì?

### 17.1. Trước mỗi run

Chụp một ảnh có:

- Đồng hồ Windows.
- Tên file JMX.
- Cấu hình VU/ramp-up/duration.
- Run ID.
- Terminal backend đang hoạt động.

Ví dụ:

```text
evidence/load/01_load_configuration.png
```

### 17.2. Trong mỗi run

Sắp xếp màn hình:

```text
Bên trái: PowerShell đang chạy JMeter non-GUI
Bên phải: Task Manager
```

Trong Task Manager:

1. Mở tab `Details`.
2. Tìm `node.exe`.
3. Hiển thị CPU và Memory của process backend.
4. Có thể mở thêm tab `Performance` để chụp CPU/RAM/Disk toàn hệ thống.

Cần ít nhất:

```text
evidence/load/02_load_running_with_task_manager.png
evidence/load/03_load_cpu_memory_peak.png

evidence/stress/02_stress_running_with_task_manager.png
evidence/stress/03_stress_highest_stage.png

evidence/spike/02_pre_spike.png
evidence/spike/03_during_spike.png
evidence/spike/04_recovery.png
```

“Tool + resource monitor trong cùng frame” nghĩa là một ảnh/video frame phải đồng thời nhìn thấy JMeter terminal và Task Manager.

### 17.3. Sau mỗi run

Mở:

```text
results/<scenario>/html-report/index.html
```

Chụp:

- Dashboard overview.
- APDEX nếu sử dụng.
- Statistics.
- Response time percentiles.
- Response time over time.
- Active threads over time.
- Transactions per second.
- Errors hoặc response-code distribution.

Ví dụ:

```text
evidence/load/04_html_dashboard.png
evidence/load/05_statistics.png
evidence/load/06_response_time_percentiles.png
evidence/load/07_throughput.png
```

Không chỉ chụp Summary Report. Raw JTL vẫn bắt buộc phải nộp đầy đủ.

## 18. Xử lý run bị lỗi

### Nếu có 401

Kiểm tra:

- Login có trả token không.
- Header có đúng `Bearer ${token}` không.
- Có dấu cách sau `Bearer` không.
- JSON Extractor có đúng `$.token` không.

### Nếu có 403

Có thể tài khoản bị lock hoặc token sai.

- Dừng run.
- Chụp response và thời điểm.
- Không để hàng nghìn response 403 tiếp tục làm bẩn kết quả.
- Chờ lock hết hoặc reset database.
- Chạy lại smoke 1 VU.
- Sau đó tạo một run mới.

Source hiện tại tăng failed-login attempt sai hai đơn vị và khóa 180 giây, trong khi yêu cầu nói tăng một đơn vị và khóa 30 giây. Đây là lỗi chức năng, không phải kết quả performance: [Login implementation](https://github.com/ttbhanh/eshop-sut/blob/main/backend/server.js).

### Nếu coupon duplicate

Đây là lỗi test data. Sửa code uniqueness và chạy lại.

### Nếu CSV EOF

Đây là lỗi test script/data. Không dùng run đó để kết luận capacity.

### Nếu 500 xuất hiện

Đọc response body và backend log:

- Nếu `UNIQUE constraint`: lỗi dữ liệu.
- Nếu assertion sai: lỗi script.
- Nếu database lock, timeout hoặc resource saturation: có thể là performance issue, nhưng cần resource evidence trước khi kết luận.

## 19. Bước 14 – Tìm stress threshold

Sau khi Stress chạy xong, chia theo stage:

| Stage | VU | Throughput | p95 | Error rate | CPU | RAM | Kết luận |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 1 | 10 | Thật | Thật | Thật | Thật | Thật | Stable/Unstable |
| 2 | 20 | Thật | Thật | Thật | Thật | Thật | Stable/Unstable |
| 3 | 40 | Thật | Thật | Thật | Thật | Thật | Stable/Unstable |
| 4 | 60 | Thật | Thật | Thật | Thật | Thật | Stable/Unstable |

Ví dụ cách kết luận, không được sao chép số:

```text
40 VU là stage cao nhất còn thỏa error rate ≤ 1% và p95 ≤ 1000 ms.
Tại 60 VU, p95 vượt ngưỡng trong 80 giây và throughput không tăng thêm.
Vì vậy 60 VU là first sustained breach.
```

Không lấy stage có RPS cao nhất làm threshold nếu error rate rất cao.

## 20. Bước 15 – Chạy soak 10–15 phút

Chọn mức bằng hoặc thấp hơn stage ổn định cuối của Stress.

Ví dụ nếu 40 VU ổn định nhưng 60 VU không ổn định:

```text
Soak có thể chạy 30–40 VU trong 10–15 phút
```

Nên lưu thêm:

```text
test-plans/23127104_Soak_YYYYMMDD.jmx
results/soak/23127104_Soak_YYYYMMDD_raw.jtl
results/soak/html-report/
```

Chụp ít nhất:

- RAM lúc bắt đầu.
- RAM khoảng giữa run.
- RAM lúc kết thúc.
- CPU/RAM cao nhất.
- Terminal JMeter và Task Manager cùng frame.

Bảng kết quả:

| Thuộc tính | Giá trị thật |
| --- | --- |
| Duration | 10–15 phút |
| VU | Thật |
| Stable RPS | Thật |
| p95 | Thật |
| Error rate | Thật |
| CPU range/peak | Thật |
| Memory start/peak/end | Thật |
| Disk observation | Thật |
| Stable hay không | Kết luận |

Endurance threshold nên viết kiểu:

```text
Trên hardware X, workload cao nhất được xác nhận ổn định trong 15 phút là
Y requests/second với p95 = Z ms, error rate = E%, CPU peak = C%,
RAM tăng từ A MB lên B MB và ổn định ở khoảng D MB.
```

Threshold là RPS đo thật đi kèm điều kiện, không chỉ là số VU.

## 21. Bước 16 – Phân tích JTL bằng AI

Dùng script có sẵn:

```powershell
python agent-skill-kit/hw05-performance-testing/scripts/analyze_jtl.py `
  results/load/23127104_Load_20260829_raw.jtl `
  --output results/load/analysis.json
```

Làm tương tự cho Stress và Spike.

Prompt phân tích:

```text
Hãy phân tích file JTL thật tôi cung cấp.

Yêu cầu:
1. Xác nhận tên các cột và đơn vị thời gian.
2. Báo riêng theo từng sampler label:
   sample count, error count, error rate, throughput,
   mean, p50, p90, p95, p99, max.
3. Báo phân bố response code.
4. Không được tính percentile bằng cách lấy trung bình percentile của các nhóm.
5. Phân biệt elapsed time, latency và connect time.
6. Nếu có Transaction Controller TC_*, phải nêu rõ chúng có làm đếm trùng hay không.
7. Không được kết luận root cause chỉ từ JTL.
8. Mọi kết luận phải ghi label và cửa sổ thời gian hỗ trợ.
9. Những dữ kiện không có phải ghi “không đủ evidence”.

Sau đó đề xuất performance threshold và đánh dấu rõ phần nào là:
- measured fact;
- inference;
- recommendation.
```

Bạn phải giữ output thật của AI để đưa vào audit.

## 22. Bước 17 – Tìm chỗ AI hiểu sai

Bạn phải đối chiếu ít nhất:

- Sample count.
- Error count/error rate.
- p95.
- Response code.
- Stage/window thời gian.

Các lỗi AI thường mắc:

- Gọi p95 là request chậm nhất.
- Lấy mean thay cho p95.
- Lấy trung bình p95 của các endpoint.
- Tính cả dòng Transaction Controller làm request thật.
- Gọi mọi lỗi 500 là overload dù thực tế coupon trùng.
- Thấy RAM tại cuối cao hơn đầu rồi kết luận memory leak.
- Thấy latency cao rồi tự kết luận thiếu database index.
- So sánh Load và Spike dù hai workload khác nhau.

Bảng cần điền:

| AI claim | Raw evidence đúng | Verdict | Correction |
| --- | --- | --- | --- |
| AI nói p95 là X | JTL/file/label/window cho thấy Y | Sai | Giải thích phương pháp |
| AI nói server overload | Các lỗi là coupon duplicate | Unsupported | Lỗi dữ liệu, không phải saturation |
| AI nói memory leak | Chỉ có hai điểm RAM | Không đủ evidence | Cần xu hướng liên tục |

Nếu AI không sai số, bạn vẫn có thể chỉ ra một kết luận thiếu căn cứ, ví dụ AI tuyên bố “SQLite là bottleneck” nhưng JTL không chứng minh root cause.

## 23. Bước 18 – Yêu cầu AI đề xuất tối ưu

Prompt:

```text
Dựa trên JTL, HTML report, CPU/RAM/Disk evidence và source architecture
Node.js + Express + SQLite mà tôi cung cấp, hãy đề xuất các optimization.

Với từng đề xuất, hãy ghi:
1. Dấu hiệu đo được hỗ trợ đề xuất.
2. Source hoặc cấu hình cần kiểm tra.
3. Cách benchmark A/B để xác nhận.
4. Rủi ro hoặc trade-off.
5. Mức confidence.
6. Không được tuyên bố database bottleneck nếu chưa có evidence.
```

Sau đó bạn tự phân loại:

| Đề xuất | Phân loại |
| --- | --- |
| Có evidence và làm được | Feasible |
| Có thể đúng nhưng cần benchmark | Conditional |
| Không đủ bằng chứng | Unsupported |
| Không phù hợp kiến trúc/source | Hallucinated |

Ví dụ, “thêm connection pool” không tự động phù hợp với SQLite. Cần kiểm tra driver và access pattern trước.

## 24. Bước 19 – AI Critique 200–300 từ

Chỉ viết sau khi có AI claim sai thật.

Cấu trúc:

1. AI đã giúp bạn việc gì.
2. AI đã nói sai/thiếu điều gì.
3. Giá trị đúng trong raw JTL là gì.
4. Vì sao AI sai.
5. Bạn sửa như thế nào.
6. Recommendation nào feasible/unsupported.
7. Bài học khi cộng tác với AI.

Điền vào [AI_CRITIQUE.md](../report/AI_CRITIQUE.md).

Đếm 200–300 từ. Không giữ placeholder.

## 25. Bước 20 – AI Audit Report

Với mỗi tương tác quan trọng, ghi:

````markdown
- Name of the AI tool: Codex
- Date/time: 2026-08-29T14:30:00+07:00
- Prompt:
```text
Nguyên văn prompt bạn đã nhập
```
- AI Output:
```text
Tóm tắt hoặc phần output quan trọng
```
````

Timestamp phải lấy từ thời gian thật, ví dụ PowerShell:

```powershell
Get-Date -Format "yyyy-MM-ddTHH:mm:sszzz"
```

Các interaction nên log:

- AI hiểu đề.
- AI thiết kế workflow.
- AI đề xuất Load.
- AI đề xuất Stress.
- AI đề xuất Spike.
- AI review JMX/CSV.
- AI phân tích JTL.
- AI đề xuất optimization.
- AI review báo cáo.
- AI Audit Logger nếu bạn gọi nó.

Không đợi đến cuối mới nhớ lại timestamp.

## 26. Bước 21 – Continuous Performance Testing

Trong report đã có flowchart mẫu. Bạn cần giải thích:

```text
Commit/PR
→ xem file nào thay đổi
→ nếu chỉ docs thì skip và ghi lý do
→ nếu backend/database/config thay đổi thì build
→ seed dữ liệu cố định
→ smoke test
→ chạy performance baseline
→ thu JTL và resource metrics
→ so p95/error rate với baseline
→ nếu regression thì flag
→ chạy lại xác nhận
→ human review
```

Cần bàn luận:

- Chạy performance mỗi commit tốn thời gian và máy.
- Shared CI runner gây nhiễu CPU.
- p95 dao động có thể tạo false alarm.
- Sample nhỏ làm p95/p99 không ổn định.
- Tự động cập nhật baseline có thể hợp thức hóa performance xấu.
- Nên chạy profile ngắn trên PR, test sâu vào nightly/release.
- Pipeline chỉ flag regression, không tự tuyên bố root cause.

Giá trị `X% p95 regression` phải được chọn từ baseline thật của bạn, không để nguyên TODO.

## 27. Bước 22 – Demo Agent Skill

Repo đã có skill ở:

```text
agent-skill-kit/hw05-performance-testing
```

Copy toàn bộ thư mục vào:

```text
.agents/skills/hw05-performance-testing
```

Giữ đầy đủ:

```text
SKILL.md
references/
scripts/
agents/
```

Reload Codex rồi gọi:

```text
$hw05-performance-testing Hãy review JMeter plan Workflow 5 của tôi.
Kiểm tra JWT correlation, category ID correlation, CSV uniqueness,
assertions, workload shape và listener. Không được tạo kết quả chạy giả.
```

Sau khi có JTL thật:

```text
$hw05-performance-testing Phân tích file
results/load/23127104_Load_20260829_raw.jtl theo label.
Báo sample count, error rate, throughput, mean, p50, p90, p95,
p99, max và response codes. Liệt kê các kết luận cần human review.
```

Trong video cần cho thấy:

- Gọi skill.
- Skill phát hiện token/category correlation.
- Skill nhắc coupon phải unique.
- Chạy smoke thật.
- Script đọc JTL thật.
- Bạn đối chiếu một metric.
- Skill không tự điền evidence còn thiếu.

Chi tiết nằm trong [03_HUONG_DAN_AGENT_SKILL_KIT.md](03_HUONG_DAN_AGENT_SKILL_KIT.md).

## 28. Bước 23 – Quay video ít nhất 6 phút

Kịch bản gợi ý:

| Thời gian | Nội dung |
| --- | --- |
| 0:00–0:40 | Giới thiệu MSSV, workflow, SUT commit |
| 0:40–1:30 | CSV, JWT correlation, category ID correlation |
| 1:30–2:20 | Cấu hình Load/Stress/Spike |
| 2:20–3:30 | Chạy JMeter CLI và Task Manager cùng frame |
| 3:30–4:20 | HTML dashboard, p95, throughput, error rate |
| 4:20–5:00 | Stress threshold và soak threshold |
| 5:00–5:40 | AI misinterpretation và phần bạn sửa |
| 5:40–6:40 | Demo Agent Skill |
| 6:40–7:00 | Kết luận và limitations |

Yêu cầu:

- Nói bằng giọng thật của bạn, tiếng Việt.
- Tool và resource monitor phải xuất hiện cùng frame khi chạy.
- Nên dài 7–8 phút để tránh thiếu 6 phút do cắt video.
- Upload YouTube ở chế độ Unlisted, không chọn Private.
- Mở link bằng cửa sổ ẩn danh để kiểm tra.

## 29. Bước 24 – GitHub Issues

Chỉ tạo issue khi có lỗi thật.

Issue cần:

```text
Title
Environment
SUT commit SHA
Workload
Steps to reproduce
Expected result
Actual result
Timestamp/window
Response code
Screenshot/JTL/server log
Impact
```

Không có lỗi thì ghi rõ:

```text
Không ghi nhận bug/performance issue đủ evidence để tạo GitHub Issue.
```

Không tạo issue chỉ để đủ số lượng.

## 30. Bước 25 – Commit theo từng phần

Thứ tự đề xuất:

```text
docs: define workflow 5 scope and environment
test(load): add data-driven admin workflow plan
test(stress): add staged stress plan
test(spike): add spike and recovery plan
results: add raw reports and hardware evidence
analysis: add AI review and JTL corrections
docs: add continuous performance proposal
skill: add reusable HW05 performance skill
docs: finalize report and submission checklist
```

Sau commit cuối:

```powershell
git log --date=iso-strict --pretty=format:"%h`t%ad`t%s"
```

Lưu output thật vào file text bằng cách phù hợp trong terminal hoặc copy thủ công:

```text
report/git-log.txt
```

Không bịa commit hash.

## 31. Bước 26 – Hoàn thiện báo cáo và đóng gói

Điền toàn bộ TODO trong:

- [README.md](../README.md)
- [MAIN_REPORT.md](../report/MAIN_REPORT.md)
- [AI_CRITIQUE.md](../report/AI_CRITIQUE.md)
- [AI_AUDIT_REPORT.md](../report/AI_AUDIT_REPORT.md)

Tìm TODO còn sót:

```powershell
rg -n "TODO|REAL EVIDENCE REQUIRED" README.md report docs
```

Các TODO trong tài liệu hướng dẫn có thể giữ, nhưng bản report/README nộp cuối không được còn placeholder.

Xuất PDF:

```text
report/MAIN_REPORT.pdf
report/AI_CRITIQUE.pdf
report/AI_AUDIT_REPORT.pdf
```

Tự đánh giá, ví dụ 090, rồi đóng gói:

```text
23127104_HW05_AI_Performance_090.zip
```

Mở ZIP và kiểm tra lại:

- Ba JMX.
- Ba raw JTL.
- Ba HTML report folder.
- CSV.
- Soak evidence.
- Ảnh phần cứng/tài nguyên.
- Markdown và PDF.
- Video URL.
- Public repository URL.
- Git log.
- Agent Skill.
- Không có số liệu giả.
- Không có artifact rỗng.

## 32. Thứ tự ngắn gọn nên làm ngay

Đừng cố làm toàn bộ cùng lúc. Hãy đi đúng thứ tự:

1. Cài Java và JMeter.
2. Clone và chạy backend.
3. Ghi SUT commit SHA.
4. Chụp dxdiag và version công cụ.
5. Test thủ công sáu API.
6. Tạo CSV.
7. Tạo một JMeter plan gốc.
8. Chạy smoke 1 VU × 1 iteration.
9. Chỉ khi smoke xanh hoàn toàn mới tạo Load.
10. Chạy Load và thu evidence.
11. Dựa trên Load để chỉnh Stress.
12. Chạy Stress, tìm stable stage.
13. Dựa trên Stress để chỉnh Spike và Soak.
14. Chạy Spike.
15. Chạy Soak 10–15 phút.
16. Phân tích JTL bằng script và AI.
17. Tìm ít nhất một lỗi/thiếu sót thật trong output AI.
18. Hoàn thiện report, critique, continuous proposal.
19. Quay video.
20. Audit checklist, xuất PDF, đóng ZIP.

Runbook ngắn hơn nằm trong [02_WORKFLOW_THUC_HIEN.md](02_WORKFLOW_THUC_HIEN.md).
