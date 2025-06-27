import logging
import pandas as pd
from abc import ABC, abstractmethod
from typing import Dict, List, Any
from datetime import datetime
from etl import validators 


class BaseExtractor(ABC):
    """Lớp cơ sở trừu tượng cho trình trích xuất dữ liệu"""
    
    @abstractmethod
    def extract(self, *args, **kwargs) -> List[Dict]:
        pass

class BaseTransformer(ABC):
    """Lớp cơ sở trừu tượng cho trình biến đổi dữ liệu"""
    
    @abstractmethod
    def transform(self, raw_data: List[Dict]) -> List[Dict]:
        pass

class BaseLoader(ABC):
    """Lớp cơ sở trừu tượng cho trình tải dữ liệu"""
    
    @abstractmethod
    def load(self, transformed_data: List[Dict]) -> bool:
        pass

class ETLPipeline:
    """Bộ điều khiển pipeline ETL chính"""
    
    def __init__(self, extractor: BaseExtractor, 
                 transformer: BaseTransformer, 
                 loader: BaseLoader):
        self.extractor = extractor
        self.transformer = transformer
        self.loader = loader
        self.logger = logging.getLogger(__name__)
        
    def run(self, extract_kwargs=None, transform_kwargs=None):
        """Thực hiện quá trình ETL"""
        extract_kwargs = extract_kwargs or {}
        transform_kwargs = transform_kwargs or {}
        try:
            # Giai đoạn trích xuất
            self.logger.info("Bắt đầu trích xuất...")
            raw_data = self.extractor.extract(**extract_kwargs)
            
            # Giai đoạn biến đổi
            self.logger.info("Đang biến đổi dữ liệu...")
            transformed_data = self.transformer.transform(raw_data, **transform_kwargs)
            
            # Giai đoạn tải
            self.logger.info("Đang tải dữ liệu...")
            success = self.loader.load(transformed_data)
            
            if success:
                self.logger.info("Quá trình ETL hoàn thành thành công")
            else:
                self.logger.error("Quá trình ETL thất bại khi tải")
                
            return success
            
        except Exception as e:
            self.logger.error(f"Quá trình ETL thất bại: {str(e)}")
            raise

    def _run_validation(self, source: str, transformed: list[dict]) -> dict[str, pd.DataFrame]:
        """Tự động gọi các hàm kiểm tra tùy theo source"""
        if source == 'products':
            df = pd.DataFrame([x['products'] for x in transformed])
            return validators.validate_products(df)
        elif source == 'factories':
            df = pd.DataFrame([x['factories'] for x in transformed])
            return validators.validate_factories(df)
        elif source == 'warehouses':
            df = pd.DataFrame([x['warehouses'] for x in transformed])
            return validators.validate_warehouses(df)
        elif source == 'regions':
            df = pd.DataFrame([x['regions'] for x in transformed])
            return validators.validate_regions(df)
        elif source == 'stores':
            df = pd.DataFrame([x['stores'] for x in transformed])
            # ⚠️ Cần warehouse_df để validate region logic, có thể nạp thủ công từ DB hoặc inject từ transform_kwargs
            return validators.validate_stores(df, pd.DataFrame())  # Tạm thời để trống
        else:
            return {}