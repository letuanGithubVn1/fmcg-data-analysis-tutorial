# transformers.py
from typing import List, Dict
import re
import ftfy
import pandas as pd
from datetime import datetime
from etl.pipelines import BaseTransformer

class RetailDataTransformer(BaseTransformer):
    """Biến đổi dữ liệu API thô để khớp với lược đồ cơ sở dữ liệu đích"""
    
    def __init__(self):
        # Định nghĩa ánh xạ cho các hệ thống nguồn khác nhau
        self.source_mappings = {
            'openfoodfacts': self._transform_openfoodfacts
        }
        self.counter = 0
    def transform(self, raw_data: List[Dict], source: str) -> List[Dict]:
        """Biến đổi dữ liệu dựa trên hệ thống nguồn"""
        if source not in self.source_mappings:
            raise ValueError(f"Nguồn dữ liệu không được hỗ trợ: {source}")
            
        return self.source_mappings[source](raw_data)
    
    def _clean_text(self, text: str) -> str:
        """Sửa lỗi mã hóa, loại bỏ khoảng trắng thừa, chuẩn hóa chữ."""
        if not isinstance(text, str):
            return ''
        text = ftfy.fix_text(text)              
        text = text.strip()                   
        text = re.sub(r'\s+', ' ', text)
        text = text.lower().title()        
        return text
    
    def _transform_openfoodfacts(self, products: List[Dict]) -> List[Dict]:
        """Biến đổi dữ liệu Open Food Facts sang lược đồ của chúng ta"""
        transformed_products = []
        for product in products:
            try:
                # Thêm id cho từng sản phẩm
                self.counter +=1 
                product_id = self.counter

                # # Xử lý product_name
                # product_name = self._clean_text(product.get('product_name', ''))
                # # Nếu giá trị product_name = None/'' thì chạy tiếp
                # if not product_name:
                #     continue
                
                # Tạo bản ghi sản phẩm
                transformed = {
                    'products': {
                        'product_id': product_id,
                        'product_name': self._clean_text(product.get('product_name', '')),
                        'brand': self._clean_text(product.get('brands', '')),
                        'category': self._clean_text(product.get('categories', '')),
                        'sku': product.get('code', '').strip(),
                        'last_modified': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'unit_price': '1.12'
                    }
                }
                
                transformed_products.append(transformed)
                
            except Exception as e:
                self.logger.error(f"Error transforming product {product.get('code')}: {str(e)}")
                continue
                
        return transformed_products

