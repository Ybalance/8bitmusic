import unittest
import sys
import os
import numpy as np

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from engine.dsp.vintage import VintageEffects
from engine.dsp.communication import CommunicationEffects
from engine.ai.style_transfer import AIStyleTransfer

class TestAdvancedFeatures(unittest.TestCase):
    
    def setUp(self):
        self.vintage = VintageEffects()
        self.comm = CommunicationEffects()
        self.ai = AIStyleTransfer()
        self.samplerate = 44100
        # Create 1 second of silence/sine wave
        t = np.linspace(0, 1, self.samplerate)
        self.audio = np.sin(2 * np.pi * 440 * t)

    def test_vinyl_effects(self):
        """Test Vinyl crackle and wow/flutter"""
        processed = self.vintage.apply_vinyl(
            self.audio, 
            self.samplerate, 
            noise_level=0.01,
            crackle_density=0.001,
            wow_rate=1.0,
            wow_depth=0.005
        )
        self.assertEqual(processed.shape, self.audio.shape)
        self.assertFalse(np.array_equal(processed, self.audio))
        
    def test_telephone_effects(self):
        """Test Telephone bandpass and distortion"""
        processed = self.comm.apply_telephone(self.audio, self.samplerate)
        self.assertEqual(processed.shape, self.audio.shape)
        # Check if output is clipped/limited range
        self.assertTrue(np.max(np.abs(processed)) <= 0.85) 

    def test_ai_mock_processing(self):
        """Test AI processing pipeline (Mock)"""
        # We can't easily load audio in test without a file, 
        # so we'll just test if the class initializes and has methods
        self.assertTrue(hasattr(self.ai, 'process'))
        self.assertTrue(hasattr(self.ai, 'model'))

if __name__ == '__main__':
    unittest.main()
