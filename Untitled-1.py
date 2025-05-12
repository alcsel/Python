import openai
import pyttsx3

def ai_response(prompt):
    openai.api_key = "YOUR_API_KEY"  # OpenAI API anahtarınızı buraya ekleyin

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Hata: {str(e)}"

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    user_input = input("Bir metin girin: ")
    response = ai_response(user_input)
    print("Yapay Zeka Cevabı:", response)
    speak(response)