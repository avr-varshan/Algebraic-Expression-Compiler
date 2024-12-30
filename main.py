# main.py

import streamlit as st
from src.parser import tokenize, parse_expression, Node
from src.compiler import Compiler
from src.evaluator import evaluate
from graphviz import Digraph
from pyvis.network import Network
import streamlit.components.v1 as components
import math
from typing import Set
import os
import logging

# Configure logging
logging.basicConfig(
    filename='algebraic_evaluator.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.ERROR
)

def collect_variables(node: Node, variables: Set[str]):
    """
    Recursively traverse the expression tree to collect all unique variable names.

    Parameters:
    - node: Node
        The current node in the expression tree.
    - variables: set
        A set to store unique variable names.
    """
    if node is None:
        return

    # If the node is a string and not a function, consider it a variable
    if isinstance(node.value, str):
        if node.value.isalpha() and node.value not in (
            "sin", "cos", "tan", "log", "sqrt", "abs", "exp", "floor", "ceil", "pi", "e"
        ):
            variables.add(node.value)

    # Recursively collect from left and right children
    collect_variables(node.left, variables)
    collect_variables(node.right, variables)


def process_expression(expression: str):
    """
    Process the input expression by tokenizing, parsing, simplifying, and generating IR.

    Parameters:
    - expression: str
        The mathematical expression input by the user.

    Returns:
    - tokens: list
        List of tokens from the expression.
    - tree: Node
        The original expression tree.
    - simplified_tree: Node
        The simplified expression tree.
    - ir: str
        Intermediate representation of the simplified tree.
    """
    tokens = tokenize(expression)
    tree = parse_expression(tokens)
    simplified_tree = Compiler.simplify(tree)
    ir = Compiler.generate_intermediate_representation(simplified_tree)
    return tokens, tree, simplified_tree, ir


def create_tree_visualization(node: Node, graph=None, parent_id=None):
    """
    Create a Graphviz visualization of the expression tree.

    Parameters:
    - node: Node
        The current node in the expression tree.
    - graph: Digraph or None
        The Graphviz Digraph object.
    - parent_id: str or None
        The ID of the parent node.

    Returns:
    - graph: Digraph
        The complete Graphviz Digraph object.
    """
    if graph is None:
        graph = Digraph(format="png")
        graph.attr(rankdir="TB")  # Top to bottom layout

    if node is not None:
        node_id = str(id(node))
        label = f"{node.value}"
        if isinstance(node.value, str) and node.value.isalpha():
            label += f"\n({node.value})"
        graph.node(node_id, label)
        if parent_id:
            graph.edge(parent_id, node_id)
        create_tree_visualization(node.left, graph, node_id)
        create_tree_visualization(node.right, graph, node_id)
    return graph


def create_interactive_tree(node: Node):
    """
    Create an interactive PyVis visualization of the expression tree.

    Parameters:
    - node: Node
        The current node in the expression tree.

    Returns:
    - net: Network
        The PyVis Network object.
    """
    net = Network(height="500px", width="100%", directed=True)

    def add_nodes_edges(node: Node, parent_id=None):
        if node is None:
            return
        node_id = str(id(node))
        net.add_node(node_id, label=str(node.value), title=f"Node: {node.value}")
        if parent_id:
            net.add_edge(parent_id, node_id)
        add_nodes_edges(node.left, node_id)
        add_nodes_edges(node.right, node_id)

    add_nodes_edges(node)
    return net


