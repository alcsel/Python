from flask import Flask, request
from flask_cors import CORS
import os, wave, vosk, json
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

app = Flask(__name__)
CORS(app)
# Vosk modeli
model_path = "models/vosk-model-small-tr-0.3"
if not os.path.exists(model_path):
    raise FileNotFoundError("Vosk modeli bulunamadı.")
vosk_model = vosk.Model(model_path)

# Hugging Face Türkçe T5 modeli
model_id = "Turkish-NLP/t5-efficient-base-turkish"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForSeq2SeqLM.from_pretrained(model_id)
generator = pipeline("text2text-generation", model=model, tokenizer=tokenizer)

@app.route('/convert', methods=['POST'])
def convert_and_respond():
    if 'audio' not in request.files:
        return "Ses dosyası bulunamadı.", 400

    audio_file = request.files['audio']
    audio_path = "temp_audio.webm"
    pcm_path = "temp_audio.wav"

    try:
        audio_file.save(audio_path)
        os.system(f"ffmpeg -y -i {audio_path} -ac 1 -ar 16000 -sample_fmt s16 {pcm_path}")
    except Exception as e:
        return f"Ses işlenemedi: {e}", 500

    try:
        with wave.open(pcm_path, "rb") as wf:
            if wf.getnchannels() != 1 or wf.getsampwidth() != 2:
                return "WAV dosyası mono ve 16-bit olmalı.", 400

            recognizer = vosk.KaldiRecognizer(vosk_model, wf.getframerate())
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

        if not text.strip():
            return "Boş metin tanındı.", 400

        with open("kayit_metni.txt", "w", encoding="utf-8") as f:
            f.write(text)

        # GPT2 ile kısa Türkçe cevap üret
        prompt = text.strip()
        response = generator(prompt, max_length=80, temperature=0.7)[0]['generated_text']

        with open("cikti.txt", "w", encoding="utf-8") as f:
            f.write(response)

        return response

    except Exception as e:
        return f"Hata oluştu: {e}", 500
    finally:
        if os.path.exists(audio_path): os.remove(audio_path)
        if os.path.exists(pcm_path): os.remove(pcm_path)

if __name__ == '__main__':
    app.run(debug=True, port=5000)