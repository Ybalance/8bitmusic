import os
import yaml
import logging
from typing import Dict, List, Any

class PresetManager:
    """
    Manages audio processing presets.
    Supported formats: YAML, JSON
    """
    
    def __init__(self, preset_dir: str = "presets"):
        self.logger = logging.getLogger(__name__)
        self.preset_dir = preset_dir
        self.presets: Dict[str, Any] = {}
        self._load_all_presets()

    def _load_all_presets(self):
        """Load all presets from the preset directory"""
        if not os.path.exists(self.preset_dir):
            os.makedirs(self.preset_dir)
            return

        for root, _, files in os.walk(self.preset_dir):
            for file in files:
                if file.endswith(('.yaml', '.yml', '.json')):
                    self.load_preset(os.path.join(root, file))

    def load_preset(self, path: str):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                name = data.get('name', os.path.basename(path))
                self.presets[name] = data
                self.logger.info(f"Loaded preset: {name}")
        except Exception as e:
            self.logger.error(f"Failed to load preset {path}: {e}")

    def get_preset(self, name: str) -> Dict[str, Any]:
        return self.presets.get(name)

    def save_preset(self, name: str, data: Dict[str, Any]):
        filename = f"{name.lower().replace(' ', '_')}.yaml"
        path = os.path.join(self.preset_dir, filename)
        
        try:
            with open(path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f)
            self.presets[name] = data
            self.logger.info(f"Saved preset: {name}")
        except Exception as e:
            self.logger.error(f"Failed to save preset {name}: {e}")

    def create_ai_preset(self, name: str, model_path: str):
        """Create a new preset for a trained AI model"""
        data = {
            "name": name,
            "category": "AI Custom",
            "engine_type": "ai",
            "style": "neural_style",
            "description": f"Custom trained AI model: {name}",
            "params": {
                "model_path": model_path
            }
        }
        self.save_preset(name, data)

    def list_presets(self) -> List[str]:
        return list(self.presets.keys())

    def create_default_presets(self):
        """Generate some starter presets based on project specs"""
        defaults = [
            {
                "name": "Nintendo 8-bit",
                "category": "Vintage",
                "engine_type": "dsp",
                "style": "8bit",
                "params": {"bit_depth": 8, "downsample": 4}
            },
            {
                "name": "VHS Tape",
                "category": "Vintage",
                "engine_type": "dsp",
                "style": "tape",
                "params": {"drive": 0.4, "hiss": 0.1}
            },
             {
                "name": "Cyberpunk 2077",
                "category": "Sci-Fi",
                "engine_type": "hybrid",
                "style": "synth_wave",
                "params": {"distortion": "digital", "reverb": "large_hall"}
            }
        ]
        
        for p in defaults:
            self.save_preset(p['name'], p)
