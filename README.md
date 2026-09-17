# 🎙️ One-Click Voice Studio

A real-time, low-latency desktop voice changer and audio processing application built with Python. Powered by **Pedalboard** (DSP) and **SoundDevice**, featuring a modern and responsive dark-mode UI built with **CustomTkinter**.

---

## ✨ Features

- **Real-Time Audio Processing:** Ultra-low latency DSP chain with minimal buffer delay.
- **Signal Cleaning & Mastering Chain:** Integrated `NoiseGate`, `HighpassFilter`, `Compressor`, and `Limiter` to eliminate noise and prevent clipping.
- **Categorized Voice Presets:**
  - **Human & Vocal:** Deep Male, Helium, Anime / High-Pitch, Trap Vocal.
  - **Cinema & Characters:** Darth Vader, Ogre, Goblin, Zombie, Alien Signal.
  - **Technology & Devices:** Vintage Police Radio, Broken Robot, Megaphone, Telephone.
  - **Atmosphere & Space:** Grand Cathedral, Empty Cave, Dream Dimension.
- **Live Audio Meter:** Dynamic visual RMS feedback bar reflecting microphone input volume.
- **Zero Configuration:** Automatically binds to the default Windows input and output audio endpoints.

---

## 🛠️ Built With

- **Python 3.10+**
- [Pedalboard](https://github.com/spotify/pedalboard) - Spotify's audio effects library
- [SoundDevice](https://python-sounddevice.readthedocs.io/) - Real-time audio I/O
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - Modern desktop UI
- [NumPy](https://numpy.org/) - Audio buffer manipulation

---

## 🚀 Quick Start

### Prerequisites
Ensure you have Python 3.10 or higher installed.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Zwsup/Voice-Changer.git
   cd Voice-Changer


Install dependencies:
pip install -r requirements.txt

Run the application:
python main.py
