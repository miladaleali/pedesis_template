#!/usr/bin/env python
"""Pedesis's command-line utility for administrative tasks."""
import os


def main():
    """Run administrative tasks."""
    os.environ.setdefault('PEDESIS_SETTINGS_MODULE', 'app.caisssa.settings')
    try:
        from pedesis.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Pedesis. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line()


if __name__ == '__main__':
    main()
