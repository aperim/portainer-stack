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
        variables[key] = os.environ[key]
    logger.info("Environment variables loaded and overridden if necessary")

    return variables


def render_template(template_name: str, variables: Dict[str, Any], output_path: str) -> None:
    """Render a Jinja2 template to an output file.

    Args:
        template_name: Name of the template file.
        variables: Variables to use in rendering.
        output_path: Path to the output file.
    """
    env = Environment(loader=FileSystemLoader('template'),
                      trim_blocks=True, lstrip_blocks=True)
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
