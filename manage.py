#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os  # Import the os module for interacting with the operating system
import sys  # Import the sys module for access to system-specific parameters and functions

def main():
    """Run administrative tasks."""
    # Set the default settings module for the Django project
    # This ensures that the settings specified in 'talking_box_project.settings' are used
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'talking_box_project.settings')

    try:
        # Import the Django management module
        # This module provides the command-line utility to execute Django management commands
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Raise an ImportError if Django is not installed or not available in the PYTHONPATH
        # This is a common issue if the virtual environment is not activated
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Execute the Django management command specified in the command line arguments
    # sys.argv contains the command-line arguments passed to the script
    execute_from_command_line(sys.argv)

# Check if the script is being run directly (not imported as a module)
if __name__ == '__main__':
    # Call the main function to handle the administrative tasks
    main()
