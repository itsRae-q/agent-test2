class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def preorder(node, visit):
    if node is None:
        return
    visit(node.value)
    preorder(node.left, visit)
    preorder(node.right, visit)


def build_sample_tree():
    return Node(
        1,
        left=Node(2, left=Node(4), right=Node(5)),
        right=Node(3)
    )


def main():
    root = build_sample_tree()
    result = []
    preorder(root, lambda val: result.append(str(val)))

    output_path = "preorder_output.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(" ".join(result))

    print(f"前序遍历结果: {' '.join(result)}")
    print(f"已将结果写入 {output_path}")


if __name__ == "__main__":
    main()
