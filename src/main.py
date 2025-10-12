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
            print(f"Identified module {lAppLaunch}")

        except (ValueError, IndexError):
            print(f"Error on arguments {args}")

        except OSError as e:
            print(f"Error launching application as separate process: {e}")
            return

    if lAppLaunch == "test":
        if "--module" in args:
            lModIndex = args.index("--module")
            lModLaunch = args[lModIndex + 1]

        try:
            lCmd = [sys.executable, f".\\src\\test\\test_{lModLaunch}.py"]
            subprocess.Popen(lCmd)

        except Exception as e:
            print(f"Failed to load tes': {e}")
            return


    else:
        try:
            lModule = importlib.import_module(f"{lAppLaunch}.main")
            print(f"Module {lAppLaunch}.main loaded")

        except Exception as e:
            print(f"Failed to load dashboard from '{lAppLaunch}': {e}")
            return

        lExitCode = lModule.main()

    sys.exit(lExitCode)


if __name__ == "__main__":
    main()
