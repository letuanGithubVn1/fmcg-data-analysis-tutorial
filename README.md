
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
## Ví Dụ Phân Tích Thực Tế

**Phần 1: Xây dựng Dashboard**  
Xây dựng dashboard Giám sát Hiệu suất Kho hàng.  
Chức năng của dashboard:
- Theo dõi tỷ lệ sử dụng kho.
- Kiểm soát tổng tồn kho toàn hệ thống.
- Cảnh báo tỷ lệ hàng sắp hết hạn sử dụng.
- So sánh tồn kho theo vùng địa lý.
- Phân tích xu hướng sử dụng kho theo thời gian.


![Dashboard 1](https://github.com/letuanGithubVn1/fmcg-data-analysis-tutorial/raw/master/Images/Dashboard_1.png)
---

**Phần 2: Xác định vấn đề**

1. Mức sử dụng kho(Warehouse Utilization) chỉ 31.15%  
    - Tổng mức sử dụng kho của toàn hệ thống chỉ đạt ~31% → Phần lớn sức chứa đang bị bỏ trống.
    -   Khoảng 69% công suất chưa được khai thác hiệu quả → Chi phí kho bãi bị lãng phí.  
    🚨 Hệ quả kinh doanh :
        - Lãng phí chi phí thuê kho, bảo trì, vận hành.
        - Chưa tối ưu hóa phân bổ hàng hóa giữa các kho.

2. Nguy Cơ Hàng Cận Date Tồn Kho  
    - Các SKU cận date có thể đang nằm ở kho quá tải.      
    🚨 Hệ quả kinh doanh:  
        - Tổn thất tài chính → do phải bán giảm giá hoặc hủy hàng  
        - Ảnh hưởng uy tín nếu bán ra hàng cận date

3. Mất Cân Bằng Kho Hàng   
    - DC Đà Nẵng: vượt 101.45% công suất → Nguy cơ quá tải
    - Các kho khác: chỉ sử dụng 11% – 47% → Lãng phí nghiêm trọng  
    🚨 Hệ quả kinh doanh:
        - Các hàng tồn kho lâu không bán được → Dễ hư hỏng
        - Chậm xuất hàng → mất doanh số
        - Lãng phí chi phí kho bãi

4. Tỷ Suất Sử Dụng Kho Q2/2025 Giảm Mạnh  
    - Warehouse utilization giảm từ 2.29% xuống 1.59% trong Q1 2025 → Có dấu hiệu bất thường.  
    🚨Hệ quả kinh doanh:
        - Nguy cơ đứt hàng, không đáp ứng kịp nhu cầu thị trường.
        - Rủi ro ảnh hưởng đến doanh thu toàn hệ thống.  

---

**Phần 3: Tìm nguyên nhân của vấn đề**  

### **3.1: Vấn đề Tỷ Suất Sử Dụng Kho Q2/2025 Giảm Mạnh**  
> "Tại sao tại Q2-2025 giảm xuống chỉ còn 2.1%

> Sự sụt giảm này là do yếu tố tạm thời hay có vấn đề vận hành nghiêm trọng?"

---

### **3.2 Phân tích chi tiết**  
#### 3.2.1 giả thuyết - Việc nhập hàng ít tại Quý 2–2025

**Cách phân tích:** sử dụng câu lệnh trong Mysql
```sql
SELECT 
    YEAR(shipment_date) AS year,
    QUARTER(shipment_date) AS quarter,
    SUM(quantity) AS total_shipment
FROM shipments
GROUP BY YEAR(shipment_date), QUARTER(shipment_date)
ORDER BY year, quarter;
```

**Kết quả tổng hợp:**

| Năm  | Q1     | Q2     | Q3     | Q4     |
|------|--------|--------|--------|--------|
| 2022 | 77,665 | 75,964 | 81,956 | 78,446 |
| 2023 | 77,056 | 77,263 | 81,999 | 80,750 |
| 2024 | 79,651 | 74,962 | 78,047 | 79,238 |
| 2025 | 79,673 | **51,602** |        |        |

**Nhận xét:**

- **Quý 2/2025 chỉ nhập 51,602 đơn vị hàng**, thấp hơn rõ rệt so với các quý trước:
  - Q2/2024: 74,962 → giảm ~31%
  - Q1/2025: 79,673 → giảm ~35%

- **Sự sụt giảm nhập hàng là bất thường** có khả năng là nguyên nhân chính gây nên:
  - Mức sử dụng kho (utilization rate) trong Q2-2025 giảm mạnh chỉ còn ~2.1%
  - Gây lãng phí tài nguyên kho, thiếu hàng cục bộ


#### 3.2.2 giả thuyết - tỷ lệ bán hàng ở Quý 2–2025 tăng đột biến

**Cách phân tích:** Vẽ biểu đồ doanh thu theo thời gian bằng python. 
Code chi tiết tại: file eda.py(Supply_Chain_Optimization_Project)

![Sales by Quarter](http://github.com/letuanGithubVn1/fmcg-data-analysis-tutorial/raw/master/Images/sales_by_quarter.png)

**Nhận xét:**
- Doanh số bán hàng **tăng liên tục qua các quý**.
- **Q2-2025** tiếp tục là quý có **doanh số cao nhất**.
- **Không có dấu hiệu doanh số sụt giảm** → Nhu cầu thị trường đang **tăng mạnh**.



#### 3.2.3 Câu hỏi - Có chiến dịch khuyến mãi đẩy hàng mạnh gây giảm tồn kho tại Q2- không?

**Cách phân tích:** sử dụng thư viện Matplotlib vẽ biểu đồ khuyến mãi tại quý 2-2025.  
Code chi tiết tại: file eda.py(Supply_Chain_Optimization_Project)  

![Promotion Result](https://github.com/letuanGithubVn1/fmcg-data-analysis-tutorial/raw/master/Images/promotion_result.png)

**Nhận xét:** Q2-2025 có rất nhiều khuyến mãi
- **Mua 1 tặng 1:** hơn 500 chương trình → Loại khuyến mãi tác động rất mạnh đến hành vi mua hàng.
- **Giảm %:** hơn 300 chương trình → Khuyến khích mua sắm số lượng lớn.
- **Tặng quà kèm:** khoảng 150 chương trình → Tăng giá trị cảm nhận của khách hàng.

--> **Khối lượng khuyến mãi đặc biệt lớn trong Q2-2025 tạo ra sức mua đột biến.**

#### 3.2.4 giả thuyết - lượng hàng xuất kho để chuyển đến cửa hàng(store) trong Q2-2025 có tăng

**Cách phân tích:** Vẽ biểu đồ tổng lượng vận chuyển đến cửa hàng theo thời gian. 
Code chi tiết tại: file eda.py(Supply_Chain_Optimization_Project)

![Goods to Stores](https://github.com/letuanGithubVn1/fmcg-data-analysis-tutorial/raw/master/Images/Goods_to_stores.png)

**Nhận xét:**
- **Q2-2025 có lượng vận chuyển đến cửa hàng giảm đột ngột.**
- Các quý trước dao động quanh **75,000 – 82,000 đơn vị.**
- **Q2-2025 chỉ còn khoảng 52,000 đơn vị** → Giảm rất mạnh so với các kỳ trước.
- Trong khi đó, **doanh số Q2-2025 lại cao nhất.**
- **Doanh số tăng mạnh nhưng lượng vận chuyển lại giảm** → Đây là dấu hiệu **bất thường.**


**Tóm tắt phát hiện chính:**  
- Tỷ suất sử dụng kho Q2/2025 giảm mạnh từ 2.29% xuống còn 1.59% so với Q1/2025, mặc dù doanh số bán hàng vẫn tăng cao.
- Nguyên nhân chính: Số lượng hàng nhập kho trong Q2/2025 giảm đột biến (~35% so với quý trước).
- Khuyến mãi trong Q2/2025 rất nhiều, bao gồm các chương trình mua 1 tặng 1, giảm giá %, tặng quà → Dẫn đến sức mua tăng mạnh.
- Lượng vận chuyển từ kho đến cửa hàng lại giảm mạnh (~30% so với quý trước) trong khi nhu cầu thị trường đang tăng → Dấu hiệu cho thấy có thể đang gặp vấn đề trong vận hành logistics hoặc thiếu hàng để giao

**Kết luận tổng thể:**  
- Tỷ suất sử dụng kho giảm là do Việc nhập hàng giảm bất thường.
- Sức mua của khách hàng và doanh số bán hàng vẫn tăng, nhưng kho không được bổ sung hàng hóa kịp thời dẫn đến nguy cơ đứt hàng, bỏ lỡ doanh số tiềm năng và giảm khả năng đáp ứng thị trường.

---
**Phần 4: Đề xuất hành động**  

### Đề Xuất Hành Động Tối Kho hàng

| Đề xuất hành động | Lý do đề xuất |
|-------------------|---------------|
| Xem xét nâng công suất vận chuyển trong các kỳ khuyến mãi lớn | Để đáp ứng kịp nhu cầu tăng đột biến trong các kỳ khuyến mãi, tránh tình trạng đứt hàng cục bộ |
| Tối ưu tuyến vận chuyển để đảm bảo tốc độ bổ sung hàng về cửa hàng theo nhịp bán | Đảm bảo hàng hóa được bổ sung kịp thời tại cửa hàng, đồng bộ với tốc độ tiêu thụ thực tế |
| Xây dựng hệ thống cảnh báo stock-out sớm | Giúp doanh nghiệp phát hiện sớm nguy cơ thiếu hàng và có biện pháp xử lý kịp thời |
| Xây dựng mô hình dự báo nhu cầu chính xác hơn, đặc biệt trong các kỳ khuyến mãi | Đảm bảo dự báo sát với nhu cầu thực tế, hạn chế sai lệch dẫn đến thiếu hàng hoặc tồn kho quá mức |
| Phân tích trước các chương trình marketing lớn để chuẩn bị đủ hàng và năng lực vận chuyển tương ứng | Chủ động trong việc chuẩn bị hàng hóa và năng lực logistics, tránh tình trạng bị động khi khuyến mãi diễn ra |
---


> #### Tương tự với các vấn đề khác, áp dụng quy trình phân tích như sau: 
> - Trước tiên, chúng ta đặt ra các câu hỏi kinh doanh hoặc giả thuyết cụ thể để định hướng phân tích.  
> - Tiếp theo, sử dụng các công cụ phù hợp như SQL, Python, Power BI hoặc các phần mềm phân tích khác để khai thác dữ liệu, trực quan hóa và kiểm tra giả thuyết....   
> - Từ đó, chúng ta rút ra insight có giá trị thực tiễn, đưa ra nhận định khách quan và đề xuất các hành động cụ thể.

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
