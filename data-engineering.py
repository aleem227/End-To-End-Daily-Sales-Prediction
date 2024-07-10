import sqlite3
import os
import pandas as pd

# Define the path to the SQLite database file
db_path = 'olist.sqlite'

# Connect to the SQLite database
conn = sqlite3.connect(db_path)

# List of tables and their relevant columns
tables_and_columns = {
    'orders': ['order_id', 'order_purchase_timestamp', 'order_status'],
    'order_items': ['order_id', 'product_id', 'order_item_id', 'price'],
    'products': ['product_id', 'product_category_name']
}

# Function to read specific columns from a table
def read_table(table_name, columns):
    query = f"SELECT {', '.join(columns)} FROM {table_name}"
    return pd.read_sql_query(query, conn)

# Read relevant data from each table
orders = read_table('orders', tables_and_columns['orders'])
order_items = read_table('order_items', tables_and_columns['order_items'])
products = read_table('products', tables_and_columns['products'])

# Close the connection
conn.close()

# Filter only completed orders
completed_orders = orders[orders['order_status'] == 'delivered']

# Merge the dataframes to create a consolidated dataframe
merged_df = pd.merge(completed_orders, order_items, on='order_id')
merged_df = pd.merge(merged_df, products, on='product_id')

# Convert order_purchase_timestamp to datetime
merged_df['order_purchase_timestamp'] = pd.to_datetime(merged_df['order_purchase_timestamp'])

# Extract the date from order_purchase_timestamp for daily aggregation
merged_df['order_date'] = merged_df['order_purchase_timestamp'].dt.date

# Aggregate daily sales count and revenue per product
daily_sales = merged_df.groupby(['order_date', 'product_id', 'product_category_name']).agg(
    daily_sales_count=('order_item_id', 'count'),
    daily_revenue=('price', 'sum')
).reset_index()

# Print the resulting dataframe
print(daily_sales)

# Optionally, save the resulting dataframe to a CSV file for further analysis
daily_sales.to_csv('daily_sales.csv', index=False)
