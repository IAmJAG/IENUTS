# ==================================================================================
import importlib
import subprocess
import sys

# ==================================================================================
from jAGFx.logger import debug, error, info


def main(args: list = sys.argv):
    lAppLaunch: str = "dashboard"
    lExitCode: int = 0
    if "--launch" in args:
        try:
            lAppIndex = args.index("--launch")
            lAppLaunch = args[lAppIndex + 1]
            debug(f"[dashboard]: Identified module to launch: {lAppLaunch}")

        except (ValueError, IndexError):
            debug(f"Error on arguments {args}")

        except OSError as e:
            debug(f"Error launching application as separate process: {e}")
            return

    if lAppLaunch == "test":
        if "--module" in args:
            lModIndex = args.index("--module")
            lModLaunch = args[lModIndex + 1]

        try:
            lCmd = [sys.executable, f".\\src\\test\\test_{lModLaunch}.py"]
            subprocess.Popen(lCmd)

        except Exception as e:
            debug(f"Failed to load tes': {e}")
            return


    else:
        try:
            lModule = importlib.import_module(f"{lAppLaunch}.main")
            debug(f"[dashboard]: Module {lAppLaunch}.main loaded")

        except Exception as e:
            error(f"Failed to load dashboard from '{lAppLaunch}': {e}", e)
            return

        lExitCode = lModule.main()

    sys.exit(lExitCode)


if __name__ == "__main__":
    main()
