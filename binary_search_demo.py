import csv
from typing import List


def binary_search(numbers: List[int], target: int) -> int:
    """Return the index of target in numbers or -1 if not found."""
    left = 0
    right = len(numbers) - 1

    while left <= right:
        mid = (left + right) // 2
        guess = numbers[mid]

        if guess == target:
            return mid
        if guess < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


def main() -> None:
    sorted_numbers = list(range(0, 101, 5))
    targets = [0, 35, 55, 100, 42]
    results = []

    for target in targets:
        index = binary_search(sorted_numbers, target)
        results.append(
            {
                "target": target,
                "found": index != -1,
                "index": index,
                "value": sorted_numbers[index] if index != -1 else None,
            }
        )

    csv_path = "binary_search_results.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["target", "found", "index", "value"])
        writer.writeheader()
        writer.writerows(results)

    print(f"Results saved to {csv_path}")


if __name__ == "__main__":
    main()