def main():
    # Set Streamlit page configuration
    st.set_page_config(page_title="🧮 Algebraic Expression Evaluator", layout="wide")
    st.title("🧮 Algebraic Expression Evaluator")
    st.write("""
    ### Features:
    - **Operators:** +, -, *, /, %, ^, //
    - **Functions:** sin(), cos(), tan(), log(), sqrt(), abs(), exp(), floor(), ceil()
    - **Factorials:** n!
    - **Parentheses for grouping:** ()
    - **Variables:** x, y, etc. (their values will be prompted)
    - **Modular arithmetic and integer division**
    - **Visualization:** Expression trees
    - **History Tracking:** View your previous evaluations
    """)

    # Sidebar for Help
    st.sidebar.title("📚 Help")
    st.sidebar.info("""
    **How to Use:**
    1. **Enter Expression:** Input your mathematical expression in the text box.
    2. **Define Variables:** If your expression contains variables (e.g., x, y), enter their values when prompted.
    3. **View Results:** See the expression tree and the final evaluated result.
    4. **Visualization:** Click the button to view an interactive expression tree.
    5. **History:** Check your last five evaluations in the main page.

    **Supported Functions:**
    - **Trigonometric:** sin(), cos(), tan()
    - **Logarithmic and Roots:** log(), sqrt()
    - **Others:** abs(), exp(), floor(), ceil()
    - **Factorial:** n!

    **Constants:**
    - pi (~3.14159)
    - e (~2.71828)
    """)

    # Input field for mathematical expression
    expression = st.text_input("📝 Enter your mathematical expression:", "")

    if expression:
        try:
            with st.spinner("Processing your expression..."):
                # Process the expression
                tokens, tree, simplified_tree, ir = process_expression(expression)

            # Display original expression tree
            st.subheader("🌳 Expression Tree")
            with st.spinner("Generating expression tree..."):
                graph = create_tree_visualization(tree)
                st.graphviz_chart(graph.source)

            # Detect variables and collect user input
            variables = set()
            collect_variables(simplified_tree, variables)
            context = {'pi': math.pi, 'e': math.e}

            if variables:
                st.subheader("🔢 Variables Detected")
                st.write(', '.join(sorted(variables)))
                for var in sorted(variables):
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        st.markdown(f"**{var}:**")
                    with col2:
                        value = st.text_input(f"Enter the value for '{var}':", key=var)
                        if value:
                            try:
                                # Attempt to parse the input as a float or int
                                if '.' in value:
                                    context[var] = float(value)
                                else:
                                    context[var] = int(value)
                            except ValueError:
                                st.error(f"Invalid value for '{var}'. Please enter a valid number.")

            # Evaluate the expression
            if not variables or all(var in context for var in variables):
                st.subheader("✅ Final Evaluation")
                try:
                    with st.spinner("Evaluating the expression..."):
                        result = evaluate(simplified_tree, context)
                    st.success(f"**Final Result:** {result}")
                    # Add to history
                    if 'history' not in st.session_state:
                        st.session_state.history = []
                    st.session_state.history.append((expression, result))
                except ValueError as ve:
                    st.error(f"Evaluation Error: {ve}")
                    logging.error(f"Evaluation Error: {ve}")
                except Exception as e:
                    st.error(f"Unexpected Evaluation Error: {e}")
                    logging.error(f"Unexpected Evaluation Error: {e}")
            else:
                st.warning("Please provide values for all detected variables.")

        except ValueError as ve:
            st.error(f"Input Error: {ve}")
            logging.error(f"Input Error: {ve}")
        except Exception as e:
            st.error("An unexpected error occurred. Please check your expression and try again.")
            logging.error(f"Unexpected Error: {e}")

        # Button to show interactive tree
        if st.button("🌐 Show Interactive Expression Tree"):
            try:
                with st.spinner("Generating interactive expression tree..."):
                    net = create_interactive_tree(tree)
                    net.show("interactive_tree.html")
                    if os.path.exists("interactive_tree.html"):
                        HtmlFile = open("interactive_tree.html", 'r', encoding='utf-8')
                        source_code = HtmlFile.read()
                        components.html(source_code, height=500)
                    else:
                        st.error("Failed to generate the interactive expression tree.")
            except Exception as e:
                st.error(f"Interactive Tree Generation Error: {e}")
                logging.error(f"Interactive Tree Generation Error: {e}")

    # Display history
    if 'history' in st.session_state and st.session_state.history:
        st.subheader("📜 History")
        for idx, (expr, res) in enumerate(reversed(st.session_state.history[-5:]), 1):  # Show last 5
            st.write(f"{idx}. **{expr}** = {res}")

if __name__ == "__main__":
    main()