from collections import deque
from typing import Any, Iterable, List, Optional


class TreeNode:
    """简单的二叉树节点。"""

    def __init__(self, value: Any, left: Optional["TreeNode"] = None, right: Optional["TreeNode"] = None) -> None:
        self.value = value
        self.left = left
        self.right = right


class BinaryTree:
    """支持按层构建与广度优先遍历的二叉树。"""

    def __init__(self, values: Optional[Iterable[Any]] = None) -> None:
        self.root: Optional[TreeNode] = None
        if values:
            self.root = self._build_from_level_order(values)

    def _build_from_level_order(self, values: Iterable[Any]) -> Optional[TreeNode]:
        iterator = iter(values)
        try:
            first_value = next(iterator)
        except StopIteration:
            return None

        root = TreeNode(first_value)
        queue: deque[TreeNode] = deque([root])

        for value in iterator:
            parent = queue[0]
            new_node = TreeNode(value)
            if parent.left is None:
                parent.left = new_node
            elif parent.right is None:
                parent.right = new_node
                queue.popleft()
            queue.append(new_node)

        return root

    def bfs(self) -> List[Any]:
        """返回广度优先遍历结果。"""
        if self.root is None:
            return []

        result: List[Any] = []
        queue: deque[TreeNode] = deque([self.root])

        while queue:
            node = queue.popleft()
            result.append(node.value)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        return result


def main() -> None:
    """简单示例：构建二叉树并输出 BFS 结果。"""
    values = [1, 2, 3, 4, 5, 6, 7]
    tree = BinaryTree(values)
    traversal = tree.bfs()
    print("二叉树的 BFS 遍历结果:", traversal)


if __name__ == "__main__":
    main()
