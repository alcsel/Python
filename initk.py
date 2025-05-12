import os
from kokoro import KPipeline
import soundfile as sf

# 1. Kokoro pipeline'ını başlat
pipeline = KPipeline(lang_code='a')  # 'a' Amerikan İngilizcesi için

# 2. .txt dosyasından metni oku
with open("C:/Users/alcse/Downloads/kayit_metni.txt", "r", encoding="utf-8") as file:
    user_prompt = file.read().strip()

print("Kullanıcının sorusu:", user_prompt)

# 3. Basit bir yanıt oluştur (örnek amaçlı)
response = user_prompt  # Kullanıcının metnini seslendir

# 4. Yanıtı seslendir
generator = pipeline(response, voice='af_heart')  # 'af_heart' varsayılan ses

for i, (gs, ps, audio) in enumerate(generator):
    output_path = f"cevap_{i}.wav"
    sf.write(output_path, audio, 24000)
    # Ses dosyasını çal
    if os.name == "nt":  # Windows
        os.system(f'start {output_path}')
    else:
        os.system(f'aplay {output_path}')

