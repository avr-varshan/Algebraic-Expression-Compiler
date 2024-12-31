from src.parser import Node

class Compiler:
    """
    The Compiler module optimizes and simplifies the parsed expression tree.
    """

    @staticmethod
    def simplify(node: Node):
        """
        Simplify the expression tree by:
          - Evaluating constant subtrees
          - Combining obvious like terms (e.g., x + x => 2x)
        """
        if node is None:
            return None

        # If it's a numeric leaf, return as-is
        if isinstance(node.value, (int, float)):
            return node

        # Simplify left and right subtrees
        left = Compiler.simplify(node.left)
        right = Compiler.simplify(node.right)

        # If current node is a binary operator
        if node.value in ("+", "-", "*", "/", "%", "^", "//"):
            # If both left & right are numeric, evaluate them directly
            if (
                left and right
                and isinstance(left.value, (int, float))
                and isinstance(right.value, (int, float))
            ):
                return Node(Compiler.evaluate_constant(node.value, left.value, right.value))

            # x + x => 2x
            if node.value == "+" and left and right and left.value == right.value:
                if isinstance(left.value, (int, float)):
                    # e.g., 2 + 2 => 4
                    return Node(left.value * 2)
                else:
                    # e.g., x + x => 2 * x
                    return Node("*", left=Node(2), right=left)

            # x - x => 0
            if node.value == "-" and left and right and left.value == right.value:
                return Node(0)

            # Return node with simplified subtrees
            return Node(node.value, left=left, right=right)

        # If it’s a unary operator like "!"
        if node.value == "!":
            # If we have an integer on the left, evaluate its factorial
            if left and isinstance(left.value, int):
                return Node(Compiler.factorial(left.value))
            return Node(node.value, left=left)

        # If it’s a unary + or - (no left child)
        if node.value in ("+", "-") and node.left is None:
            right_simpl = right
            if isinstance(right_simpl.value, (int, float)):
                if node.value == "+":
                    return right_simpl
                else:
                    return Node(-right_simpl.value)
            return Node(node.value, right=right_simpl)

        # If it's a function call, just keep it with simplified child
        return Node(node.value, left=left, right=right)

    @staticmethod
    def evaluate_constant(operator, left, right):
        """
        Evaluate a constant operation for a binary operator.
        """
        if operator == "+":
            return left + right
        elif operator == "-":
            return left - right
        elif operator == "*":
            return left * right
        elif operator == "/":
            if right == 0:
                raise ValueError("Division by zero in constant expression.")
            return left / right
        elif operator == "%":
            if right == 0:
                raise ValueError("Modulo by zero in constant expression.")
            return left % right
        elif operator == "^":
            return left ** right
        elif operator == "//":
            if right == 0:
                raise ValueError("Integer division by zero in constant expression.")
            return left // right

        raise ValueError(f"Unsupported operator: {operator}")

    @staticmethod
    def factorial(n: int) -> int:
        """
        Compute the factorial of a non-negative integer n.
        """
        if n < 0:
            raise ValueError("Factorial is not defined for negative integers.")
        if n == 0 or n == 1:
            return 1

        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

    @staticmethod
    def generate_intermediate_representation(node: Node, depth=0) -> str:
        """
        Generate a human-readable string representation of the expression tree.
        """
        if node is None:
            return ""

        left_repr = Compiler.generate_intermediate_representation(node.left, depth + 1)
        right_repr = Compiler.generate_intermediate_representation(node.right, depth + 1)

        representation = f"{'  ' * depth}{node.value}\n"
        if left_repr:
            representation += left_repr
        if right_repr:
            representation += right_repr

        return representation
