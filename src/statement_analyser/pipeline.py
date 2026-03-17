from typing import List
import pandas as pd

from statement_analyser.processor import (
    process_upi_narration,
    set_column_types,
    transform_paytm_transactions_df,
    transform_statement_df,
    transform_transactions_df,
)
from statement_analyser.loader import (
    load_hdfc_bank_statement,
    load_paytm_statement_df,
    load_phonepe_statement_df,
)


def etl_hdfc_bank_statement_df(statement_file_path: str) -> pd.DataFrame:
    """
    ETL process the bank statement DataFrame.

    Args:
        statement_file_path (str): The path to the Excel file.
    Returns:
        pd.DataFrame: The processed bank statement DataFrame.
    """
    statement_df = load_hdfc_bank_statement(statement_file_path)
    statement_df = set_column_types(statement_df)
    statement_df = transform_statement_df(statement_df)
    statement_df = process_upi_narration(statement_df)
    return statement_df


def etl_phonepe_statement_df(pdf_file: str) -> List[dict]:
    """
    Extract UPI transactions from a PhonePe statement PDF file.

    Args:
        pdf_file (str): The path to the PhonePe statement PDF file.
    Returns:
        pd.DataFrame: A DataFrame containing the extracted UPI transactions.
    """
    transactions_df = load_phonepe_statement_df(pdf_file)
    transactions_df = transform_transactions_df(transactions_df)
    return transactions_df


def etl_paytm_statement_df(excel_file: str) -> List[dict]:
    """
    Extract UPI transactions from a Paytm statement Excel file.

    Args:
        excel_file (str): The path to the Paytm statement Excel file.
    Returns:
        pd.DataFrame: A DataFrame containing the extracted UPI transactions.
    """
    transactions_df = load_paytm_statement_df(excel_file)
    transactions_df = transform_paytm_transactions_df(transactions_df)
    return transactions_df