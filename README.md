# BPMN to DFA Converter

This repository contains a tool that parses BPMN XML files into Deterministic Finite Automata (DFA) and then converts the DFA into an Adjacency List. 
This is done to extract all possible paths in the process model while respecting BPMN gateway logic and guidelines.

## Features

- Parse BPMN XML files.
- Convert parsed BPMN into a DFA.
- Convert DFA into an Adjacency List.
- Find all possible paths in the BPMN process model.

- [Example](#example)
<img width="1090" alt="Screenshot 2024-07-04 at 22 20 19" src="https://github.com/jing-yaoo/BPMN-XML-DFA-TreeTraversal/assets/85895529/f0c0680e-0c17-41b0-9945-a7a92463181a">
Process model
<img width="1091" alt="Screenshot 2024-07-04 at 22 21 34" src="https://github.com/jing-yaoo/BPMN-XML-DFA-TreeTraversal/assets/85895529/428597a3-cb17-477b-becb-dfa3a947c401">
XML file
<img width="381" alt="Screenshot 2024-07-04 at 22 25 35" src="https://github.com/jing-yaoo/BPMN-XML-DFA-TreeTraversal/assets/85895529/d2e946a1-24d6-4d9c-9770-637f06e2ae81">
Adjacency List
<img width="1267" alt="Screenshot 2024-07-04 at 22 26 20" src="https://github.com/jing-yaoo/BPMN-XML-DFA-TreeTraversal/assets/85895529/6c6dc0cf-3840-4be3-af07-9ecfc57f71b7">
Pathways

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/bpmn-to-dfa.git
    ```
    
2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

To use the tool, you need a BPMN XML file. The tool will parse this file, convert it into a DFA, and then generate an adjacency list to find all possible paths.

### Example

1. Place your BPMN XML file in the `data` folder and rewrite the parser path with your local path.

2. Run the script:
    ```sh
    python main.py input/your_bpmn_file.xml
    ```

3. The output will be displayed in the console and saved in the `output` directory.

