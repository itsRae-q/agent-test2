import unittest

from scripts.preorder_traversal import build_example_tree, preorder_traversal


class PreorderTraversalTest(unittest.TestCase):

    def test_example_tree(self) -> None:
        tree = build_example_tree()
        result = preorder_traversal(tree)
        self.assertEqual(result, [1, 2, 4, 5, 3, 6, 7])


if __name__ == "__main__":
    unittest.main()
