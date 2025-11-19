from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


@dataclass
class Node:
    val: int
    left: Optional["Node"] = None
    right: Optional["Node"] = None


def build_example_tree() -> Node:
    """Builds the fixed binary tree used in this example."""
    node4 = Node(4)
    node5 = Node(5)
    node6 = Node(6)
    node7 = Node(7)

    node2 = Node(2, left=node4, right=node5)
    node3 = Node(3, left=node6, right=node7)

    return Node(1, left=node2, right=node3)


def preorder_traversal(root: Optional[Node]) -> List[int]:
    """Return the preorder traversal of the provided tree."""
    if root is None:
        return []

    values = [root.val]
    values.extend(preorder_traversal(root.left))
    values.extend(preorder_traversal(root.right))
    return values


def save_preorder_result(values: List[int], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(",".join(str(v) for v in values), encoding="utf-8")


def main() -> None:
    tree = build_example_tree()
    result = preorder_traversal(tree)
    output_path = Path("data") / "preorder_result.txt"
    save_preorder_result(result, output_path)
    print("Saved preorder result to data/preorder_result.txt")


if __name__ == "__main__":
    main()
