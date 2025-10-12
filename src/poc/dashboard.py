import subprocess
import sys

from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QCloseEvent, QIcon, QMouseEvent
from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QLabel,
    QMainWindow,
    QMenu,
    QStyle,
    QSystemTrayIcon,
    QVBoxLayout,
    QWidget,
)


# --- 1. THE CUSTOM LAUNCH CARD COMPONENT ---
class LaunchCard(QWidget):
    clicked = Signal()

    def __init__(self, name, icon_path, parent=None):
        super().__init__(parent)
        self.setObjectName("LaunchCard")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumWidth(160)

        # Icon Label Setup (Using default icon for simplicity)
        style = QApplication.instance().style()
        icon = style.standardIcon(QStyle.StandardPixmap.SP_DriveHDIcon)
        pixmap = icon.pixmap(QSize(64, 64))
        self.icon_label = QLabel(pixmap=pixmap, alignment=Qt.AlignCenter)
        self.icon_label.setObjectName("LaunchCardIcon")

        # Text Label Setup
        self.text_label = QLabel(name, alignment=Qt.AlignCenter)
        self.text_label.setObjectName("LaunchCardText")
        self.text_label.setWordWrap(True)

        # Layout
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.addWidget(self.icon_label)
        layout.addWidget(self.text_label)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()


# --- 2. THE LAUNCH TILE WRAPPER (Unchanged) ---
class LaunchTile(QWidget):
    def __init__(self, name, icon_path, launch_callback):
        super().__init__()

        self.card = LaunchCard(name, icon_path)
        self.card.clicked.connect(launch_callback)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.card)


# --- 3. THE INDEPENDENT APPLICATION FORM (Target App) ---
class IndependentApp(QMainWindow):
    """
    This window runs in its own separate Python process and QApplication.
    """

    def __init__(self, app_name):
        super().__init__()
        self.setWindowTitle(f"Independent App: {app_name}")
        self.setGeometry(300, 300, 400, 300)

        style_sheet = """
        QMainWindow { background-color: #E0FFFF; }
        QLabel { color: #008080; font-size: 14pt; }
        """
        self.setStyleSheet(style_sheet)

        central_widget = QLabel(f"Launched App: {app_name}. (PID: {QApplication.instance().applicationPid()})")
        central_widget.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(central_widget)


# --- 4. THE DASHBOARD WINDOW (The Launcher) ---
class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modern Flat Launcher Dashboard 🚀")
        self.setGeometry(100, 100, 700, 500)

        self.active_apps = {}
        self._setup_ui()
        self._setup_tray_icon()
        self.apply_qss()

    def _setup_ui(self):
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(main_widget)

        # --- Section Header (Contrast Fix) ---
        header_label = QLabel("Main Applications")
        main_layout.addWidget(header_label)

        # Wrapper for Grid (provides left/right padding)
        grid_wrapper = QWidget()
        grid_wrapper_layout = QVBoxLayout(grid_wrapper)
        grid_wrapper_layout.setContentsMargins(30, 30, 30, 30)

        app_grid = QGridLayout()
        app_grid.setHorizontalSpacing(20)
        app_grid.setVerticalSpacing(20)

        # Tiles: NOTE: app_names are now strings passed to the new process
        tile_a = LaunchTile("App Alpha: Project Manager", "icon_alpha.png", lambda: self._launch_app("App Alpha"))
        app_grid.addWidget(tile_a, 0, 0)

        tile_b = LaunchTile("App Beta: Data Viewer", "icon_beta.png", lambda: self._launch_app("App Beta"))
        app_grid.addWidget(tile_b, 0, 1)

        tile_c = LaunchTile("Utility Tool Gamma", "icon_gamma.png", lambda: self._launch_app("App Gamma"))
        app_grid.addWidget(tile_c, 1, 0)

        grid_wrapper_layout.addLayout(app_grid)
        main_layout.addWidget(grid_wrapper)
        main_layout.addStretch(1)

    def _setup_tray_icon(self):
        style = QApplication.instance().style()
        icon = style.standardIcon(QStyle.StandardPixmap.SP_DesktopIcon)
        self.tray_icon = QSystemTrayIcon(icon, self)
        self.tray_icon.setToolTip("Modern Launcher")

        menu = QMenu()
        show_action = menu.addAction("Show Dashboard")
        show_action.triggered.connect(self.showNormal)
        exit_action = menu.addAction("Exit")
        exit_action.triggered.connect(QApplication.instance().quit)
        self.tray_icon.setContextMenu(menu)
        self.tray_icon.show()

    # --- LAUNCH LOGIC: USE SUBPROCESS FOR INDEPENDENCE ---
    def _launch_app(self, app_name):
        # Command: [Python executable path, current script path, argument flag, app name]
        command = [sys.executable, sys.argv[0], "--launch-app", app_name]
        print(command)

        # Launch the new application in a separate process
        # This achieves true independence.
        try:
            subprocess.Popen(command)
        except OSError as e:
            print(f"Error launching application as separate process: {e}")
            return

        self.hide()

    def closeEvent(self, event: QCloseEvent):
        self.hide()
        event.ignore()

    def apply_qss(self):
        style_sheet = """
        /* GLOBAL STYLES */
        QMainWindow { background-color: #D8E0E5; }

        /* LAUNCH CARDS */
        QWidget#LaunchCard {
            background-color: #FFFFFF;
            color: #333333;
            border: 1px solid #CCCCCC;
            border-radius: 8px;
        }

        /* TEXT */
        QLabel#LaunchCardText {
            font-size: 11pt;
            font-weight: 500;
            background-color: transparent;
        }

        /* INTERACTIVITY */
        QWidget#LaunchCard:hover {
            background-color: #EAF2FF;
            border: 1px solid #4A90E2;
        }
        QWidget#LaunchCard:pressed {
            background-color: #DDEEFC;
        }

        /* SECTION HEADERS (Inner Contrast) */
        QLabel {
            font-size: 16pt;
            font-weight: bold;
            color: #444444;
            padding: 10px 30px;
            margin-top: 0;
            background-color: #FFFFFF; /* High contrast band */
            border-bottom: 1px solid #CCCCCC;
        }
        """
        self.setStyleSheet(style_sheet)


# --- 5. EXECUTION MODEL: RUNS DASHBOARD OR LAUNCHED APP ---
def run_app():
    """Entry point for the script, determines whether to run Dashboard or App."""

    app = QApplication(sys.argv)
    app_to_launch = None

    # Check for the argument passed by the subprocess launch
    if "--launch-app" in sys.argv:
        try:
            # Get the app name from the argument list
            index = sys.argv.index("--launch-app")
            app_to_launch = sys.argv[index + 1]
        except (ValueError, IndexError):
            pass  # No valid app name argument

    if app_to_launch:
        # RUN INDEPENDENT APPLICATION
        window = IndependentApp(app_to_launch)
        window.show()
    else:
        # RUN DASHBOARD (DEFAULT)
        if not QSystemTrayIcon.isSystemTrayAvailable():
            print("System tray not available.")

        window = Dashboard()
        window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    run_app()
