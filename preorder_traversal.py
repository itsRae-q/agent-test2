# 简单的前序遍历函数

class TreeNode:
    """二叉树节点定义"""
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def preorder_traversal(root):
    """
    前序遍历二叉树 (根 -> 左 -> 右)
    
    Args:
        root: TreeNode - 二叉树的根节点
    
    Returns:
        list: 前序遍历的结果列表
    """
    if not root:
        return []
    
    result = []
    result.append(root.val)  # 访问根节点
    result.extend(preorder_traversal(root.left))   # 遍历左子树
    result.extend(preorder_traversal(root.right))  # 遍历右子树
    
    return result

# 示例用法
if __name__ == "__main__":
    # 构建一个简单的二叉树
    #       1
    #      / \
    #     2   3
    #    / \
    #   4   5
    
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    
    # 执行前序遍历
    result = preorder_traversal(root)
    print(f"前序遍历结果: {result}")  # 输出: [1, 2, 4, 5, 3]