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

def test_df_not_null(df):
    assert df.isnull().sum().sum() == 0, "DataFrame contains null values."
