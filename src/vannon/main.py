# ==================================================================================
import ctypes
import ctypes.wintypes
import sys

# ==================================================================================
from PySide6.QtWidgets import QApplication

# ==================================================================================
from jAGFx.configuration import iConfiguration
from jAGFx.dependencyInjection import Provider
from jAGFx.logger import *

# ==================================================================================
from utilities import LoadFonts, LoadQSS, loadConfig

# ==================================================================================
from .configuration import vAnnonConfiguration

# ==================================================================================
from .UI import MainWindow


def main(args=sys.argv):
    loadConfig()
    debug("Logger config loaded VANNON")

    lExitCode: int = 0

    try:
        debug("Configure taskbar icon")
        cfg: vAnnonConfiguration = Provider.Resolve(iConfiguration)
        lAppUserID = f"{cfg.Company}.{cfg.Title}"
        if sys.platform == "win32":
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(ctypes.wintypes.LPWSTR(lAppUserID))

        debug(f"Starting {cfg.AppId}...")
        lApp = QApplication(args)
        debug("Loading resources...")
        LoadFonts()
        LoadQSS(cfg.Style)

        main = MainWindow()
        main.show()

        lExitCode = lApp.exec()

    except KeyboardInterrupt:
        warning("Shutdown requested (ctnrl-c)...")

    except AttributeError as e:
        error("Error: AttributeError", e)

    except Exception as e:
        error("Unhandled exception", e)

    finally:
        info("Saving configuration...")
        sys.exit(lExitCode)


if __name__ == "__main__":
    main()
