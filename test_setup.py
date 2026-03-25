"""
Simple tests to verify bot setup
"""
import sys
import os

def check_python_version():
    """Check if Python version is 3.11 or higher"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 11:
        print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python version {version.major}.{version.minor} is too old. Need 3.11+")
        return False

def check_dependencies():
    """Check if required dependencies are installed"""
    required = [
        'telegram', 'dotenv', 'pymongo', 'ffmpeg',
        'PIL', 'aiohttp', 'motor', 'pyrogram', 'yt_dlp'
    ]
    
    missing = []
    for module in required:
        try:
            __import__(module)
            print(f"✅ {module} installed")
        except ImportError:
            print(f"❌ {module} not installed")
            missing.append(module)
    
    return len(missing) == 0

def check_ffmpeg():
    """Check if FFmpeg is installed"""
    import subprocess
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.split('\n')[0]
            print(f"✅ FFmpeg installed: {version}")
            return True
    except FileNotFoundError:
        print("❌ FFmpeg not installed")
        return False

def check_env_file():
    """Check if .env file exists and has required variables"""
    if not os.path.exists('.env'):
        print("❌ .env file not found")
        print("   Run: cp .env.example .env")
        return False
    
    print("✅ .env file exists")
    
    required_vars = ['BOT_TOKEN', 'API_ID', 'API_HASH', 'MONGODB_URI']
    
    from dotenv import load_dotenv
    load_dotenv()
    
    missing = []
    for var in required_vars:
        value = os.getenv(var)
        if not value or value == f"your_{var.lower()}_here" or value == "your_api_id" or value == "your_api_hash":
            print(f"⚠️  {var} not configured")
            missing.append(var)
        else:
            print(f"✅ {var} configured")
    
    return len(missing) == 0

def check_directories():
    """Check if required directories exist"""
    dirs = ['downloads', 'uploads', 'logs', 'utils', 'handlers']
    
    all_exist = True
    for dir_name in dirs:
        if os.path.exists(dir_name):
            print(f"✅ {dir_name}/ directory exists")
        else:
            print(f"❌ {dir_name}/ directory missing")
            all_exist = False
    
    return all_exist

def main():
    """Run all checks"""
    print("=" * 50)
    print("All-in-One Video Editor Bot - Setup Verification")
    print("=" * 50)
    print()
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("FFmpeg", check_ffmpeg),
        ("Environment File", check_env_file),
        ("Directories", check_directories),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n{name}:")
        print("-" * 50)
        results.append(check_func())
    
    print("\n" + "=" * 50)
    if all(results):
        print("✅ All checks passed! You're ready to run the bot.")
        print("   Run: python bot.py")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        print("   See SETUP.md for detailed instructions.")
    print("=" * 50)

if __name__ == "__main__":
    main()