class FileDataTransformer(BaseTransformer):
    """Biến đổi dữ liệu từ các file CSV"""

    def __init__(self):
        self.source_mappings = {
            'products': self._transform_products,
            'stores': self._transform_stores,
            'warehouses': self._transform_warehouses,
            'regions': self._transform_regions,
            'factories': self._transform_factories,
            'inventory': self._transform_inventory,
            'shipments': self._transform_shipments,
            'store_inventory_transactions': self._transform_store_inventory_transactions,
            'customers': self._transform_customers,
            'customer_segments': self._transform_customer_segments,
            'competitors': self._transform_competitors,
            'sales': self._transform_sales,
            'times': self._transform_time,
            'promotions': self._transform_promotions
        }

    def transform(self, raw_data: List[Dict], source: str) -> List[Dict]:
        if source not in self.source_mappings:
            raise ValueError(f"Nguồn dữ liệu không được hỗ trợ: {source}")
        return self.source_mappings[source](raw_data)

    def _clean_text(self, text: str) -> str:
        if not isinstance(text, str):
            return ''
        text = ftfy.fix_text(text)
        text = text.strip()
        text = re.sub(r'\s+', ' ', text)
        return text

    # ---- Biến đổi từng bảng cụ thể ----


    # bảng products
    def _transform_products(self, data: List[Dict]) -> List[Dict]:
        """Chuẩn hóa bảng sản phẩm từ file CSV products.csv"""
        result = []
        for row in data:
            transformed_row = {
                'products': {
                    'product_id': int(row['product_id']),
                    'product_name': self._clean_text(row['product_name']),
                    'brand': self._clean_text(row['brand']),
                    'category': self._clean_text(row['category']),
                    'sub_category': self._clean_text(row.get('sub_category', '')),
                    'source_type': row.get('source_type', 'inhouse'),
                    'factory_id': None if pd.isna(row.get('factory_id')) else int(row['factory_id']),
                    'shelf_life': int(row.get('shelf_life', 0)),
                    'packaging_type': self._clean_text(row.get('packaging_type', '')),
                    'unit_size': self._clean_text(row.get('unit_size', '')),
                    'sku': str(row.get('sku', '')).strip(),
                    'last_modified': row.get('last_modified') or datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            }
            result.append(transformed_row)
        return result

    # bảng stores
    def _transform_stores(self, data: List[Dict]) -> List[Dict]:
        """Chuẩn hóa bảng cửa hàng"""
        result = []
        for row in data:
            transformed = {
            'stores': {
                'store_id': int(row['store_id']),
                'store_name': self._clean_text(row['store_name']),
                'store_type': self._clean_text(row.get('store_type', '')),
                'channel_type': self._clean_text(row.get('channel_type', '')),
                'region_id': int(row['region_id']) if not pd.isna(row['region_id']) else None,
                'warehouse_id': int(row['warehouse_id']) if not pd.isna(row['warehouse_id']) else None,
                'partner_name': self._clean_text(row.get('partner_name', '')),
                'opened_date': row.get('opened_date') or None
                }
            }
            result.append(transformed)
        return result

    # bảng warehouses
    def _transform_warehouses(self, data: List[Dict]) -> List[Dict]:
        """Chuẩn hóa bảng kho"""
        return [{'warehouses': row} for row in data]

    # bảng regions
    def _transform_regions(self, data: List[Dict]) -> List[Dict]:
        """Chuẩn hóa bảng vùng"""
        return [{'regions': row} for row in data]

    # bảng factories
    def _transform_factories(self, data: List[Dict]) -> List[Dict]:
        """Chuẩn hóa bảng nhà máy"""
        return [{'factories': row} for row in data]
    
    # bảng inventory
    def _transform_inventory(self, data: List[Dict]) -> List[Dict]:
        result = []
        for row in data:
            result.append({
                'inventory': {
                    'inventory_id': int(row['inventory_id']),
                    'product_id': int(row['product_id']) if not pd.isna(row['product_id']) else None,
                    'store_id': int(row['store_id']) if not pd.isna(row['store_id']) else None,
                    'warehouse_id': int(row['warehouse_id']) if not pd.isna(row['warehouse_id']) else None,
                    'date_id': row.get('date_id'),
                    'stock_on_hand': int(row.get('stock_on_hand', 0)),
                    'stock_in': int(row.get('stock_in', 0)),
                    'stock_out': int(row.get('stock_out', 0)),
                    'reorder_point': int(row.get('reorder_point', 0)),
                    'lead_time_days': int(row.get('lead_time_days', 0)),
                    'expiry_date': row.get('expiry_date'),  # dạng YYYY-MM-DD
                    'batch_number': self._clean_text(row.get('batch_number', '')),
                    'batch_id': str(row.get('batch_id', '')).strip()
                }
            })
        return result

    # bảng shipments
    def _transform_shipments(self, data: List[Dict]) -> List[Dict]:
        result = []
        for row in data:
            result.append({
                'shipments': {
                    'shipment_id': int(row['shipment_id']),
                    'warehouse_id': int(row['warehouse_id']),
                    'store_id': int(row['store_id']),
                    'product_id': int(row['product_id']),
                    'shipment_date': pd.to_datetime(row['shipment_date']).strftime('%Y-%m-%d'),
                    'shipping_time_days': int(row['shipping_time_days']),
                    'transportation_cost': float(row['transportation_cost']),
                    'delivery_status': str(row['delivery_status']).strip(),
                    'quantity': int(row['quantity']),
                }
            })
        return result

    # bảng store_inventory_transactions
    def _transform_store_inventory_transactions(self, data: List[Dict]) -> List[Dict]:
        result = []
        for row in data:
            try:
                result.append({
                    'store_inventory_transactions': {
                        'transaction_id': int(row['transaction_id']),
                        'store_id': int(row['store_id']),
                        'product_id': int(row['product_id']),
                        'date_id': row.get('date_id'),
                        'transaction_type': self._clean_text(row.get('transaction_type')),
                        'quantity': int(row.get('quantity', 0)),
                        'reference_sale_id': int(row['reference_sale_id']) if not pd.isna(row['reference_sale_id']) else None,
                        'reference_shipment_id': int(row['reference_shipment_id']) if not pd.isna(row['reference_shipment_id']) else None
                    }
                })
            except Exception as e:
                self.logger.warning(f"Lỗi transform inventory transaction: {e} | {row}")
                continue
        return result

    # bảng customers
    def _transform_customers(self, data: List[Dict]) -> List[Dict]:
        result = []
        for row in data:
            result.append({
                    'customers': {
                        'customer_id': int(row['customer_id']),
                        'customer_name': self._clean_text(row.get('name', '')),
                        'birthdate': row.get('birthdate'),
                        'region_id': int(row['region_id']) if not pd.isna(row['region_id']) else None,
                        'customer_segment_id': int(row['customer_segment_id']) if not pd.isna(row['customer_segment_id']) else None,
                        'customer_type': self._clean_text(row.get('customer_type', ''))
                    }
                })
        return result

    # bảng customers_segments
    def _transform_customer_segments(self, data: List[Dict]) -> List[Dict]:
        result = []
        for row in data:
           result.append({
                'customer_segments': {
                    'customer_segment_id': int(row['customer_segment_id']),
                    'segment_name': self._clean_text(row.get('segment_name', '')),
                    'buying_frequency': self._clean_text(row.get('buying_frequency', '')),
                    'average_spending': float(row.get('average_spending', 0.0))
                }
            })
        return result

    # bảng competitors
    def _transform_competitors(self, data: List[Dict]) -> List[Dict]:
        result = []
        for row in data:
           result.append({
                'competitors': {
                    'competitor_id': int(row['competitor_id']),
                    'competitor_brand': self._clean_text(row.get('competitor_brand', '')),
                    'competitor_channel': self._clean_text(row.get('competitor_channel', '')),
                    'competitor_location': self._clean_text(row.get('competitor_location', '')),
                    'product_id': int(row['product_id']) if not pd.isna(row['product_id']) else None,
                    'competitor_price': float(row.get('competitor_price', 0.0)),
                    'competitor_promo_id': int(row['competitor_promo_id']) if not pd.isna(row.get('competitor_promo_id')) else None,
                    'date_id': row.get('date_id')  # dạng YYYY-MM-DD
                }
            })
        return result

    # Bảng time
    def _transform_time(self, data: List[Dict]) -> List[Dict]:
        result = []
        for row in data:
            result.append({
                    'times': {
                        'date_id': row['date_id'], 
                        'day': int(row['day']),
                        'month': int(row['month']),
                        'fiscal_quarter': self._clean_text(row.get('fiscal_quarter', '')),
                        'year': int(row['year']),
                        'week_number': int(row['week_number']) if str(row.get('week_number', '')).isdigit() else None,
                        'weekend_flag': bool(row.get('is_weekend', False)),
                        'holiday_flag': bool(row.get('is_holiday', False))
                    }
                })
        return result

    # Bảng sales
    def _transform_sales(self, data: List[Dict]) -> List[Dict]:
        result = []
        for row in data:
            result.append({
                'sales': {
                    'sale_id': int(row['sale_id']),
                    'product_id': int(row['product_id']),
                    'customer_id': int(row['customer_id']),
                    'store_id': int(row['store_id']),
                    'date_id': pd.to_datetime(row['date_id']).strftime('%Y-%m-%d'),
                    'quantity': int(row['quantity']),
                    'unit_price': float(row['unit_price']),
                    'total_amount': float(row['total_amount']),
                    'promo_id': int(row['promo_id']) if row['promo_id'] != '' and not pd.isna(row['promo_id']) else None,
                    'inventory_id': int(row['inventory_id']) if row['inventory_id'] != '' and not pd.isna(row['inventory_id']) else None,
                    'shipment_id': int(row['shipment_id']) if row['shipment_id'] != '' and not pd.isna(row['shipment_id']) else None,
                }    
            })
        return result

    # Bảng promotions
    def _transform_promotions(self, data: List[Dict]) -> List[Dict]:
        result = []
        for row in data:
            result.append({
                'promotions': {
                    'promo_id': int(row['promo_id']),
                    'promo_type': self._clean_text(row.get('promo_type', '')),
                    'discount_applied': float(row.get('discount_applied', 0.0)),
                    'promo_start': row.get('promo_start'),
                    'promo_end': row.get('promo_end'),
                    'apply_scope': self._clean_text(row.get('apply_scope', ''))
                }
            })
        return result

