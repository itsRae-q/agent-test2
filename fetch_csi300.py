#!/usr/bin/env python3
"""
Fetch the most recent year of CSI 300 (沪深300) daily data and save to CSV.
"""

from __future__ import annotations

import datetime as dt
from pathlib import Path
from typing import List

import pandas as pd
import requests


API_URL = "https://push2his.eastmoney.com/api/qt/stock/kline/get"
SECID = "1.000300"  # 1 = Shanghai, 000300 = CSI 300 Index
KLT = 101  # Daily data granularity
FQT = 1  # Forward-adjusted prices
ROWS_LIMIT = 450  # Fetch a little more than a year to ensure coverage
OUTPUT_PATH = Path("csi300_last_year.csv")

COLUMN_NAMES = [
    "date",
    "open",
    "close",
    "high",
    "low",
    "volume",
    "amount",
    "amplitude_pct",
    "pct_change",
    "change",
    "turnover_pct",
]


def get_date_range() -> tuple[dt.date, dt.date]:
    today = dt.date.today()
    start = today - dt.timedelta(days=365)
    return start, today


def fetch_kline_rows(end_date: dt.date) -> List[str]:
    params = {
        "secid": SECID,
        "ut": "fa5fd1943c7b386f172d6893dbfba10b",
        "fields1": "f1,f2,f3,f4,f5,f6",
        "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
        "klt": KLT,
        "fqt": FQT,
        "end": end_date.strftime("%Y%m%d"),
        "lmt": ROWS_LIMIT,
    }
    response = requests.get(API_URL, params=params, timeout=15)
    response.raise_for_status()
    payload = response.json()
    klines = payload.get("data", {}).get("klines")
    if not klines:
        raise RuntimeError("No kline data returned by the API.")
    return klines


def parse_rows(klines: List[str], start_date: dt.date) -> pd.DataFrame:
    records = []
    for entry in klines:
        parts = entry.split(",")
        if len(parts) < len(COLUMN_NAMES):
            continue
        row_date = dt.datetime.strptime(parts[0], "%Y-%m-%d").date()
        if row_date < start_date:
            continue
        numeric_values = [float(x) for x in parts[1:6]]
        volume = float(parts[6])
        amount = float(parts[7])
        amplitude_pct = float(parts[8])
        pct_change = float(parts[9])
        change = float(parts[10])
        turnover_pct = float(parts[11]) if len(parts) > 11 else None
        records.append(
            {
                "date": row_date,
                "open": numeric_values[0],
                "close": numeric_values[1],
                "high": numeric_values[2],
                "low": numeric_values[3],
                "volume": volume,
                "amount": amount,
                "amplitude_pct": amplitude_pct,
                "pct_change": pct_change,
                "change": change,
                "turnover_pct": turnover_pct,
            }
        )

    if not records:
        raise RuntimeError("No records found within the last year.")

    df = pd.DataFrame(records)
    df.sort_values("date", inplace=True)
    df["date"] = df["date"].astype(str)
    return df.reset_index(drop=True)


def save_to_csv(df: pd.DataFrame, output_path: Path) -> None:
    df.to_csv(output_path, index=False)


def main() -> None:
    start_date, end_date = get_date_range()
    klines = fetch_kline_rows(end_date)
    df = parse_rows(klines, start_date)
    save_to_csv(df, OUTPUT_PATH)
    print(f"Saved {len(df)} rows to {OUTPUT_PATH.resolve()}")


if __name__ == "__main__":
    main()
