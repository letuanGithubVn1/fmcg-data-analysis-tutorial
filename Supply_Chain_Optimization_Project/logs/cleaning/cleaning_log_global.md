# Data Cleaning Log

**Dự án:** Tối ưu kho vận  
**Người thực hiện:** Lê Tuấn  
**Ngày cập nhật:** [21-06-2025]  
**Dataset gốc:** Cơ sở dữ liệu  


## **Thông tin truy cập cơ sở dữ liệu:**
<!-- mysql://root:AYpcIHEUVAjCFaAWBHxZzYdzcmcHwBiG@nozomi.proxy.rlwy.net:31562/railway -->
username = root  
password = AYpcIHEUVAjCFaAWBHxZzYdzcmcHwBiG  
host = nozomi.proxy.rlwy.net  
port = 31562  
database = railway  

---

## 1. Tổng quan dữ liệu ban đầu
| Tên bảng              | Số dòng | Ghi chú                                   |
|-----------------------|---------|-------------------------------------------|
| competitors           | 90      | Thông tin đối thủ cạnh tranh              |
| customer_segments     | 2       | Phân loại nhóm khách hàng                 |
| customers             | 5,000   | Thông tin khách hàng                      |
| factories             | 7       | Thông tin nhà máy sản xuất                |
| inventory             | 12,000  | Dữ liệu tồn kho hằng ngày                 |
| products              | 2,037   | Thông tin sản phẩm                        |
| promotions            | 105     | Chi tiết các chương trình khuyến mãi      |
| regions               | 8       | Thông tin khu vực và vùng miền            |
| sales                 | 12,972  | Lịch sử bán hàng                          |
| shipments             | 12,000  | Giao hàng từ kho đến cửa hàng             |
| stores                | 800     | Thông tin cửa hàng                        |
| store_inventory_transactions | 24,972 | Giao dịch nhập/xuất tại cửa hàng    |
| times                 | 1,462   | Bảng thời gian chuẩn hóa                  |
| warehouses            | 8       | Danh sách kho và năng lực lưu trữ         |


---

## 2. Log Làm Sạch Dữ Liệu Theo Bảng

### 1. `times.csv`
| Cột | Vấn đề | Cách xử lý |
|------|--------|------------|
| `date_id` | Không chuẩn datetime | Parse datetime |

### 2. `sales.csv`
| Cột | Vấn đề | Cách xử lý | Lý do
|------|--------|------------| ---- |
| `promo_id` | Null một số chỗ | Chấp nhận giữ nguyên | Giao dịch không có khuyến mãi
| `date_id` | Không chuẩn datetime | Parse datetime |

### 3. `shipments.csv`
| Cột | Vấn đề | Cách xử lý |
|------|--------|------------|
| `shipment_date` | Không định dạng datetime | Parse datetime |

### 4. `inventory.csv`
| Cột | Vấn đề | Cách xử lý |
|------|--------|------------|
| `expiry_date` | Không định dạng datetime | Parse datetime |

### 5. `store_inventory_transactions.csv`
| Cột | Vấn đề | Cách xử lý | Lý do
|------|--------|------------| ---------- |  
| `date_id` | Không chuẩn datetime | Parse datetime |
| `reference_sale_id` | bị missing 12000 dòng | Giữ nguyên | Vì transaction_type = 'shipment'

### 6. `products.csv`
| Cột | Vấn đề | Cách xử lý |
|------|--------|------------|
| `production_site_id` | null | giữ nguyên |

### 7. `competitors.csv`
| Cột | Vấn đề | Cách xử lý |
|-----|--------|------------|
| `date_id` | Không chuẩn datetime | Parse datetime |

### 8. `customers.csv`
| Cột | Vấn đề | Cách xử lý |
|------|--------|------------|
| `birthdate` | Không đúng định dạng | Parse datetime |

### 9. `promotions.csv`
| Cột | Vấn đề | Cách xử lý |
|------|--------|------------|
| `promo_start`, `promo_end` | Không phải datetime | Parse datetime |

---

## 3.  Ghi chú thêm

- Các cột có dạng datetime nhưng kiểu Không chuẩn datetime thì Parse
- Các cột Object chuyển sang string
- Đây chỉ là các trường hợp làm sạch tổng thể. Các trường hợp Outlier hoặc missing sẽ được xử lý theo giả định từng trường hợp phân tích

