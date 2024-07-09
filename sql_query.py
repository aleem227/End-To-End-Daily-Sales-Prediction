import sqlite3
import os

# Define the path to the SQLite database file
db_path = 'olist.sqlite'

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# List of tables you are interested in
tables_of_interest = [
    'product_category_name_translation',
    'products',
    'orders',
    'order_items',
    'order_reviews'
]

# Iterate over the tables of interest and print their contents
for table_name in tables_of_interest:
    print(f"Table: {table_name}")
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    
    # Print column names
    column_names = [description[0] for description in cursor.description]
    print(column_names)
    
# Close the connection
conn.close()
