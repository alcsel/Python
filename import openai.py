from transformers import pipeline

# Hugging Face pipeline'ını kullanarak bir model yükle
model = pipeline("text-generation", model="gpt2")

# Giriş dosyasını oku
with open("Downloads/kayit_metni.txt", "r", encoding="utf-8") as file:
    input_text = file.read()

# Modeli kullanarak yanıt üret
response = model(input_text, max_length=500, num_return_sequences=1, truncation=True)

# Üretilen yanıtı al
answer = response[0]['generated_text']

# Yanıtı çıktı dosyasına yaz
with open("cikti.txt", "w", encoding="utf-8") as file:
    file.write(answer)

print("Yapay zeka yanıtı cikti.txt dosyasına yazıldı.")