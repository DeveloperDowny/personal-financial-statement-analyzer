from statement_analyser.helper import (
    encode_column,
    enrich_anomaly_results,
    find_anomaly,
    prepare_data_for_isolation_forest,
)
import pandas as pd
from scipy.stats import zscore


def find_anomalous_transactions(
    statement_df: pd.DataFrame, isolated_col: str, contamination: float = 0.01
) -> pd.DataFrame:
    """Main workflow function to process financial statement data.
    Arguments:
        statement_file_path {str | Path} -- Path to the financial statement file.
    """
    # ---- update UPI_Name col to
    statement_df["ToLabel"] = statement_df.apply(
        lambda row: row["UPI_Name"] or row["Chq./Ref.No."], axis=1
    )
    statement_df = encode_column(statement_df, "ToLabel", "UPI_Name_Labelled")
    df_to_process = prepare_data_for_isolation_forest(statement_df, isolated_col)
    anomaly_df = find_anomaly(df_to_process, isolated_col, contamination)
    enriched_anomaly_df = enrich_anomaly_results(statement_df, anomaly_df, isolated_col)
    # enriched_anomaly_df = anomaly_df
    return enriched_anomaly_df


def find_anomalies_zscore(
    statement_df: pd.DataFrame, threshold: float = 3.0
) -> pd.DataFrame:
    """
    Get anomalies in the statement DataFrame using Z-Score method.

    Args:
        statement_df (pd.DataFrame): The bank statement DataFrame.
        threshold (float): The Z-Score threshold to identify anomalies.
    Returns:
        pd.DataFrame: The DataFrame with anomaly labels.
    """

    statement_df["Withdrawal Z-Score"] = zscore(
        statement_df["Withdrawal Amt."], nan_policy="omit"
    )
    statement_df["Deposit Z-Score"] = zscore(
        statement_df["Deposit Amt."], nan_policy="omit"
    )

    # ---- create a column Anomaly based on zscore threshold
    statement_df["Anomaly_ZScore"] = statement_df.apply(
        lambda row: (
            "Anomaly"
            if (
                abs(row["Withdrawal Z-Score"]) > threshold
                or abs(row["Deposit Z-Score"]) > threshold
            )
            else "Normal"
        ),
        axis=1,
    )
    return statement_df
