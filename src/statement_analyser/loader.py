from typing import List
import pandas as pd

from statement_analyser.extractor import extract_text_from_pdf, parse_phonepe_statement


def load_hdfc_bank_statement(statement_file_path: str) -> pd.DataFrame:
    """
    Load the bank statement from an Excel file.

    Args:
        statement_file_path (str): The path to the Excel file.
    Returns:
        pd.DataFrame: The loaded bank statement DataFrame.
    """
    statement_df = pd.read_excel(statement_file_path, skiprows=20, skipfooter=18)
    statement_df.drop(index=0, inplace=True)
    print(statement_df.head())
    print(statement_df.tail())
    return statement_df


def load_phonepe_statement_df(pdf_file: str) -> List[dict]:
    """
    Extract UPI transactions from a PhonePe statement PDF file.

    Args:
        pdf_file (str): The path to the PhonePe statement PDF file.
    Returns:
        pd.DataFrame: A DataFrame containing the extracted UPI transactions.
    """
    text = extract_text_from_pdf(pdf_file)
    transactions = parse_phonepe_statement(text)
    transactions_df = pd.DataFrame(transactions)

    return transactions_df
