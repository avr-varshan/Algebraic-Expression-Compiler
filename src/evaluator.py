# src/evaluator.py
import math
from src.parser import Node

def evaluate(node: Node, context: dict = None):
    """
    Recursively evaluate the expression tree and return a numerical result.

    Parameters:
    - node: Node
        The root of the expression tree.
    - context: dict
        A dictionary mapping variable names to their numerical values.
    """
    if node is None:
        return 0

    # If node is a numeric value, just return it
    if isinstance(node.value, (int, float)):
        return node.value

    # If node is a variable, look up its value in the context
    if isinstance(node.value, str) and node.value.isalpha():
        if node.value in ("pi", "e"):
            # Predefined constants
            return context.get(node.value, getattr(math, node.value))
        if context and node.value in context:
            return context[node.value]
        else:
            raise ValueError(f"Variable '{node.value}' is not defined.")

    # Handle binary operators
    if node.value in ("+", "-", "*", "/", "%", "^", "//"):
        left_val = evaluate(node.left, context)
        right_val = evaluate(node.right, context)

        if node.value == "+":
            return left_val + right_val
        elif node.value == "-":
            return left_val - right_val
        elif node.value == "*":
            return left_val * right_val
        elif node.value == "/":
            if right_val == 0:
                raise ValueError("Division by zero is not allowed.")
            return left_val / right_val
        elif node.value == "%":
            if right_val == 0:
                raise ValueError("Modulo by zero is not allowed.")
            return left_val % right_val
        elif node.value == "^":
            return left_val ** right_val
        elif node.value == "//":
            if right_val == 0:
                raise ValueError("Integer division by zero is not allowed.")
            return left_val // right_val  # floor division

    # Handle unary operators
    if node.value == "!":
        # Factorial
        value = evaluate(node.left, context)
        if not isinstance(value, int) or value < 0:
            raise ValueError("Factorial is only defined for non-negative integers.")
        return math.factorial(value)

    if node.value in ("+", "-") and node.left is None and node.right is not None:
        # Unary plus or minus
        right_val = evaluate(node.right, context)
        if node.value == "+":
            return right_val
        else:  # unary minus
            return -right_val

    # Handle functions
    if node.value in ("sin", "cos", "tan", "log", "sqrt", "abs", "exp", "floor", "ceil"):
        arg_val = evaluate(node.left, context)
        if node.value == "sin":
            # Assuming input is in degrees; convert to radians
            return math.sin(math.radians(arg_val))
        elif node.value == "cos":
            return math.cos(math.radians(arg_val))
        elif node.value == "tan":
            return math.tan(math.radians(arg_val))
        elif node.value == "log":
            if arg_val <= 0:
                raise ValueError("Logarithm is only defined for positive numbers.")
            return math.log(arg_val)
        elif node.value == "sqrt":
            if arg_val < 0:
                raise ValueError("Square root is not defined for negative numbers.")
            return math.sqrt(arg_val)
        elif node.value == "abs":
            return abs(arg_val)
        elif node.value == "exp":
            return math.exp(arg_val)
        elif node.value == "floor":
            return math.floor(arg_val)
        elif node.value == "ceil":
            return math.ceil(arg_val)

    # If none of the above matched, it's either an unsupported function/operator or a variable
    raise ValueError(f"Unsupported operation or variable: {node.value}")