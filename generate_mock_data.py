import csv
import random
from typing import List, Dict


FIRST_NAMES = [
    "Alice",
    "Bob",
    "Carol",
    "David",
    "Eve",
    "Frank",
    "Grace",
    "Heidi",
    "Ivan",
    "Judy",
]

LAST_NAMES = [
    "Anderson",
    "Brown",
    "Clark",
    "Davis",
    "Edwards",
    "Foster",
    "Garcia",
    "Harris",
    "Ivanov",
    "Johnson",
]

EMAIL_DOMAINS = ["example.com", "testmail.com", "mockdata.org"]


def _build_email(name: str) -> str:
    username = name.lower().replace(" ", ".")
    suffix = random.randint(10, 99)
    domain = random.choice(EMAIL_DOMAINS)
    return f"{username}{suffix}@{domain}"


def generate_mock_data(rows: int = 10) -> List[Dict[str, str]]:
    records = []
    for identifier in range(1, rows + 1):
        name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        age = random.randint(18, 70)
        email = _build_email(name)
        records.append(
            {
                "id": identifier,
                "name": name,
                "age": age,
                "email": email,
            }
        )
    return records


def write_csv(records: List[Dict[str, str]], filename: str = "mock_data.csv") -> None:
    fieldnames = ["id", "name", "age", "email"]
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)


def main() -> None:
    data = generate_mock_data(rows=10)
    write_csv(data)
    print("mock_data.csv 已生成，包含 10 行测试数据。")


if __name__ == "__main__":
    main()
