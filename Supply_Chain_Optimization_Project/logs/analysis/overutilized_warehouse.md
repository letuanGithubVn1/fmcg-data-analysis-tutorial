# Analysis Log – Mất cân bằng kho

**Dự án:** Tối ưu kho vận  
**Người thực hiện:** Lê Tuấn   
**Ngày:** 2025-06-24  
**Dashboard phát hiện vấn đề:** `Warehouses monitor`

---

## 1. Vấn đề phát hiện từ dashboard

- KPI **warehouse utilization** **DC Đà Nẵng vượt 100% công suất** (101.45%), trong khi **các kho khác chỉ sử dụng từ 11% đến 47%** 
- Câu hỏi chính:  
    > **Tại sao DC Đà Nẵng bị quá tải tồn kho, trong khi các kho khác lại hoạt động rất thấp hiệu suất?**  
    > Đây là bất thường hay là kết quả của một chính sách vận hành có chủ đích?

---


## 2. Mục tiêu phân tích

Phân tích nguyên nhân khiến **kho DC Đà Nẵng bị quá tải (utilization > 100%)**, trong khi các kho khác chỉ sử dụng từ 11% đến 47% công suất. Tìm hiểu:
- SKU nào gây quá tải?
- Chính sách vận hành có sai lệch?
- Có dự báo sai, vận chuyển sai tuyến hoặc cố tình dồn hàng về kho này không?

---

##  3. Các bước phân tích & lý do


| Bước | Phân Tích                                              | Mục Tiêu / Nội Dung                                                                                   | Lý Do Cần Phân Tích                                                                                                                      |
|------|---------------------------------------------------------|--------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| 1    | Phân Tích SKU Chiếm Chỗ Lớn Ở DC Đà Nẵng                  | Liệt kê SKU có số lượng tồn kho cao nhất tại kho này.                                                 | Xác định SKU nào đang chiếm diện tích nhiều nhất → Có thể do SKU bán chậm dẫn đến tồn kho vượt ngưỡng.                   |
| 2    | Phân tích lịch sử nhập hàng vào DC Đà Nẵng             | Truy vấn shipments đổ về kho này theo thời gian (ngày/tháng/quý).                                     | Phát hiện xem có phải vận hành đang dồn hàng sai lệch về kho này hay không → Có thể do sai chính sách phân bổ hoặc tuyến vận chuyển. |
| 3    | Kiểm tra tuyến phân phối đến các cửa hàng              | Xác định các store mà DC Đà Nẵng đang phục vụ, đặc biệt kiểm tra vùng miền của store.                 | Phát hiện lỗi vận hành: kho miền Trung cấp hàng cho store miền Nam/Bắc → Sai tuyến phân phối gây dồn hàng không hợp lý.               |
| 4    | So sánh forecast và actual sales khu vực Miền Trung    | Đối chiếu dự báo nhu cầu với thực tế bán hàng theo từng SKU trong khu vực Miền Trung.                 | Nếu forecast sai → Có thể dồn hàng dư vào kho nhưng bán không hết → Gây quá tải tồn kho.                                               |
| 5    | Kiểm tra lý do dồn hàng (ưu tiên chi phí)              | Kiểm tra chi phí lưu kho giữa các DC để xác định có chủ đích dồn về kho chi phí thấp.                | Nếu doanh nghiệp đang ưu tiên giảm chi phí nhưng gây rủi ro vận hành → Cần đánh giá lại bài toán chi phí vs an toàn.                 |


## 4. Kết quả từng bước
### ✅ Bước 1 – Phân Tích SKU Chiếm Chỗ Lớn Ở DC Đà Nẵng
#### 1.1 Lấy các SKU có tỷ lệ đóng góp(contribution_pct) trên 20% ở DC Đà Nẵng
| Ngưỡng Contribution | Diễn Giải       | Tác Động                                      |
|---------------------|------------------|-----------------------------------------------|
| Dưới 10%            | Bình thường      | Phân bổ hợp lý                                |
| 10% - 20%           | Cần theo dõi     | SKU chiếm chỗ lớn, dễ tạo mất cân bằng        |
| Trên 20%            | Nguy cơ cao      | Quá phụ thuộc 1 SKU, dễ gây nghẽn kho          |

```sql
SELECT 
    i.product_id,
    p.product_name,
    SUM(i.stock_on_hand) AS total_stock,
    SUM(i.stock_on_hand) * 100.0 / (
        SELECT SUM(stock_on_hand) 
        FROM inventory i2
        JOIN warehouses w2 ON i2.warehouse_id = w2.warehouse_id
        WHERE w2.warehouse_name = 'DC Da Nang'
    ) AS contribution_pct
FROM inventory i
JOIN warehouses w ON i.warehouse_id = w.warehouse_id
JOIN products p ON i.product_id = p.product_id
WHERE w.warehouse_name = 'DC Da Nang'
GROUP BY i.product_id, p.product_name
HAVING contribution_pct >= '0.20'
ORDER BY contribution_pct DESC;
``` 
#### Kết quả:
| product_id | product_name                          | total_stock | contribution_pct |
|------------|----------------------------------------|-------------|------------------|
| 569        | Suntory Better Premium 700ml           | 834         | 0.25689          |
| 1308       | TH True Milk Service Premium 500ml     | 654         | 0.20145          |

