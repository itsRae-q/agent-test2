"""
下载沪深300（CSI 300）近一年或指定区间的日度行情数据，并保存为 CSV 文件。
"""

from __future__ import annotations

import argparse
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Tuple

import akshare as ak
import pandas as pd

DEFAULT_OUTPUT = "data/csi300_last_year.csv"
INDEX_SYMBOL = "sh000300"

COLUMN_MAPPING = {
    "日期": "date",
    "开盘": "open",
    "收盘": "close",
    "最高": "high",
    "最低": "low",
    "成交量": "volume",
    "成交额": "turnover",
    "振幅": "amplitude",
    "涨跌幅": "pct_change",
    "涨跌额": "change",
    "换手率": "turnover_rate",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="查询沪深300近一年的行情数据并保存为 CSV 文件。"
    )
    parser.add_argument(
        "--days",
        type=int,
        default=365,
        help="向前回溯的天数（当未指定 --start 时生效，默认 365）",
    )
    parser.add_argument(
        "--start",
        type=str,
        help="开始日期（YYYY-MM-DD），若提供则优先于 --days",
    )
    parser.add_argument(
        "--end",
        type=str,
        help="结束日期（YYYY-MM-DD），默认为今天",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=DEFAULT_OUTPUT,
        help=f"输出 CSV 路径（默认 {DEFAULT_OUTPUT}）",
    )
    return parser.parse_args()


def resolve_period(args: argparse.Namespace) -> Tuple[date, date]:
    today = date.today()
    if args.end:
        end = datetime.strptime(args.end, "%Y-%m-%d").date()
    else:
        end = today

    if args.start:
        start = datetime.strptime(args.start, "%Y-%m-%d").date()
    else:
        start = end - timedelta(days=args.days)

    if start > end:
        raise ValueError("开始日期不能晚于结束日期。")

    return start, end


def fetch_csi300_history(start: date, end: date) -> pd.DataFrame:
    raw_df = ak.index_zh_a_hist(symbol=INDEX_SYMBOL, adjust="")
    if raw_df.empty:
        raise RuntimeError("未能从 akshare 获取沪深300数据。")

    raw_df["日期"] = pd.to_datetime(raw_df["日期"])
    mask = (raw_df["日期"] >= pd.Timestamp(start)) & (raw_df["日期"] <= pd.Timestamp(end))
    df = raw_df.loc[mask].copy()

    if df.empty:
        raise RuntimeError(f"在 {start} 至 {end} 区间内未查询到有效数据。")

    df.rename(columns=COLUMN_MAPPING, inplace=True)
    numeric_cols = [col for col in df.columns if col != "date"]
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")
    return df[["date"] + numeric_cols].sort_values("date")


def save_to_csv(df: pd.DataFrame, output_path: str) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8")
    return path


def main() -> None:
    args = parse_args()
    start, end = resolve_period(args)
    print(f"正在下载沪深300行情数据：{start} -> {end}")
    df = fetch_csi300_history(start, end)
    output_path = save_to_csv(df, args.output)
    print(f"下载完成，共 {len(df)} 行，已保存至 {output_path}")


if __name__ == "__main__":
    main()
