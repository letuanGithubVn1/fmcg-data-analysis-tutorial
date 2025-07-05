
# TỐI ƯU CHUỖI CUNG ỨNG FMCG

## Giới thiệu
Hãy tượng tưởng, bạn là 1 data analyst của 1 công ty thuộc lĩnh vực FMCG(Fast Moving Consumer Goods), bạn được nhận nhiệm vụ "tối ưu chuỗi cung ứng" nhằm: giảm chi phí vận hành, đáp ứng nhu cầu thị trường nhanh hơn, tăng mức độ hài lòng của khách hàng... Vì phạm vi phân tích của mục tiêu ban đầu rất lớn nên bạn cần chia ra nhiều mục tiêu nhỏ hơn như: 

### Các mục tiêu chi tiết:
- Tối ưu hóa sản xuất (Factories)
- Tối ưu kho vận (Warehouses)
- Tối ưu vận chuyển (Shipments)
- Tối ưu phân phối đến cửa hàng (Stores)
- Quản lý hàng tồn (Inventory)

---

## Thông Tin Kết Nối Cơ Sở Dữ Liệu
```text
Username: root
Password: AYpcIHEUVAjCFaAWBHxZzYdzcmcHwBiG
Host: nozomi.proxy.rlwy.net
Port: 31562
Database: railway
```

---

## Tổng Quan Về Dữ Liệu
**Dimension Tables:**
- products, customers, stores, warehouses, factories, regions, promotions, competitors, times, customer_segments

**Fact Tables:**
- sales, shipments, inventory, store_inventory_transactions

### Mô tả chi tiết
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


### ERD: (Entity Relationship Diagram)
![Sơ đồ ERD](https://github.com/letuanGithubVn1/fmcg-data-analysis-tutorial/raw/master/Images/ERD.png)


--- 

### Cách bước thực hiện:

1. Xây dựng các Dashboard theo dõi chuyện gì đang xảy ra như sau:
    - Hiệu xuất sản xuất
    - Hiệu suất hoạt động kho
    - Hiệu xuất giao hàng 
    - Hiệu xuất hàng tồn kho
2. Xác định vấn đề dựa trên Dashboard
3. Tìm nguyên nhân của vấn đề
4. Đưa đề xuất hành động

---















## Giới thiệu về các thành phần trong reponsitory

### Supply_Chain_Optimization_Project
```text
Supply_Chain_Optimization_Project/
├── data/                                 
│   └── dataset.md                         # File mô tả bộ dữ liệu
│
├── images/                                # Thư mục lưu hình ảnh sử dụng trong báo cáo
│
├── issues/                                # Các vấn đề cần giải quyết trong dự án
│   └── warehouse_optimization.md
│
├── logs/                                  # Ghi chú quá trình làm sạch và phân tích
│   ├── analysis/                          # Log chi tiết quá trình phân tích
│   │   ├── 2025-q2_utilization_drop_analysis_log.md  # Phân tích giảm tỷ suất sử dụng Q2/2025
│   │   └── overutilized_warehouse.md                # Phân tích các kho bị quá tải
│   │
│   └── cleaning/                          # Log quá trình làm sạch dữ liệu
│       └── cleaning_log_global.md                    # Tổng hợp xử lý dữ liệu toàn bộ
│
├── reports/                               # Các báo cáo chính thức
│   └── warehouse_utilization_q2_2025_report.md
│
├── results/                               # Thư mục xuất file kết quả phân tích
│   └── stock_to_sales_analysis.csv
│
├── scripts/                               # Code Python phục vụ quá trình xử lý dữ liệu
│   ├── __init__.py
│   ├── cleaned_data.py                    # Xử lý dữ liệu đã làm sạch
│   ├── eda.py                             # Thực hiện phân tích khám phá dữ liệu (EDA)
│   ├── raw.py                             # Xử lý dữ liệu thô
│   └── validation.py                      # Kiểm tra tính hợp lệ của dữ liệu
│
├── venv/                                  # Môi trường ảo cho dự án
│
├── .env                                   
├── main.py                                
├── Node.txt                              
├── README.md                              # Tài liệu giới thiệu dự án và mô tả cách phân tích
└── requirements.txt                       # File khai báo thư viện cần thiết
```


### retail_elt_project
```text
retail_etl_project/
├── data/                                   # Thư mục chứa dữ liệu thô
│   └── times.csv                           # File dữ liệu mẫu
│
├── extractors/                             # Module trích xuất dữ liệu (Extract)
│   ├── __init__.py
│   └── extractors.py
│
├── loaders/                                # Module nạp dữ liệu vào đích (Load)
│   ├── __init__.py
│   └── loaders.py
│
├── transformers/                           # Module chuyển đổi dữ liệu (Transform)
│   ├── __init__.py
│   ├── transformers.py
│   └── pipelines.py                        # Xây dựng luồng xử lý ETL hoàn chỉnh
│
├── venv/                                   # Môi trường ảo Python
│
├── .env                                    
├── .env.example                           
├── .gitignore                              
├── main.py                                 

```

### File Dashboard.pbix: sử dụng power bi để mở
Chứa các dashboard:
- Hiệu xuất sản xuất
- Hiệu suất hoạt động kho
- Hiệu xuất giao hàng 
- Hiệu xuất hàng tồn kho

## Hướng Dẫn Sử Dụng

### 1. Cài Đặt Môi Trường
```bash
python -m venv venv
source venv/bin/activate    # Trên Linux/Mac
venv\Scripts\activate     # Trên Windows

```
### 2. Cài đặt thư viện
```bash
pip install -r requirements.txt
```


### 5. Mở Rộng và Tùy Biến
- Có thể bổ sung thêm các phương pháp phân tích khác trong `eda.py`.
- Có thể viết thêm các hàm kiểm tra dữ liệu mới trong `validation.py`.
