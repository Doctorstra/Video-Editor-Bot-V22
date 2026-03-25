# Quick Reference Guide

## 🚀 Quick Start

```bash
# Clone and setup
git clone https://github.com/astlindijo/all-in-one.git
cd all-in-one
cp .env.example .env

# Edit .env with your credentials
nano .env

# Docker method (recommended)
docker-compose up -d

# Or manual method
pip install -r requirements.txt
python bot.py
```

## 📋 Command Cheatsheet

| Command | Description | Example |
|---------|-------------|---------|
| `/start` | Start the bot | `/start` |
| `/help` | Show all commands | `/help` |
| `/compress` | Compress video | `/compress` then send video |
| `/trim` | Trim video | `/trim 00:00:10 00:00:30` |
| `/merge` | Merge videos | `/merge` then send videos |
| `/rename` | Rename file | `/rename NewName.mp4` |
| `/screenshot` | Take screenshot | `/screenshot 00:00:05` |
| `/extract_audio` | Extract audio | `/extract_audio` |
| `/add_watermark` | Add watermark | `/add_watermark` |
| `/archive` | Create archive | `/archive zip` |
| `/extract` | Extract archive | `/extract` |
| `/download` | Download from URL | `/download <url>` |
| `/metadata` | View file info | `/metadata` |
| `/storage` | Check storage | `/storage` |
| `/stats` | Your statistics | `/stats` |

## 🎯 Common Workflows

### Compress & Upload
1. `/compress`
2. Send video
3. Choose HEVC or Fast
4. Receive compressed video

### Create Video Archive
1. `/archive zip`
2. Send video files
3. `/done`
4. Receive archive

### Download from Streaming
1. `/download https://...`
2. Wait for download
3. Receive video

## ⚙️ Environment Variables

```env
# Required
BOT_TOKEN=123456:ABC-DEF...
API_ID=12345678
API_HASH=abc123def456...
MONGODB_URI=mongodb://...

# Optional
ADMIN_IDS=123456,789012
LOG_CHANNEL_ID=-100123456
MAX_FILE_SIZE=2000
```

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Bot not responding | Check BOT_TOKEN in .env |
| MongoDB error | Verify MONGODB_URI is correct |
| FFmpeg error | Install: `apt install ffmpeg` |
| Permission denied | Run: `chmod 755 downloads uploads` |
| Module not found | Run: `pip install -r requirements.txt` |

## 🔗 Useful Links

- [Full Setup Guide](SETUP.md)
- [Contributing](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)
- [GitHub Issues](https://github.com/astlindijo/all-in-one/issues)

## 📝 Notes

- Max file size: 2GB (configurable)
- Supported formats: MP4, MKV, AVI, MOV, WebM
- Archive types: ZIP, TAR, RAR
- Compression modes: HEVC (better), Fast (quicker)

---

**Need Help?** Check [SETUP.md](SETUP.md) for detailed instructions!
