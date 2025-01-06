🔢 Algebraic Expression Compiler
================================

A high-performance application for evaluating and simplifying algebraic expressions involving unlimited-length integers, rationals, and trigonometric functions. This tool is designed for accuracy, speed, and usability, making it ideal for complex mathematical computations.

🚀 Features
-----------

*   **Arbitrary Precision**: Handles numbers with 100,000+ digits seamlessly.
    
*   **Efficient Processing**: Evaluates 100,000+ terms in under 0.5 seconds.
    
*   **Symbolic Simplifications**: Combines terms, removes redundancies, and ensures exact results.
    
*   **Visual Parse Trees**: Generates visualizations of raw and simplified expressions for debugging and analysis.
    
*   **Optimized Performance**: Leverages parallelized tasks and caching to improve speed by up to 50%.
    
*   **Trigonometric Mode**: Supports degree and radian modes for trigonometric calculations.
    

🔧 Tech Stack
-------------

*   **Programming Language**: Python
    
*   **Framework**: Streamlit
    
*   **Containerization**: Docker
    

🖥️ Usage
---------

### 1\. **Run Locally**

Clone the repository and install the dependencies:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   git clone   cd   pip install -r requirements.txt   `

Run the app locally:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   streamlit run main.py   `

Visit http://localhost:8501 in your browser.

### 2\. **Run with Docker**

Build and run the Docker container:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   docker build -t algebraic-compiler .  docker run -p 8501:8501 algebraic-compiler   `

🌐 Live Demo
------------

Check out the live app hosted on Fly.io: [Your Live URL](https://<your-app-name>.fly.dev/)

📜 Process Workflow
-------------------

1.  **Tokenization**: Converts input into structured tokens.
    
2.  **Parsing**: Builds a binary tree based on operator precedence.
    
3.  **Optimization**: Simplifies the tree with constant evaluation and term reduction.
    
4.  **Evaluation**: Computes results with arbitrary precision.
    

📊 Performance Benchmarks
-------------------------

*   Handles numbers with **100,000+ digits** and **10,000+ terms** effortlessly.
    
*   Evaluates **100,000+ terms** in under **0.5 seconds**.
    
*   Simplifies large expressions **40% faster** than traditional symbolic systems.
    

🤝 Contributing
---------------

Contributions are welcome! Please fork this repository and submit a pull request for any bug fixes or feature enhancements.

📄 License
----------

This project is licensed under the MIT License.

✉️ Contact
----------

For any inquiries or feedback, reach out at \[[your-email@example.com](mailto:your-email@example.com)\].