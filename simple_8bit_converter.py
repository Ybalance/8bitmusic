import subprocess
import sys
import os
import shutil

def get_ffmpeg_path():
    """
    Check if ffmpeg is installed and accessible.
    Prioritizes local tools/ffmpeg/bin/ffmpeg.exe
    """
    # 1. Check local project tools
    base_dir = os.path.dirname(os.path.abspath(__file__))
    local_ffmpeg = os.path.join(base_dir, "tools", "ffmpeg", "bin", "ffmpeg.exe")
    
    if os.path.exists(local_ffmpeg):
        return local_ffmpeg
        
    # 2. Check system PATH
    system_ffmpeg = shutil.which("ffmpeg")
    if system_ffmpeg:
        return system_ffmpeg
        
    return None

def convert_to_8bit(input_path, output_path=None):
    ffmpeg_exe = get_ffmpeg_path()
    
    if not ffmpeg_exe:
        print("❌ Error: FFmpeg is not found.")
        print("1. Please check your internet connection and run 'python setup_ffmpeg.py' again.")
        print("2. Or install FFmpeg manually and add it to your PATH.")
        return

    if not os.path.exists(input_path):
        print(f"❌ Error: Input file '{input_path}' not found.")
        return

    if output_path is None:
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_8bit.wav"

    print(f"🎵 Converting '{input_path}' to 8-bit style...")
    print(f"Using FFmpeg at: {ffmpeg_exe}")

    # FFmpeg filters for 8-bit effect:
    filters = "aresample=11025,acrusher=bits=5:samples=16:mode=log,volume=1.5"
    
    cmd = [
        ffmpeg_exe,
        "-y",               # Overwrite output
        "-i", input_path,   # Input
        "-af", filters,     # Audio Filters
        "-ac", "1",         # Mono
        output_path
    ]

    try:
        # Run ffmpeg
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"✅ Success! Output saved to: {output_path}")
    except subprocess.CalledProcessError as e:
        print("❌ Error occurred during conversion.")
        print(e.stderr.decode() if e.stderr else "Unknown error")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python simple_8bit_converter.py <input_file> [output_file]")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        convert_to_8bit(input_file, output_file)
