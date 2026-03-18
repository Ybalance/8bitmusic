import os
import argparse
import logging
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import torchaudio

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- 1. Define Model Architecture ---
class StyleNet(nn.Module):
    """
    A simple Autoencoder-like architecture for learning style features.
    In a real scenario, this could be a VAE or GAN generator.
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
            nn.Tanh() # Assuming normalized audio/spectrogram
        )

    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded

# --- 2. Define Dataset ---
class AudioDataset(Dataset):
    """
    Loads audio files from a directory for training.
    """
    def __init__(self, audio_dir, sample_rate=22050, duration=2):
        self.audio_dir = audio_dir
        self.sample_rate = sample_rate
        self.duration = duration
        self.files = [f for f in os.listdir(audio_dir) if f.endswith(('.wav', '.mp3'))]
        if not self.files:
            logger.warning(f"No audio files found in {audio_dir}. Using random noise for demonstration.")

    def __len__(self):
        return len(self.files) if self.files else 100 # Mock length if empty

    def __getitem__(self, idx):
        if not self.files:
            # Generate random spectrogram for demo if no files
            return torch.randn(1, 128, 128)

        file_path = os.path.join(self.audio_dir, self.files[idx])
        try:
            waveform, sr = torchaudio.load(file_path)
            # Resample if needed
            if sr != self.sample_rate:
                resampler = torchaudio.transforms.Resample(sr, self.sample_rate)
                waveform = resampler(waveform)
            
            # Cut/Pad to fixed duration
            num_samples = int(self.sample_rate * self.duration)
            if waveform.shape[1] > num_samples:
                waveform = waveform[:, :num_samples]
            else:
                padding = num_samples - waveform.shape[1]
                waveform = torch.nn.functional.pad(waveform, (0, padding))

            # Convert to Spectrogram
            spec_transform = torchaudio.transforms.Spectrogram(n_fft=255) # Results in 128 freq bins
            spec = spec_transform(waveform)
            
            # Take first channel and crop/resize to fixed size for CNN (e.g., 128x128)
            # For simplicity, we just take a slice
            spec = spec[0:1, :128, :128] 
            
            # Normalize
            spec = (spec - spec.mean()) / (spec.std() + 1e-6)
            
            return spec
            
        except Exception as e:
            logger.error(f"Error loading {file_path}: {e}")
            return torch.randn(1, 128, 128)

# --- 3. Training Loop ---
def train(args):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logger.info(f"Training on {device}")

    # Initialize Dataset & Dataloader
    dataset = AudioDataset(args.data_dir)
    dataloader = DataLoader(dataset, batch_size=args.batch_size, shuffle=True)

    # Initialize Model
    model = StyleNet().to(device)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=args.lr)

    logger.info("Starting training...")
    model.train()
    
    for epoch in range(args.epochs):
        total_loss = 0
        for i, batch in enumerate(dataloader):
            batch = batch.to(device)
            
            optimizer.zero_grad()
            outputs = model(batch)
            loss = criterion(outputs, batch) # Autoencoder reconstruction loss
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
        
        avg_loss = total_loss / len(dataloader)
        logger.info(f"Epoch [{epoch+1}/{args.epochs}], Loss: {avg_loss:.4f}")

    # Save Model
    os.makedirs(args.save_dir, exist_ok=True)
    save_path = os.path.join(args.save_dir, f"{args.style_name}.pth")
    torch.save(model.state_dict(), save_path)
    logger.info(f"Model saved to {save_path}")

def main():
    parser = argparse.ArgumentParser(description="Train Audio Style Model")
    parser.add_argument("--data_dir", type=str, required=True, help="Directory containing training audio files (wav/mp3)")
    parser.add_argument("--style_name", type=str, default="custom_style", help="Name of the style to save")
    parser.add_argument("--save_dir", type=str, default="models", help="Directory to save trained models")
    parser.add_argument("--epochs", type=int, default=10, help="Number of training epochs")
    parser.add_argument("--batch_size", type=int, default=4, help="Batch size")
    parser.add_argument("--lr", type=float, default=0.001, help="Learning rate")

    args = parser.parse_args()
    
    if not os.path.exists(args.data_dir):
        logger.warning(f"Data directory '{args.data_dir}' does not exist. Creating it for demo purposes.")
        os.makedirs(args.data_dir)
        
    train(args)

if __name__ == "__main__":
    main()
