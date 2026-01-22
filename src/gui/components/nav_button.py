"""
Custom Navigation Button component for the sidebar navigation.
"""

from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import pyqtSignal

from ...utils.constants import Colors


class NavButton(QPushButton):
    """
    A custom styled navigation button for the sidebar.
    
    Features:
    - Toggle behavior (active/inactive states)
    - Custom styling with hover effects
    - Emits signal when clicked with workspace ID
    """
    
    # Signal emitted when button is clicked, carries workspace_id
    workspace_selected = pyqtSignal(str)
    
    def __init__(self, text: str, workspace_id: str, parent=None):
        """
        Initialize the navigation button.
        
        Args:
            text: The button label text.
            workspace_id: The ID of the workspace this button activates.
            parent: Parent widget.
        """
        super().__init__(text, parent)
        self.workspace_id = workspace_id
        self._is_active = False
        
        self._setup_style()
        self._connect_signals()
    
    def _setup_style(self):
        """Apply the custom styling to the button."""
        self.setFixedHeight(50)
        self.setCursor(self.cursor())
        self._update_style()
    
    def _connect_signals(self):
        """Connect button signals."""
        self.clicked.connect(self._on_clicked)
    
    def _on_clicked(self):
        """Handle button click."""
        if not self._is_active:
            self.workspace_selected.emit(self.workspace_id)
    
    @property
    def is_active(self) -> bool:
        """Return whether this button is currently active."""
        return self._is_active
    
    def set_active(self, active: bool):
        """
        Set the active state of the button.
        
        Args:
            active: True to set as active, False for inactive.
        """
        self._is_active = active
        self._update_style()
    
    def _update_style(self):
        """Update the button style based on active state."""
        if self._is_active:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {Colors.ACTIVE};
                    color: {Colors.TEXT_LIGHT};
                    border: none;
                    border-radius: 6px;
                    font-size: 14px;
                    font-weight: bold;
                    padding: 10px 20px;
                    text-align: center;
                }}
                QPushButton:hover {{
                    background-color: {Colors.ACTIVE};
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {Colors.SECONDARY};
                    color: {Colors.TEXT_LIGHT};
                    border: none;
                    border-radius: 6px;
                    font-size: 14px;
                    font-weight: bold;
                    padding: 10px 20px;
                    text-align: center;
                }}
                QPushButton:hover {{
                    background-color: {Colors.HOVER};
                }}
            """)

