#!/usr/bin/env python3
"""
Cell Image Analyzer - Main Entry Point

A GUI-based platform for cell image analysis.

Usage:
    python main.py
"""

import sys


def main() -> int:
    """
    Main entry point for the application.
    
    Returns:
        int: Exit code (0 for success, non-zero for errors).
    """
    from src.app import create_app
    
    app = create_app()
    return app.run()


if __name__ == "__main__":
    sys.exit(main())

