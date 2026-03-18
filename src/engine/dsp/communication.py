import numpy as np
from scipy import signal

class CommunicationEffects:
    """
    Simulates communication devices:
    - Telephone (Landline, Mobile)
    - Radio (Walkie-Talkie, AM/FM)
    """

    def apply_telephone(self, data, samplerate, connection_quality='good'):
        """
        Simulate telephone sound.
        Bandpass: 300Hz - 3400Hz
        """
        # Bandpass Filter
        low_cut = 300
        high_cut = 3400
        
        # Design filter
        sos = signal.butter(4, [low_cut, high_cut], btype='band', fs=samplerate, output='sos')
        filtered = signal.sosfilt(sos, data, axis=0)
        
        # Add static/noise based on quality
        noise_level = 0.005 if connection_quality == 'good' else 0.05
        noise = np.random.normal(0, noise_level, filtered.shape)
        
        # Hard limiting (clipping) often found in cheap speakers
        processed = np.clip(filtered + noise, -0.8, 0.8)
        
        return processed

    def apply_radio(self, data, samplerate, freq_shift=0, bandwidth=5000):
        """
        Simulate AM/Shortwave radio.
        """
        # Lowpass/Bandpass
        sos = signal.butter(4, bandwidth, btype='low', fs=samplerate, output='sos')
        filtered = signal.sosfilt(sos, data, axis=0)
        
        # Add white noise (static)
        static = np.random.normal(0, 0.05, filtered.shape)
        
        # Ring modulation / Heterodyne noise (optional simple simulation)
        t = np.arange(len(data)) / samplerate
        carrier = np.sin(2 * np.pi * 1000 * t) * 0.02 # Subtle whistle
        if data.ndim > 1:
             carrier = carrier[:, np.newaxis]
        
        return filtered + static + carrier
