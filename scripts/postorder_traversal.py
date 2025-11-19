from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional


data_dir = Path(__file__).resolve().parent.parent / "data"
data_dir.mkdir(parents=True, exist_ok=True)


@dataclass
class TreeNode:
    val: int
    left: Optional["TreeNode"] = None
    right: Optional["TreeNode"] = None


def postorder_traversal_recursive(root: Optional[TreeNode]) -> List[int]:
    result: List[int] = []

    def helper(node: Optional[TreeNode]) -> None:
        if node is None:
            return
        helper(node.left)
        helper(node.right)
        result.append(node.val)

    helper(root)
    return result


def postorder_traversal_iterative(root: Optional[TreeNode]) -> List[int]:
    if root is None:
        return []

    stack: List[TreeNode] = [root]
    result: List[int] = []

    while stack:
        node = stack.pop()
        result.append(node.val)
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)

    return result[::-1]


def build_sample_tree() -> TreeNode:
    return TreeNode(
        1,
        left=TreeNode(2, TreeNode(4), TreeNode(5)),
        right=TreeNode(3, TreeNode(6), TreeNode(7)),
    )


def main() -> None:
    tree = build_sample_tree()
    recursive_result = postorder_traversal_recursive(tree)
    iterative_result = postorder_traversal_iterative(tree)

    payload = {
        "recursive": recursive_result,
        "iterative": iterative_result,
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "tree_description": "Perfect binary tree with values 1-7"
    }

    json_path = data_dir / "postorder_result.json"
    txt_path = data_dir / "postorder_result.txt"

    json_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    lines = [
        f"recursive: {recursive_result}",
        f"iterative: {iterative_result}",
    ]
    txt_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("Postorder traversal (recursive):", recursive_result)
    print("Postorder traversal (iterative):", iterative_result)
    print(f"Results saved to {json_path.relative_to(Path.cwd())} and {txt_path.relative_to(Path.cwd())}")


if __name__ == "__main__":
    main()
