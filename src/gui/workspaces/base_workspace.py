"""
Base workspace class that all workspaces inherit from.
Provides a consistent interface and common functionality.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt


class BaseWorkspace(QWidget):
    """
    Base class for all workspace panels.
    
    Each workspace (INPUT, ANALYSIS, OUTPUT) should inherit from this class
    and implement the required methods.
    
    Subclasses MUST implement:
    - _init_ui(): Initialize the workspace UI components
    - workspace_id (property): Return the unique identifier
    - workspace_title (property): Return the display title
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_base_layout()
        self._init_ui()
    
    def _setup_base_layout(self):
        """Set up the base layout for the workspace."""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(10)
    
    def _init_ui(self):
        """
        Initialize the workspace UI components.
        Must be overridden by subclasses.
        """
        raise NotImplementedError("Subclasses must implement _init_ui()")
    
    @property
    def workspace_id(self) -> str:
        """
        Return the unique identifier for this workspace.
        Must be overridden by subclasses.
        """
        raise NotImplementedError("Subclasses must implement workspace_id property")
    
    @property
    def workspace_title(self) -> str:
        """
        Return the display title for this workspace.
        Must be overridden by subclasses.
        """
        raise NotImplementedError("Subclasses must implement workspace_title property")
    
    def on_activated(self):
        """
        Called when this workspace becomes the active workspace.
        Override in subclasses if needed.
        """
        pass
    
    def on_deactivated(self):
        """
        Called when this workspace is no longer the active workspace.
        Override in subclasses if needed.
        """
        pass
    
    def _create_header(self, title: str) -> QLabel:
        """
        Create a styled header label for the workspace.
        
        Args:
            title: The header text to display.
            
        Returns:
            QLabel: A styled header label.
        """
        header = QLabel(title)
        header.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #2C3E50;
                padding-bottom: 10px;
                border-bottom: 2px solid #3498DB;
            }
        """)
        header.setAlignment(Qt.AlignmentFlag.AlignLeft)
        return header
