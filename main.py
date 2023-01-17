import os
import openai
from dotenv import load_dotenv
import speech_recognition
import pyttsx3
import playsound
from gtts import gTTS

print("voice recognition started:")
recognizer = speech_recognition.Recognizer()


def voice_assistant_speak(input_text):
    tts = gTTS(text=input_text, lang='en')
    filename = 'speech_content.mp3'
    tts.save(filename)
    playsound.playsound(filename)


def speak_text(input_stream):
    engine = pyttsx3.init()
    engine.say(input_stream)
    engine.runAndWait()


text = ''

load_dotenv()
openai.organization = os.getenv('ORG_ID')
openai.api_key = os.getenv('OPENAI_API_KEY')

try:
    while True:
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                text = recognizer.recognize_google(audio)
                text = text.lower()

                print(f"Recognized {text}")

        except Exception as e:
            print(str(e))
            recognizer = speech_recognition.Recognizer()
            continue

        input_prompt = input("A Question has been asked -> please press enter: ")
        prompt = text
        completions = openai.Completion.create(
            prompt=prompt,
            engine="text-davinci-003",
            max_tokens=100

        )
        completion = completions.choices[0].text
        print(completion)
        voice_assistant_speak(completion)
except Exception as e:
    raise e
