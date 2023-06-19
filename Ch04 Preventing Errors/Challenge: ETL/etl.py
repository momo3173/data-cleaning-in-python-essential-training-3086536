"""
Load traffic.csv into "traffic" table in sqlite3 database.

Drop and report invalid rows.
- ip should be valid IP (see ipaddress)
- time must not be in the future
- path can't be empty
- status code must be a valid HTTP status code (see http.HTTPStatus)
- size can't be negative or empty

Report the percentage of bad rows. Fail the ETL if there are more than 5% bad rows
"""
# %%
import sqlite3

from contextlib import closing
from http import HTTPStatus
from ipaddress import ip_address

import pandas as pd

# %%
def validity_check(row):
    # ip must be a valid IP
    try:
        ip_address(row["ip"])
    except ValueError:
        return False

    # time must not be in the future
    today = pd.Timestamp.now()
    if row["time"] > today:
        return False

    # path must not be empty
    if pd.isnull(row["path"]) or not row["path"].strip():
        return False

    # status code must be a valid HTTP status code
    status_code = set(HTTPStatus)
    if row["status"] not in status_code:
        return False

    # size must not be negative or empty
    if (row["size"] < 0) or pd.isnull(row["size"]):
        return False

    return True

# %%
def traffic_ETL(in_file, out_file):
    df = pd.read_csv(in_file, parse_dates=["time"])

    bad_rows = df[~df.apply(validity_check, axis=1)]

    max_bad_rows_percent = 5

    if len(bad_rows) > 0:
        percent_bad = len(bad_rows)/len(df) * 100
        print(f"{len(bad_rows)} ({percent_bad:.2f}%) bad rows")
        if percent_bad >= max_bad_rows_percent:
            raise ValueError(
                "There are too many bad rows ({percent_bad: .2f} %)")

    df = df[~df.index.isin(bad_rows.index)]
    with closing(sqlite3.connect(out_file)) as conn:
        conn.execute("BEGIN")
        with conn:
            df.to_sql("traffic", conn, if_exists="append", index=False)

# %%
traffic_ETL("traffic.csv", "traffic.db")