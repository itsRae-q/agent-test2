"""
获取沪深300近一年行情并绘制折线图
"""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta
from pathlib import Path

import akshare as ak
import matplotlib.pyplot as plt
import pandas as pd


def fetch_csi300_history(start_date: str, end_date: str) -> pd.DataFrame:
    """
    从 akshare 获取沪深300在指定区间的每日行情
    """
    try:
        data = ak.index_zh_a_hist(
            symbol="000300",
            period="daily",
            start_date=start_date,
            end_date=end_date,
        )
    except Exception as err:  # pragma: no cover - 网络波动可能导致请求失败
        raise RuntimeError(f"调用 akshare 获取沪深300数据失败: {err}") from err

    if data.empty:
        raise ValueError("未获取到任何沪深300行情数据，请检查时间区间或网络连接。")

    data = data.copy()
    data["日期"] = pd.to_datetime(data["日期"], format="%Y-%m-%d")
    data.sort_values("日期", inplace=True)
    data.set_index("日期", inplace=True)
    return data


def plot_csi300(data: pd.DataFrame, output_path: Path) -> None:
    """
    绘制沪深300收盘价折线图并保存
    """
    plt.figure(figsize=(10, 5))
    plt.plot(data.index, data["收盘"], label="沪深300收盘价", color="#0052D9")
    plt.title("沪深300近一年行情走势")
    plt.xlabel("日期")
    plt.ylabel("指数点位")
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.legend()
    plt.tight_layout()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150)
    plt.close()


def main(days: int, output: Path) -> Path:
    end_date = datetime.today().date()
    start_date = end_date - timedelta(days=days)
    start_str = start_date.strftime("%Y%m%d")
    end_str = end_date.strftime("%Y%m%d")

    data = fetch_csi300_history(start_str, end_str)
    last_year_data = data.loc[start_date:end_date]
    plot_csi300(last_year_data, output)

    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="获取沪深300近一年行情并输出折线图")
    parser.add_argument(
        "--days",
        type=int,
        default=365,
        help="回溯的自然日天数，默认365天",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("output/csi300_last_year.png"),
        help="折线图输出路径，默认 output/csi300_last_year.png",
    )

    args = parser.parse_args()
    output_path = main(args.days, args.output)
    print(f"折线图已保存至: {output_path}")
