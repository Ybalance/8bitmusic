import logging

class HybridProcessor:
    """
    Combines DSP and AI techniques for optimal results.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # Lazy imports
        from ..dsp.processor import DspProcessor
        from ..ai.style_transfer import AIStyleTransfer
        
        self.dsp = DspProcessor()
        self.ai = AIStyleTransfer()

    def process(self, input_path, output_path, params):
        self.logger.info("Starting Hybrid processing...")
        
        # Example pipeline: AI for timbre transfer -> DSP for polishing
        
        # Step 1: AI Processing
        temp_path = input_path + ".temp.wav"
        self.ai.process(input_path, temp_path, params)
        
        # Step 2: DSP Post-processing
        self.dsp.process(temp_path, output_path, params)
        
        self.logger.info("Hybrid processing finished.")
