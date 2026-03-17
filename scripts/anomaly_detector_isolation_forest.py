from pathlib import Path

import plotly.express as px

from statement_analyser.analyzer import find_anomalous_transactions
from statement_analyser.constants import HDFC_WITHDRAWAL_COL
from statement_analyser.pipeline import (
    etl_hdfc_bank_statement_df,
    etl_phonepe_statement_df,
)
from statement_analyser.processor import filter_deposit_withdrawal

curr_dir = Path(__file__).parent
target_dir = curr_dir / ".." / "data"
phonepe_statement_file_path = (
    target_dir / "PhonePe_Statement_Jan2025_Jan2026 (1).pdf"
)
statement_file_path = target_dir / "y25-v2.xls"


pdf_file = phonepe_statement_file_path
isolated_col = HDFC_WITHDRAWAL_COL
statement_df = etl_hdfc_bank_statement_df(statement_file_path)
tdf = etl_phonepe_statement_df(pdf_file)


# ---- pulls photo of anomalous dates


(
    withdrawal_statements_df,
    withdrawal_transactions_df,
    deposit_statements_df,
    deposit_transactions_df,
) = filter_deposit_withdrawal(statement_df, tdf)

contamination = 0.05
withdrawal_statements_df = withdrawal_statements_df[
    withdrawal_statements_df["Date_Formated"].str.contains("Sep")
]
withdrawal_statements_df  # done till Jul


enriched_df_to_process = find_anomalous_transactions(
    withdrawal_statements_df, isolated_col, contamination
)


anomalies_df = enriched_df_to_process[enriched_df_to_process["Anomaly"] == -1]
anomalies_df.head()


anomalies_df.sample(5)


len(anomalies_df)


anomalies_df.columns

# Index(['UPI_Name_Labelled_anomaly', 'Withdrawal Amt._anomaly', 'Anomaly',
#        'Key', 'Date', 'Narration', 'Chq./Ref.No.', 'Value Dt',
#        'Withdrawal Amt._original', 'Deposit Amt.', 'Closing Balance',
#        'Date_Formated', 'UPIs', 'UPI_Name', 'UPI_Bank', 'UPI_Description',
#        'ToLabel', 'UPI_Name_Labelled_original'],
#       dtype='object')


# ---- use plotly to plot interesting visualization for this anomalies_df


# Create a bar chart showing the count of anomalies by date
anomalies_count_by_date = (
    anomalies_df.groupby("Date").size().reset_index(name="Count")
)
fig_bar = px.bar(
    anomalies_count_by_date,
    x="Date",
    y="Count",
    title="Count of Anomalies by Date",
    labels={"Count": "Number of Anomalies"},
)
fig_bar.show()

# Create a scatter plot of withdrawal amounts with anomalies highlighted
fig_scatter = px.scatter(
    anomalies_df,
    x="Date",
    y="Withdrawal Amt._original",
    color="Anomaly",
    title="Scatter Plot of Withdrawal Amounts with Anomalies Highlighted",
    labels={
        "Withdrawal Amt._original": "Withdrawal Amount",
        "Anomaly": "Anomaly Status",
    },
    hover_data=["Narration", "UPI_Bank"],
)
fig_scatter.show()

# Create a pie chart showing the distribution of anomalies by UPI Bank
anomalies_by_bank = anomalies_df["UPI_Name"].value_counts().reset_index()
anomalies_by_bank.columns = ["UPI_Name", "Count"]
fig_pie = px.pie(
    anomalies_by_bank,
    names="UPI_Name",
    values="Count",
    title="Distribution of Anomalies by UPI_Name",
)
fig_pie.show()
