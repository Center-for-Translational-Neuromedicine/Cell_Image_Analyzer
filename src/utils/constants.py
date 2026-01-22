"""
Application-wide constants and configuration values.
"""

# Application Info
APP_NAME = "Cell Image Analyzer"
APP_VERSION = "0.1.0"

# Window Settings
WINDOW_MIN_WIDTH = 1024
WINDOW_MIN_HEIGHT = 768
WINDOW_DEFAULT_WIDTH = 1280
WINDOW_DEFAULT_HEIGHT = 800

# Navigation Panel Settings
NAV_PANEL_WIDTH = 160

# Workspace Identifiers
class WorkspaceID:
    """Enumeration of workspace identifiers."""
    INPUT = "input"
    ANALYSIS = "analysis"
    OUTPUT = "output"

# Default workspace on startup
DEFAULT_WORKSPACE = WorkspaceID.INPUT

# Color Palette (can be customized later)
class Colors:
    """Application color scheme."""
    PRIMARY = "#2C3E50"       # Dark blue-gray
    SECONDARY = "#34495E"     # Lighter blue-gray
    ACCENT = "#3498DB"        # Bright blue
    BACKGROUND = "#ECF0F1"    # Light gray
    TEXT = "#2C3E50"          # Dark text
    TEXT_LIGHT = "#FFFFFF"    # Light text
    BORDER = "#BDC3C7"        # Gray border
    HOVER = "#2980B9"         # Hover blue
    ACTIVE = "#1ABC9C"        # Teal for active state

