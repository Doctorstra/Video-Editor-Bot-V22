# Video-Editor-Bot-V22
🤓 A Powerful Telegram Video Editor Bot.🛠️Advance Features like Video Merging, Video Trimming, Video Hevc/Fast Compressor, Video Renamer, Video Screenshot Generator, Video Watermark Adder, Video Encoder, Video Subtitle Extractor Adder, Video Audio Extractor Adder, Video Convert file/Video, Video Archiver (tar,rar,Zip),Archive Extractor, Direct Download link Generator,Url Uploader html (mx-player,Zee 5,Hotstar,Voot,Sony etc.), Video Metadata, Video Information, With Permanent Thumbnail Support 📌 

### Demo Bot:
<a href="https://t.me/Dads_links_Bot"><img src="https://img.shields.io/badge/Demo-Telegram%20Bot-blue.svg?logo=telegram"></a>

### Support Group:
<a href="https://t.me/Dads_links"><img src="https://img.shields.io/badge/Telegram-Join%20Telegram%20Group-blue.svg?logo=telegram"></a>


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

### Deploy on Heruko
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/Doctorstra/Video-Editor-Bot-V22)


### Deploy on Railway

[![Deploy To Railway](https://railway.app/button.svg)](https://railway.app)


### Deploy your bot on `Okteto`
  
[![Develop on Okteto](https://okteto.com/develop-okteto.svg)](https://cloud.okteto.com)


`Alternate way:`

#### The Hard Way 🤕
```sh
git clone https://github.com/Doctorstra/Video-Editor-Bot-V22)

cd Video-Editor-Bot-V22
virtualenv -p python3 VENV
. ./VENV/bin/activate
pip3 install -r requirements.txt
--- EDIT configs.py values appropriately ---
python3 bot.py
```

### Follow on:
<p align="left">
<a href="https://github.com/Doctorstra"><img src="https://img.shields.io/badge/GitHub-Follow%20on%20GitHub-inactive.svg?logo=github"></a>
</p>

<b>🧰 Project Structure</b>

Video-Editor-Bot-V22/
│
├── bot/
│   ├── handlers/
│   │   ├── start.py
│   │   ├── merge.py
│   │   ├── trim.py
│   │   ├── compress.py
│   │   ├── rename.py
│   │   ├── screenshot.py
│   │   ├── watermark.py
│   │   ├── encode.py
│   │   ├── subtitle.py
│   │   ├── audio.py
│   │   ├── archive.py
│   │   ├── extract_archive.py
│   │   ├── download_link.py
│   │   ├── url_uploader.py
│   │   └── metadata.py
│   │
│   ├── utils/
│   │   ├── ffmpeg_utils.py
│   │   ├── database.py
│   │   └── storage.py
│   │
│   ├── config.py
│   └── main.py
│
├── requirements.txt
├── .gitignore
└── README.md
