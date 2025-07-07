import os
import whisper
from docx import Document

video_path = "PATH_TO_VIDEO.mp4" 
audio_output_folder = "sample_outputs/audio/"
text_output_folder = "sample_outputs/transcriptions/"

os.makedirs(audio_output_folder, exist_ok=True)
os.makedirs(text_output_folder, exist_ok=True)

video_filename = os.path.splitext(os.path.basename(video_path))[0]
audio_output_path = os.path.join(audio_output_folder, f"{video_filename}.wav")
text_output_path = os.path.join(text_output_folder, f"{video_filename}.docx")

# Sesi wav formatında çıkar (mono)
from pydub import AudioSegment
AudioSegment.converter = "/usr/bin/ffmpeg"
audio = AudioSegment.from_file(video_path)
audio = audio.set_channels(1)
audio.export(audio_output_path, format="wav")
print(f"✅ Ses dosyası kaydedildi: {audio_output_path}")

# Transkripsiyon yap
model = whisper.load_model("base")
result = model.transcribe(audio_output_path, language="turkish")

if result["text"].strip():
    doc = Document()
    doc.add_paragraph(result["text"])
    doc.save(text_output_path)
    print(f"✅ Whisper ile metin dosyası kaydedildi: {text_output_path}")
else:
    print("❌ Metin bulunamadı, dosya oluşturulmadı!")
