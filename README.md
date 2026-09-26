# 🎥 Universal Video Downloader

A modern, fast, and user-friendly desktop application built with Python to download videos and audio from over 1,500+ websites (including YouTube, Instagram, TikTok, Facebook, Twitter, and more).

---

## 📌 Overview

**Universal Video Downloader** makes downloading online videos simple and efficient. Powered by `yt-dlp` and `FFmpeg`, it automatically extracts high-definition video streams and merges audio seamlessly. Built with `CustomTkinter`, it features a sleek modern dark-themed interface with custom resolution options and real-time speed tracking.

---

## ✨ Features

- **🌐 Multi-Platform Support:** Works on YouTube, Instagram Reels, TikTok, Twitter/X, Reddit, Vimeo, and 1,500+ platforms.
- **🎯 Resolution Selection:** Select your preferred quality before downloading (Best Quality, 1080p, 720p, 480p, 360p).
- **🎵 Dedicated MP3 Extractor:** One-click option to download audio-only files directly in high-quality `.mp3` format.
- **⚡ Real-Time Progress Tracking:** Monitor exact download percentage, real-time speed (MB/s), and estimated time remaining (ETA).
- **🚫 Cancel Anytime:** Stop active downloads instantly with the integrated emergency cancel button.
- **📁 Folder Chooser:** Select any directory on your computer to save your downloaded files.


---

## 🛠️ Technologies Used

| Technology | Purpose |
| :--- | :--- |
| **Python 3** | Core Programming Language |
| **CustomTkinter** | Modern UI framework for Desktop Application |
| **yt-dlp** | Core media extraction & scraper engine |
| **FFmpeg** | High-Definition video and audio stream merging |

---

## 📂 Project Structure

```text
Universal-Video-Downloader/
├── main.py                    # Application Entry Point
├── requirements.txt           # Python Project Dependencies
├── README.md                  # Project Documentation
└── src/
    ├── __init__.py            # Package Marker
    ├── downloader.py          # Core yt-dlp backend & progress logic
    └── gui.py                 # CustomTkinter User Interface
