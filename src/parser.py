import re
import unicodedata

class Node:
    """
    Represents a node in the expression tree.

    Attributes:
    - value: str, int, float
        The operator or the numeric/variable value.
    - left: Node or None
        Left child node.
    - right: Node or None
        Right child node.
    """
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self):
        return f"Node({self.value}, left={self.left}, right={self.right})"


def normalize_expression(expr: str) -> str:
    """
    Normalize the expression to remove or replace any non-standard whitespace.
    """
    expr = unicodedata.normalize('NFKC', expr)
    expr = expr.replace('\u00A0', ' ')   # Replace non-breaking space
    expr = expr.replace('\u200B', '')    # Remove zero-width spaces
    return expr


def tokenize(expression: str):
    """
    Convert a mathematical expression into a list of tokens (numbers, variables,
    operators, parentheses, etc.).
    """
    expression = normalize_expression(expression).strip()
    if not expression:
        raise ValueError("Input expression is empty.")

    # Pattern covers:
    # 1) Numbers (integers, floats)
    # 2) Variables (alphanumeric + underscore)
    # 3) Operators (+ - * / // % ^ !)
    # 4) Parentheses
    token_pattern = r"(?:\d+(?:\.\d+)?)|(?:[a-zA-Z_][a-zA-Z_0-9]*)|//|[+\-*/^%!()]"
    tokens_raw = re.findall(token_pattern, expression)

    if not tokens_raw:
        raise ValueError("Failed to tokenize input. Check your expression syntax.")

    # Lowercase any alpha tokens for case-insensitive function/variable handling
    normalized_tokens = []
    for t in tokens_raw:
        if t.isalpha():
            normalized_tokens.append(t.lower())
        else:
            normalized_tokens.append(t)

    return normalized_tokens


def parse_expression(tokens):
    """
    Parse the list of tokens into a binary tree, respecting operator precedence.
    Returns the root of the expression tree.
    """
    index = 0  # Pointer to current token in the list

    def parse_factor():
        nonlocal index
        node = parse_term()
        # Factor handles exponentiation and factorial
        while index < len(tokens) and tokens[index] in ("^", "!"):
            operator = tokens[index]
            index += 1
            if operator == "!":
                # Factorial (unary)
                node = Node(operator, left=node)
            else:
                # Exponentiation is right-associative
                right = parse_term()
                node = Node(operator, left=node, right=right)
        return node

    def parse_term():
        nonlocal index
        if index >= len(tokens):
            raise ValueError("Unexpected end of tokens while parsing a term.")
        token = tokens[index]

        if token == "(":
            index += 1  # consume '('
            node = parse_top_level()
            if index >= len(tokens) or tokens[index] != ")":
                raise ValueError("Unmatched '(' - missing ')'.")
            index += 1  # consume ')'
            return node

        elif token.replace('.', '', 1).isdigit():
            # Numeric literal
            index += 1
            return Node(float(token) if '.' in token else int(token))

        elif token.isalpha():
            # Could be a function or a variable
            func_name = token
            index += 1
            if index < len(tokens) and tokens[index] == "(":
                # Function call
                index += 1  # consume '('
                argument = parse_top_level()
                if index >= len(tokens) or tokens[index] != ")":
                    raise ValueError(f"Function '{func_name}' missing closing ')'.")
                index += 1  # consume ')'
                return Node(func_name, left=argument)
            else:
                # Just a variable
                return Node(func_name)

        elif token in ("+", "-"):
            # Unary plus or minus
            operator = token
            index += 1  # consume operator
            operand = parse_term()
            return Node(operator, right=operand)

        else:
            raise ValueError(f"Unexpected token: '{token}' while parsing term.")

    def parse_expr():
        nonlocal index
        # parse_expr() handles * / % //
        node = parse_factor()
        while index < len(tokens) and tokens[index] in ("*", "/", "%", "//"):
            operator = tokens[index]
            index += 1
            right = parse_factor()
            node = Node(operator, left=node, right=right)
        return node

    def parse_top_level():
        nonlocal index
        # parse_top_level() handles + -
        node = parse_expr()
        while index < len(tokens) and tokens[index] in ("+", "-"):
            operator = tokens[index]
            index += 1
            right = parse_expr()
            node = Node(operator, left=node, right=right)
        return node

    parsed_tree = parse_top_level()

    if index < len(tokens):
        leftover = tokens[index:]
        raise ValueError(f"Extra tokens remaining after parse: {leftover}")

    return parsed_tree
