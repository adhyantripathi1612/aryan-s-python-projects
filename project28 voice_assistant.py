from g4f.models import gpt_4
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import g4f
import pywhatkit
import webbrowser

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 170)

def ask_llm(query):
       response = requests.post("http://localhost:11434/api/generate", json={
        "model": gpt_4,
        "prompt": f"You are a helpful voice assistant. Answer briefly: {query}",
        "stream": False
    })
    


def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nWaiting for your command...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)
        try:
            query = recognizer.recognize_google(audio, language='en-in')
            print(f"User: {query}\n")
            return query.lower()
        except Exception:
            return "none"

def run_assistant():
    speak("I am online. How can I help you today? And if you want to quit then say 'stop', or 'quit'")
    while True:
        query = take_command()

        if 'time' in query:
            now = datetime.datetime.now().strftime("%H:%M")
            speak(f"The current time is {now}")

        elif 'play' in query:
            song = query.replace('play', '')
            speak(f"Playing {song}")
            pywhatkit.playonyt(song)

        elif 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            speak(results)

        elif 'open google' in query:
            webbrowser.open("google.com")
            speak("Opening Google")

        elif 'stop' in query or 'exit' in query:
            speak("Goodbye!")
            break

if __name__ == "__main__":
    run_assistant()
