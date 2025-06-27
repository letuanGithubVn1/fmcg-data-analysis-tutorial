
import pandas as pd

### VALIDATION DÙNG CHUNG ###

def check_missing_data(df):
    return df.isnull().sum().to_dict()

def check_negative_values(df, numeric_cols):
    return {col: int((df[col] < 0).sum()) for col in numeric_cols if (df[col] < 0).any()}

def check_duplicate_keys(df, key_cols):
    return int(df.duplicated(subset=key_cols).sum())

def check_total_consistency(df, qty_col, price_col, total_col, tolerance=0.01):
    df["_expected"] = df[qty_col] * df[price_col]
    df["_delta"] = abs(df["_expected"] - df[total_col])
    count = int((df["_delta"] > tolerance * df[total_col]).sum())
    df.drop(columns=["_expected", "_delta"], inplace=True)
    return count

def check_case_inconsistency(df):
    inconsistent_columns = {}
    
    for col in df.select_dtypes(include='object').columns:
        values = df[col].astype(str)
        lower_map = {}
        
        for val in values:
            val_lower = val.lower()
            if val_lower not in lower_map:
                lower_map[val_lower] = set()
            lower_map[val_lower].add(val)
        
        # Nếu có ít nhất một nhóm có nhiều hơn 1 cách viết
        inconsistent = {k: list(v) for k, v in lower_map.items() if len(v) > 1}
        if inconsistent:
            inconsistent_columns[col] = inconsistent
    
    return inconsistent_columns


### VALIDATION RIÊNG THEO BẢNG ###

def validate_sales(df):
    return {
        "missing_data": check_missing_data(df),
        "negatives": check_negative_values(df, ["quantity", "unit_price", "total_amount"]),
        "duplicates": check_duplicate_keys(df, ["sale_id"]),
        "mismatch_total": check_total_consistency(df, "quantity", "unit_price", "total_amount"),
        "case_inconsistency": check_case_inconsistency(df)
    }

def validate_inventory(df):
    return {
        "missing_data": check_missing_data(df),
        "negatives": check_negative_values(df, ["stock_on_hand", "stock_in", "stock_out"]),
        "duplicates": check_duplicate_keys(df, ["inventory_id"]),
        "case_inconsistency": check_case_inconsistency(df)
    }

def validate_shipments(df):
    return {
        "missing_data": check_missing_data(df),
        "negatives": check_negative_values(df, ["shipping_time_days", "transportation_cost", "quantity"]),
        "duplicates": check_duplicate_keys(df, ["shipment_id"]),
        "case_inconsistency": check_case_inconsistency(df)
    }

def validate_products(df):
    return {
        "missing_data": check_missing_data(df),
        "duplicates": check_duplicate_keys(df, ["product_id"]),
        "case_inconsistency": check_case_inconsistency(df)
    }

def validate_stores(df):
    return {
        "missing_data": check_missing_data(df),
        "duplicates": check_duplicate_keys(df, ["store_id"]),
        "case_inconsistency": check_case_inconsistency(df)
    }

def validate_warehouses(df):
    return {
        "missing_data": check_missing_data(df),
        "duplicates": check_duplicate_keys(df, ["warehouse_id"]),
        "negatives": check_negative_values(df, ["capacity"]),
        "case_inconsistency": check_case_inconsistency(df)
    }

def validate_times(df):
    return {
        "missing_data": check_missing_data(df),
        "duplicates": check_duplicate_keys(df, ["date_id"]),
        "case_inconsistency": check_case_inconsistency(df)
    }

def validate_promotions(df):
    return {
        "missing_data": check_missing_data(df),
        "negatives": check_negative_values(df, ["discount_applied"]),
        "duplicates": check_duplicate_keys(df, ["promo_id"]),
        "case_inconsistency": check_case_inconsistency(df)
    }

def validate_store_inventory_transactions(df):
    return {
        "missing_data": check_missing_data(df),
        "negatives": check_negative_values(df, ["quantity"]),
        "duplicates": check_duplicate_keys(df, ["transaction_id"]),
        "case_inconsistency": check_case_inconsistency(df)
    }

def validate_factories(df):
    return {
        "missing_data": check_missing_data(df),
        "duplicates": check_duplicate_keys(df, ["factory_id"]),
        "case_inconsistency": check_case_inconsistency(df)
    }

def validate_regions(df):
    return {
        "missing_data": check_missing_data(df),
        "duplicates": check_duplicate_keys(df, ["region_id"]),
        "case_inconsistency": check_case_inconsistency(df)
    }

def validate_customers(df):
    return {
        "missing_data": check_missing_data(df),
        "duplicates": check_duplicate_keys(df, ["customer_id"]),
        "case_inconsistency": check_case_inconsistency(df)
    }

def validate_competitors(df):
    return {
        "missing_data": check_missing_data(df),
        "negatives": check_negative_values(df, ["competitor_price"]),
        "duplicates": check_duplicate_keys(df, ["competitor_id"]),
        "case_inconsistency": check_case_inconsistency(df)
    }

def validate_customer_segments(df):
    return {
        "missing_data": check_missing_data(df),
        "duplicates": check_duplicate_keys(df, ["customer_segment_id"]),
        "case_inconsistency": check_case_inconsistency(df)
    }