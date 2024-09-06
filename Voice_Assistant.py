from email.mime import audio
from socket import timeout
import openai # type: ignore
import pyttsx3 # type: ignore
import speech_recognition as sr # type: ignore
import time

openai.api_key = ""

engine = pyttsx3.init()

def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        print("Skipping Unknown Error")

def generate_response(prompt):
    response = openai.Completion.create(
        engine= "text-davinci-003",
        prompt = prompt,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response["choices"][0]["text"]

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def main():
    while True:
        greeting = "Hi, My name is Saturday developed by Himanshu Panday. How may I assist you?"
        speak_text(greeting)
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)
                if transcription.lower() == "Saturday":
                    filename = "input.wav"
                    print("say your question...")
                    with sr.Microphone() as source:
                        recognizer = sr.Recognizer()
                        source.pause_threshold = 1
                        audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                        with open(filename, "wb") as f:
                            f.write(audio.get_wav_data())

                    text = transcribe_audio_to_text(filename)
                    if text:
                        print(f"you said: {text}")
                        response= generate_response(text)
                        print(f"GPT-3 says: {response}")
                        tts = gTTS(text = response, lang='en') # type: ignore
                        tts.save("sample.mp3")
                        speak_text(response)
            except Exception as e:
                print("An error occurred: {}".format(e))

if __name__ == "__main__":
    main()