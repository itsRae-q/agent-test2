#!/usr/bin/env python3
"""
简单的百度热搜热点新闻爬取脚本。

运行示例：
    python hot_news.py --output data/hot_news.md
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any, Dict, List
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

API_URL = "https://top.baidu.com/api/board?tab=realtime"
USER_AGENT = (
    "Mozilla/5.0 (compatible; HotNewsBot/1.0; +https://github.com/openai/cursor)"
)


def fetch_hot_news(timeout: int = 10) -> List[Dict[str, Any]]:
    """从百度热搜榜抓取热点新闻数据。"""
    request = Request(API_URL, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=timeout) as response:  # nosec B310
        payload = response.read()
    data = json.loads(payload.decode("utf-8"))

    cards = data.get("data", {}).get("cards", [])
    hot_list = None
    for card in cards:
        if card.get("component") == "hotList":
            hot_list = card.get("content", [])
            break
    if hot_list is None:
        raise RuntimeError("未能在响应中找到热搜数据")

    cleaned: List[Dict[str, Any]] = []
    for idx, item in enumerate(hot_list, start=1):
        cleaned.append(
            {
                "rank": item.get("index", idx),
                "title": (item.get("word") or "").strip(),
                "summary": (item.get("desc") or "").strip(),
                "hot_score": int(item.get("hotScore") or 0),
                "detail_url": item.get("url")
                or item.get("rawUrl")
                or item.get("appUrl")
                or "",
                "image_url": item.get("img") or "",
            }
        )
    return cleaned


def format_markdown(news: List[Dict[str, Any]], timestamp: dt.datetime) -> str:
    """将新闻列表渲染为 Markdown 文本。"""
    header = [
        "# 今日百度热搜热点",
        f"- 数据来源：{API_URL}",
        f"- 抓取时间：{timestamp:%Y-%m-%d %H:%M:%S}",
        "",
    ]
    body: List[str] = []
    for item in news:
        title = item["title"] or "（未提供标题）"
        url = item["detail_url"] or "#"
        summary = item["summary"] or "暂无摘要"
        body.extend(
            [
                f"{item['rank']}. [{title}]({url})",
                f"   - 热度值：{item['hot_score']}",
                f"   - 摘要：{summary}",
                "",
            ]
        )
    return "\n".join(header + body).rstrip() + "\n"


def save_output(
    news: List[Dict[str, Any]],
    output_path: Path,
    fmt: str,
    timestamp: dt.datetime,
) -> None:
    """以指定格式保存抓取结果。"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if fmt == "json":
        payload = {
            "source": API_URL,
            "fetched_at": timestamp.isoformat(timespec="seconds"),
            "items": news,
        }
        output_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    else:
        output_path.write_text(
            format_markdown(news, timestamp), encoding="utf-8"
        )


def parse_args() -> argparse.Namespace:
    today_str = dt.datetime.now().strftime("%Y%m%d")
    parser = argparse.ArgumentParser(description="抓取百度热搜热点新闻。")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(f"hot_news_{today_str}.md"),
        help="输出文件路径，默认为当前目录下以日期结尾的 Markdown 文件。",
    )
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="输出格式，可选 markdown 或 json，默认 markdown。",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="请求超时时间（秒），默认 10 秒。",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    timestamp = dt.datetime.now()
    try:
        news = fetch_hot_news(timeout=args.timeout)
    except (URLError, HTTPError, RuntimeError, json.JSONDecodeError) as exc:
        raise SystemExit(f"抓取失败：{exc}")

    fmt = args.format
    if fmt == "json":
        output_path = args.output if args.output.suffix else args.output.with_suffix(".json")
    else:
        output_path = args.output if args.output.suffix else args.output.with_suffix(".md")

    save_output(news, output_path, fmt, timestamp)
    print(f"已抓取 {len(news)} 条热点新闻，保存至 {output_path.resolve()}")


if __name__ == "__main__":
    main()
