import pytest
import pandas as pd
from os import path

@pytest.fixture(scope="session")
def df():
    df_path = 'df.csv'
    assert path.exists(df_path), f"{df_path} does not exist."
    df = pd.read_csv(df_path)
    assert not df.empty, "DataFrame is empty."
    return df

def test_df_columns(df):
    expected_columns = ['month', 'day_of_week', 'product_category_name', 'daily_sales_count', 'daily_revenue', 'year', 'order_date']
    assert all(col in df.columns for col in expected_columns), f"DataFrame columns mismatch. Expected: {expected_columns}"
