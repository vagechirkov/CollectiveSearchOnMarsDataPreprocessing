from typing import List

import pandas as pd


def merge_traces_dataframes(dfs: List[pd.DataFrame], resource: pd.DataFrame) -> pd.DataFrame:
    """Merges traces dataframes into one."""

    # resource data
    resource['time'] = round(resource["timestamp"] / 1000, 1)
    resource.columns = [f"{col}_resource" for col in resource.columns if col != "time"]

    for i, df in enumerate(dfs):
        # round to the nearest 100ms
        df['time'] = round(df["timestamp"] / 1000, 1)

        # add index `i` to all columns
        df.columns = [f"{col}_{i}" for col in df.columns if col != "time"]

    # merge all dataframes
    df_all = resource
    for df in dfs:
        # tolerance=pd.Timedelta("2D")
        df_all = pd.merge_asof(df_all, df, on="time")

    return df_all
