import logging
import os
from datetime import datetime
from typing import Optional

import pytz


class DateRotatingFileHandler(logging.FileHandler):
    def __init__(
        self,
        filenameTemplate,
        encoding=None,
        errors=None,
        dateFormat: str = "%Y%m%d",
        maximumBackups: int = 10,
        maximumLogs: int = 5,
        directories: Optional[dict] = None,
        maximumSize: int = 10000000,  # 10 MB default size
        logExtension: str = "log",
        archiveTimeStampFormat: str = "%Y%m%d%H%M%S%",
        archiveRetention: int = 15,  # 15 days
        timezone: str | None = None,  # Add timezone parameter, None
    ):
        directories = (
            {"log": "./logs/", "archive": "./logs/archive"}
            if directories is None
            else directories
        )
        for lDir in directories.values():
            os.makedirs(lDir, exist_ok=True)
        os.makedirs(os.path.join(directories["archive"], "backups"), exist_ok=True)

        self._encoding = encoding
        self._errors = errors

        self._directories: dict[str, str] = directories
        self._maximumLogs: int = (
            1
            if maximumLogs is None
            or not isinstance(maximumLogs, int)
            or maximumLogs < 1
            else maximumLogs
        )
        self._maximumBackups: int = (
            1
            if maximumBackups is None
            or not isinstance(maximumBackups, int)
            or maximumBackups < 1
            else maximumBackups
        )
        self._maximumSize: int = (
            10000000
            if maximumSize is None
            or not isinstance(maximumSize, int)
            or maximumSize < 10000000
            else maximumSize
        )
        self._logfileExtention: str = logExtension
        self._archiveDateFormat: str = archiveTimeStampFormat
        self._archiveRetention: int = archiveRetention

        self._dateFormat: str = dateFormat
        self._filenameTemplate: str = filenameTemplate
        self._baseFilename: str = ""
        self._currentLogPath: str = ""

        self._fileSize: int = 0
        self._timezone = (
            pytz.timezone(timezone) if timezone else datetime.now().astimezone().tzinfo
        )
        self._stream = None
        self._xRotate()

        logging.FileHandler.__init__(
            self,
            self._currentLogPath,
            mode="a",
            encoding=encoding,
            delay=False,
            errors=errors,
        )

    def _getTimeStampedFilename(
        self, template: str, ext: str = "log", datetimeFormat: str = "%Y%m%d"
    ):
        now = datetime.now(self._timezone)  # Use timezone-aware datetime
        return f"{template.format(timestamp=now.strftime(datetimeFormat))}.{ext}"

    def _rotate(self):
        self.close()
        self._xRotate()
        self._open()

    def _xRotate(self):
        self._currentLogPath = os.path.join(
            self._directories["log"],
            self._getTimeStampedFilename(
                self._filenameTemplate, self._logfileExtention, self._dateFormat
            ),
        )
        self._baseFilename = os.path.splitext(self._currentLogPath)[0]

        self.baseFilename = self._currentLogPath

        self._manageArchives()

    def _shiftBackup(self):
        lArchDir = os.path.join(self._directories["log"], "archive", "backups")
        lArchBackup = [
            {"File": f, "Directory": lArchDir}
            for f in os.listdir(lArchDir)
            if f.startswith(self._baseFilename) and f.endswith(".bak")
        ]

        lBackDir = self._directories["log"]
        lBackupList = [
            {"File": f, "Directory": lBackDir}
            for f in os.listdir(lBackDir)
            if f.startswith(self._baseFilename) and f.endswith(".bak")
        ]

        lBackupList.extend(lArchBackup)
        lBackupList.sort(key=lambda item: item["File"], reverse=True)

        lSeq = len(lBackupList)
        while len(lBackupList) > 0:
            lBackupInfo = lBackupList.pop()
            lOldBackupPath = os.path.join(
                lBackupInfo["Directory"], lBackupInfo["File"]
            )  # Correct path join
            lNewBackupPath = os.path.join(
                lBackupInfo["Directory"], f"{self._baseFilename}({lSeq:03}).bak"
            )  # Correct path join
            os.rename(lOldBackupPath, lNewBackupPath)
            lSeq -= 1  # Decrement the sequence number

    def _shouldRotate(self):
        lCurrFilePath = os.path.join(
            self._directories["log"],
            self._getTimeStampedFilename(
                self._filenameTemplate, self._logfileExtention, self._dateFormat
            ),
        )

        lFilenameRotate = lCurrFilePath != self._currentLogPath
        lFileSizeRotate = self._fileSize >= self._maximumSize

        if lFilenameRotate or lFileSizeRotate:
            self._shiftBackup()
            os.rename(self._currentLogPath, f"{self._baseFilename}(000).bak")

        return lFilenameRotate or lFileSizeRotate

    def format(self, record):
        try:
            formatedMsg = super().format(record)
            self._fileSize += len(formatedMsg)

            return formatedMsg

        except ValueError:
            return ""

        except Exception as e:
            raise e

    def _manageArchives(self):
        self._archiveOldLogs()
        self._archiveOldBackups()
        self._purgeOldArchives()

    def _archiveOldLogs(self):
        lSortedLogFiles = sorted(
            [f for f in os.listdir(self._directories["log"]) if f.endswith(".log")],
            key=lambda f: os.path.getctime(os.path.join(self._directories["log"], f)),
            reverse=True,
        )

        try:
            while len(lSortedLogFiles) > self._maximumLogs:
                lOldLogFile = lSortedLogFiles.pop()
                lOldLogPath = os.path.join(self._directories["log"], lOldLogFile)
                lArchivePath = os.path.join(
                    self._directories["archive"],
                    f"{lOldLogFile}.{datetime.now(self._timezone).strftime(self._archiveDateFormat)}",
                )

                os.rename(lOldLogPath, lArchivePath)

        except OSError as e:
            logging.error(f"Error archiving log: {e}")

        except Exception as e:
            raise e

    def _archiveOldBackups(self):
        try:
            lSortedBackups = sorted(
                [
                    f
                    for f in os.listdir(self._directories["log"])
                    if f.startswith(self._baseFilename + ".") and f.endswith(".bak")
                ],
                key=lambda f: os.path.getctime(
                    os.path.join(self._directories["log"], f)
                ),
                reverse=True,
            )

        except Exception as ex:
            print("Sorting backup", ex)

        while len(lSortedBackups) > self._maximumBackups:
            lOldestBackup = lSortedBackups.pop()
            lOldBackupPath = os.path.join(self._directories["log"], lOldestBackup)
            lArchivePath = os.path.join(
                self._directories["archive"],
                "backups",
                f"{lOldestBackup}.{datetime.now(self._timezone).strftime(self._archiveDateFormat)}",
            )
            try:
                os.rename(lOldBackupPath, lArchivePath)

            except OSError as e:
                logging.error(f"Error archiving backup: {e}")

            except Exception as e:
                raise e

    def _purgeOldArchives(self):
        lNow = datetime.now(self._timezone)  # Timezone-aware "now"

        for lArchiveDir in [
            self._directories["archive"],
            os.path.join(self._directories["archive"], "backups"),
        ]:
            for lFilename in os.listdir(lArchiveDir):
                lFilePath = os.path.join(lArchiveDir, lFilename)
                if not os.path.isdir(lFilePath):
                    try:
                        # Attempt to extract the timestamp from the filename. Handles both .log.YYYYMMDDHHMMSS and .bak.YYYYMMDDHHMMSS
                        lFileParts = lFilename.split(".")
                        if len(lFileParts) >= 3:
                            lTimeStampStr = lFileParts[-1]
                            try:  # nested try to handle potential datetime parse errors
                                lArchiveTime = datetime.strptime(
                                    lTimeStampStr, self._archiveDateFormat
                                ).replace(
                                    tzinfo=self._timezone
                                )  # Make archive time timezone-aware
                                lTimeDiff = (
                                    lNow - lArchiveTime
                                )  # Compare timezone-aware datetimes
                                if lTimeDiff.days > self._archiveRetention:
                                    os.remove(lFilePath)

                            except ValueError:
                                logging.warning(
                                    f"Could not parse timestamp in filename: {lFilename}. Skipping deletion."
                                )

                        else:
                            logging.warning(
                                f"Could not parse timestamp in filename: {lFilename}. Skipping deletion."
                            )

                    except OSError as e:  # Handle file removal errors
                        logging.error(f"Error processing archive file {lFilename}: {e}")

                    except Exception as e:
                        raise e

    def close(self):
        self._fileSize = 0
        return super().close()

    def _open(self):
        self._fileSize = 0
        return open(
            self._currentLogPath, "a", encoding=self._encoding, errors=self._errors
        )

    def emit(self, record):
        try:
            if self._shouldRotate():
                self._rotate()

            super().emit(record)

        except ValueError:
            pass

        except Exception as e:
            raise e
