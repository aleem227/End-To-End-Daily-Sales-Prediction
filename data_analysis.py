import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('daily_sales.csv')

# Convert order_date to datetime format
df['order_date'] = pd.to_datetime(df['order_date'])

# Filter the data to include only from January 2017 onwards
df = df[df['order_date'] >= '2017-01-01']

# Check for null values in the DataFrame
null_values = df.isnull().sum()
print("Null values in each column:\n", null_values)

# Drop rows with any null values
df = df.dropna()

# Extract year, month, and day of the week from the order_date
df['year'] = df['order_date'].dt.year
df['month'] = df['order_date'].dt.month
df['day_of_week'] = df['order_date'].dt.dayofweek

# Display the DataFrame with new features
print(df.head())


## Data Visualisation

# Plot daily sales count over time
plt.figure(figsize=(12, 6))
sns.lineplot(data=df, x='order_date', y='daily_sales_count')
plt.title('Daily Sales Count Over Time')
plt.xlabel('Date')
plt.ylabel('Daily Sales Count')
plt.show()

# Plot daily revenue over time
plt.figure(figsize=(12, 6))
sns.lineplot(data=df, x='order_date', y='daily_revenue')
plt.title('Daily Revenue Over Time')
plt.xlabel('Date')
plt.ylabel('Daily Revenue')
plt.show()

# Plot sales count by product category
plt.figure(figsize=(12, 6))
sns.barplot(data=df, x='product_category_name', y='daily_sales_count', estimator=sum)
plt.title('Total Sales Count by Product Category')
plt.xlabel('Product Category')
plt.ylabel('Total Sales Count')
plt.xticks(rotation=90)
plt.show()

# Plot sales count by product category
plt.figure(figsize=(12, 6))
sns.barplot(data=df, x='product_category_name', y='daily_sales_count', estimator=sum)
plt.title('Total Sales Count by Product Category')
plt.xlabel('Product Category')
plt.ylabel('Total Sales Count')
plt.xticks(rotation=90)
plt.show()

# Optionally, save the resulting dataframe to a CSV file for further analysis
df.to_csv('df.csv', index=False)

