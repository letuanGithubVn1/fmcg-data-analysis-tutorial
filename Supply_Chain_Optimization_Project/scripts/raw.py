import pandas as pd


def load_data(engine):
    warehouses_df = pd.read_sql("SELECT * FROM warehouses", engine)
    shipments_df = pd.read_sql("SELECT * FROM shipments", engine)
    inventory_df = pd.read_sql("SELECT * FROM inventory", engine)
    stores_df = pd.read_sql("SELECT * FROM stores", engine)
    products_df = pd.read_sql("SELECT * FROM products", engine)
    times_df = pd.read_sql("SELECT * FROM times", engine)
    sales_df = pd.read_sql("SELECT * FROM sales", engine)
    promotions_df = pd.read_sql("SELECT * FROM promotions", engine)
    competitors_df = pd.read_sql("SELECT * FROM competitors", engine)
    store_inv_trans_df = pd.read_sql("SELECT * FROM store_inventory_transactions", engine)
    customers_df = pd.read_sql("SELECT * FROM customers", engine)
    customer_segments_df = pd.read_sql("SELECT * FROM customer_segments", engine)
    factories_df = pd.read_sql("SELECT * FROM factories", engine)
    regions_df = pd.read_sql("SELECT * FROM regions", engine)

    return {
        "warehouses": warehouses_df,
        "shipments": shipments_df,
        "inventory": inventory_df,
        "stores": stores_df,
        "products": products_df,
        "times": times_df,
        "sales": sales_df,
        "promotions": promotions_df,
        "competitors": competitors_df,
        "store_inventory_transactions": store_inv_trans_df,
        "customers": customers_df,
        "customer_segments": customer_segments_df,
        "factories": factories_df,
        "regions": regions_df,
    }
