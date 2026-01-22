"""
Input Workspace - For loading and managing input images/data.
Organized with tabs for different input-related functions.
"""

from PyQt6.QtWidgets import QTabWidget
from PyQt6.QtCore import Qt

from .base_workspace import BaseWorkspace
from .input_tabs import FileImportTab
from ...utils.constants import WorkspaceID, Colors


class InputWorkspace(BaseWorkspace):
    """
    Workspace for handling input operations.
    
    Uses a tabbed interface to organize different input functions:
    - File Import: Select and import image files
    - (Future tabs can be added here)
    """
    
    @property
    def workspace_id(self) -> str:
        return WorkspaceID.INPUT
    
    @property
    def workspace_title(self) -> str:
        return "Input"
    
    def _init_ui(self):
        """Initialize the Input workspace UI with tabs."""
        # Remove default margins since tabs will handle spacing
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet(f"""
            QTabWidget::pane {{
                border: none;
                background-color: {Colors.BACKGROUND};
            }}
            QTabBar::tab {{
                background-color: {Colors.SECONDARY};
                color: {Colors.TEXT_LIGHT};
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                font-size: 12px;
                font-weight: bold;
            }}
            QTabBar::tab:selected {{
                background-color: {Colors.ACTIVE};
                color: {Colors.TEXT_LIGHT};
            }}
            QTabBar::tab:hover:!selected {{
                background-color: {Colors.HOVER};
            }}
        """)
        
        # Create and add tabs
        self._create_tabs()
        
        # Add tab widget to layout
        self.main_layout.addWidget(self.tab_widget)
        
        # Connect tab change signal
        self.tab_widget.currentChanged.connect(self._on_tab_changed)
    
    def _create_tabs(self):
        """Create and add all tabs to the tab widget."""
        # File Import tab
        self.file_import_tab = FileImportTab()
        self.tab_widget.addTab(self.file_import_tab, self.file_import_tab.tab_name)
        
        # Future tabs can be added here:
        # self.some_other_tab = SomeOtherTab()
        # self.tab_widget.addTab(self.some_other_tab, self.some_other_tab.tab_name)
    
    def _on_tab_changed(self, index: int):
        """Handle tab change events."""
        # Notify the previous tab that it's being deselected
        for i in range(self.tab_widget.count()):
            tab = self.tab_widget.widget(i)
            if hasattr(tab, 'on_tab_deselected') and i != index:
                tab.on_tab_deselected()
        
        # Notify the new tab that it's being selected
        current_tab = self.tab_widget.widget(index)
        if hasattr(current_tab, 'on_tab_selected'):
            current_tab.on_tab_selected()
    
    def on_activated(self):
        """Called when Input workspace becomes active."""
        # Notify current tab
        current_tab = self.tab_widget.currentWidget()
        if hasattr(current_tab, 'on_tab_selected'):
            current_tab.on_tab_selected()
    
    def get_selected_files(self) -> list[str]:
        """
        Get the list of selected files from the File Import tab.
        
        Returns:
            list[str]: List of selected file paths.
        """
        return self.file_import_tab.get_selected_files()
