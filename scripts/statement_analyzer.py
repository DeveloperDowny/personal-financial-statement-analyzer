from pathlib import Path

import plotly.express as px

from statement_analyser.constants import HDFC_WITHDRAWAL_COL
from statement_analyser.helper import filter_by_time
from statement_analyser.pipeline import (
    etl_hdfc_bank_statement_df,
    etl_phonepe_statement_df,
)
from statement_analyser.processor import (
    filter_deposit_withdrawal,
    get_extended_statement,
)

curr_dir = Path(__file__).parent
target_dir = curr_dir / ".." / "data"
phonepe_statement_file_path = target_dir / "PhonePe_Statement_Jan2025_Jan2026 (1).pdf"
statement_file_path = target_dir / "y25-v2.xls"

statement_df = etl_hdfc_bank_statement_df(statement_file_path)
transactions_df = etl_phonepe_statement_df(phonepe_statement_file_path)

(
    withdrawal_statements_df,
    withdrawal_transactions_df,
    deposit_statements_df,
    deposit_transactions_df,
) = filter_deposit_withdrawal(statement_df, transactions_df)
extended_withdrawal_df = get_extended_statement(
    withdrawal_statements_df, withdrawal_transactions_df
)
morning_transactions_df = filter_by_time(
    extended_withdrawal_df, start_time_str="07:00 AM", end_time_str="10:00 AM"
)
morning_transactions_df = morning_transactions_df[
    morning_transactions_df["Date_Formated"].str.contains("Oct")
]


morning_transactions_df.head()


# fig = px.scatter(morning_transactions_df, x='Date_Formated', y=WITHDRAWAL_COL, title='Morning Withdrawals by UPI Name')
fig = px.scatter(
    morning_transactions_df,
    x="Date_Formated",
    y=HDFC_WITHDRAWAL_COL,
    hover_data=["Time", "UPI_Name"],
    title="Morning Withdrawals by UPI Name",
)
fig.show()
