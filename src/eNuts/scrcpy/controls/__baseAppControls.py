from adbutils import AdbDevice, AdbError
from PIL.Image import Image

from jAGFx.logger import debug, error, warning

from ..control import ControlSender


class BaseAppControl(ControlSender):
    def ScreenCapture(self) -> Image:
        return self.Parent.Device.screenshot()

    def OpenApp(self):
        try:
            debug(f"Attempting to open {self.Parent.Title}")
            if self.Parent.PackageName is None:
                warning("Un-identified package.")
                return
            lDevice: AdbDevice = self.Parent.Device
            lDevice.shell(f"monkey -p {self.Parent.PackageName} -c android.intent.category.LAUNCHER 1")

        except AdbError as e:
            warning(f"Error opening app {self.Parent.Title}", e)

        except Exception as e:
            warning(f"An unexpected error occurred opening {self.Parent.Title}", e)

    def CloseApp(self):
        try:
            if self.Parent.PackageName is None:
                warning("Un-identified package.")
                return

            lDevice: AdbDevice = self.Parent.Device
            debug(f"Attempting to stop {self.Parent.PackageName}...")
            lDevice.shell(f"am force-stop {self.Parent.PackageName}")

            debug(f"{self.Parent.Title} should now be stopped.")

        except AdbError as e:
            warning(f"Error closing app {self.Parent.Title}", e)

        except Exception as e:
            warning(f"An unexpected error occurred closing {self.Parent.Title}", e)
