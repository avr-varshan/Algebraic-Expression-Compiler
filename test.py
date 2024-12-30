import unittest
from src.parser import tokenize, parse_expression
from src.compiler import Compiler
from src.evaluator import evaluate

class TestCompiler(unittest.TestCase):

    def test_simplify_constants(self):
        """Test simplifying expressions with constant subtrees."""
        tokens = tokenize("3 + 5")
        tree = parse_expression(tokens)
        simplified_tree = Compiler.simplify(tree)
        self.assertEqual(simplified_tree.value, 8)

        tokens = tokenize("2 ^ 3")
        tree = parse_expression(tokens)
        simplified_tree = Compiler.simplify(tree)
        self.assertEqual(simplified_tree.value, 8)

        tokens = tokenize("10 % 3")
        tree = parse_expression(tokens)
        simplified_tree = Compiler.simplify(tree)
        self.assertEqual(simplified_tree.value, 1)

    def test_simplify_redundant(self):
        """Test simplifying redundant expressions like x + x or x - x."""
        tokens = tokenize("x + x")
        tree = parse_expression(tokens)
        simplified_tree = Compiler.simplify(tree)
        self.assertEqual(simplified_tree.value, "*")
        self.assertEqual(simplified_tree.left.value, 2)
        self.assertEqual(simplified_tree.right.value, "x")

        tokens = tokenize("x - x")
        tree = parse_expression(tokens)
        simplified_tree = Compiler.simplify(tree)
        self.assertEqual(simplified_tree.value, 0)

    def test_simplify_factorial(self):
        """Test simplifying expressions with factorials."""
        tokens = tokenize("5!")
        tree = parse_expression(tokens)
        simplified_tree = Compiler.simplify(tree)
        self.assertEqual(simplified_tree.value, 120)

        tokens = tokenize("0!")
        tree = parse_expression(tokens)
        simplified_tree = Compiler.simplify(tree)
        self.assertEqual(simplified_tree.value, 1)

    def test_intermediate_representation(self):
        """Test generating intermediate representations of trees."""
        tokens = tokenize("(3 + 5) * 2")
        tree = parse_expression(tokens)
        simplified_tree = Compiler.simplify(tree)
        representation = Compiler.generate_intermediate_representation(simplified_tree)
        self.assertIn("16", representation)

    def test_mixed_operations(self):
        """Test simplifying expressions with mixed operations."""
        tokens = tokenize("(2 + 3) * 4 - 6")
        tree = parse_expression(tokens)
        simplified_tree = Compiler.simplify(tree)
        self.assertEqual(evaluate(simplified_tree), 14)

if __name__ == "__main__":
    unittest.main()
