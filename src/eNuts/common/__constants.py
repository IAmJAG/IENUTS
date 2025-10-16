# src/eNuts/common/__constants.py
import os

lBaseDir = os.path.dirname(os.path.abspath(__file__))
for _ in range(3):
    lBaseDir = os.path.dirname(lBaseDir)

PROJECT_ROOT = os.path.join(lBaseDir)  # Constant
