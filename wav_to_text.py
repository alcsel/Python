import os
import wave
import json
import vosk
import subprocess

def download_and_extract_model(model_url, extract_path):
    import requests
    import zipfile

    zip_path = os.path.join(extract_path, "model.zip")
    if not os.path.exists(extract_path):
        os.makedirs(extract_path)

    print("🔽 Vosk Türkçe modeli indiriliyor...")
    response = requests.get(model_url, stream=True)
    total = int(response.headers.get('content-length', 0))
    with open(zip_path, 'wb') as f:
        downloaded = 0
        for data in response.iter_content(chunk_size=1024 * 1024):
            downloaded += len(data)
            f.write(data)
            done = int(50 * downloaded / total)
            print(f"\r[{'█' * done}{'.' * (50 - done)}] % {int(downloaded / total * 100)}", end='')

    print("\n📦 İndirme tamamlandı, çıkartılıyor...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    os.remove(zip_path)
    print("✅ Model başarıyla indirildi ve çıkartıldı.")

def convert_webm_to_pcm(input_file, output_file):
    try:
        # FFmpeg komutunu çalıştırarak dönüştürme işlemini yap
        subprocess.run([
            "ffmpeg", "-i", input_file, "-ac", "1", "-ar", "16000", "-sample_fmt", "s16", output_file
        ], check=True)
        print(f"🎵 {input_file} → {output_file} olarak dönüştürüldü.")
    except Exception as e:
        print(f"❌ FFmpeg dönüştürme hatası: {e}")

def wav_to_text(wav_file, output_txt_file, model_path):
    try:
        if not os.path.exists(model_path):
            model_url = "https://alphacephei.com/vosk/models/vosk-model-small-tr-0.3.zip"
            download_and_extract_model(model_url, model_path)

        model = vosk.Model(model_path)

        with wave.open(wav_file, "rb") as wf:
            if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() not in [8000, 16000, 32000, 44100, 48000]:
                raise ValueError("WAV dosyası mono, 16-bit olmalı ve desteklenen bir örnekleme oranında olmalıdır.")

            recognizer = vosk.KaldiRecognizer(model, wf.getframerate())
            text = ""

            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    text += result.get("text", "") + " "

            final_result = json.loads(recognizer.FinalResult())
            text += final_result.get("text", "")

        with open(output_txt_file, "w", encoding="utf-8") as file:
            file.write(text.strip())

        print(f"📝 Metin başarıyla kaydedildi: {output_txt_file}")
    except Exception as e:
        print(f"❌ Hata oluştu: {e}")

# Kullanım
input_webm_file = "c:\\Users\\alcse\\Downloads\\kayit.webm"  # WebM formatındaki giriş dosyası
output_pcm_wav_file = "c:\\Users\\alcse\\Downloads\\kayit_pcm.wav"  # PCM formatındaki çıkış dosyası
convert_webm_to_pcm(input_webm_file, output_pcm_wav_file)

# PCM dosyasını metne çevirme işlemini başlat
wav_file = output_pcm_wav_file
output_txt_file = "c:\\Users\\alcse\\Documents\\kayit_metni.txt"  # Çıktı metin dosyasının tam yolu
model_dir = "models/vosk-model-small-tr-0.3"  # Modelin bulunduğu dizin

wav_to_text(wav_file, output_txt_file, model_dir)
