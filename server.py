from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import wave
import vosk
import json

app = Flask(__name__)
CORS(app)  # CORS desteği ekleniyor

# Vosk modelini yükle
model_path = "models/vosk-model-small-tr-0.3"
if not os.path.exists(model_path):
    raise FileNotFoundError("Vosk modeli bulunamadı. Lütfen doğru model yolunu sağlayın.")
model = vosk.Model(model_path)

@app.route('/convert', methods=['POST'])
def convert_audio_to_text():
    if 'audio' not in request.files:
        return "Ses dosyası bulunamadı.", 400

    audio_file = request.files['audio']
    audio_path = "temp_audio.webm"
    pcm_path = "temp_audio.wav"

    # WebM dosyasını kaydet
    try:
        audio_file.save(audio_path)
    except Exception as e:
        return f"Ses dosyası kaydedilemedi: {e}", 500

    # FFmpeg ile PCM'e dönüştür
    try:
        os.system(f"ffmpeg -i {audio_path} -ac 1 -ar 16000 -sample_fmt s16 {pcm_path}")
    except Exception as e:
        return f"FFmpeg dönüştürme hatası: {e}", 500

    # WAV dosyasını metne çevir
    try:
        with wave.open(pcm_path, "rb") as wf:
            if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() not in [8000, 16000, 32000, 44100, 48000]:
                return "WAV dosyası mono, 16-bit olmalı ve desteklenen bir örnekleme oranında olmalıdır.", 400

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

        return text.strip()
    except Exception as e:
        return f"Hata oluştu: {e}", 500
    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)
        if os.path.exists(pcm_path):
            os.remove(pcm_path)

if __name__ == '__main__':
    app.run(debug=True, port=5000)