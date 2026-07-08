# Telegram Media Mirror

A production-ready Telegram Media Mirror Bot built with **Python 3.14** and **Aiogram 3**.

Automatically mirrors supported media from linked Telegram groups or channels to destination groups using an asynchronous processing pipeline.

---

## Features

- 📸 Photo Mirroring
- 🎥 Video Mirroring
- 📄 Document Mirroring
- 🎵 Audio Mirroring
- 🎤 Voice Note Mirroring
- 🎬 Video Note Mirroring
- 🎞 GIF / Animation Mirroring
- 📚 Album (Media Group) Support
- 📝 Caption Preservation
- ⚡ Queue-based Processing
- 🔄 Automatic Download & Upload
- 🚦 Configurable Rate Limiting
- 🔁 Retry System
- ⏳ Telegram FloodWait Handling
- 🗄 SQLite Database
- 👤 Owner-only Administration
- 📋 Link & Unlink Commands
- 📑 Activity & Error Logging

---

## Supported Media

- Photos
- Videos
- Documents
- Audio
- Voice Notes
- Video Notes
- GIFs / Animations
- Albums (Media Groups)

---

## Commands

| Command | Description |
|---------|-------------|
| `/start` | Start the bot |
| `/help` | Show help |
| `/link` | Select source group |
| `/finishlink` | Link destination group |
| `/unlink` | Select source to unlink |
| `/finishunlink` | Remove mirror |
| `/list` | Show all linked groups |
| `/status` | Bot status |

---

## Project Structure

```text
telegram-media-mirror/
│
├── bot/
├── config/
├── database/
├── services/
├── utils/
│
├── app.py
├── requirements.txt
├── .env.example
├── README.md
├── LICENSE
└── CHANGELOG.md
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/archit-dot/telegram-media-mirror.git
```

Move into the project

```bash
cd telegram-media-mirror
```

Create a virtual environment

```bash
python -m venv venv
```

Activate it

### Windows

```bash
venv\Scripts\activate
```

### Linux

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create the environment file

```bash
cp .env.example .env
```

Edit `.env`

```env
BOT_TOKEN=YOUR_BOT_TOKEN
OWNER_ID=YOUR_TELEGRAM_ID
```

Run the bot

```bash
python app.py
```

---

## Architecture

```
Telegram

↓

Message Handler

↓

Processing Queue

↓

Downloader

↓

Retry Handler

↓

Rate Limiter

↓

Uploader

↓

Destination Group
```

---

## Tech Stack

- Python 3.14
- Aiogram 3
- SQLite
- AsyncIO
- AioSQLite
- Python Dotenv
- Aiofiles

---

## Deployment

The bot is designed to run 24/7 on an Ubuntu VPS using a Python virtual environment and `systemd`.

---

## License

This project is licensed under the MIT License.
