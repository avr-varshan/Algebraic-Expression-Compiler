import math
from src.parser import Node

def evaluate(node: Node, context: dict = None, use_degrees: bool = True):
    """
    Recursively evaluate the expression tree and return a numerical result.

    Parameters:
    - node: Node
        The root of the expression tree.
    - context: dict
        A dictionary mapping variable names to their numerical values.
    - use_degrees: bool
        If True, trigonometric functions interpret angles as degrees.
        If False, use radians.
    """
    if node is None:
        return 0
    if context is None:
        context = {}

    # If node is numeric, return it
    if isinstance(node.value, (int, float)):
        return node.value

    # If node is a recognized function or constant
    if isinstance(node.value, str) and node.value.isalpha():
        # Recognized functions
        if node.value in ("sin", "cos", "tan", "log", "sqrt", "abs", "exp", "floor", "ceil"):
            return _evaluate_function(node, context, use_degrees)
        elif node.value in ("pi", "e"):
            return getattr(math, node.value)
        # Otherwise, treat as a variable
        if node.value in context:
            return context[node.value]
        raise ValueError(f"Variable '{node.value}' is not defined.")

    # Handle binary operators
    if node.value in ("+", "-", "*", "/", "%", "^", "//"):
        left_val = evaluate(node.left, context, use_degrees)
        right_val = evaluate(node.right, context, use_degrees)

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
            return left_val // right_val

    # Handle unary operators
    if node.value == "!":
        # Factorial
        value = evaluate(node.left, context, use_degrees)
        if not isinstance(value, int) or value < 0:
            raise ValueError("Factorial is only defined for non-negative integers.")
        return math.factorial(value)

    if node.value in ("+", "-") and node.left is None and node.right is not None:
        # Unary plus or minus
        right_val = evaluate(node.right, context, use_degrees)
        if node.value == "+":
            return right_val
        else:  # unary minus
            return -right_val

    raise ValueError(f"Unsupported operation or variable: {node.value}")


def _evaluate_function(node: Node, context: dict, use_degrees: bool):
    """
    Helper to evaluate built-in functions: sin, cos, tan, log, sqrt, abs, exp, floor, ceil.
    """
    arg_val = evaluate(node.left, context, use_degrees)

    # Decide degrees vs radians for trig
    if use_degrees and node.value in ("sin", "cos", "tan"):
        arg_val = math.radians(arg_val)

    if node.value == "sin":
        return math.sin(arg_val)
    elif node.value == "cos":
        return math.cos(arg_val)
    elif node.value == "tan":
        return math.tan(arg_val)
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
    else:
        raise ValueError(f"Unsupported function '{node.value}'")
