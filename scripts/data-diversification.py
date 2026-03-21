import pandas as pd
import numpy as np
import os
import random

# 1. Load the original data
data_path = 'data/customer_shopping_behavior.csv'
df = pd.read_csv(data_path)

# Create a directory for the new structure
new_data_dir = 'data/processed'
os.makedirs(new_data_dir, exist_ok=True)

# --- TASK 1: MULTI-TABLE SCHEMA (Star Schema) ---

# Customer Dimension Table
cust_cols = ['Customer ID', 'Age', 'Gender', 'Location', 'Subscription Status']
dim_customers = df[cust_cols].drop_duplicates(subset=['Customer ID'])
dim_customers.to_csv(f'{new_data_dir}/dim_customers.csv', index=False)

# Product Dimension Table
# Combine unique items and their common categories
prod_cols = ['Item Purchased', 'Category']
dim_products = df[prod_cols].drop_duplicates().reset_index(drop=True)
dim_products['Product ID'] = range(1001, 1001 + len(dim_products))
dim_products.to_csv(f'{new_data_dir}/dim_products.csv', index=False)

# FACT Sales Table
# Mapping Product ID back to sales data
df = df.merge(dim_products, on=['Item Purchased', 'Category'])
fact_sales = df[['Customer ID', 'Product ID', 'Purchase Amount (USD)', 'Size', 'Color', 'Season', 
                 'Review Rating', 'Shipping Type', 'Discount Applied', 'Promo Code Used', 
                 'Previous Purchases', 'Payment Method', 'Frequency of Purchases']]
fact_sales.to_csv(f'{new_data_dir}/fact_sales.csv', index=False)

# --- TASK 2: EXTERNAL DATA (Review Sentiment) ---

reviews = [
    "Amazing quality, fits perfectly!", "Standard shipping was slow but product is great.",
    "Very disappointed with the material.", "Excellent customer service and fast delivery.",
    "The color is slightly different from the photo.", "Best purchase I've made this year!",
    "Too small, need to return it.", "Good value for money.", "Exactly what I was looking for.",
    "Material feels cheap, wouldn't recommend."
]

review_data = []
for cid in df['Customer ID'].unique()[:500]: # Sample first 500 customers
    review_data.append({
        'Customer ID': cid,
        'Review Text': random.choice(reviews),
        'Review Date': pd.to_datetime('2026-01-01') + pd.to_timedelta(random.randint(0, 80), unit='d')
    })

df_reviews = pd.DataFrame(review_data)
df_reviews.to_csv(f'{new_data_dir}/customer_reviews.csv', index=False)

# --- TASK 3: TEMPORAL DATA (Inventory) ---

inventory_data = []
for pid in dim_products['Product ID']:
    inventory_data.append({
        'Product ID': pid,
        'Stock Level': random.randint(5, 150),
        'Last Restock Date': pd.to_datetime('2026-03-01') - pd.to_timedelta(random.randint(1, 30), unit='d')
    })

df_inventory = pd.DataFrame(inventory_data)
df_inventory.to_csv(f'{new_data_dir}/inventory_logs.csv', index=False)

print("Data diversification completed successfully!")
print(f"New files created in {new_data_dir}: dim_customers.csv, dim_products.csv, fact_sales.csv, customer_reviews.csv, inventory_logs.csv")
