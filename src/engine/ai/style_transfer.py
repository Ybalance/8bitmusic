import logging
import os

try:
    import torch
    import torch.nn as nn
    import torchaudio
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    # Dummy classes for type hinting or fallback
    class nn:
        class Module: pass
    torch = None

if AI_AVAILABLE:
    class StyleNet(nn.Module):
        """
        The same Autoencoder architecture used in training.
        Must match src/train.py definition.
        """
        def __init__(self):
            super(StyleNet, self).__init__()
            # Encoder
            self.encoder = nn.Sequential(
                nn.Conv2d(1, 16, kernel_size=3, stride=2, padding=1),
                nn.ReLU(),
                nn.Conv2d(16, 32, kernel_size=3, stride=2, padding=1),
                nn.ReLU(),
                nn.Conv2d(32, 64, kernel_size=3, stride=2, padding=1),
                nn.ReLU()
            )
            # Decoder
            self.decoder = nn.Sequential(
                nn.ConvTranspose2d(64, 32, kernel_size=3, stride=2, padding=1, output_padding=1),
                nn.ReLU(),
                nn.ConvTranspose2d(32, 16, kernel_size=3, stride=2, padding=1, output_padding=1),
                nn.ReLU(),
                nn.ConvTranspose2d(16, 1, kernel_size=3, stride=2, padding=1, output_padding=1),
                nn.Tanh() 
            )

        def forward(self, x):
            encoded = self.encoder(x)
            decoded = self.decoder(encoded)
            return decoded
else:
    StyleNet = None

class AIStyleTransfer:
    """
    AI-based Audio Style Transfer Engine
    """
    
    def __init__(self, model_path=None):
        self.logger = logging.getLogger(__name__)
        
        if not AI_AVAILABLE:
            self.logger.warning("PyTorch or Torchaudio not found. AI features disabled.")
            self.device = "cpu"
            self.model = None
            return

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.logger.info(f"AI Engine initialized on {self.device}")
        
        self.model = StyleNet().to(self.device)
        
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
        else:
            self.logger.info("No model path provided or file not found. Using initialized weights (random).")
        
        self.model.eval()

    def load_model(self, model_path):
        try:
            self.logger.info(f"Loading model weights from {model_path}")
            # Map location to handle loading GPU models on CPU
            state_dict = torch.load(model_path, map_location=self.device)
            self.model.load_state_dict(state_dict)
        except Exception as e:
            self.logger.error(f"Failed to load model weights: {e}")

    def process(self, input_path, output_path, params):
        """
        Perform neural audio style transfer
        """
        if not AI_AVAILABLE:
            self.logger.error("AI features are not available.")
            return

        self.logger.info("Starting AI processing...")
        
        try:
            waveform, sample_rate = torchaudio.load(input_path)
            waveform = waveform.to(self.device)
        except Exception as e:
            self.logger.error(f"Failed to load audio: {e}")
            return

        target_style = params.get('style', 'neural')
        
        if target_style == "neural_style":
            output_waveform = self._neural_style_transfer(waveform, sample_rate)
        elif target_style == "genre_morph":
            output_waveform = self._genre_morph(waveform, params.get('genre'))
        else:
            output_waveform = waveform

        # Save output
        try:
            # Move to CPU before saving
            output_waveform = output_waveform.cpu()
            torchaudio.save(output_path, output_waveform, sample_rate)
            self.logger.info(f"AI processing finished. Saved to {output_path}")
        except Exception as e:
            self.logger.error(f"Failed to save output: {e}")

    def _neural_style_transfer(self, waveform, sample_rate):
        self.logger.info("Running Neural Style Transfer algorithm...")
        
        # 1. Compute Spectrogram
        n_fft = 255
        transform = torchaudio.transforms.Spectrogram(n_fft=n_fft).to(self.device)
        spectrogram = transform(waveform)
        
        # 2. Process with Autoencoder
        # We need to reshape for CNN: (Batch, Channel, Freq, Time)
        # Assuming mono for simplicity or processing channels independently
        original_shape = spectrogram.shape
        
        # Crop/Pad to fit model requirements (128 bins freq)
        # Note: In real app, we need smarter handling. Here we just take 128 bins.
        spec_input = spectrogram[:, :128, :]
        
        # Add batch and channel dim if needed [B, C, H, W]
        # Spectrogram is [Channels, Freq, Time]
        # Treat audio channels as batch items or separate channels?
        # Let's treat as [B=1, C=Channels, Freq, Time]
        spec_input = spec_input.unsqueeze(0)
        
        # Ensure Time is multiple of 8 (3 pooling layers with stride 2 = 8x downsample)
        pad_time = (8 - (spec_input.shape[3] % 8)) % 8
        if pad_time > 0:
             spec_input = torch.nn.functional.pad(spec_input, (0, pad_time))
             
        # Normalize
        mean = spec_input.mean()
        std = spec_input.std() + 1e-6
        spec_input_norm = (spec_input - mean) / std
        
        # Inference
        with torch.no_grad():
            styled_spec = self.model(spec_input_norm)
            
        # De-normalize
        styled_spec = styled_spec * std + mean
        
        # Remove padding
        if pad_time > 0:
            styled_spec = styled_spec[..., :-pad_time]
            
        # Pad frequency back to original if we cropped
        if original_shape[1] > 128:
            padding_freq = original_shape[1] - 128
            styled_spec = torch.nn.functional.pad(styled_spec, (0, 0, 0, padding_freq))
            
        # Squeeze batch dim
        styled_spec = styled_spec.squeeze(0)
        
        # 3. Invert back to audio (Griffin-Lim)
        griffin_lim = torchaudio.transforms.GriffinLim(n_fft=n_fft).to(self.device)
        output_waveform = griffin_lim(styled_spec)
        
        # Ensure length matches original
        if output_waveform.shape[1] > waveform.shape[1]:
            output_waveform = output_waveform[:, :waveform.shape[1]]
        elif output_waveform.shape[1] < waveform.shape[1]:
             padding = waveform.shape[1] - output_waveform.shape[1]
             output_waveform = torch.nn.functional.pad(output_waveform, (0, padding))
             
        return output_waveform

    def _genre_morph(self, waveform, genre):
        # ... existing implementation ...
        self.logger.info(f"Morphing to genre: {genre}")
        effects = []
        if genre == 'classical':
            effects.append(["speed", "0.8"])
            effects.append(["reverb", "50", "50", "100"])
        elif genre == 'electronic':
            effects.append(["speed", "1.2"])
            effects.append(["bass", "+5"])
            
        if effects:
            try:
                waveform, _ = torchaudio.sox_effects.apply_effects_tensor(waveform, 44100, effects)
            except Exception:
                self.logger.warning("Sox effects not available, returning original.")
                
        return waveform
