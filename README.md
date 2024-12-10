# Python project template

> This repository is a template for Python projects.
>
> It includes a basic structure and files to get started with a new project with linting and testing.
>
> The following README gives template instructions for setting up the project.

## Project Title

![Test Status](https://img.shields.io/github/actions/workflow/status/Segolene-Albouy/python-project-template/test.yml?branch=main)

[//]: # (![Test Status]&#40;https://img.shields.io/github/actions/workflow/status/<user>/<repo>/test.yml?branch=main&#41;)

A brief description of what the project does and its purpose.

> **Table of Contents**
>
> - [Getting Started](#getting-started)
> - [Installation](#installation)
> - [Contributing](#contributing)
> - [Contact](#contact)

### Getting Started

Instructions on setting up the project locally for development or testing.

#### Prerequisites

- **Sudo** privileges
- **Python** >= 3.10
- **Git**: `sudo apt install git`

#### Installation

Step-by-step instructions on how to install the project and its dependencies.

1. Clone the repository:
    ```bash
    git clone git@github.com:<username>/<repository>.git
    cd <repository>
    ```
2. Set up environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    pip install -r requirements-dev.txt
    pre-commit install
    ```
4. Run the project:
    ```bash
    python src/main.py
    ```

#### Tests

Explain how to run the automated tests for this system.
```bash
# run pytest on tests/
pytest

# run pre-commit hooks
pre-commit run --all-files
```

### Contributing
Guidelines for contributing to the project:

1. Fork the repository
2. Create a branch for your feature (`git checkout -b feature`)
3. Commit your changes (`git commit -m '[FEATURE] addition of this feature'`)
4. Push to the branch (`git push origin feature`)
5. Open a Pull Request

### Contact

Your Name – your.email@example.com
