"""
前序遍历（Pre-order Traversal）实现
前序遍历顺序：根节点 -> 左子树 -> 右子树
"""

class TreeNode:
    """二叉树节点类"""
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def preorder_traversal_recursive(root):
    """
    递归实现前序遍历
    
    Args:
        root: 二叉树根节点
        
    Returns:
        list: 前序遍历结果列表
    """
    if not root:
        return []
    
    result = []
    
    # 访问根节点
    result.append(root.val)
    
    # 递归遍历左子树
    result.extend(preorder_traversal_recursive(root.left))
    
    # 递归遍历右子树
    result.extend(preorder_traversal_recursive(root.right))
    
    return result

def preorder_traversal_iterative(root):
    """
    迭代实现前序遍历（使用栈）
    
    Args:
        root: 二叉树根节点
        
    Returns:
        list: 前序遍历结果列表
    """
    if not root:
        return []
    
    result = []
    stack = [root]
    
    while stack:
        # 弹出栈顶节点
        node = stack.pop()
        
        # 访问当前节点
        result.append(node.val)
        
        # 先压入右子节点，再压入左子节点
        # 这样左子节点会先被弹出（栈是后进先出）
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    
    return result

def print_tree_structure(root, level=0, prefix="Root: "):
    """
    打印二叉树结构（辅助函数）
    
    Args:
        root: 二叉树根节点
        level: 当前层级
        prefix: 前缀字符串
    """
    if root is not None:
        print(" " * (level * 4) + prefix + str(root.val))
        if root.left is not None or root.right is not None:
            if root.left:
                print_tree_structure(root.left, level + 1, "L--- ")
            else:
                print(" " * ((level + 1) * 4) + "L--- None")
            if root.right:
                print_tree_structure(root.right, level + 1, "R--- ")
            else:
                print(" " * ((level + 1) * 4) + "R--- None")

# 测试用例
def test_preorder_traversal():
    """测试前序遍历算法"""
    print("=== 前序遍历测试 ===\n")
    
    # 测试用例1: 空树
    print("测试用例1: 空树")
    root1 = None
    recursive_result1 = preorder_traversal_recursive(root1)
    iterative_result1 = preorder_traversal_iterative(root1)
    print(f"递归结果: {recursive_result1}")
    print(f"迭代结果: {iterative_result1}")
    print(f"结果一致: {recursive_result1 == iterative_result1}\n")
    
    # 测试用例2: 单个节点
    print("测试用例2: 单个节点")
    root2 = TreeNode(1)
    print("树结构:")
    print_tree_structure(root2)
    recursive_result2 = preorder_traversal_recursive(root2)
    iterative_result2 = preorder_traversal_iterative(root2)
    print(f"递归结果: {recursive_result2}")
    print(f"迭代结果: {iterative_result2}")
    print(f"结果一致: {recursive_result2 == iterative_result2}\n")
    
    # 测试用例3: 完整二叉树
    print("测试用例3: 完整二叉树")
    #       1
    #      / \
    #     2   3
    #    / \ / \
    #   4  5 6  7
    root3 = TreeNode(1)
    root3.left = TreeNode(2)
    root3.right = TreeNode(3)
    root3.left.left = TreeNode(4)
    root3.left.right = TreeNode(5)
    root3.right.left = TreeNode(6)
    root3.right.right = TreeNode(7)
    
    print("树结构:")
    print_tree_structure(root3)
    recursive_result3 = preorder_traversal_recursive(root3)
    iterative_result3 = preorder_traversal_iterative(root3)
    print(f"递归结果: {recursive_result3}")
    print(f"迭代结果: {iterative_result3}")
    print(f"结果一致: {recursive_result3 == iterative_result3}")
    print(f"期望结果: [1, 2, 4, 5, 3, 6, 7]")
    print(f"递归正确: {recursive_result3 == [1, 2, 4, 5, 3, 6, 7]}\n")
    
    # 测试用例4: 不平衡树
    print("测试用例4: 不平衡树（只有左子树）")
    #   1
    #  /
    # 2
    #/
    #3
    root4 = TreeNode(1)
    root4.left = TreeNode(2)
    root4.left.left = TreeNode(3)
    
    print("树结构:")
    print_tree_structure(root4)
    recursive_result4 = preorder_traversal_recursive(root4)
    iterative_result4 = preorder_traversal_iterative(root4)
    print(f"递归结果: {recursive_result4}")
    print(f"迭代结果: {iterative_result4}")
    print(f"结果一致: {recursive_result4 == iterative_result4}")
    print(f"期望结果: [1, 2, 3]")
    print(f"递归正确: {recursive_result4 == [1, 2, 3]}\n")

if __name__ == "__main__":
    test_preorder_traversal()