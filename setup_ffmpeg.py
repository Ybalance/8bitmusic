import os
import sys
import zipfile
import shutil
import urllib.request

FFMPEG_URL = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
TOOLS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools")
FFMPEG_DIR = os.path.join(TOOLS_DIR, "ffmpeg")
FFMPEG_BIN = os.path.join(FFMPEG_DIR, "bin", "ffmpeg.exe")

def download_progress(count, block_size, total_size):
    percent = int(count * block_size * 100 / total_size)
    sys.stdout.write(f"\rDownloading FFmpeg... {percent}%")
    sys.stdout.flush()

def setup_ffmpeg():
    if os.path.exists(FFMPEG_BIN):
        print(f"\n✅ FFmpeg already found at: {FFMPEG_BIN}")
        return FFMPEG_BIN

    if not os.path.exists(TOOLS_DIR):
        os.makedirs(TOOLS_DIR)

    zip_path = os.path.join(TOOLS_DIR, "ffmpeg.zip")
    
    print(f"Downloading FFmpeg from {FFMPEG_URL}...")
    try:
        urllib.request.urlretrieve(FFMPEG_URL, zip_path, reporthook=download_progress)
        print("\nDownload complete. Extracting...")
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Get the root folder name in the zip
            root_folder = zip_ref.namelist()[0].split('/')[0]
            zip_ref.extractall(TOOLS_DIR)
            
        # Rename extracted folder to 'ffmpeg'
        extracted_path = os.path.join(TOOLS_DIR, root_folder)
        if os.path.exists(FFMPEG_DIR):
            shutil.rmtree(FFMPEG_DIR)
        os.rename(extracted_path, FFMPEG_DIR)
        
        # Cleanup
        os.remove(zip_path)
        
        print(f"✅ FFmpeg setup complete! Binary at: {FFMPEG_BIN}")
        return FFMPEG_BIN
        
    except Exception as e:
        print(f"\n❌ Failed to setup FFmpeg: {e}")
        return None

if __name__ == "__main__":
    setup_ffmpeg()
