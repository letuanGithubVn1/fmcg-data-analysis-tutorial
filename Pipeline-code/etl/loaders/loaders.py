# loaders.py
from typing import List, Dict
from sqlalchemy import create_engine, Table, MetaData
from etl.pipelines import BaseLoader

class DatabaseLoader(BaseLoader):
    """Tải dữ liệu đã biến đổi vào cơ sở dữ liệu đích"""
    
    def __init__(self, db_uri: str):
        self.engine = create_engine(db_uri)
        self.metadata = MetaData()
        self._reflect_tables()
        
    def _reflect_tables(self):
        """Án xạxạ các bảng cơ sở dữ liệu với SQLAlchemy"""
        self.tables = {
            'products': Table('products', self.metadata, autoload_with=self.engine),
            'inventory': Table('inventory', self.metadata, autoload_with=self.engine),
            'stores': Table('stores', self.metadata, autoload_with=self.engine),
            'factories': Table('factories', self.metadata, autoload_with=self.engine),
            'warehouses': Table('warehouses', self.metadata, autoload_with=self.engine),
            'regions': Table('regions', self.metadata, autoload_with=self.engine),
            'shipments': Table('shipments', self.metadata, autoload_with=self.engine),
            'store_inventory_transactions': Table('store_inventory_transactions', self.metadata, autoload_with=self.engine),
            'customers': Table('customers', self.metadata, autoload_with=self.engine),
            'customer_segments': Table('customer_segments', self.metadata, autoload_with=self.engine),
            'competitors': Table('competitors', self.metadata, autoload_with=self.engine),
            'sales': Table('sales', self.metadata, autoload_with=self.engine),
            'times': Table('times', self.metadata, autoload_with=self.engine),
            'promotions': Table('promotions', self.metadata, autoload_with=self.engine)
            # Thêm các bảng khác khi cần
        }
            
    def load(self, transformed_data: List[Dict]) -> bool:
        """Tải dữ liệu vào các bảng phù hợp"""
        try:
            with self.engine.begin() as connection:
                # print(f"transformed_data: {transformed_data}")
                for data_chunk in transformed_data:
                    for table_name, table_data in data_chunk.items():
                        # print(">> Loading to table:", table_name)
                        # print(">> Data:", table_data)
                        if table_name in self.tables:
                            stmt = self.tables[table_name].insert().values(table_data)
                            connection.execute(stmt)
            return True
        except Exception as e:
            print(f"Lỗi khi tải dữ liệu: {str(e)}")
            return False

   
