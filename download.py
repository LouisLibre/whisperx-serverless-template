# In this file, we define download_model
# It runs during container build time to get model weights built into the container

# In this example: A Huggingface BERT model

import whisperx
import torch

DEVICE = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

def download_model():
    print(f"HELLO; CUDA available? {torch.cuda.is_available()}, device: {DEVICE}")
    model = whisperx.load_model("large", DEVICE)

if __name__ == "__main__":
    download_model()
