import datetime as dt

import yfinance as yf


def main() -> None:
    symbol = "000300.SS"
    end = dt.date.today()
    start = end - dt.timedelta(days=365)

    data = yf.download(symbol, start=start, end=end + dt.timedelta(days=1))
    output = "hs300_last_year.csv"
    data.to_csv(output, index_label="Date")

    print(f"下载区间: {start} ~ {end}")
    print(f"共获取 {len(data)} 条记录，已保存到 {output}")


if __name__ == "__main__":
    main()
