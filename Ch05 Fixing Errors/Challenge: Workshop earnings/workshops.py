# %%
import pandas as pd

df = pd.read_csv('workshops.csv')
df

# %%
"""
Fix the data frame. At the end, row should have the following columns:
- start: pd.Timestemap
- end: pd.Timestamp
- name: str
- topic: str (python or go)
- earnings: np.float64
"""
def fix_col(col):
    """Fix column name
    >>> fix_col('Year')
    'year'
    """
    return (
        col.lower()
    )

df.rename(columns=fix_col, inplace=True)
df

# %%
df["year"].fillna(method="ffill", inplace=True)
df["month"].fillna(method="ffill", inplace=True)
df

# %%
df = df[pd.notnull(df["earnings"])].copy()
df

# %%
def convert_to_date(row, col):
    year = int(row["year"])
    month = row["month"]
    day = int(row[col])
    ts = f'{month} {day}, {year}'
    return pd.to_datetime(ts, format="%B %d, %Y")

df["start"] = df.apply(convert_to_date, axis=1, args=('start',))
df["end"] = df.apply(convert_to_date, axis=1, args=("end",))
df

# %%
def topic(name):
    if "go" in name:
        return "go"
    if "python" in name:
        return "python"

df["topic"] = df["name"].str.lower().apply(topic)
df

# %%
import numpy as np
df["earnings"] = pd.to_numeric(
    df["earnings"].str.replace(r"[$,]", '')
).astype(np.float64)
df

# %%
df = df[["start", "end", "name", "topic", "earnings"]]
df