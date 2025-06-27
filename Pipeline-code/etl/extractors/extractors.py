# extractors.py
import requests
import pandas as pd
from etl.pipelines import BaseExtractor
from typing import List, Dict
from pathlib import Path


class OpenFoodFactsExtractor(BaseExtractor):
    """Trình trích xuất API Open Food Facts"""
    
    def __init__(self, api_url: str = "https://world.openfoodfacts.org/cgi/search.pl"):
        self.api_url = api_url
        self.default_params = {
            'json': 1,
            'page': 1,
            'page_size': 100,
            'action': 'process',
            'fields': 'product_name,brands,countries,code,nutriments,nutrition_grades_tags,url',
            'tagtype_0': 'countries',
            'tag_contains_0': 
            'contains',
        }
    def extract(self, search_terms: List[str] = None, **kwargs) -> List[Dict]:
        """Trích xuất dữ liệu sản phẩm từ API Open Food Facts"""
        merged_params = {**self.default_params, **kwargs}
        if search_terms:
            merged_params['search_terms'] = " ".join(search_terms)
        
        try:
            response = requests.get(self.api_url, params=merged_params)
            response.raise_for_status()
            data = response.json()
            products = data.get('products', [])
            return products
        except Exception as e:
            raise Exception(f"Trích xuất từ Open Food Facts thất bại: {str(e)}")


class CSVFileExtractor(BaseExtractor):
    """Trình trích xuất dữ liệu từ file CSV"""

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def extract(self, *args, **kwargs) -> List[Dict]:
        if not self.file_path.exists():
            raise FileNotFoundError(f"Không tìm thấy file: {self.file_path}")
        try:
            df = pd.read_csv(self.file_path)
            return df.to_dict(orient='records')
        except Exception as e:
            raise Exception(f"Lỗi khi đọc file CSV {self.file_path.name}: {str(e)}")