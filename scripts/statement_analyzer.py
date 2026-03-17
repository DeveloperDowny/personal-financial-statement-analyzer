from pathlib import Path

import plotly.express as px

from statement_analyser.constants import HDFC_WITHDRAWAL_COL
from statement_analyser.helper import filter_by_time
from statement_analyser.pipeline import (
    etl_hdfc_bank_statement_df,
    # etl_phonepe_statement_df,
    etl_paytm_statement_df,
)
from statement_analyser.processor import (
    # filter_deposit_withdrawal,
    filter_deposit_withdrawal_paytm,
    get_extended_statement,
)

curr_dir = Path(__file__).parent
target_dir = curr_dir / ".." / "data"
upi_transactions_file_path = target_dir / "paytm.xlsx"
statement_file_path = target_dir / "hdfc.xls"

statement_df = etl_hdfc_bank_statement_df(statement_file_path)
# transactions_df = etl_phonepe_statement_df(phonepe_statement_file_path)
transactions_df = etl_paytm_statement_df(upi_transactions_file_path)

(
    withdrawal_statements_df,
    withdrawal_transactions_df,
    deposit_statements_df,
    deposit_transactions_df,
) = filter_deposit_withdrawal_paytm(statement_df, transactions_df)
# ) = filter_deposit_withdrawal(statement_df, transactions_df)
extended_withdrawal_df = get_extended_statement(
    withdrawal_statements_df, withdrawal_transactions_df
)
morning_transactions_df = filter_by_time(
    extended_withdrawal_df, start_time_str="07:00 AM", end_time_str="11:00 AM"
)
morning_transactions_df = morning_transactions_df[
    morning_transactions_df["Date_Formated"].str.contains("Feb")
]


morning_transactions_df.head()

max_withdrawal_rows = morning_transactions_df.groupby("Date_Formated")[
    HDFC_WITHDRAWAL_COL
].idxmax()
day_wise_max = morning_transactions_df.loc[max_withdrawal_rows]


day_wise_max = day_wise_max[
    ["Date_Formated", HDFC_WITHDRAWAL_COL, "Time_Parsed", "UPI_Name"]
]
print(day_wise_max)

print(day_wise_max[HDFC_WITHDRAWAL_COL].sum() - 188)
# fig = px.scatter(
#     morning_transactions_df,
#     x='Date_Formated',
#     y=WITHDRAWAL_COL,
#     title='Morning Withdrawals by UPI Name',
# )
fig = px.scatter(
    morning_transactions_df,
    x="Date_Formated",
    # y=HDFC_WITHDRAWAL_COL,
    y="Time_Parsed",
    hover_data=["Time", "UPI_Name", HDFC_WITHDRAWAL_COL],
    title="Morning Withdrawals by UPI Name",
)
fig.show()
