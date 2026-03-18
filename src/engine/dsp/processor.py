import logging
import numpy as np
import soundfile as sf
import os

class DspProcessor:
    """
    Traditional Digital Signal Processing Engine
    Handles effects chains, filtering, and physical modeling.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # Initialize sub-modules
        from .vintage import VintageEffects
        from .communication import CommunicationEffects
        
        self.vintage = VintageEffects()
        self.comm = CommunicationEffects()

    def process(self, input_path, output_path, params):
        """
        Process audio using DSP techniques
        """
        self.logger.info("Starting DSP processing...")
        
        try:
            # Load audio
            data, samplerate = sf.read(input_path)
        except Exception as e:
            self.logger.error(f"Failed to read input file: {e}")
            # Generate silence for testing if file missing
            samplerate = 44100
            data = np.zeros((samplerate * 2, 2))
            
        # Dispatch based on style
        style = params.get('style', 'default')
        p = params.get('params', {})
        
        if style == '8bit':
            self.logger.info("Applying 8-bit vintage effect")
            data = self.vintage.apply_8bit(data, samplerate, **p)
            
        elif style == 'tape':
            self.logger.info("Applying tape saturation effect")
            data = self.vintage.apply_tape(data, **p)
            
        elif style == 'vinyl':
            self.logger.info("Applying vinyl effect")
            data = self.vintage.apply_vinyl(data, samplerate, **p)
            
        elif style == 'telephone':
            self.logger.info("Applying telephone effect")
            data = self.comm.apply_telephone(data, samplerate, **p)
            
        elif style == 'radio':
            self.logger.info("Applying radio effect")
            data = self.comm.apply_radio(data, samplerate, **p)
            
        # Save output
        try:
            sf.write(output_path, data, samplerate)
            self.logger.info(f"DSP processing finished. Output saved to {output_path}")
        except Exception as e:
            self.logger.error(f"Failed to write output file: {e}")
