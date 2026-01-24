import pandas as pd

from statement_analyser.constants import HDFC_DEPOSITED_COL, HDFC_WITHDRAWAL_COL
from statement_analyser.extractor import extract_upi_description, extract_upi_name
from statement_analyser.helper import parse_time


def process_upi_narration(df: pd.DataFrame) -> pd.DataFrame:
    """
    Process the 'Narration' column in the DataFrame to extract UPI-related information.

    Args:
        df (pd.DataFrame): The input DataFrame with a 'Narration' column.
    Returns:
        pd.DataFrame: The DataFrame with additional UPI-related columns.
    """
    df["Narration"] = df["Narration"].astype(str)
    df["UPIs"] = df["Narration"].str.split("@", expand=True)[0]
    df["UPI_Name"] = df["UPIs"].apply(extract_upi_name)
    df["UPI_Bank"] = df["Narration"].str.extract(r"@(.*?)-")
    df["UPI_Description"] = df["Narration"].apply(extract_upi_description)
    return df


def set_column_types(statement_df: pd.DataFrame) -> pd.DataFrame:
    """
    Set the appropriate data types for the statement DataFrame columns.

    Args:
        statement_df (pd.DataFrame): The bank statement DataFrame.
    Returns:
        pd.DataFrame: The DataFrame with updated column types.
    """
    dtypes = {
        HDFC_WITHDRAWAL_COL: float,
        HDFC_DEPOSITED_COL: float,
        "Closing Balance": float,
        "Date": "datetime64[ns]",
    }
    statement_df = statement_df.astype(dtypes)
    return statement_df


def transform_transactions_df(transactions_df: pd.DataFrame) -> pd.DataFrame:
    transactions_df["Date"] = transactions_df["Date"].str.replace("Sept", "Sep")
    transactions_df["Date_Formated"] = pd.to_datetime(
        transactions_df["Date"]
    ).dt.strftime("%d-%b-%Y")
    transactions_df["Time_Parsed"] = transactions_df["Time"].apply(parse_time)

    return transactions_df


def filter_deposit_withdrawal(
    statement_df: pd.DataFrame, transactions_df: pd.DataFrame
):
    """
    Filter the statement and transactions DataFrames into withdrawals and deposits.

    Args:
        statement_df (pd.DataFrame): The bank statement DataFrame.
        transactions_df (pd.DataFrame): The transactions DataFrame.
    Returns:
        Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]: Four DataFrames -
            withdrawal_statements_df, withdrawal_transactions_df,
            deposit_statements_df, deposit_transactions_df.
    """
    withdrawal_statements_df = statement_df[statement_df[HDFC_WITHDRAWAL_COL].notnull()]
    withdrawal_transactions_df = transactions_df[transactions_df["Type"] == "DEBIT"]
    deposit_statements_df = statement_df[statement_df[HDFC_DEPOSITED_COL].notnull()]
    deposit_transactions_df = transactions_df[transactions_df["Type"] == "CREDIT"]
    return (
        withdrawal_statements_df,
        withdrawal_transactions_df,
        deposit_statements_df,
        deposit_transactions_df,
    )


def get_extended_statement(
    statement_df: pd.DataFrame, transactions_df: pd.DataFrame, withdrawal: bool = True
) -> pd.DataFrame:
    """
    Get an extended statement DataFrame by merging the statement DataFrame
    with the transactions DataFrame on matching dates and withdrawal/deposit amounts.

    Args:
        statement_df (pd.DataFrame): The bank statement DataFrame.
        transactions_df (pd.DataFrame): The transactions DataFrame.
    """
    if withdrawal:
        statement_col = HDFC_WITHDRAWAL_COL
    else:
        statement_col = HDFC_DEPOSITED_COL

    extended_statement_df = pd.merge(
        statement_df,
        transactions_df,
        left_on=["Date_Formated", statement_col],
        right_on=["Date_Formated", "Amount"],
        how="inner",
        suffixes=("_stmt", "_txn"),
    )
    return extended_statement_df


def build_summary_df(statement_df: pd.DataFrame) -> pd.DataFrame:
    """
    Build a summary DataFrame from the statement DataFrame.

    Args:
        statement_df (pd.DataFrame): The bank statement DataFrame.
    Returns:
        pd.DataFrame: The summary DataFrame.
    """
    withdrawal_df = statement_df[HDFC_WITHDRAWAL_COL].dropna()
    deposit_df = statement_df[HDFC_DEPOSITED_COL].dropna()
    withdrawal_summary_df = withdrawal_df.agg(["sum", "mean", "max"])
    withdrawal_summary_df.columns = [
        f"Withdrawal_{col}" for col in withdrawal_summary_df.columns
    ]
    deposit_summary_df = deposit_df.agg(["sum", "mean", "max"])
    deposit_summary_df.columns = [
        f"Deposit_{col}" for col in deposit_summary_df.columns
    ]

    common_summary_df = statement_df.agg(
        {
            "Closing Balance": ["min", "max"],
            "Date": ["min", "max"],
        }
    )
    extended_summary_df = pd.concat(
        [withdrawal_summary_df, deposit_summary_df, common_summary_df], axis=1
    )
    return extended_summary_df
