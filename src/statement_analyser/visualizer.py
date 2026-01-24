import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


def plot_amounts(df: pd.DataFrame, title: str, xlabel: str, ylabel: str):
    # ---- Plot day wise max deposit and withdrawal using pandas

    # df.plot(kind="bar", figsize=(12, 6))
    # ---- bigger size
    df.plot(kind="bar", figsize=(14, 7))

    # ---- show x ticks at intervals
    plt.xticks(ticks=range(0, len(df.index), 5))
    plt.xticks(rotation=45)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid()
    plt.show()
    # ---- tilt x labels


def plot_amounts_plotly(df: pd.DataFrame, title: str, xlabel: str, ylabel: str):

    fig = px.bar(
        df,
        # x=df.index,
        y=["Withdrawal Amt.", "Deposit Amt."],
        title=title,
        labels={"x": xlabel, "value": ylabel, "variable": "Transaction Type"},
    )
    fig.show()
