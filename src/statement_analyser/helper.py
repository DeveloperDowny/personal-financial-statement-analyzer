import pandas as pd
from datetime import datetime
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder


def parse_time(time_str) -> datetime.time:
    """
    Function to parse time strings in "HH:MM AM/PM" format.

    Args:
        time_str (str): The time string to parse.
    Returns:
        datetime.time: The parsed time object.
    """
    return datetime.strptime(time_str, "%I:%M %p").time()


def parse_time_24(time_str) -> datetime.time:
    """
    Function to parse time strings in "HH:MM:SS" format.

    Args:
        time_str (str): The time string to parse.
    Returns:
        datetime.time: The parsed time object.
    """
    return datetime.strptime(time_str, "%H:%M:%S").time()


def format_date(date_str):
    try:
        formatted_date = pd.to_datetime(date_str).strftime("%d-%b-%Y")
        return formatted_date
    except Exception:
        return date_str


def filter_by_time(
    df: pd.DataFrame,
    start_time_str: str = "09:00 AM",
    end_time_str: str = "11:00 AM",
    inplace: bool = False,
) -> pd.DataFrame:
    """
    Filter the DataFrame to include only rows where the 'Time_Parsed' column
    falls within the specified time range.

    Args:
        df (pd.DataFrame): The input DataFrame containing a 'Time_Parsed' column.
        start_time_str (str): The start time in "HH:MM AM/PM" format.
        end_time_str (str): The end time in "HH:MM AM/PM" format.
        inplace (bool): If True, modify the DataFrame in place. Default is False.
    Returns:
        pd.DataFrame: The filtered DataFrame.
    """
    if not inplace:
        df = df.copy()

    start_time = datetime.strptime(start_time_str, "%I:%M %p")
    end_time = datetime.strptime(end_time_str, "%I:%M %p")

    df = df[(df["Time_Parsed"] >= start_time.time()) & (df["Time_Parsed"] <= end_time.time())]
    return df


def encode_column(df: pd.DataFrame, column_name: str, new_column_name: str) -> pd.DataFrame:
    le = LabelEncoder()
    labelled_df = df.copy()
    labelled_df[new_column_name] = le.fit_transform(labelled_df[column_name])
    return labelled_df


def prepare_data_for_isolation_forest(df: pd.DataFrame, isolated_col: str) -> pd.DataFrame:
    df_to_process = df[["UPI_Name_Labelled", isolated_col]]
    return df_to_process


def find_anomaly(
    df_to_process: pd.DataFrame, isolated_col: str, contamination: float = 0.01
) -> pd.DataFrame:
    df_to_process = df_to_process.dropna(subset=[isolated_col])
    iso_forest = IsolationForest(contamination=contamination, random_state=42)
    df_to_process["Anomaly"] = iso_forest.fit_predict(df_to_process)
    return df_to_process


def enrich_anomaly_results(
    original_df: pd.DataFrame, anomaly_df: pd.DataFrame, isolated_col: str
) -> pd.DataFrame:
    def get_key(row):
        upi = str(int(row["UPI_Name_Labelled"]))
        amount = str(int(row[isolated_col]))
        return f"U{upi}_A{amount}"

    anomaly_df["Key"] = anomaly_df.apply(get_key, axis=1)
    original_df["Key"] = original_df.apply(get_key, axis=1)
    enriched_df = pd.merge(
        anomaly_df,
        original_df,
        on="Key",
        how="right",
        suffixes=("_anomaly", "_original"),
    )
    return enriched_df
