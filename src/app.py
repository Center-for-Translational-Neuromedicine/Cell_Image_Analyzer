"""
Application orchestrator - Initializes and runs the application.
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

from .gui.main_window import MainWindow
from .utils.constants import APP_NAME


class CellImageAnalyzerApp:
    """
    Main application class that orchestrates the application lifecycle.
    
    This class is responsible for:
    - Creating the QApplication instance
    - Initializing the main window
    - Running the event loop
    """
    
    def __init__(self):
        """Initialize the application."""
        self._app: QApplication | None = None
        self._main_window: MainWindow | None = None
    
    def run(self) -> int:
        """
        Run the application.
        
        Returns:
            int: The exit code from the application event loop.
        """
        # Create QApplication instance
        self._app = QApplication(sys.argv)
        self._app.setApplicationName(APP_NAME)
        
        # Apply global application styles
        self._apply_global_styles()
        
        # Create and show main window
        self._main_window = MainWindow()
        self._main_window.show()
        
        # Start event loop
        return self._app.exec()
    
    def _apply_global_styles(self):
        """Apply global application styles."""
        if self._app is None:
            return
        
        # Global stylesheet for consistent look
        self._app.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            
            QToolTip {
                background-color: #2C3E50;
                color: white;
                border: 1px solid #34495E;
                padding: 5px;
                border-radius: 3px;
            }
        """)


def create_app() -> CellImageAnalyzerApp:
    """
    Factory function to create the application instance.
    
    Returns:
        CellImageAnalyzerApp: A new application instance.
    """
    return CellImageAnalyzerApp()

