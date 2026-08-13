# Forge

> A lightweight AI coding agent built with Python, OpenRouter, and tool calling.

![Forge Tool Calls](docs/images/forge-tool-calls.png)

Forge is an educational AI coding agent that uses an LLM as a decision-making engine and a controlled set of Python tools to inspect files, read and modify code, and execute Python programs.

The project was built as part of the [Boot.dev](https://www.boot.dev/) AI Agent course to understand the fundamentals behind agentic coding systems and tool-calling workflows.

---

## Overview

Forge does not allow the LLM to directly interact with the filesystem.

Instead, the LLM can request one of the tools provided by the application. Forge executes the requested function and sends the result back to the model.

The basic workflow is:

```text
User
 │
 ▼
Forge
 │
 ▼
LLM
 │
 ├── Tool Call
 │
 ▼
Forge executes the tool
 │
 ▼
Tool Result
 │
 ▼
LLM
 │
 ├── Another Tool Call
 │
 └── Final Response
```

This feedback loop allows the agent to inspect a project, make changes, run code, and use the results of those operations to continue working.

---

## Features

Forge currently provides four tools.

### `get_files_info`

Lists the contents of a directory within the permitted working directory.

For each item, it provides:

* Name
* File size
* Directory status

Example:

```text
- main.py: file_size=744 bytes, is_dir=False
- pkg: file_size=4096 bytes, is_dir=True
```

### `get_file_content`

Reads the contents of a file within the permitted working directory.

Large files are limited to a maximum number of characters to prevent unnecessarily large amounts of data from being passed to the LLM.

### `write_file`

Creates or overwrites files within the permitted working directory.

Missing parent directories are created automatically when necessary.

### `run_python_file`

Executes Python files using `subprocess`.

The tool includes:

* Working-directory validation
* Python file validation
* `stdout` capture
* `stderr` capture
* Process exit-code handling
* A 30-second execution timeout

---

## Agent Loop

Forge can perform multiple tool calls during a single task.

For example, a request to fix a bug can result in a workflow similar to:

```text
User
 │
 │ "Fix the bug in the calculator"
 ▼
LLM
 │
 ├── get_files_info
 ▼
Tool Result
 │
 ▼
LLM
 │
 ├── get_file_content
 ▼
Tool Result
 │
 ▼
LLM
 │
 ├── write_file
 ▼
Tool Result
 │
 ▼
LLM
 │
 ├── run_python_file
 ▼
Tool Result
 │
 ▼
LLM
 │
 └── Final Response
```

The agent maintains the conversation history throughout this process so that each new model response has access to previous tool calls and their results.

The loop is also limited to a fixed number of iterations to prevent an agent from running indefinitely.

---

## Project Structure

```text
forge/
├── calculator/
│   ├── lorem.txt
│   ├── main.py
│   ├── README.md
│   ├── tests.py
│   └── pkg/
│       ├── calculator.py
│       └── render.py
│
├── functions/
│   ├── get_file_content.py
│   ├── get_files_info.py
│   ├── run_python_file.py
│   └── write_file.py
│
├── call_functions.py
├── main.py
├── prompts.py
│
├── test_get_file_content.py
├── test_get_files_info.py
├── test_run_python_file.py
├── test_write_file.py
│
├── pyproject.toml
├── uv.lock
├── README.md
└── .gitignore
```

The `calculator` directory is the example project that Forge operates on.

The `functions` directory contains the tools exposed to the LLM.

`call_functions.py` connects the model's tool calls to the corresponding Python functions.

`main.py` contains the application and agent loop.

---

## Requirements

* Python 3.14+
* [uv](https://docs.astral.sh/uv/)
* An [OpenRouter](https://openrouter.ai/) API key

---

## Installation

Clone the repository:

```bash
git clone <your-repository-url>
cd forge
```

Install the dependencies:

```bash
uv sync
```

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=your_api_key_here
```


---

## Usage

Run Forge with:

```bash
uv run main.py "your prompt"
```

For example:

```bash
uv run main.py "what files are in the current working directory?"
```

Verbose mode can be enabled with:

```bash
uv run main.py "what files are in the current working directory?" --verbose
```

Verbose mode displays additional information such as:

* User prompt
* Prompt token usage
* Response token usage
* Tool calls
* Tool results

---

## Example

Running:

```bash
uv run main.py "what files are in the current working directory?"
```

can result in a tool call such as:

```text
- Calling function: get_files_info
```

followed by the tool result:

```text
- README.md: file_size=12 bytes, is_dir=False
- main.py: file_size=744 bytes, is_dir=False
- lorem.txt: file_size=28 bytes, is_dir=False
- tests.py: file_size=1433 bytes, is_dir=False
- pkg: file_size=4096 bytes, is_dir=True
```

The result is then returned to the LLM, which produces the final response for the user.

---

## Testing

Each tool has a corresponding test module.

Run the individual tool tests with:

```bash
uv run test_get_files_info.py
uv run test_get_file_content.py
uv run test_write_file.py
uv run test_run_python_file.py
```

The calculator project can also be tested with:

```bash
uv run calculator/tests.py
```

---

## Security Warning

**Forge is an educational toy AI agent and is not production-ready.**

The agent has access to operations that can:

* Read files
* Create and overwrite files
* Execute Python code

The current implementation includes basic safeguards such as working-directory restrictions and a timeout for Python execution, but these protections are intentionally limited.

Do not expose Forge as a general-purpose service.

Do not give it access to directories containing sensitive information.

Do not run it against important production systems.

Do not assume that the current security model provides a complete sandbox.

This project is intended for learning and experimentation with agentic coding systems.

---

## Architecture

Forge is built around three main components.

### System Prompt

The system prompt defines the agent's role, available operations, and rules for interacting with the tools.

### Tool Declarations

Each Python function is described to the LLM using a structured tool declaration.

The model does not directly execute the Python functions.

Instead, it produces a tool call containing:

```text
Function name
Arguments
```

Forge receives the request, executes the corresponding function, and returns the result to the model.

### Tool Dispatcher

`call_functions.py` maps tool names requested by the LLM to the actual Python functions:

```text
LLM
 │
 ▼
Tool Call
 │
 ▼
call_function()
 │
 ▼
function_map
 │
 ├── get_files_info()
 ├── get_file_content()
 ├── write_file()
 └── run_python_file()
```

---

## Technology

Forge currently uses:

* Python
* OpenAI Python SDK
* OpenRouter
* `subprocess`
* `argparse`
* `python-dotenv`
* `uv`

---

## Future Development

The current version intentionally remains close to the educational implementation.

Future versions or separate releases may explore additional capabilities such as:

* A dedicated `forge` CLI
* Configurable working directories
* Improved filesystem sandboxing
* More robust error handling
* Additional tools
* Better test coverage
* Improved prompt engineering
* Support for additional LLM providers
* Model selection
* Git integration
* Improved logging
* Safer code execution
* Support for working with different codebases

These features are considered potential future development and are **not part of the current version**.

---

## Disclaimer

Forge is an educational project inspired by the fundamentals of agentic coding systems.

It is intentionally much simpler and less secure than production coding agents such as Claude Code, Cursor, or similar development environments.

Use it responsibly and only in environments where you understand and accept the risks of giving an LLM access to your filesystem and Python interpreter.
