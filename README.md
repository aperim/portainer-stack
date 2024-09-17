# Template Repository for Portainer GitOps with Docker Swarm

Welcome to the **Template Repository for Portainer GitOps with Docker Swarm**. This repository is designed to help you automate the generation and management of Docker Swarm stack files (`docker-compose.yaml` and `stack.env`) for use with [Portainer's GitOps functionality](https://www.portainer.io/solutions/gitops).

By leveraging Jinja2 templating and GitHub Actions, you can easily customise your Docker Swarm services and deploy them using Portainer with minimal manual effort.

---

## Table of Contents

- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Clone or Use as Template](#clone-or-use-as-template)
  - [Customise the Templates](#customise-the-templates)
  - [Define Your Variables](#define-your-variables)
  - [Set Environment Variables (Optional)](#set-environment-variables-optional)
  - [Commit and Push](#commit-and-push)
  - [Configure Portainer](#configure-portainer)
- [Files and Their Purpose](#files-and-their-purpose)
  - [`template/docker-compose.yaml.j2`](#templatedocker-composeyamlj2)
  - [`template/environment.j2`](#templateenvironmentj2)
  - [`template/variables.yaml`](#templatevariablesyaml)
  - [`render_templates.py`](#render_templatespy)
  - [GitHub Actions Workflow](#github-actions-workflow)
- [Additional Notes](#additional-notes)
  - [Environment Variables Precedence](#environment-variables-precedence)
  - [Handling Secrets](#handling-secrets)
  - [Customising the Workflow](#customising-the-workflow)
  - [Error Handling](#error-handling)
- [Support](#support)
- [License](#license)

---

## Overview

This template repository aims to simplify the deployment of Docker Swarm stacks using Portainer's GitOps feature. By using templated Docker Compose files and a GitHub Actions workflow, you can:

- Define your services and configurations using templates with variable placeholders.
- Store default variables in a YAML file.
- Override variables using environment variables, allowing for sensitive data to be managed securely.
- Automatically generate and commit the `docker-compose.yaml` and `stack.env` files upon each commit or pull request.
- Seamlessly integrate with Portainer to deploy your Docker Swarm services.

---

## Repository Structure

```bash
your-repo/
├── .github/
│   └── workflows/
│       └── generate-stack-files.yml
├── template/
│   ├── docker-compose.yaml.j2
│   ├── environment.j2
│   └── variables.yaml
├── render_templates.py
├── docker-compose.yaml
├── stack.env
└── README.md
```

- **`.github/workflows/generate-stack-files.yml`**: GitHub Actions workflow that generates and commits the `docker-compose.yaml` and `stack.env` files on pushes and pull requests.
- **`template/docker-compose.yaml.j2`**: Jinja2 template for your Docker Compose file.
- **`template/environment.j2`**: Jinja2 template for your environment variables file.
- **`template/variables.yaml`**: Source file containing default variables for the templates.
- **`render_templates.py`**: Python script that renders the templates using the variables.
- **`docker-compose.yaml`**: Generated Docker Compose file used by Portainer (auto-generated).
- **`stack.env`**: Generated environment variables file used by Portainer (auto-generated).
- **`README.md`**: This readme file.

---

## Getting Started

### Prerequisites

- **Git**: Ensure you have Git installed to clone repositories.
- **GitHub Account**: Required to use the repository as a template and set environment variables.
- **Portainer Account**: To deploy and manage your Docker Swarm stacks.
- **Basic Knowledge of Docker and Docker Compose**: Familiarity with Docker services and configurations.

### Clone or Use as Template

1. **Use as Template**:

   Click the "Use this template" button on GitHub to create your own repository based on this template.

2. **Clone Your Repository**:

   Clone your newly created repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/your-repo.git
   ```

### Customise the Templates

#### Docker Compose Template (`template/docker-compose.yaml.j2`)

- Define your services, networks, and volumes using Docker Compose syntax.
- Use Jinja2 templating syntax to include variables: `{{ variable_name }}`.
- **Example**:

  ```yaml
  version: '3.8'
  services:
    {{ service_name }}:
      image: '{{ image_name }}:{{ image_tag }}'
      ports:
        - '{{ host_port }}:{{ container_port }}'
      environment:
        - DATABASE_URL={{ database_url }}
  ```

#### Environment Template (`template/environment.j2`)

- Define environment variables required by your services.
- **Example**:

  ```env
  DATABASE_USER={{ database_user }}
  DATABASE_PASSWORD={{ database_password }}
  ```

### Define Your Variables

#### Variable Source File (`template/variables.yaml`)

- Store default values for your variables.
- Use YAML format for easy readability.
- **Example**:

  ```yaml
  service_name: web
  image_name: nginx
  image_tag: latest
  host_port: 8080
  container_port: 80
  database_url: 'postgres://{{ database_user }}:{{ database_password }}@db:5432/mydb'
  database_user: admin
  database_password: secret
  ```

### Set Environment Variables (Optional)

- Environment variables can override variables defined in `variables.yaml`.
- Useful for sensitive data such as passwords.
- **Setting Environment Variables in GitHub**:

  1. Go to your repository on GitHub.
  2. Navigate to **Settings > Secrets and variables > Actions**.
  3. Click **New repository variable**.
  4. Add your variable name and value.

- **Example Variables**:

  - `DATABASE_PASSWORD`: `supersecretpassword`
  - `IMAGE_TAG`: `1.0.0`

### Commit and Push

- After customising your templates and variables, commit and push your changes:

  ```bash
  git add .
  git commit -m "Customised templates and variables"
  git push origin main
  ```

- The GitHub Actions workflow will automatically generate `docker-compose.yaml` and `stack.env` and commit them back to your repository.

### Configure Portainer

- In Portainer, set up a GitOps stack deployment pointing to your repository.
- **Steps**:

  1. Log in to your Portainer instance.
  2. Navigate to **Stacks** and click **Add stack**.
  3. Choose **Deploy a stack from a git repository**.
  4. Enter your repository URL and branch name.
  5. Specify the **Compose path** (e.g., `docker-compose.yaml`).
  6. Provide the **Environment file path** (e.g., `stack.env`).
  7. Deploy the stack.

---

## Files and Their Purpose

### `template/docker-compose.yaml.j2`

This is a [Jinja2](https://jinja.palletsprojects.com/en/3.0.x/) template for your Docker Compose file. It allows you to use variables from `variables.yaml` and environment variables to customise your stack configuration.

**Example Contents**:

```yaml
version: '3.8'
services:
  {{ service_name }}:
    image: '{{ image_name }}:{{ image_tag }}'
    deploy:
      replicas: {{ replicas }}
      update_config:
        parallelism: 2
        delay: 10s
    ports:
      - '{{ host_port }}:{{ container_port }}'
    environment:
      - DATABASE_URL={{ database_url }}
```

### `template/environment.j2`

This is a Jinja2 template for your environment variables file. It's useful for defining variables that your Docker services might need at runtime.

**Example Contents**:

```env
DATABASE_USER={{ database_user }}
DATABASE_PASSWORD={{ database_password }}
```

### `template/variables.yaml`

This YAML file contains the default values for your template variables.

**Example Contents**:

```yaml
service_name: web
image_name: nginx
image_tag: latest
host_port: 8080
container_port: 80
database_url: 'postgres://{{ database_user }}:{{ database_password }}@db:5432/mydb'
database_user: admin
database_password: changeme
replicas: 3
```

### `render_templates.py`

This Python script renders the Jinja2 templates using the variables provided in `variables.yaml` and environment variables.

**Contents**:

```python
#!/usr/bin/env python3
"""
Script to render Jinja2 templates for Docker Compose and environment files.

Author: Troy Kelly, @troykelly, troy@aperim.com
Date: Monday, 16 September 2024
"""

import os
import sys
import yaml
from typing import Dict, Any
from jinja2 import Environment, FileSystemLoader, Template
import signal
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_variables() -> Dict[str, Any]:
    """Load variables from variables.yaml and environment variables.

    Returns:
        Dictionary of variables for templates.
    """
    variables: Dict[str, Any] = {}
    try:
        # Load variables from YAML file
        with open('template/variables.yaml', 'r', encoding='utf-8') as file:
            variables = yaml.safe_load(file)
        logger.info("Loaded variables from variables.yaml")
    except FileNotFoundError:
        logger.warning("variables.yaml not found. Proceeding without it.")

    # Override with environment variables
    for key in os.environ:
        variables[key.lower()] = os.environ[key]
    logger.info("Environment variables loaded and overridden if necessary")

    return variables


def render_template(template_name: str, variables: Dict[str, Any], output_path: str) -> None:
    """Render a Jinja2 template to an output file.

    Args:
        template_name: Name of the template file.
        variables: Variables to use in rendering.
        output_path: Path to the output file.
    """
    env = Environment(loader=FileSystemLoader('template'), trim_blocks=True, lstrip_blocks=True)
    template: Template = env.get_template(template_name)
    output: str = template.render(variables)

    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(output)
    logger.info(f"Rendered {template_name} to {output_path}")


def main() -> None:
    """Main function to render templates."""
    variables = load_variables()
    render_template('docker-compose.yaml.j2', variables, 'docker-compose.yaml')
    render_template('environment.j2', variables, 'stack.env')


def handle_signal(signal_number: int, frame) -> None:
    """Handle termination signals.

    Args:
        signal_number: The signal number.
        frame: The current stack frame.
    """
    logger.info(f"Received signal {signal_number}. Exiting gracefully.")
    sys.exit(0)


if __name__ == "__main__":
    # Handle termination signals
    signal.signal(signal.SIGINT, handle_signal)    # Ctrl+C
    signal.signal(signal.SIGTERM, handle_signal)   # Termination
    try:
        main()
    except Exception as e:
        logger.exception("An error occurred during template rendering.")
        sys.exit(1)
```

**Key Points**:

- Loads variables from `variables.yaml` and environment variables (with environment variables taking precedence).
- Renders the templates and outputs `docker-compose.yaml` and `stack.env`.
- Handles exceptions and signals gracefully.
- Uses fully typed variables and functions as per the Google Python Style Guide.

### GitHub Actions Workflow

The GitHub Actions workflow automates the generation of your stack files whenever there's a push or pull request to the repository.

**`/.github/workflows/generate-stack-files.yml`**:

```yaml
name: Generate Stack Files

on:
  push:
    branches:
      - '**'
  pull_request:
    branches:
      - '**'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      # Step 1: Check out the repository.
      - name: Check out repository
        uses: actions/checkout@v3

      # Step 2: Set up Python environment.
      - name: Set up Python 3.8
        uses: actions/setup-python@v4
        with:
          python-version: '3.8'

      # Step 3: Install dependencies.
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install PyYAML Jinja2

      # Step 4: Render templates.
      - name: Render templates
        run: |
          python render_templates.py

      # Step 5: Configure Git user.
      - name: Set Git user
        run: |
          git config --local user.name "GitHub Action"
          git config --local user.email "action@github.com"

      # Step 6: Commit and push changes.
      - name: Commit and push changes
        run: |
          git add docker-compose.yaml stack.env
          if git diff --cached --quiet; then
            echo "No changes to commit."
          else
            git commit -m "Auto-generated stack files [skip ci]"
            git push origin HEAD:${{ github.ref }}
          fi
```

**Key Features**:

- **Triggers**: Runs on pushes and pull requests to any branch.
- **Steps**:
  1. Checks out the repository.
  2. Sets up Python 3.8.
  3. Installs required Python packages (`PyYAML` and `Jinja2`).
  4. Executes the `render_templates.py` script.
  5. Configures Git user for committing.
  6. Commits and pushes the generated files if there are changes.

---

## Additional Notes

### Environment Variables Precedence

- Environment variables take precedence over variables defined in `variables.yaml`.
- This allows for secure handling of sensitive data (e.g., passwords) using GitHub Secrets.
- Environment variable names are case-insensitive in this context.

### Handling Secrets

- **Do not store sensitive information** such as passwords or API keys in `variables.yaml`.
- Use GitHub Secrets or repository variables to securely pass sensitive data to the workflow.

### Customising the Workflow

- You can modify the GitHub Actions workflow to fit your needs.
- For example, you can:
  - Add steps to run tests or linters.
  - Modify the Python version.
  - Change the trigger conditions.

### Error Handling

- The `render_templates.py` script includes exception handling and will exit gracefully on errors.
- Logs are output to help debug if the rendering process fails.
- Signals such as `SIGINT` and `SIGTERM` are caught to ensure the script exits cleanly.

---

## Support

For any issues, questions, or suggestions, please contact:

**Author**: Troy Kelly  
**GitHub**: [@troykelly](https://github.com/troykelly)  
**Email**: troy@aperim.com  

---

## License

This project is licensed under the **GNU LESSER GENERAL PUBLIC LICENSE**. See the [LICENSE](LICENSE) file for details.