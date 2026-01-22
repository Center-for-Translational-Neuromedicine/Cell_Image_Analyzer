"""
File Import Tab - For selecting and importing image files.
"""

import os
from pathlib import Path
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QComboBox, QListWidget,
    QListWidgetItem, QFrame, QFileDialog, QAbstractItemView
)
from PyQt6.QtCore import Qt, pyqtSignal

from .base_tab import BaseTab
from ....utils.settings import settings
from ....utils.constants import Colors


class FileImportTab(BaseTab):
    """
    Tab for importing image files.
    
    Features:
    - Directory browser with persistent last-used directory
    - File format filter dropdown
    - Scrollable file list with checkboxes
    - Select All / Clear All functionality
    """
    
    # Signal emitted when file selection changes
    files_selected = pyqtSignal(list)
    
    # Supported file formats
    FILE_FORMATS = [
        ("TIFF Images", [".tif", ".tiff"]),
        ("PNG Images", [".png"]),
        ("JPEG Images", [".jpg", ".jpeg"]),
        ("ND2 Images", [".nd2"]),
        ("All Supported", [".tif", ".tiff", ".png", ".jpg", ".jpeg", ".nd2"]),
    ]
    
    @property
    def tab_name(self) -> str:
        return "File Import"
    
    def _init_ui(self):
        """Initialize the File Import tab UI."""
        # Directory section
        self._create_directory_section()
        
        # File format filter section
        self._create_filter_section()
        
        # File list section
        self._create_file_list_section()
        
        # Selection controls section
        self._create_selection_controls()
        
        # Initialize with last used directory
        self._current_directory = settings.get_last_directory()
        self._update_directory_display()
        self._refresh_file_list()
    
    def _create_directory_section(self):
        """Create the directory display and browse button."""
        # Section label
        dir_label = QLabel("📁 Current Directory:")
        dir_label.setStyleSheet(f"""
            QLabel {{
                font-size: 13px;
                font-weight: bold;
                color: {Colors.TEXT};
            }}
        """)
        self.main_layout.addWidget(dir_label)
        
        # Directory row
        dir_row = QHBoxLayout()
        dir_row.setSpacing(10)
        
        # Directory path display
        self.directory_input = QLineEdit()
        self.directory_input.setReadOnly(True)
        self.directory_input.setStyleSheet(f"""
            QLineEdit {{
                padding: 8px 12px;
                border: 1px solid {Colors.BORDER};
                border-radius: 4px;
                background-color: #FFFFFF;
                font-size: 12px;
                color: {Colors.TEXT};
            }}
        """)
        dir_row.addWidget(self.directory_input, 1)
        
        # Browse button
        self.browse_button = QPushButton("Browse")
        self.browse_button.setFixedWidth(100)
        self.browse_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.browse_button.setStyleSheet(f"""
            QPushButton {{
                padding: 8px 16px;
                background-color: {Colors.ACCENT};
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 12px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {Colors.HOVER};
            }}
            QPushButton:pressed {{
                background-color: {Colors.PRIMARY};
            }}
        """)
        self.browse_button.clicked.connect(self._on_browse_clicked)
        dir_row.addWidget(self.browse_button)
        
        self.main_layout.addLayout(dir_row)
    
    def _create_filter_section(self):
        """Create the file format filter dropdown."""
        # Section label
        filter_label = QLabel("🔍 File Format:")
        filter_label.setStyleSheet(f"""
            QLabel {{
                font-size: 13px;
                font-weight: bold;
                color: {Colors.TEXT};
                margin-top: 10px;
            }}
        """)
        self.main_layout.addWidget(filter_label)
        
        # Filter dropdown
        self.format_combo = QComboBox()
        self.format_combo.setFixedWidth(200)
        self.format_combo.setStyleSheet(f"""
            QComboBox {{
                padding: 8px 12px;
                border: 1px solid {Colors.BORDER};
                border-radius: 4px;
                background-color: #FFFFFF;
                font-size: 12px;
                color: {Colors.TEXT};
            }}
            QComboBox:hover {{
                border-color: {Colors.ACCENT};
            }}
            QComboBox::drop-down {{
                border: none;
                width: 30px;
            }}
            QComboBox::down-arrow {{
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid {Colors.TEXT};
                margin-right: 10px;
            }}
            QComboBox QAbstractItemView {{
                background-color: #FFFFFF;
                border: 1px solid {Colors.BORDER};
                selection-background-color: {Colors.ACCENT};
                selection-color: white;
            }}
        """)
        
        # Add format options
        for format_name, _ in self.FILE_FORMATS:
            self.format_combo.addItem(format_name)
        
        # Select "All Supported" by default
        self.format_combo.setCurrentIndex(len(self.FILE_FORMATS) - 1)
        
        # Connect signal
        self.format_combo.currentIndexChanged.connect(self._on_format_changed)
        
        self.main_layout.addWidget(self.format_combo)
    
    def _create_file_list_section(self):
        """Create the scrollable file list with checkboxes."""
        # Section label
        files_label = QLabel("📄 Available Files:")
        files_label.setStyleSheet(f"""
            QLabel {{
                font-size: 13px;
                font-weight: bold;
                color: {Colors.TEXT};
                margin-top: 10px;
            }}
        """)
        self.main_layout.addWidget(files_label)
        
        # File list widget
        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.file_list.setStyleSheet(f"""
            QListWidget {{
                border: 1px solid {Colors.BORDER};
                border-radius: 4px;
                background-color: #FFFFFF;
                font-size: 12px;
                padding: 5px;
            }}
            QListWidget::item {{
                padding: 8px;
                border-bottom: 1px solid #F0F0F0;
            }}
            QListWidget::item:hover {{
                background-color: #F8F9FA;
            }}
        """)
        self.file_list.setMinimumHeight(250)
        
        # Connect item changed signal
        self.file_list.itemChanged.connect(self._on_item_changed)
        
        self.main_layout.addWidget(self.file_list, 1)  # stretch factor 1
    
    def _create_selection_controls(self):
        """Create the selection count and control buttons."""
        # Control row
        control_row = QHBoxLayout()
        control_row.setSpacing(10)
        
        # Selected count label
        self.selected_label = QLabel("Selected: 0 files")
        self.selected_label.setStyleSheet(f"""
            QLabel {{
                font-size: 12px;
                color: {Colors.TEXT};
            }}
        """)
        control_row.addWidget(self.selected_label)
        
        control_row.addStretch()
        
        # Select All button
        self.select_all_button = QPushButton("Select All")
        self.select_all_button.setFixedWidth(100)
        self.select_all_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.select_all_button.setStyleSheet(f"""
            QPushButton {{
                padding: 6px 12px;
                background-color: {Colors.SECONDARY};
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 11px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {Colors.HOVER};
            }}
        """)
        self.select_all_button.clicked.connect(self._on_select_all)
        control_row.addWidget(self.select_all_button)
        
        # Clear All button
        self.clear_all_button = QPushButton("Clear All")
        self.clear_all_button.setFixedWidth(100)
        self.clear_all_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clear_all_button.setStyleSheet(f"""
            QPushButton {{
                padding: 6px 12px;
                background-color: #E74C3C;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 11px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #C0392B;
            }}
        """)
        self.clear_all_button.clicked.connect(self._on_clear_all)
        control_row.addWidget(self.clear_all_button)
        
        self.main_layout.addLayout(control_row)
    
    def _update_directory_display(self):
        """Update the directory input field."""
        self.directory_input.setText(self._current_directory)
    
    def _get_current_extensions(self) -> list[str]:
        """Get the list of extensions for the current filter."""
        index = self.format_combo.currentIndex()
        if 0 <= index < len(self.FILE_FORMATS):
            return self.FILE_FORMATS[index][1]
        return []
    
    def _refresh_file_list(self):
        """Refresh the file list based on current directory and filter."""
        self.file_list.clear()
        
        if not os.path.isdir(self._current_directory):
            return
        
        extensions = self._get_current_extensions()
        
        try:
            # Get all files in directory
            files = []
            for filename in os.listdir(self._current_directory):
                filepath = os.path.join(self._current_directory, filename)
                if os.path.isfile(filepath):
                    ext = os.path.splitext(filename)[1].lower()
                    if ext in extensions:
                        files.append(filename)
            
            # Sort files alphabetically
            files.sort(key=str.lower)
            
            # Add files to list
            for filename in files:
                item = QListWidgetItem(filename)
                item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                item.setCheckState(Qt.CheckState.Unchecked)
                self.file_list.addItem(item)
        
        except PermissionError:
            # Handle permission errors gracefully
            pass
        
        self._update_selected_count()
    
    def _update_selected_count(self):
        """Update the selected files count label."""
        count = self._get_selected_count()
        self.selected_label.setText(f"Selected: {count} file{'s' if count != 1 else ''}")
    
    def _get_selected_count(self) -> int:
        """Get the number of selected files."""
        count = 0
        for i in range(self.file_list.count()):
            item = self.file_list.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                count += 1
        return count
    
    def _on_browse_clicked(self):
        """Handle browse button click."""
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Directory",
            self._current_directory,
            QFileDialog.Option.ShowDirsOnly
        )
        
        if directory:
            self._current_directory = directory
            settings.set_last_directory(directory)
            self._update_directory_display()
            self._refresh_file_list()
    
    def _on_format_changed(self, index: int):
        """Handle file format filter change."""
        self._refresh_file_list()
    
    def _on_item_changed(self, item: QListWidgetItem):
        """Handle file item checkbox change."""
        self._update_selected_count()
        self._emit_selection_changed()
    
    def _on_select_all(self):
        """Select all files in the list."""
        for i in range(self.file_list.count()):
            item = self.file_list.item(i)
            item.setCheckState(Qt.CheckState.Checked)
        self._update_selected_count()
        self._emit_selection_changed()
    
    def _on_clear_all(self):
        """Clear all file selections."""
        for i in range(self.file_list.count()):
            item = self.file_list.item(i)
            item.setCheckState(Qt.CheckState.Unchecked)
        self._update_selected_count()
        self._emit_selection_changed()
    
    def _emit_selection_changed(self):
        """Emit signal with current selection."""
        selected_files = self.get_selected_files()
        self.files_selected.emit(selected_files)
    
    def get_selected_files(self) -> list[str]:
        """
        Get the list of selected file paths.
        
        Returns:
            list[str]: Full paths to selected files.
        """
        selected = []
        for i in range(self.file_list.count()):
            item = self.file_list.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                filepath = os.path.join(self._current_directory, item.text())
                selected.append(filepath)
        return selected
    
    def get_data(self) -> dict:
        """Get the current tab data."""
        return {
            "directory": self._current_directory,
            "selected_files": self.get_selected_files(),
            "format_filter": self.format_combo.currentText(),
        }

