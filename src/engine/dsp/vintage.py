import numpy as np
from scipy import signal

class VintageEffects:
    """
    Implements vintage audio effects:
    - 8-bit / Bitcrushing
    - Tape saturation
    - Vinyl crackle and Wow & Flutter
    """
    
    def apply_8bit(self, data, samplerate, bit_depth=8, downsample_factor=4):
        """
        Simulate 8-bit game console sound
        """
        # Downsampling (sample rate reduction)
        if downsample_factor > 1:
            # Simple decimation and zero-order hold
            data = data[::downsample_factor]
            data = np.repeat(data, downsample_factor)
            # Handle length mismatch if any
            
        # Bit reduction
        scale = 2 ** (bit_depth - 1)
        data = np.round(data * scale) / scale
        
        return data

    def apply_tape(self, data, drive=0.5, hiss_level=0.01):
        """
        Simulate tape saturation and hiss
        """
        # Saturation
        saturated = np.tanh(data * (1 + drive))
        
        # Tape Hiss (White/Pink noise approximation)
        hiss = np.random.normal(0, hiss_level, data.shape)
        
        return saturated + hiss

    def apply_vinyl(self, data, samplerate, noise_level=0.02, crackle_density=0.001, wow_rate=0.5, wow_depth=0.002):
        """
        Add vinyl characteristics:
        - Surface noise
        - Crackle (pops)
        - Wow & Flutter (pitch variation)
        """
        # 1. Surface Noise
        noise = np.random.normal(0, noise_level, data.shape)
        
        # 2. Crackle (Impulse noise)
        # Create a mask of random events
        crackle_mask = np.random.random(data.shape) < crackle_density
        crackle = crackle_mask * np.random.random(data.shape) * 0.5 # clicks
        
        # 3. Wow & Flutter (Delay modulation)
        # Generate a slowly varying LFO
        t = np.arange(len(data)) / samplerate
        lfo = np.sin(2 * np.pi * wow_rate * t) * wow_depth
        
        # Apply variable delay (resampling effect)
        # We map output time t to input time t + lfo(t)
        # Using linear interpolation for simplicity
        indices = np.arange(len(data))
        shifted_indices = indices + (lfo * samplerate)
        
        # Clamp indices
        shifted_indices = np.clip(shifted_indices, 0, len(data) - 1)
        
        # Interpolate
        # Note: interp is 1D, so we might need to handle stereo channels separately if data is 2D
        if data.ndim == 1:
            wow_data = np.interp(shifted_indices, indices, data)
        else:
            wow_data = np.zeros_like(data)
            for ch in range(data.shape[1]):
                wow_data[:, ch] = np.interp(shifted_indices, indices, data[:, ch])
                
        return wow_data + noise + crackle
