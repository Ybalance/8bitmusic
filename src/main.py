import os
import argparse
import logging
from engine.core import AudioMorphEngine
from presets.manager import PresetManager

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def main():
    setup_logging()
    logger = logging.getLogger("AudioMorphStudio")
    
    parser = argparse.ArgumentParser(description="Audio Morph Studio Pro CLI")
    parser.add_argument("--input", "-i", help="Input audio file path")
    parser.add_argument("--output", "-o", help="Output audio file path")
    parser.add_argument("--preset", "-p", help="Preset name to apply")
    parser.add_argument("--list-presets", action="store_true", help="List available presets")
    
    args = parser.parse_args()
    
    # Initialize components
    # Ensure preset directory exists relative to this script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    preset_dir = os.path.join(base_dir, "presets_data")
    
    preset_manager = PresetManager(preset_dir)
    
    # Create defaults if empty
    if not os.path.exists(preset_dir) or not os.listdir(preset_dir):
        preset_manager.create_default_presets()
        
    engine = AudioMorphEngine()
    
    if args.list_presets:
        print("Available Presets:")
        for p in preset_manager.list_presets():
            print(f"- {p}")
        return

    if args.input and args.output:
        if not args.preset:
            logger.error("Please specify a preset with --preset")
            return
            
        preset_data = preset_manager.get_preset(args.preset)
        if not preset_data:
            logger.error(f"Preset '{args.preset}' not found.")
            return
            
        logger.info(f"Starting conversion: {args.input} -> {args.output}")
        try:
            # check if input file exists
            if not os.path.exists(args.input):
                 logger.error(f"Input file not found: {args.input}")
                 # For demo purposes, we might skip actual processing if file doesn't exist
                 return

            engine.process_audio(args.input, args.output, preset_data)
            logger.info("Conversion successful!")
        except Exception as e:
            logger.error(f"Conversion failed: {e}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
