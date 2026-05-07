import speech_recognition as sr
import pyttsx3
import pyautogui
import subprocess
import os
import requests
import openai
import spacy
import datetime
import wikipediaapi
import json

# Load spaCy model for NLP
nlp = spacy.load("en_core_web_sm")

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech

# OpenAI API key (set your key here or use environment variable)
openai.api_key = os.getenv('OPENAI_API_KEY')

# Wikipedia API
wiki_wiki = wikipediaapi.Wikipedia('en')

# Memory file
MEMORY_FILE = 'assistant_memory.json'

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_memory(memory):
    with open(MEMORY_FILE, 'w') as f:
        json.dump(memory, f)

memory = load_memory()

def speak(text):
    print(f"Hanry: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
            return ""
        except sr.RequestError:
            speak("Sorry, speech service is down.")
            return ""

def wake_word_detected(command):
    return "hey hanry" in command or "hanry" in command

def authenticate_user():
    # Basic authentication: for now, just check wake word
    # For advanced: implement voiceprint recognition (requires additional setup)
    speak("Voice authenticated. How can I help?")
    return True

def classify_intent(command):
    doc = nlp(command)
    if "open" in command:
        return "open_app"
    elif "search" in command or "google" in command:
        return "search_web"
    elif "shutdown" in command or "shut down" in command:
        return "shutdown"
    elif "time" in command or "what time" in command:
        return "time"
    elif "weather" in command:
        return "weather"
    elif "wikipedia" in command or "wiki" in command:
        return "wikipedia"
    elif "exit" in command or "quit" in command:
        return "exit"
    else:
        return "general"

def get_time():
    now = datetime.datetime.now()
    return now.strftime("The current time is %I:%M %p")

def get_weather():
    # Using wttr.in for weather (no API key needed)
    try:
        response = requests.get("https://wttr.in?format=3")
        return response.text.strip()
    except:
        return "Unable to fetch weather information."

def search_wikipedia(query):
    page = wiki_wiki.page(query)
    if page.exists():
        return page.summary[:500] + "..."  # Limit summary
    else:
        return "No Wikipedia page found for that query."

def ai_response(command):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Hanry, an advanced AI assistant. Respond helpfully and concisely."},
                {"role": "user", "content": command}
            ],
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except:
        return "I'm sorry, I couldn't process that request."

def execute_command(command):
    intent = classify_intent(command)
    if intent == "open_app":
        app = command.replace("open", "").strip()
        try:
            subprocess.run(["start", app], shell=True)  # Windows
            speak(f"Opening {app}")
        except:
            speak("Could not open that application.")
    elif intent == "search_web":
        query = command.replace("search", "").replace("google", "").strip()
        url = f"https://www.google.com/search?q={query}"
        pyautogui.hotkey('ctrl', 't')  # Open new tab
        pyautogui.typewrite(url)
        pyautogui.press('enter')
        speak(f"Searching for {query}")
    elif intent == "shutdown":
        speak("Shutting down the system.")
        os.system("shutdown /s /t 1")  # Windows shutdown
    elif intent == "time":
        time_str = get_time()
        speak(time_str)
    elif intent == "weather":
        weather = get_weather()
        speak(weather)
    elif intent == "wikipedia":
        query = command.replace("wikipedia", "").replace("wiki", "").strip()
        info = search_wikipedia(query)
        speak(info)
    elif intent == "exit":
        speak("Goodbye!")
        return False
    else:
        # Use AI for general queries
        response = ai_response(command)
        speak(response)
    return True

def main():
    speak("Voice assistant initialized. Say 'Hey Hanry' to wake me up.")
    while True:
        command = listen()
        if wake_word_detected(command):
            if authenticate_user():
                while True:
                    command = listen()
                    if not execute_command(command):
                        break

if __name__ == "__main__":
    main()