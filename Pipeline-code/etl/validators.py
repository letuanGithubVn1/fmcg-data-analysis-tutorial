import pandas as pd

# ----------------------- FUNCTION CHUNG -----------------------

def check_uniqueness(df, column):
    return df[df.duplicated(column, keep=False)]

def check_null(df, column):
    return df[df[column].isnull()]

def check_allowed_values(df, column, allowed_values):
    return df[~df[column].isin(allowed_values)]

def check_non_negative(df, column):
    return df[df[column] < 0]

# ----------------------- VALIDATE CÁC BẢNG -----------------------

def validate_factories(factory_df):
    results = {}
    results['factory_id_duplicated'] = check_uniqueness(factory_df, 'factory_id')
    results['factory_name_null'] = check_null(factory_df, 'factory_name')
    results['capacity_invalid'] = check_non_negative(factory_df, 'capacity_per_year')
    results['region_id_null'] = check_null(factory_df, 'region_id')
    return results

def validate_warehouses(warehouse_df):
    results = {}
    results['warehouse_id_duplicated'] = check_uniqueness(warehouse_df, 'warehouse_id')
    results['warehouse_name_null'] = check_null(warehouse_df, 'warehouse_name')
    results['region_id_null'] = check_null(warehouse_df, 'region_id')
    no_storage = warehouse_df[
        ~(warehouse_df['has_dry'] | warehouse_df['has_fresh'] | warehouse_df['has_frozen'])
    ] if {'has_dry', 'has_fresh', 'has_frozen'}.issubset(warehouse_df.columns) else pd.DataFrame()
    results['storage_invalid'] = no_storage
    return results

def validate_regions(region_df):
    results = {}
    results['region_id_duplicated'] = check_uniqueness(region_df, 'region_id')
    results['region_name_null'] = check_null(region_df, 'region_name')
    return results

def validate_products(product_df):
    results = {}
    results['product_id_duplicated'] = check_uniqueness(product_df, 'product_id')
    results['product_name_null'] = check_null(product_df, 'product_name')
    results['brand_null'] = check_null(product_df, 'brand')
    results['sku_duplicated'] = check_uniqueness(product_df, 'sku')

    allowed_source = ['inhouse', 'distributed']
    if 'source_type' in product_df.columns:
        results['source_type_invalid'] = check_allowed_values(product_df, 'source_type', allowed_source)

    if 'shelf_life' in product_df.columns:
        results['shelf_life_invalid'] = product_df[product_df['shelf_life'] < 90]

    return results

def validate_stores(store_df, warehouse_df):
    results = {}
    results['store_id_duplicated'] = check_uniqueness(store_df, 'store_id')
    results['store_name_null'] = check_null(store_df, 'store_name')

    allowed_store_types = ['WinMart', 'WinMart+', 'Partner']
    if 'store_type' in store_df.columns:
        results['store_type_invalid'] = check_allowed_values(store_df, 'store_type', allowed_store_types)

    allowed_channels = ['MT', 'GT', 'Horeca']
    if 'channel_type' in store_df.columns:
        results['channel_type_invalid'] = check_allowed_values(store_df, 'channel_type', allowed_channels)

    if 'warehouse_id' in store_df.columns and 'region_id' in store_df.columns:
        if 'warehouse_id' in warehouse_df.columns and 'region_id' in warehouse_df.columns:
            merged = store_df.merge(
                warehouse_df[['warehouse_id', 'region_id']],
                on='warehouse_id',
                suffixes=('', '_wh')
            )
            results['region_mismatch'] = merged[merged['region_id'] != merged['region_id_wh']]

    if 'opened_date' in store_df.columns:
        store_df['opened_date'] = pd.to_datetime(store_df['opened_date'], errors='coerce')
        results['opened_date_invalid'] = store_df[store_df['opened_date'] > pd.Timestamp.today()]

    return results
