# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Cấu hình cơ sở dữ liệu
    DB_URI = os.getenv("DB_URI")
    print(f"DB_URI: {DB_URI}")
    # Cấu hình API
    # OPENFOODFACTS_PARAMS = {
    #     "page_size": 50,
    #     "sort_by": "unique_scans_n"
    # }
    
    # SHOPEE_PARAMS = {
    #     "limit": 50,
    #     "offset": 0
    # }
    pass