#### 1.2 Lấy Top 10 SKU bán đang chạy tại khu vực Miền Trung (vùng của DC Đà Nẵng)
```sql
SELECT 
    s.product_id,
    p.product_name,
    SUM(s.quantity) AS total_sales
FROM sales s
JOIN products p ON s.product_id = p.product_id
JOIN stores st ON s.store_id = st.store_id
JOIN regions r ON st.region_id = r.region_id
WHERE r.region_name = 'Miền Trung'
GROUP BY s.product_id, p.product_name
ORDER BY total_sales DESC limit 10;
```
#### Kết quả:
| product_id | product_name                              | total_sales |
|------------|--------------------------------------------|-------------|
| 380        | Nestlé Commercial Đặc Biệt 700ml           | 92          |
| 1494       | Unilever Usually Premium 250ml             | 67          |
| 552        | TH True Milk News Dinh Dưỡng 700ml         | 65          |
| 754        | Nestlé Easy Thượng Hạng 250ml              | 65          |
| 1974       | Vinamilk Despite Dinh Dưỡng 330ml          | 62          |
| 269        | Vinamilk Hear Thượng Hạng 250ml            | 62          |
| 114        | TH True Milk Send Thượng Hạng 1kg          | 60          |
| 290        | Vinamilk Cell Đặc Biệt 500ml               | 56          |
| 1630       | PepsiCo Ask Đặc Biệt 100g                  | 55          |
| 1241       | P&G Second Premium 250ml                   | 55          |

#### 1.3 Tính  Stock-to-Sales Ratio (Hàng Tồn So Với Doanh Số)

Theo các nguyên tắc quản lý tồn kho chuẩn ngành, **chỉ số SSR (Stock to Sales Ratio)** được dùng để đánh giá mức độ hợp lý của hàng tồn kho so với doanh số.

| Chỉ Số SSR   | Ý Nghĩa                   | Hành Động Khuyến Nghị                                         |
|--------------|----------------------------|----------------------------------------------------------------|
| SSR ~ 1 – 1.5 | Hợp lý                    | Tồn kho đủ để đáp ứng nhu cầu bán hàng ngắn hạn               |
| SSR ~ 2 – 3   | Có thể dư hàng             | Cần theo dõi thêm → chưa đến mức cảnh báo nhưng có dấu hiệu   |
| SSR > 3       | Tồn kho cao bất thường     | Nguy cơ giam vốn, hàng tồn đọng, có thể dẫn đến hết hạn, giảm giá |


#### Nhận định:
Kết quả dữ liệu đầy đủ tại:  
`results/sku_inventory_danang_q2_2025.csv`
- Tổng số dòng: **1,981 SKU**
- danh sách sau là các sản phẩm tại kho không bán được(trích 1 phần trong file trên)

| Product ID | Product Name                                         | Total Stock | Total Sales | Stock to Sales Ratio |
|------------|------------------------------------------------------|-------------|-------------|----------------------|
| 26 | Wake-Up 247 Nước tăng lực 500ml | 214 | 0 | inf |
| 2003 | Nestlé Election Vị Mới 100g | 162 | 0 | inf |
| 51 | Vinamilk Which Đặc Biệt 250ml | 243 | 0 | inf |
| 1629 | Acecook Her Đặc Biệt 250ml | 115 | 0 | inf |
| 655 | Acecook Particularly Dinh Dưỡng 500ml | 129 | 0 | inf |
| 294 | Suntory Son Dinh Dưỡng 1kg | 138 | 0 | inf |
| 244 | PepsiCo Adult Thượng Hạng 250ml | 112 | 0 | inf |
| 790 | Nestlé Two Dinh Dưỡng 330ml | 144 | 0 | inf |
| 170 | PepsiCo No Premium 1L | 144 | 0 | inf |
| 1107 | Acecook Pattern Premium 500g | 143 | 0 | inf |
| 1024 | Suntory Dog Thượng Hạng 700ml | 97 | 0 | inf |
| 409 | Ajinomoto Letter Premium 100g | 115 | 0 | inf |
| 335 | PepsiCo Each Vị Mới 250ml | 222 | 0 | inf |
| 502 | TH True Milk Investment Vị Mới 500g | 137 | 0 | inf |
| 448 | Ajinomoto Onto Thượng Hạng 100g | 47 | 0 | inf |
| 1883 | TH True Milk Teach Vị Mới 500g | 70 | 0 | inf |
| 1085 | Suntory Lawyer Premium 700ml | 211 | 0 | inf |
| 1771 | Nestlé Program Dinh Dưỡng 500ml | 61 | 0 | inf |


#### Nhận định:
Đây là nhóm SKU đang chiếm diện tích trong kho nhưng không có doanh số.




