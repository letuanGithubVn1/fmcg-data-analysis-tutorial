#  Báo Cáo Phân Tích Tình Trạng Giảm Tỷ Lệ Sử Dụng Kho Q2-2025

**Người thực hiện:** Lê Tuấn  
**Ngày báo cáo:** 2025-06-24  
**Nguồn phát hiện:** Dashboard `Warehouses Monitor`

---

## 🔎 Vấn đề phát hiện

Tỷ lệ sử dụng kho (**warehouse utilization**) trong **quý 2/2025** giảm đột ngột chỉ còn **2.1%**, thấp hơn rất nhiều so với mức trung bình ~30% các quý trước.

---

## 📊 Tóm tắt kết quả phân tích

### ✅ Bước 1: Nhập hàng theo quý
- Lượng shipment trong Q2-2025 chỉ còn **51,602**, thấp hơn ~30–35% so với các quý khác.
- → Đây là một **nguyên nhân chính dẫn đến tồn kho giảm**.

### ✅ Bước 2: Doanh số bán hàng theo quý
- Doanh số bán **tăng mạnh**, Q2-2025 là quý có doanh số cao nhất.
- → Tồn kho giảm là hợp lý theo cung – cầu.

### ✅ Bước 3: Hoạt động khuyến mãi
- Q2-2025 diễn ra hàng loạt khuyến mãi lớn như **mua 1 tặng 1, giảm giá, tặng quà**.
- → Dẫn đến sức mua tăng đột biến → góp phần giảm tồn kho.

### ✅ Bước 4: Kiểm tra lượng hàng chuyển đến store
- Số lượng hàng chuyển từ kho đến cửa hàng trong Q2-2025 **lại giảm mạnh** (~52,000 → thấp hơn mức trung bình 75k–82k).
- → Dấu hiệu bất thường giữa **cầu tăng – cung giảm** → nghi vấn lỗi vận hành hoặc thiếu dự báo.

---

## 🧠 Kết luận cuối cùng

Việc giảm mạnh tồn kho trong Q2-2025 là **kết quả của nhiều yếu tố kết hợp**:

- ✅ Doanh số bán tăng đột biến do khuyến mãi
- ✅ Nhập hàng giảm → dẫn đến thiếu tồn kho
- ⚠️ **Năng lực vận chuyển không đáp ứng đủ** → không kịp bổ sung về cửa hàng
- ⚠️ Có thể có vấn đề **dự báo sai hoặc lỗi cập nhật shipment**

---

## 🚀 Khuyến nghị hành động

- 📦 **Tăng cường năng lực vận chuyển** trong các kỳ có chiến dịch khuyến mãi lớn.
- 🔄 Tối ưu lại **lịch và tuyến vận chuyển** để theo sát nhịp độ tiêu thụ.
- ⚠️ Xây dựng hệ thống **cảnh báo thiếu hàng (stock-out) theo thời gian thực**.
- 📈 Phát triển mô hình **dự báo nhu cầu sát thực tế hơn**, đặc biệt khi có yếu tố marketing tác động.
- 🗓️ Chủ động phân tích dữ liệu **trước mỗi chiến dịch khuyến mãi**, lên kế hoạch cung ứng phù hợp.

---

## 📎 Tài liệu tham chiếu

- Log phân tích chi tiết: `logs/analysis/2025-q2_utilization_drop_analysis_log.md`
- Dashboard: `Warehouses Monitor`
- Biểu đồ: `images/salesbyquater20250625.png`, `promotion_on_Q2.png`, `shipments_by_quarter.png`
