from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QPushButton

from ..mwHelper import *


def Dashboard():
    lDBPage, lDBContent = CreatePage("--DASHBOARD--")
    lDBPage.setObjectName("DASHBOARD")

    lWelcomeLabel = QLabel("Welcome to eNuts!")
    lWelcomeLabel.setObjectName("WELCOME")
    lWelcomeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
    lWelcomeLabel.setStyleSheet("font-size: 24px; font-weight: bold; color: #f0f0f0;")
    lDBContent.layout().addWidget(lWelcomeLabel)

    lDescriptionLabel = QLabel("Your evolving Neural user training system.")
    lDescriptionLabel.setObjectName("DESCRIPTION")
    lDescriptionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
    lDescriptionLabel.setStyleSheet("font-size: 14px; color: #cccccc;")
    lDBContent.layout().addWidget(lDescriptionLabel)

    lBtn = QPushButton("Start Training")
    lBtn.setObjectName("TRAININGBUTTON")
    lBtn.setFixedSize(150, 40)
    lBtn.setStyleSheet("""
            QPushButton {
                background-color: #007acc;
                color: white;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #005f99;
            }
            QPushButton:pressed {
                background-color: #003f66;
            }
        """)
    lDBContent.layout().addWidget(lBtn, alignment=Qt.AlignmentFlag.AlignCenter)
    lDBContent.layout().addStretch()

    return lDBPage
