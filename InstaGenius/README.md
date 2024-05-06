---

# InstaGenius

InstaGenius is a Python application that leverages the Groq and Serper APIs to perform certain tasks.

## Prerequisites

Before running InstaGenius, ensure you have the following prerequisites installed on your system:

- Python 3.11 or any
- [Poetry](https://python-poetry.org/docs/) for managing dependencies

## Configuration

1. Rename the `.env.example` file to `.env`.
2. Obtain your Groq and Serper API keys.
3. Insert your API keys into the `.env` file.

## Installation

1. Open a terminal or command prompt.
2. Navigate to the root directory of the InstaGenius project.
3. Run the following commands to set up the project environment:

```bash
poetry shell
poetry install --no-root
```

## Execution

To execute InstaGenius, run the following command:

```bash
python main.py
```
