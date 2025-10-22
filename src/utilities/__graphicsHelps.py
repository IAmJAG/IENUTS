from cv2 import (
    CHAIN_APPROX_SIMPLE,
    COLOR_BGR2GRAY,
    COLOR_BGR2RGB,
    MORPH_CLOSE,
    RETR_EXTERNAL,
    Canny,
    GaussianBlur,
    boxPoints,
    contourArea,
    cvtColor,
    findContours,
    minAreaRect,
    morphologyEx,
)
from numpy import intp, ndarray, ones, uint8
from numpy import max as npmax
from numpy import min as npmin
from PySide6.QtCore import QRectF
from PySide6.QtGui import QImage, QPixmap

from jAGFx.logger import debug


def findContourRect(lRawImage: ndarray, rect: QRectF):
    try:
        x, y, w, h = int(rect.x()), int(rect.y()), int(rect.width()), int(rect.height())
        # Crop the image to the ROI
        lROI = lRawImage[y : y + h, x : x + w]

        # Convert ROI to grayscale and blur
        if len(lROI.shape) == 3:
            # It's a color image, so we convert it to grayscale
            lGROI = cvtColor(lROI, COLOR_BGR2GRAY)
        else:
            # It's already grayscale, no conversion needed
            lGROI = lROI

        lBlrROI = GaussianBlur(lGROI, (5, 5), 0)

        # Canny edge detection
        lEdges = Canny(lBlrROI, 50, 150)

        # Morphological closing to fill small gaps
        lKernel = ones((5, 5), uint8)
        closing = morphologyEx(lEdges, MORPH_CLOSE, lKernel)

        # Find contours
        lContours, _ = findContours(closing, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE)

        if lContours:
            # Find the largest contour within the ROI
            lLrgstContour = max(lContours, key=contourArea)

            # Get the minimum area rotated bounding box
            lMinAreaRect = minAreaRect(lLrgstContour)

            # Get the integer bounding box points
            lBoxPoints = boxPoints(lMinAreaRect)
            lBoxPoints = intp(lBoxPoints)

            # Find the new upright bounding box from the rotated one
            lNewXRIO = npmin(lBoxPoints[:, 0])  # type: ignore
            lNewYRIO = npmin(lBoxPoints[:, 1])  # type: ignore
            lNewWRIO = npmax(lBoxPoints[:, 0]) - lNewXRIO  # type: ignore
            lNewHRIO = npmax(lBoxPoints[:, 1]) - lNewYRIO  # type: ignore

            # Adjust the coordinates to the full image
            return QRectF(x + lNewXRIO, y + lNewYRIO, lNewWRIO, lNewHRIO)

        # Return original rect
        return rect

    except Exception as e:
        debug(f"An error occurred during snapping: {e}")

    return None


def NDArrayToPixmap(frame: ndarray):
    # Get the image dimensions
    lHeight, lWidth, lChannels = frame.shape

    # Calculate the bytes per line (stride)
    lBytesPerLine = lChannels * lWidth
    # Convert the BGR frame to RGB for correct color display in Qt
    lRGBFrame = cvtColor(frame, COLOR_BGR2RGB)

    # Create the QImage from the RGB-formatted data
    lImage: QImage = QImage(lRGBFrame.data, lWidth, lHeight, lBytesPerLine, QImage.Format_RGB888)
    return QPixmap.fromImage(lImage)
