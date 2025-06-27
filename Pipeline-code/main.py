# main.py
import logging
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from etl.extractors import OpenFoodFactsExtractor, CSVFileExtractor
from etl.transformers import RetailDataTransformer, FileDataTransformer
from etl.loaders import DatabaseLoader
from etl.pipelines import ETLPipeline

# Cấu hình logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# URI kết nối database (cập nhật tùy môi trường)
load_dotenv()

# Đọc các biến môi trường
username = os.getenv("username")
password = os.getenv("password")
host = os.getenv("host")
port = os.getenv("port")
database = os.getenv("database")

# Kết nối DB bằng pymysql
DB_URI = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"

# Khởi tạo loader duy nhất cho toàn bộ pipeline
loader = DatabaseLoader(DB_URI)

# Danh sách các file CSV và nguồn tương ứng
csv_sources = {
    'products': 'data/products.csv',
    'stores': 'data/stores.csv',
    'warehouses': 'data/warehouses.csv',
    'regions': 'data/regions.csv',
    'factories': 'data/factories.csv',
    'customers': 'data/customers.csv',
    'customer_segments': 'data/customer_segments.csv',
    'competitors': 'data/competitors.csv',
    'times': 'data/time.csv',
    'promotions': 'data/promotions.csv',
    'inventory': 'data/inventory.csv',
    'shipments': 'data/shipments.csv',
    'store_inventory_transactions': 'data/Store_Inventory_Transactions.csv',
    'sales': 'data/sales.csv',
}

def run_csv_pipelines():
    """Chạy ETL pipeline cho toàn bộ file CSV"""
    transformer = FileDataTransformer()
    for source_name, file_path in csv_sources.items():
        print(f"\n>>> Đang xử lý nguồn: {source_name} từ {file_path}")
        try:
            extractor = CSVFileExtractor(file_path)
            pipeline = ETLPipeline(extractor, transformer, loader)
            pipeline.run(transform_kwargs={'source': source_name})
        except Exception as e:
            print(f"[LỖI] Pipeline cho nguồn {source_name} thất bại: {str(e)}")

def run_openfoodfacts_pipeline():
    """Chạy ETL pipeline cho API Open Food Facts"""
    print("\n>>> Đang xử lý API Open Food Facts")
    try:
        extractor = OpenFoodFactsExtractor()
        transformer = RetailDataTransformer()
        pipeline = ETLPipeline(extractor, transformer, loader)
        pipeline.run(extract_kwargs={'search_terms': ['noodle', 'snack']}, transform_kwargs={'source': 'openfoodfacts'})
    except Exception as e:
        print(f"[LỖI] Pipeline API Open Food Facts thất bại: {str(e)}")

if __name__ == "__main__":
    run_csv_pipelines()
    # run_openfoodfacts_pipeline()
    print("\n✅ Toàn bộ pipeline đã chạy xong.")
