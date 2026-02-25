# generator.py

from transformers import AutoProcessor, MusicgenForConditionalGeneration
import scipy
import torch
import os
from pathlib import Path

# Load model and processor once (avoid reloading each time)
processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")

OUTPUT_DIR = Path("generated_beats")
OUTPUT_DIR.mkdir(exist_ok=True)

def generate_beat(prompt: str) -> str:
    """Generates a beat from prompt and returns filename."""
    inputs = processor(
        text=prompt,
        padding=True,
        return_tensors="pt"
    )

    audio_values = model.generate(**inputs, max_new_tokens=1024)

    sampling_rate = model.config.audio_encoder.sampling_rate

    # Generate unique filename
    safe_name = "".join(c if c.isalnum() else "_" for c in prompt)[:20]
    filename = f"{safe_name}_{torch.randint(0, 10000, (1,)).item()}.wav"
    filepath = OUTPUT_DIR / filename

    scipy.io.wavfile.write(filepath, rate=sampling_rate, data=audio_values[0, 0].numpy())

    return str(filepath)
