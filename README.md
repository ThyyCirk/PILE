# PILE - Personal Intelligent Link Engine

Special gadget that you can use to track your physical and mental health, to journal, keep track of time, and more!

[Download Latest Release](https://github.com/ThyyCirk/PILE/releases/latest)

[![MicroPython](https://img.shields.io/badge/Firmware-MicroPython-306998?style=flat&logo=python&logoColor=white)](https://docs.python.org/3/)
[![Platform](https://img.shields.io/badge/Platform-M5StickC%20PLUS2-orange?style=flat)](https://shop.m5stack.com/products/m5stickc-plus2-esp32-mini-iot-development-kit)
[![Development IDE](https://img.shields.io/badge/IDE-Thonny-blue?style=flat)](https://thonny.org/)

---

## 🚀 Overview

In an era dominated by heavy screen time and intrusive notifications, PILE offers a minimal, psychologically optimized user experience to handle daily routines. It micro-manages essential telemetry like physical steps, calorie metrics, and emotional state logs, executing everything through highly optimized code tailored for hardware-constrained microcontrollers.

The project features a modular architecture split cleanly into an **Application Frontend** and an underlying **OS Core Backend**, spanning over 1,600 lines of custom script.

---

## 🛠️ Features

### 1. Home & UI Core Engine
* **Intuitive Navigation:** Utilizes UX standard continuous state loops, tracking button clicks (`wasClicked()`) and long-press holds (`isHolding()`) across an atomic main system clock loop.
* **Smart State Loading:** The system detects whether it is the device's first boot (`WENT_THROUGH_SETUP`), safely initializing configuration parameters, setting audio volumes, and calling up structural initialization routines before loading the homepage.

### 2. Mood Tracker (Feelings Diary)
A dedicated 3-page localized mood journaling subsystem:
* **Page 1 (7-Day Overview):** Dynamically calculates the entries from the past calendar week and renders a custom visual chart along with a calculated statistical median mood.
* **Page 2 (Input Module):** Allows quick entry selection via discrete emotional scales: Excellent (`rad`), Very Good (`good`), Good (`mid`), Bad (`bad`), and Awful (`awful`).
* **Page 3 (Monthly Review):** Provides a visual calendar timeline reflecting historical emotional trends connected across a structured continuous vector line.

### 3. Fitness Engine
* Built-in step counting and active physical cycle processing algorithms that track locomotion milestones.
* Caloric expenditure computing derived dynamically from physical metrics (such as user height and weight) set up during device initialization.
* Integrated goal tracking alerts that override the UI display layer (`Msg_Overlay`) when milestone step counts are accomplished.

### 4. Custom Matrix Keyboard
* A responsive, full character-selection grid built to write, update, and persist configuration keys or logging text locally.
* Supports full alphabetical switching between Lowercase arrays, Uppercase transformations, Numeric keys, and special character string vectors.
* Employs an active coordinate calculation helper (`calcPos`) to visually move orange highlighting overlays over the currently indexed character grid spot, returning old spaces back to black seamlessly to minimize redraw flashing.

### 5. Quick Settings Manager
* Triggered seamlessly via explicit physical power buttons, provided overlay settings blockers are not active (`ALLOW_SETTINGS_PAGE`).
* Manages rapid configuration changes for global on-board peripherals including Audio state parameters, Bluetooth toggles, Wi-Fi hardware switches, system resetting, and deep sleep power preservation modes.
* Saves states directly into non-volatile memory text structures.

---

## 💻 Hardware Specifications (M5StickC PLUS2)

The system leverages the highly compact architecture of the ESP32-powered development kit:
* **SoC:** ESP32-PICO-V3-02 chip with built-in Wi-Fi and Bluetooth.
* **Storage & RAM:** 8MB Flash Memory + 2MB PSRAM.
* **Display:** 1.14" Color LCD panel (135x240 resolution, driven using the ST7789V2 driver controller).
* **Sensors:** MPU6886 IMU (Gyroscope + Accelerometer), SPM1423 PDM Microphone.
* **Peripherals:** BM8563 Real-Time Clock (RTC), Internal Piezo Buzzer, IR Transmitter, and 3 User Buttons.
* **Power:** Integrated 200mAh Battery with Type-C management.

---

## 📁 Directory Structure

```shell
├── README.md            # Project description and overview
├── apps/                # User application scripts
│   └── Pile.py          # PILE OS core application module
├── boot.py              # System boot file
├── libs/                # Dependency and helper libraries
│   ├── README.md
│   └── __init__.py
├── main.py              # Primary system entry point
└── res/                 # Static resource assets
    ├── font/            # System font configurations
    └── img/             # Graphic element and bitmap storage
        ├── default.jpg
        ├── default.png
        ├── uiflow.bmp
        ├── uiflow.jpg
        └── uiflow.png
