#!/bin/bash

# Start script for the bot

echo "🚀 Starting All-in-One Video Editor Bot..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "Please create .env file from .env.example"
    echo "Run: cp .env.example .env"
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    exit 1
fi

# Check if FFmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  Warning: FFmpeg is not installed!"
    echo "Video processing features will not work."
    echo "Please install FFmpeg: https://ffmpeg.org/download.html"
fi

# Create necessary directories
mkdir -p downloads uploads logs

# Install dependencies if not already installed
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt --quiet

# Start the bot
echo "✅ Starting bot..."
python3 bot.py
