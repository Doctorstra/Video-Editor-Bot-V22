# Video-Editor-Bot-V22

🤓 A Powerful Telegram Video Editor Bot.🛠️Advance Features like Video Merging, Video Trimming, Video Hevc/Fast Compressor, Video Renamer, Video Screenshot Generator, Video Watermark Adder, Video Encoder, Video Subtitle Extractor Adder, Video Audio Extractor Adder, Video Convert file/Video, Video Archiver (tar,rar,Zip),Archive Extractor, Direct Download link Generator,Url Uploader html (mx-player,Zee 5,Hotstar,Voot,Sony etc.), Video Metadata, Video Information, With Permanent Thumbnail Support 📌 



## Features
- [X] Video Merger.
- [X] Video Trimmer.
- [X] Video Compressor Hevc/Fast.
- [X] Video Renamer.
- [X] Video Screenshot Generator.
- [X] Video Watermark Adder.
- [X] Video Encoder.
- [X] Video Subtitle Extractor/Adder.
- [X] Video Audio Extractor/Adder
- [X] Video Archiver (tar,rar,Zip)
- [X] Archive Extractor
- [X] Direct Download link Generator
- [X] Url Uploader html (mx-player,Zee 5,Hotstar,Voot,Sony etc.)
- [X] Video Metadata
- [X] Video Storage Info
- [X] Permanent Thumbnail Support
- [X] Broadcast Support
- [X] Mongodb Added
- [X] Log Channel Added


### Follow on:
<p align="left">
<a href="https://github.com/Doctorstra"><img src="https://img.shields.io/badge/GitHub-Follow%20on%20GitHub-inactive.svg?logo=github"></a>
</p>

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.11 or higher
- FFmpeg installed on your system
- MongoDB (local or cloud)
- Telegram Bot Token (get it from [@BotFather](https://t.me/botfather))

### Quick Start with Docker (Recommended)

1. **Clone the repository:**
```bash
git clone https://github.com/Doctorstra/
Video-Editor-Bot-V22.git
cd all-in-one
```

2. **Configure environment variables:**
```bash
cp .env.example .env
# Edit .env and add your credentials
```

3. **Run with Docker Compose:**
```bash
docker-compose up -d
```

That's it! Your bot is now running! 🎉

### Manual Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Install FFmpeg:**
- **Ubuntu/Debian:** `sudo apt-get install ffmpeg`
- **macOS:** `brew install ffmpeg`
- **Windows:** Download from [ffmpeg.org](https://ffmpeg.org/download.html)

3. **Set up MongoDB:**
```bash
# Install MongoDB locally or use MongoDB Atlas (cloud)
```

4. **Configure the bot:**
```bash
cp .env.example .env
# Edit .env with your credentials
```

5. **Run the bot:**
```bash
python bot.py
```

### Environment Variables

Create a `.env` file with the following variables:

```env
# Required
BOT_TOKEN=your_telegram_bot_token
API_ID=your_telegram_api_id
API_HASH=your_telegram_api_hash
MONGODB_URI=mongodb://localhost:27017

# Optional
DATABASE_NAME=video_editor_bot
LOG_CHANNEL_ID=your_log_channel_id
ADMIN_IDS=123456789,987654321
MAX_FILE_SIZE=2000
```

### Getting Your Credentials

1. **Bot Token:** Message [@BotFather](https://t.me/botfather) on Telegram
   - Send `/newbot`
   - Follow the instructions
   - Copy the token

2. **API ID & Hash:** Visit [my.telegram.org](https://my.telegram.org)
   - Log in with your phone number
   - Go to "API Development Tools"
   - Create an application
   - Copy API ID and API Hash

---

## 📚 Usage Guide

### Basic Commands

Start the bot and use these commands:

```
/start - Start the bot and see welcome message
/help - Get list of all commands
/about - Learn more about the bot
/stats - View your statistics
```

### Video Processing

```
/compress - Compress video (choose HEVC or Fast mode)
/trim <start> <duration> - Trim video (e.g., /trim 00:00:10 00:00:30)
/merge - Merge multiple videos (send videos then /done)
/rename <name> - Rename video file
/encode - Encode video to different format
/screenshot [timestamp] - Generate screenshot (e.g., /screenshot 00:00:05)
/metadata - View video information
```

### Audio & Subtitles

```
/extract_audio - Extract audio from video
/extract_subs - Extract subtitles from video
/add_audio - Add audio to video
/add_subs - Add subtitles to video
```

### Watermark & Thumbnail

```
/add_watermark - Add watermark to video
/set_thumbnail - Set permanent thumbnail
/show_thumbnail - View your thumbnail
/delete_thumbnail - Remove your thumbnail
```

### Archives

```
/archive <type> - Create archive (zip/tar/rar)
/extract - Extract archive
```

### Download & Upload

```
/download <url> - Download from URL or streaming platform
/generate_link - Generate direct download link
```

### Storage & Info

```
/storage - Check your storage usage
```

### Admin Commands

```
/broadcast <message> - Send message to all users
/stats_all - View bot statistics
```

---

## 🎯 Example Workflows

### Compress a Video
1. Send `/compress`
2. Send your video file
3. Bot processes and sends compressed version

### Merge Videos
1. Send `/merge`
2. Send first video
3. Send second video
4. Send more videos (if needed)
5. Send `/done`
6. Bot merges and sends result

### Add Watermark
1. Send `/add_watermark`
2. Send watermark image
3. Send video
4. Bot adds watermark and sends result

---

## 🏗️ Project Structure

```
all-in-one/
├── bot.py                 # Main bot application
├── config.py             # Configuration management
├── database.py           # MongoDB operations
├── requirements.txt      # Python dependencies
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Docker Compose setup
├── .env.example         # Environment template
├── handlers/            # Command handlers
│   ├── basic_handlers.py
│   ├── video_handlers.py
│   ├── thumbnail_handlers.py
│   └── archive_handlers.py
└── utils/               # Utility modules
    ├── video_utils.py
    ├── archive_utils.py
    └── download_utils.py
```

---

## 🔧 Advanced Configuration

### File Size Limits
Edit `MAX_FILE_SIZE` in `.env` to change the upload limit (in MB).

### Custom Download Path
Set `DOWNLOAD_PATH` and `UPLOAD_PATH` in `.env`.

### Enable/Disable Features
```env
ENABLE_BROADCAST=True
ENABLE_URL_UPLOAD=True
ENABLE_WATERMARK=True
```

### Log Channel
Set `LOG_CHANNEL_ID` to send all bot activities to a Telegram channel.

---

## 📝 License

This project is licensed under the  License - see the [LICENSE](LICENSE) file for details.
