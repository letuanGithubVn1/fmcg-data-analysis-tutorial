
import pandas as pd
from scripts.raw import load_data
from scripts import cleaned_data as cd
from scripts import validation as val
from scripts import eda
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
load_dotenv()

# Đọc các biến môi trường
DB_URI = os.getenv("DB_URI")
print(DB_URI)

engine = create_engine(DB_URI)

def run_cleaning_pipeline(engine):
    raw_data = load_data(engine)

    cleaned = {
        "warehouses": cd.clean_warehouses(raw_data["warehouses"]),
        "shipments": cd.clean_shipments(raw_data["shipments"]),
        "inventory": cd.clean_inventory(raw_data["inventory"]),
        "stores": cd.clean_stores(raw_data["stores"]),
        "products": cd.clean_products(raw_data["products"]),
        "times": cd.clean_times(raw_data["times"]),
        "sales": cd.clean_sales(raw_data["sales"]),
        "promotions": cd.clean_promotions(raw_data["promotions"]),
        "competitors": cd.clean_competitors(raw_data["competitors"]),
        "store_inventory_transactions": cd.clean_store_inventory_transactions(raw_data["store_inventory_transactions"]),
        "customers": cd.clean_customers(raw_data["customers"]),
        "customer_segments": cd.clean_customer_segments(raw_data["customer_segments"]),
        "factories": cd.clean_factories(raw_data["factories"]),
        "regions": cd.clean_regions(raw_data["regions"]),
    }

    return cleaned

def run_validation_pipeline(cleaned_data):
    validators = {
        "sales": val.validate_sales,
        "inventory": val.validate_inventory,
        "shipments": val.validate_shipments,
        "products": val.validate_products,
        "stores": val.validate_stores,
        "warehouses": val.validate_warehouses,
        "times": val.validate_times,
        "promotions": val.validate_promotions,
        "competitors": val.validate_competitors,
        "store_inventory_transactions": val.validate_store_inventory_transactions,
        "customers": val.validate_customers,
        "customer_segments": val.validate_customer_segments,
        "factories": val.validate_factories,
        "regions": val.validate_regions,
    }

    print("\n VALIDATION REPORT:")
    for table, validator in validators.items():
        if table in cleaned_data:
            result = validator(cleaned_data[table])
            print(f"\n{table.upper()}:")
            for check, outcome in result.items():
                print(f" - {check}: {outcome}")
        else:
            print(f"\n{table} not found in cleaned data.")


def analyze_table(cleaned_data, table_name):
    df = cleaned_data.get(table_name)
    if df is not None:
        return df
    else:
        print(f"{table_name} not found in cleaned data.")


if __name__ == "__main__":

    # Kiểm tra dữ liệu raw
    # run_validation_pipeline(raw_data)

    cleaned_data = run_cleaning_pipeline(engine)
    # for table_name, df in cleaned_data.items():
    #     print(f"✔ Cleaned {table_name}: {df.shape[0]} rows, {df.shape[1]} columns")
   
    # Kiểm tra dữ liệu sau khi làm sạch
    # run_validation_pipeline(cleaned_data)

    sales_df = analyze_table(cleaned_data, "sales")
    times_df = analyze_table(cleaned_data, "times")
    promotion_df = analyze_table(cleaned_data, "promotions")
    shipments_df = analyze_table(cleaned_data, "shipments")
    inventory_df = analyze_table(cleaned_data, "inventory")
    warehouses_df = analyze_table(cleaned_data, "warehouses")
    stores_df = analyze_table(cleaned_data, "stores")
    regions_df = analyze_table(cleaned_data, "regions")
    products_df = analyze_table(cleaned_data, "products")

    # print(warehouses_df.head())
    # Gọi các hàm trong file eda.py
    # eda.plot_sales_by_quarter(sales_df, times_df)
    # eda.plot_promotion_summary(sales_df, promotion_df, times_df)
    eda.plot_shipments_by_quarter(shipments_df, times_df)
    # result_df = eda.analyze_stock_to_sales_ratio(inventory_df, warehouses_df, sales_df, stores_df, regions_df, products_df, times_df)
    # print(result_df.head())

    


  