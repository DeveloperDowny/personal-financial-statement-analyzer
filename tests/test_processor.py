import pandas as pd
from statement_analyser.processor import transform_transactions_df
from statement_analyser.processor import transform_statement_df


def test_transform_transactions_df():
    transactions_df_sample = pd.DataFrame(
        {
            "Date": ["01-Sept-2023", "15-Sept-2023"],
            "Time": ["10:30 AM", "02:45 PM"],
            "Type": ["DEBIT", "CREDIT"],
            "Amount": [1000, 2000],
        }
    )

    transformed_df = transform_transactions_df(transactions_df_sample)

    assert "Date_Formated" in transformed_df.columns
    assert "Time_Parsed" in transformed_df.columns
    actual_dates = transformed_df["Date_Formated"].tolist()
    expected_dates = ["01-Sep-2023", "15-Sep-2023"]
    assert actual_dates == expected_dates


def test_transform_statement_df():
    statement_df_sample = pd.DataFrame(
        {
            "Date": ["01-09-2023", "15-09-2023"],
            "Description": ["Test1", "Test2"],
            "Withdrawal": [500, None],
            "Deposit": [None, 1500],
        }
    )

    transformed_df = transform_statement_df(statement_df_sample)

    assert "Date_Formated" in transformed_df.columns
    actual_dates = transformed_df["Date_Formated"].tolist()
    expected_dates = ["01-Sep-2023", "15-Sep-2023"]
    assert actual_dates == expected_dates
