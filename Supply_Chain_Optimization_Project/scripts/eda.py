# eda.py
import matplotlib.pyplot as plt
import pandas as pd
import os


def plot_sales_by_quarter(sales_df, times_df):
    """
    Hàm này sẽ gộp dữ liệu sales với time để tính tổng số lượng theo quý, sau đó vẽ biểu đồ.

    Args:
        sales_df (DataFrame): Dữ liệu sales đã làm sạch.
        times_df (DataFrame): Dữ liệu thời gian đã làm sạch.
    """
    # Merge dữ liệu sales với time để có thông tin năm, quý
    sales_with_time = sales_df.merge(times_df, on='date_id')

    # Tính tổng sales theo năm và quý
    sales_by_quarter = sales_with_time.groupby(['year', 'fiscal_quarter'])['quantity'].sum().reset_index()

    # Sắp xếp theo năm và quý để vẽ biểu đồ đúng thứ tự thời gian
    sales_by_quarter = sales_by_quarter.sort_values(by=['year', 'fiscal_quarter'])

    # Vẽ biểu đồ
    plt.figure(figsize=(12, 6))
    plt.plot(sales_by_quarter['year'].astype(str) + sales_by_quarter['fiscal_quarter'].astype(str),
             sales_by_quarter['quantity'], marker='o')
    plt.xticks(rotation=45)
    plt.title('Tổng Sales Theo Quý')
    plt.xlabel('Năm - Quý')
    plt.ylabel('Số lượng bán')
    plt.grid()
    plt.tight_layout()
    plt.show()


def plot_promotion_summary(sales_df, promotions_df, times_df):
    """
    Hàm vẽ biểu đồ số lượng khuyến mãi theo loại trong quý 2-2025.
    """
    # Merge sales với time để biết quý
    sales_with_time = sales_df.merge(times_df, on='date_id')

    # Lọc dữ liệu Q2-2025
    sales_q2_2025 = sales_with_time[(sales_with_time['year'] == 2025) & (sales_with_time['fiscal_quarter'] == 'Q2')]

    # Lọc những giao dịch có khuyến mãi
    sales_with_promo = sales_q2_2025[sales_q2_2025['promo_id'].notnull()]

    sales_with_promo.info()

    # Merge với bảng promotions để lấy loại khuyến mãi
    sales_with_promo = sales_with_promo.merge(promotions_df, on='promo_id')

    # Tính số lượng khuyến mãi theo loại
    promotion_summary = sales_with_promo.groupby('promo_type')['promo_id'].count().reset_index()

    plt.figure(figsize=(10, 6))
    plt.bar(promotion_summary['promo_type'], promotion_summary['promo_id'])
    plt.title('Số Lượng Khuyến Mãi Theo Loại – Q2-2025')
    plt.xlabel('Loại Khuyến Mãi')
    plt.ylabel('Số Lượng')
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()


def plot_shipments_by_quarter(shipments_df, times_df):
    """
    Hàm vẽ biểu đồ tổng lượng vận chuyển đến cửa hàng theo quý.
    
    Args:
        shipments_df (DataFrame): Dữ liệu shipments đã làm sạch.
        times_df (DataFrame): Dữ liệu thời gian đã làm sạch.
    """
    # Merge shipments với time để bổ sung thông tin thời gian
    shipments_with_time = shipments_df.merge(times_df, left_on='shipment_date', right_on='date_id')

    # Tính tổng số lượng vận chuyển theo năm và quý
    shipments_by_quarter = shipments_with_time.groupby(['year', 'fiscal_quarter'])['quantity'].sum().reset_index()

    # Sắp xếp theo thời gian để vẽ đúng thứ tự
    shipments_by_quarter = shipments_by_quarter.sort_values(by=['year', 'fiscal_quarter'])

    # Vẽ biểu đồ
    plt.figure(figsize=(12, 6))
    plt.plot(shipments_by_quarter['year'].astype(str) + shipments_by_quarter['fiscal_quarter'],
             shipments_by_quarter['quantity'], marker='o')
    plt.xticks(rotation=45)
    plt.title('Tổng Lượng Vận Chuyển Đến Cửa Hàng Theo Quý')
    plt.xlabel('Năm - Quý')
    plt.ylabel('Số Lượng Vận Chuyển')
    plt.grid()
    plt.tight_layout()
    plt.show()



def analyze_stock_to_sales_ratio(inventory_df, warehouses_df, sales_df, stores_df, regions_df, products_df, times_df, output_file='stock_to_sales_analysis.csv'):
    """
    Phân tích Stock-to-Sales Ratio tại DC Đà Nẵng cho khu vực Miền Trung trong Q2-2025.
    """

    # Ghép ngày vào sales
    sales_df = sales_df.merge(times_df, on='date_id')

    # Xác định warehouse_id của DC Đà Nẵng
    dc_danang_id = warehouses_df.loc[warehouses_df['warehouse_name'] == 'Dc Da Nang', 'warehouse_id'].values[0]

    # Tính tổng tồn kho theo SKU tại DC Đà Nẵng
    stock_df = inventory_df[inventory_df['warehouse_id'] == dc_danang_id].groupby('product_id').agg({'stock_on_hand': 'sum'}).reset_index()
    stock_df.rename(columns={'stock_on_hand': 'total_stock'}, inplace=True)

    # Xác định region_id của Miền Trung
    central_region_id = regions_df.loc[regions_df['region_name'] == 'Miền trung', 'region_id'].values[0]

    # Lọc các store thuộc Miền Trung
    central_stores = stores_df[stores_df['region_id'] == central_region_id]['store_id'].unique()

    # Tính tổng sales theo SKU
    sales_summary = sales_df.groupby('product_id').agg({'quantity': 'sum'}).reset_index()
    sales_summary.rename(columns={'quantity': 'total_sales'}, inplace=True)

    # Gộp hai bảng stock và sales theo SKU
    merged_df = pd.merge(stock_df, sales_summary, on='product_id', how='outer')

    # Xử lý giá trị thiếu
    merged_df['total_stock'] = merged_df['total_stock'].fillna(0)
    merged_df['total_sales'] = merged_df['total_sales'].fillna(0)

    # Tính stock-to-sales ratio
    merged_df['stock_to_sales_ratio'] = merged_df.apply(
        lambda row: row['total_stock'] / row['total_sales'] if row['total_sales'] != 0 else float('inf'),
        axis=1
    )

    # Phân loại rủi ro
    def classify_risk(ratio):
        if ratio == float('inf'):
            return 'Nguy hiểm: Có tồn kho, không bán được'
        elif ratio > 3:
            return 'Rủi ro cao: Tồn kho lớn so với doanh số'
        elif ratio > 1.5:
            return 'Theo dõi: Có thể dư hàng'
        else:
            return 'An toàn'

    merged_df['risk_level'] = merged_df['stock_to_sales_ratio'].apply(classify_risk)

    # Ghép thêm tên sản phẩm
    final_df = merged_df.merge(products_df[['product_id', 'product_name']], on='product_id', how='left')

    # Sắp xếp theo mức độ tồn kho
    final_df = final_df.sort_values(by='stock_to_sales_ratio', ascending=False)

    # Tạo thư mục 'results' nếu chưa tồn tại
    output_dir = 'results'
    os.makedirs(output_dir, exist_ok=True)

    # Đường dẫn đầy đủ đến file kết quả
    output_path = os.path.join(output_dir, output_file)
    final_df.to_csv(output_path, index=False)

    return final_df
