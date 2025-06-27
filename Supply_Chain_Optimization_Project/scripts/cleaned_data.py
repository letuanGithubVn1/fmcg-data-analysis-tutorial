import pandas as pd

def clean_warehouses(df):
    df["warehouse_name"] = df["warehouse_name"].astype("string").str.strip().str.title()
    df["location"] = df["location"].astype("string").str.strip().str.title()
    return df

def clean_shipments(df):
    df["shipment_date"] = pd.to_datetime(df["shipment_date"], errors="coerce")
    df["delivery_status"] = df["delivery_status"].astype("string").str.strip().str.lower()
    return df

def clean_inventory(df):
    df["expiry_date"] = pd.to_datetime(df["expiry_date"], errors="coerce")
    df["batch_id"] = df["batch_id"].astype("string").str.upper().str.strip()
    df["batch_number"] = df["batch_number"].astype("string").str.upper().str.strip()
    for col in ["stock_on_hand", "stock_in", "stock_out"]:
        df[col] = df[col].apply(lambda x: max(x, 0))
    return df

def clean_stores(df):
    object_cols = df.select_dtypes(include="object").columns
    df[object_cols] = df[object_cols].astype("string")
    df["store_name"] = df["store_name"].astype("string").str.strip().str.title()
    return df

def clean_products(df):
    object_cols = df.select_dtypes(include="object").columns
    df[object_cols] = df[object_cols].astype("string")

    df["unit_size"] = df["unit_size"].str.lower().str.replace(" ", "", regex=False)
    df["last_modified"] = pd.to_datetime(df["last_modified"], errors="coerce")
    df["shelf_life"] = df["shelf_life"].apply(lambda x: x if x > 0 else None)

    return df

def clean_times(df):
    object_cols = df.select_dtypes(include="object").columns
    df[object_cols] = df[object_cols].astype("string")
    df["date_id"] = pd.to_datetime(df["date_id"], errors="coerce")
    return df

def clean_sales(df):
    df["date_id"] = pd.to_datetime(df["date_id"], errors="coerce")
    return df

def clean_promotions(df):
    object_cols = df.select_dtypes(include="object").columns
    df[object_cols] = df[object_cols].astype("string")
    df["promo_start"] = pd.to_datetime(df["promo_start"], errors="coerce")
    df["promo_end"] = pd.to_datetime(df["promo_end"], errors="coerce")
    df = df[(df["discount_applied"] >= 0) & (df["discount_applied"] <= 100)]
    return df

def clean_competitors(df):
    object_cols = df.select_dtypes(include="object").columns
    df[object_cols] = df[object_cols].astype("string")
    df["date_id"] = pd.to_datetime(df["date_id"], errors="coerce")
    return df

def clean_store_inventory_transactions(df):
    df["date_id"] = pd.to_datetime(df["date_id"], errors="coerce")
    df["transaction_type"] = df["transaction_type"].astype("string").str.upper().str.strip()
    return df

def clean_customers(df):
    object_cols = df.select_dtypes(include="object").columns
    df[object_cols] = df[object_cols].astype("string")
    df["birthdate"] = pd.to_datetime(df["birthdate"], errors="coerce")
    # df["gender"] = df["gender"].astype("string").str.strip().str.capitalize()
    return df

def clean_customer_segments(df):
    object_cols = df.select_dtypes(include="object").columns
    df[object_cols] = df[object_cols].astype("string")
    df["segment_name"] = df["segment_name"].astype("string").str.strip().str.title()
    return df

def clean_factories(df):
    object_cols = df.select_dtypes(include="object").columns
    df[object_cols] = df[object_cols].astype("string")
    df["location"] = df["location"].astype("string").str.strip().str.title()
    return df

def clean_regions(df):
    df["region_name"] = df["region_name"].astype("string").str.strip().str.capitalize()
    return df
