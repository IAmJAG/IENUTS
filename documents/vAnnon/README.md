# vAnnon - Video Annotation Tool

## Overview

vAnnon is a specialized video annotation application designed for creating bounding box annotations on video frames. It provides a comprehensive toolkit for manual video annotation workflows, enabling users to draw, edit, and manage bounding boxes across video frames with precision and efficiency.

## Purpose

The primary purpose of vAnnon is to facilitate the creation of training data for computer vision models, particularly object detection systems. It serves as a bridge between raw video content and machine learning pipelines by providing:

- **Manual Annotation**: Precise bounding box creation and editing
- **Video Playback Control**: Frame-by-frame navigation and playback
- **Tag Management**: Hierarchical classification system for annotated objects
- **Data Export**: Structured output for training data pipelines

## Key Features

- **Interactive Video Annotation**: Draw bounding boxes directly on video frames
- **Tag-Based Classification**: Organize annotations with customizable tags
- **Frame Navigation**: Precise control over video playback and frame seeking
- **Playback Speed Control**: Adjustable video playback speed for detailed annotation work
- **Annotation Management**: Add, edit, delete, and organize bounding boxes
- **Data Persistence**: Save and load annotation projects
- **Real-time Preview**: Visual feedback during annotation process
- **Precise Timing**: Accurate frame timing ensures consistent playback regardless of processing load

## Architecture

vAnnon is built using a modular architecture with clear separation of concerns:

- **Core Engine**: Video processing and playback
- **Annotation System**: Bounding box creation and management
- **UI Framework**: Interactive components for user interaction
- **Data Layer**: Serialization and persistence of annotations
- **Configuration System**: Flexible application settings

## Target Users

- **Data Scientists**: Creating training datasets for computer vision models
- **ML Engineers**: Preparing annotation data for object detection tasks
- **Research Teams**: Manual annotation workflows for academic projects
- **Quality Assurance Teams**: Reviewing and correcting automated annotations

## Integration

vAnnon is designed to integrate seamlessly with the broader eNuts ecosystem, providing specialized video annotation capabilities that complement other tools in the suite.
