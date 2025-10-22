# Project eNuts (Evolving Neural User Training System)

## Overview
**eNuts (Evolving Neural User Training System)** is an AI-driven project designed to **imitate a person's gaming habits** by deeply understanding their **behavior and mannerisms**. The system focuses on analyzing how an individual reacts to various in-game situations to create a highly realistic and predictive AI bot.

## Project Components

The project is structured into four main components:

### 0. Dashboard (Launcher)
**Dashboard** is the application launcher that provides access to all eNuts suite applications. It serves as the entry point for the entire system.

**Current Implementation Status:**
- **Implemented:** Standalone launcher application with system tray, launch cards for eNuts and vAnnon, configuration system, modular architecture
- **Components:** Main dashboard module, eNuts in-app dashboard page, POC implementation
- **Documentation:** [Dashboard Module](../dashboard/readme.md)

### 1. eNuts (Main Application)
This is the core application that acts as the **AI bot**. It utilizes the trained AI model to actively **imitate the user's behavior** within a game environment, essentially serving as a proxy or digital double of the user's playstyle.

**Current Implementation Status:**
- **Implemented:** Android device streaming via SCRCPY protocol, real-time video capture, touch and keyboard control injection, device monitoring, video recording capabilities, main window with navigation, dashboard page
- **Missing:** AI bot functionality, behavioral imitation, trained model integration, automated gameplay

### 2. vAnnon (Video Annotator)
**vAnnon** is a specialized tool used to **gather and annotate visual data** (images/frames) for training the models. This tool is crucial for preparing the necessary labeled data, especially for training the computer vision components (classifier and detector models).

**Current Implementation Status:**
- **Implemented:** Basic UI framework, tag system for annotations, media view component with bounding box creation, video playback service
- **Missing:** Full annotation workflow, computer vision model training integration, data export for training, automated object detection

### 3. Training System
This component is responsible for processing the data gathered by vAnnon and directly interacting with the user's gameplay to create and refine the final behavioral model. It is composed of two primary sub-systems:

#### Sub-System A: Computer Vision Model Training
This system handles the training of the preliminary computer vision models:
* **Image Classifier Trainer:** Develops models to categorize or classify specific in-game images or states.
* **Image Detection Model Trainer:** Develops models to locate and identify objects, characters, or elements within the game screen.

**Current Implementation Status:**
- **Implemented:** Basic neural service class (CVNeural), streaming infrastructure
- **Missing:** Actual computer vision models, training pipelines, classifier and detector implementations, model training code

#### Sub-System B: Behavioral Model Trainer
This is the **main trainer** responsible for capturing and modeling the user's decision-making process and reactions:
* **Interactive Recording:** The user plays the game directly while the system **records all key presses, taps, mouse movements, and other user actions** in real-time. This provides a direct mapping of input to in-game context.
* **Gameplay Study/Analysis:** Alternatively, the trainer can analyze recorded gameplay videos to learn and model the underlying decision-making structure and execution patterns.

**Current Implementation Status:**
- **Implemented:** Video recording functionality, input capture (touch/keyboard), streaming services
- **Missing:** Behavioral modeling, decision-making algorithms, action pattern analysis, AI training pipelines, real-time action recording and correlation with game state
