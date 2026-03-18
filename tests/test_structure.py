import unittest
import sys
import os

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from engine.core import AudioMorphEngine
from engine.dsp.processor import DspProcessor
from engine.ai.style_transfer import AIStyleTransfer
from presets.manager import PresetManager

class TestAudioMorphArchitecture(unittest.TestCase):
    
    def test_engine_initialization(self):
        """Test that the main engine initializes sub-engines correctly"""
        engine = AudioMorphEngine()
        self.assertIsInstance(engine.dsp_engine, DspProcessor)
        self.assertIsInstance(engine.ai_engine, AIStyleTransfer)
        
    def test_preset_manager(self):
        """Test preset manager functionality"""
        pm = PresetManager(preset_dir="test_presets")
        pm.create_default_presets()
        presets = pm.list_presets()
        self.assertIn("Nintendo 8-bit", presets)
        
        # Cleanup
        import shutil
        if os.path.exists("test_presets"):
            shutil.rmtree("test_presets")

if __name__ == '__main__':
    unittest.main()
