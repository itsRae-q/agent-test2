"""Simple binary search demo that also persists the dataset and result."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Sequence


def binary_search(data: Sequence[int], target: int) -> int:
    """Return the index of `target` in sorted `data`, or -1 if not present."""
    left = 0
    right = len(data) - 1

    while left <= right:
        mid = (left + right) // 2
        value = data[mid]

        if value == target:
            return mid
        if value < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


def main() -> None:
    """Run a small demo and write the inputs and result to disk."""
    sorted_numbers = [1, 3, 5, 7, 9, 11, 13]
    target_value = 7
    index = binary_search(sorted_numbers, target_value)

    output = {
        "sorted_numbers": sorted_numbers,
        "target_value": target_value,
        "index": index,
        "found": index != -1,
    }

    output_path = Path("binary_search_output.json")
    output_path.write_text(json.dumps(output, indent=2))

    print(f"结果已保存到 {output_path.resolve()}")


if __name__ == "__main__":
    main()
