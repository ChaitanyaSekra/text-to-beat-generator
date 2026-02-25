import torch
from transformers import AutoProcessor, MusicgenForConditionalGeneration
import scipy
import os

# 🧠 Check for GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"🚀 Using device: {device}")

# 📦 Load processor and model
processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small").to(device)

# 📁 Make sure output directory exists
os.makedirs("generated_beats", exist_ok=True)

while True:
    # 📝 Take user prompt
    music_text = input("🎤 Describe your beat (or type 'stop' to quit):\n").strip()
    if music_text.lower() == "stop":
        print("👋 Exiting. Peace out 🎧")
        break

    print(f"🎼 Generating beat for: \"{music_text}\" ...")

    # 🔄 Preprocess input and move tensors to GPU
    inputs = processor(text=music_text, padding=True, return_tensors="pt")
    inputs = {k: v.to(device) for k, v in inputs.items()}

    # 🎧 Generate audio (1024 tokens ≈ 15 seconds)
    with torch.no_grad():
        audio_values = model.generate(**inputs, max_new_tokens=1024)

    # 📂 Save file with clean filename
    safe_name = "".join(c if c.isalnum() else "_" for c in music_text)[:30]
    filename = f"generated_beats/{safe_name}_{torch.randint(0,9999,(1,)).item()}.wav"

    # 💾 Save to disk
    sampling_rate = model.config.audio_encoder.sampling_rate
    scipy.io.wavfile.write(filename, rate=sampling_rate, data=audio_values[0, 0].cpu().numpy())

    print(f"✅ Beat saved: {filename}\n")
