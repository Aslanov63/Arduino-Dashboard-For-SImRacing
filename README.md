# Arduino-Dashboard-For-SImRacing
These project is dream of Sim-Racer. Using this script, you can track telemetry of Asseto Corsa and display it on arduino DIY dashboard,showing essential info for racing.Game was tested in Asseto Corsa and on Arduino UNO 4
# Sim-Racing Telemetry Dashboard 🏎️📊

An interactive hardware-software system that brings real-time racing data from the simulator (**Assetto Corsa**) to a physical dashboard. This project combines Arduino microprocessing, Python data extraction, and a web interface for a fully immersive racing experience.

## 🌟 Key Features

* **Physical Dashboard:** Real-time display of Gear, Speed, and RPM on an **LCD 16x2 screen**.
* **RPM LED Bar:** A dynamic LED bar graph (via 74HC595 shift register) that visualizes engine RPM, helping with perfect shift timing.
* **IoT Web Interface:** A live web server hosted by the Arduino (WiFi) that displays detailed session stats:
    * Best Lap & Last Lap times
    * Top Speed achieved
    * Current Position & Completed Laps
* **Dual Units:** Support for both Metric (km/h) and Imperial (mph) systems via a physical toggle switch.

## 🛠 Technology Stack

* **Hardware:** Arduino (Uno R4/WiFi), LCD Display, 74HC595 Shift Register, LEDs.
* **Firmware:** C++ (Arduino) - handles hardware control and web serving.
* **Bridge Script:** Python - extracts data from Assetto Corsa's Shared Memory and communicates via Serial (USB).
* **Game:** Assetto Corsa.

## 📂 Project Structure

* `Arduino_code.ino` — The main firmware for the Arduino board.
* `Telemetry_Bridge.py` — Python script to fetch game data (uses Shared Memory).
* `Sim-Racing_Dashboard.pptx` — Project presentation and visual guide.
* `Report.docx` — Detailed technical documentation and challenges faced.

## 🚀 How to Setup

1.  **Hardware:** Assemble the circuit according to the pin definitions in the Arduino code (LCD on pins 13-2, Shift Register on 10, 11, 9).
2.  **Arduino:** * Update the `ssid` and `password` in the code to match your WiFi.
    * Upload the code to your Arduino.
3.  **Python:** * Install requirements: `pip install pyserial` (and any library used for AC shared memory).
    * Run the script while the game is active.
4.  **Race:** Open the Arduino's IP address in your browser to see the live IoT dashboard!

## 👥 Authors
* **Ali Aslanov**
* **Polad Omar**

---
*Developed as a final project for the Programming of Microprocessor Systems course. May 2025.*
