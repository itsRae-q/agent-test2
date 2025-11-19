from dataclasses import dataclass
from typing import Any, List, Optional


@dataclass
class TreeNode:
    """
    简单的二叉树节点定义
    """
    value: Any
    left: Optional["TreeNode"] = None
    right: Optional["TreeNode"] = None


def preorder_traversal(root: Optional[TreeNode]) -> List[Any]:
    """
    先序遍历（根 -> 左 -> 右）
    """
    result: List[Any] = []

    def _traverse(node: Optional[TreeNode]) -> None:
        if node is None:
            return
        result.append(node.value)
        _traverse(node.left)
        _traverse(node.right)

    _traverse(root)
    return result
