# 1. Time – Thời gian
- **date_id**: Ngày cụ thể, được dùng làm khóa chính và liên kết thời gian trong các bảng khác.
- **day**, **month**, **year**: Thành phần ngày để truy vấn phân tích theo thời gian.
- **fiscal_quarter**: Quý tài chính (Q1–Q4).
- **week_number**: Tuần trong năm.
- **holiday_flag**: đánh dấu nếu là ngày lễ.
- **weekend_flag**: đánh dấu nếu là cuối tuần.

# 2. Regions – Khu vực địa lý
- **region_id**: Mã khu vực, dùng để liên kết địa lý.
- **region_name**: Tên khu vực (Miền Bắc, Trung, Nam).

# 3. Factories – Nhà máy sản xuất
- **factory_id**: Mã nhà máy.
- **factory_name**: Tên nhà máy.
- **location**: Địa chỉ hoặc tỉnh/thành của nhà máy.
- **product_type**: Loại sản phẩm chính được sản xuất tại nhà máy (mì, gia vị...).
- **capacity_per_year**: Công suất sản xuất hàng năm.
- **region_id**: Khu vực mà nhà máy thuộc về.

# 4. Products – Sản phẩm
- **product_id**: Mã sản phẩm.
- **product_name**: Tên sản phẩm.
- **brand**: Thương hiệu (Acecook, Masan...).
- **category**: Nhóm sản phẩm chính.
- **sub_category**: Nhóm sản phẩm phụ.
- **source_type**: Nguồn cung ứng (sản xuất nội bộ, phân phối, bên thứ ba).
- **production_site_id**: Nhà máy sản xuất sản phẩm này.
- **shelf_life**: Hạn sử dụng (ngày).
- **packaging_type**: Loại bao bì.
- **unit_size**: Quy cách đóng gói (ví dụ: 500g, chai 1L...).
- **sku**: Mã định danh sản phẩm (Stock Keeping Unit).
- **last_modified**: Ngày cập nhật lần cuối.

# 5. Warehouses – Kho hàng
- **warehouse_id**: Mã kho.
- **warehouse_name**: Tên kho.
- **location**: Địa điểm kho.
- **region_id**: Khu vực kho hoạt động.
- **has_dry**, **has_fresh**, **has_frozen**: Kho có hỗ trợ bảo quản sản phẩm khô, tươi, đông lạnh.
- **capacity**: Sức chứa tối đa.

# 6. Stores – Cửa hàng bán lẻ
- **store_id**: Mã cửa hàng.
- **store_name**: Tên cửa hàng thực tế.
- **store_type**: Loại hình cửa hàng (WinMart, Partner...).
- **channel_type**: Kênh phân phối (GT, MT, Online...).
- **region_id**: Khu vực phục vụ.
- **partner_name**: Tên đối tác nếu là cửa hàng hợp tác.
- **warehouse_id**: Kho mà cửa hàng được phân phối từ đó.
- **opened_date**: Ngày khai trương.

# 7. Customer_Segments – Phân khúc khách hàng
- **customer_segment_id**: Mã phân khúc.
- **segment_name**: Tên nhóm (Khách thường xuyên, cao cấp...).
- **buying_frequency**: Tần suất mua hàng trung bình.
- **average_spending**: Chi tiêu trung bình.

# 8. Customers – Khách hàng
- **customer_id**: Mã khách hàng.
- **customer_name**: Tên khách.
- **birthdate**: Ngày sinh.
- **region_id**: Khu vực sinh sống.
- **customer_segment_id**: Nhóm khách hàng thuộc phân khúc nào.
- **customer_type**: Cá nhân hoặc doanh nghiệp.

# 9. Promotions – Chương trình khuyến mãi
- **promo_id**: Mã khuyến mãi.
- **promo_type**: Hình thức khuyến mãi (giảm giá, quà tặng...).
- **discount_applied**: Mức giảm (số tiền hoặc phần trăm).
- **promo_start**, **promo_end**: Ngày bắt đầu và kết thúc khuyến mãi.
- **apply_scope**: Phạm vi áp dụng (tất cả, riêng kênh...).

# 10. Sales – Giao dịch bán hàng
- **sale_id**: Mã giao dịch.
- **product_id**: Sản phẩm được bán.
- **customer_id**: Người mua.
- **store_id**: Nơi giao dịch diễn ra.
- **date_id**: Ngày bán hàng.
- **quantity**: Số lượng bán.
- **unit_price**: Giá đơn vị.
- **total_amount**: Tổng tiền giao dịch.
- **promo_id**: Khuyến mãi áp dụng nếu có.
- **inventory_id**: Mã tồn kho được trừ ra.
- **shipment_id**: Mã vận đơn giao hàng liên quan.

# 11. Competitors – Đối thủ cạnh tranh
- **competitor_id**: Mã đối thủ.
- **competitor_brand**: Tên thương hiệu cạnh tranh.
- **competitor_channel**: Kênh bán hàng của đối thủ.
- **competitor_location**: Khu vực hoạt động.
- **product_id**: Sản phẩm tương đương đang cạnh tranh.
- **competitor_price**: Giá bán sản phẩm tại đối thủ.
- **competitor_promo_id**: Mã khuyến mãi của đối thủ nếu có.
- **date_id**: Ngày khảo sát.

# 12. Inventory – Tồn kho
- **inventory_id**: Mã tồn kho.
- **product_id**: Mã sản phẩm.
- **store_id**: Cửa hàng chứa tồn kho.
- **warehouse_id**: Kho liên quan nếu có nhập hàng.
- **date_id**: Ngày ghi nhận.
- **stock_on_hand**: Lượng hàng hiện có.
- **stock_in**: Số hàng nhập trong ngày.
- **stock_out**: Số hàng xuất trong ngày.
- **reorder_point**: Ngưỡng cảnh báo cần đặt hàng lại.
- **lead_time_days**: Thời gian đặt hàng đến lúc nhận hàng.
- **expiry_date**: Ngày hết hạn.
- **batch_number**: Số lô.
- **batch_id**: Mã định danh lô.

# 13. Shipments – Vận chuyển
- **shipment_id**: Mã vận đơn.
- **warehouse_id**: Kho xuất hàng.
- **store_id**: Cửa hàng nhận hàng.
- **product_id**: Sản phẩm được vận chuyển.
- **shipment_date**: Ngày giao hàng.
- **shipping_time_days**: Thời gian vận chuyển.
- **transportation_cost**: Chi phí vận chuyển.
- **delivery_status**: Trạng thái giao hàng (đã giao, đang giao...).
- **quantity**: Số lượng được giao.

# 14. Store_Inventory_Transactions – Giao dịch tồn kho tại cửa hàng
- **transaction_id**: Mã giao dịch.
- **store_id**: Cửa hàng liên quan.
- **product_id**: Sản phẩm.
- **date_id**: Ngày diễn ra giao dịch.
- **transaction_type**: Loại giao dịch (bán, nhập, hoàn, điều chỉnh).
- **quantity**: Số lượng thay đổi.
- **reference_sale_id**: Giao dịch bán tương ứng nếu có.
- **reference_shipment_id**: Giao dịch vận chuyển tương ứng nếu có.
