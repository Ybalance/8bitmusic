import os
import yaml
import logging
from enum import Enum
from typing import Dict, Any, Optional

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EngineType(Enum):
    DSP = "dsp"
    AI = "ai"
    HYBRID = "hybrid"

class AudioMorphEngine:
    """
    Audio Morph Studio Pro Core Engine
    
    Orchestrates the processing of audio through various sub-engines:
    1. DSP Engine (Traditional Signal Processing)
    2. AI Engine (Machine Learning Models)
    3. Hybrid Engine (Combination)
    """
    
    def __init__(self, config_path: Optional[str] = None):
        self.logger = logging.getLogger("AudioMorphEngine")
        self.config = self._load_config(config_path) if config_path else {}
        
        # Initialize sub-engines
        self.dsp_engine = self._init_dsp_engine()
        self.ai_engine = self._init_ai_engine()
        self.hybrid_engine = self._init_hybrid_engine()
        
        self.logger.info("AudioMorphEngine initialized successfully")

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            self.logger.error(f"Failed to load config: {e}")
            return {}

    def _init_dsp_engine(self):
        # Lazy import to avoid circular dependencies
        from .dsp.processor import DspProcessor
        self.logger.info("Initializing DSP Engine...")
        return DspProcessor()

    def _init_ai_engine(self):
        from .ai.style_transfer import AIStyleTransfer
        self.logger.info("Initializing AI Engine...")
        return AIStyleTransfer()

    def _init_hybrid_engine(self):
        from .hybrid.processor import HybridProcessor
        self.logger.info("Initializing Hybrid Engine...")
        return HybridProcessor()

    def process_audio(self, input_path: str, output_path: str, preset: Dict[str, Any]):
        """
        Main processing pipeline
        
        Args:
            input_path: Path to input audio file
            output_path: Path to save processed audio
            preset: Dictionary containing processing parameters
        """
        self.logger.info(f"Processing {input_path} with preset: {preset.get('name', 'Custom')}")
        
        engine_type = preset.get('engine_type', EngineType.DSP.value)
        
        try:
            if engine_type == EngineType.DSP.value:
                self.dsp_engine.process(input_path, output_path, preset)
            elif engine_type == EngineType.AI.value:
                self.ai_engine.process(input_path, output_path, preset)
            elif engine_type == EngineType.HYBRID.value:
                self.hybrid_engine.process(input_path, output_path, preset)
            else:
                raise ValueError(f"Unknown engine type: {engine_type}")
                
            self.logger.info(f"Processing complete. Saved to {output_path}")
            
        except Exception as e:
            self.logger.error(f"Error during processing: {e}")
            raise

    def get_supported_styles(self):
        return {
            "vintage": ["8bit", "tape", "vinyl"],
            "genre": ["electronic", "classical", "rock"],
            "ai": ["style_transfer", "generative"]
        }
