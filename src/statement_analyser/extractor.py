from typing import List, Optional
import fitz  # PyMuPDF
import re


def extract_upi_name(upi_string: str) -> Optional[str]:
    """
    Extract UPI name from the given UPI string based on its format.

    Args:
        upi_string (str): The UPI string to extract the name from.
    Returns:
        Optional[str]: The extracted UPI name or None if not found.
    """
    if upi_string.startswith("UPI-"):
        return upi_string.split("-")[1] if "-" in upi_string else None

    elif upi_string.startswith("POS"):
        parts = upi_string.split(" ")
        return parts[2] if len(parts) > 2 else None

    elif "RTGS" in upi_string or "NEFT" in upi_string:
        parts = upi_string.split("-")
        return parts[2] if len(parts) > 2 else None

    elif upi_string.startswith("CASH DEPOSIT BY"):
        parts = upi_string.split("-")
        return parts[1].strip() if len(parts) > 1 else None

    else:
        return None


def extract_upi_description(upi_string: str) -> Optional[str]:
    """
    Extract UPI description from the given UPI string based on its format.
    Args:
        upi_string (str): The UPI string to extract the description from.
    Returns:
        Optional[str]: The extracted UPI description or None if not found.
    """

    if upi_string.startswith("POS"):
        parts = upi_string.split(" ")
        return " ".join(parts[2:]) if len(parts) > 2 else None

    elif "RTGS" in upi_string or "NEFT" in upi_string:
        parts = upi_string.split("-")
        return parts[-2] if len(parts) > 2 else parts[-1]

    elif upi_string.startswith("CASH DEPOSIT BY"):
        parts = upi_string.split("-")
        return parts[-1].strip() if len(parts) > 2 else None

    else:
        return upi_string.split("-")[-1]


def parse_phonepe_statement(text: str) -> List[dict]:
    """
    Parse the text extracted from a PhonePe transaction statement PDF.

    Args:
        text (str): The text extracted from the PDF.
    Returns:
        List[dict]: A list of dictionaries, each representing a transaction.

    """

    transactions = []
    lines = text.splitlines()

    # Regex patterns to match relevant parts of the data
    date_pattern = re.compile(
        r"^[A-Za-z]+\s\d{1,2},\s\d{4}"
    )  # Matches dates like Sep 28, 2024
    amount_pattern = re.compile(r"₹[\d,]+(\.\d+)?")  # Matches amounts like ₹65
    debit_credit_pattern = re.compile(r"(DEBIT|CREDIT)")

    current_transaction = {}
    for line in lines:
        # Detect date to identify the start of a new transaction
        if date_pattern.match(line):
            if current_transaction:  # Save the previous transaction if it exists
                transactions.append(current_transaction)
                current_transaction = {}
            current_transaction["Date"] = line.strip()

        # Capture the time and transaction details
        elif re.match(r"\d{1,2}:\d{2}\s(am|pm)", line):
            current_transaction["Time"] = line.strip()

        # Capture the transaction details and type
        elif "Paid to" in line or "Received from" in line:
            current_transaction["Transaction Details"] = line.strip()

        elif debit_credit_pattern.search(line):
            current_transaction["Type"] = debit_credit_pattern.search(line).group()

        # Capture the amount
        elif amount_pattern.search(line):
            current_transaction["Amount"] = float(
                (amount_pattern.search(line).group()).replace("₹", "").replace(",", "")
            )

        # Capture the transaction ID
        elif "Transaction ID" in line:
            current_transaction["Transaction ID"] = line.split("Transaction ID")[
                -1
            ].strip()

        # Capture the UTR number
        elif "UTR No." in line:
            current_transaction["UTR No."] = line.split("UTR No.")[-1].strip()

        # Capture paid by details
        elif "Paid by" in line:
            current_transaction["Paid By"] = line.split("Paid by")[-1].strip()

    # Append the last transaction if it exists
    if current_transaction:
        transactions.append(current_transaction)

    return transactions


def extract_text_from_pdf(pdf_file: str) -> str:
    """
    Extract text from a PDF file using PyMuPDF.

    Args:
        pdf_file (str): The path to the PDF file.
    Returns:
        str: The extracted text from the PDF.
    """
    with fitz.open(pdf_file) as pdf:
        text = ""
        for page_num in range(len(pdf)):
            text += pdf.load_page(page_num).get_text()
    return text
