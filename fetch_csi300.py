"""
获取沪深300近一年行情并绘制折线图。
"""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import font_manager
import pandas as pd
import yfinance as yf


TICKER = "000300.SS"  # Yahoo Finance 中的沪深300指数代码


def fetch_csi300_data(start: datetime, end: datetime) -> pd.DataFrame:
    """
    从 Yahoo Finance 拉取沪深300指数在 [start, end) 区间的行情数据。
    """
    data = yf.download(
        TICKER,
        start=start.strftime("%Y-%m-%d"),
        end=end.strftime("%Y-%m-%d"),
        auto_adjust=False,
        progress=False,
    )

    if data.empty:
        raise RuntimeError("无法获取到行情数据，请稍后重试或检查网络。")

    data.index = pd.to_datetime(data.index)
    data = data.sort_index()
    data.index.name = "Date"

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = [col[0] for col in data.columns]

    desired_order = ["Open", "High", "Low", "Close", "Adj Close", "Volume"]
    data = data[[col for col in desired_order if col in data.columns]]

    return data


def ensure_chinese_font() -> bool:
    """
    尝试启用常见中文字体，返回是否成功。
    """
    preferred_fonts = [
        "SimHei",
        "Microsoft YaHei",
        "WenQuanYi Micro Hei",
        "Noto Sans CJK SC",
        "Source Han Sans SC",
    ]

    for font in preferred_fonts:
        try:
            font_manager.findfont(font, fallback_to_default=False)
        except ValueError:
            continue

        plt.rcParams["font.sans-serif"] = [font]
        plt.rcParams["axes.unicode_minus"] = False
        return True

    return False


def plot_close_curve(data: pd.DataFrame, output_path: Path) -> None:
    """
    绘制收盘价折线图并保存。
    """
    has_chinese_font = ensure_chinese_font()
    title = "沪深300指数近一年收盘价" if has_chinese_font else "CSI 300 Index Close (Last Year)"
    xlabel = "日期" if has_chinese_font else "Date"
    ylabel = "收盘价 (CNY)" if has_chinese_font else "Close Price (CNY)"

    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data["Close"], color="#1f77b4", linewidth=1.5)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True, linestyle="--", alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


def run(days: int, output_dir: Path) -> tuple[Path, Path]:
    """
    执行完整流程，返回数据与图片路径。
    """
    end = datetime.now(timezone.utc) + timedelta(days=1)
    start = end - timedelta(days=days)

    df = fetch_csi300_data(start, end)

    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "csi300_last_year.csv"
    img_path = output_dir / "csi300_last_year.png"

    df.to_csv(csv_path, encoding="utf-8", index_label="Date")
    plot_close_curve(df, img_path)

    return csv_path, img_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="获取沪深300近一年行情并绘图")
    parser.add_argument(
        "--days",
        type=int,
        default=365,
        help="回溯的自然日天数，默认365天",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs"),
        help="保存数据与图片的目录，默认 outputs",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    csv_path, img_path = run(args.days, args.output_dir)
    print(f"数据已保存至: {csv_path}")
    print(f"折线图已保存至: {img_path}")


if __name__ == "__main__":
    main()
