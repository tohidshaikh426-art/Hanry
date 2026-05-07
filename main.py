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
import vosk
import pyaudio
import time

# Load spaCy model for NLP
nlp = spacy.load("en_core_web_sm")

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech
voices = engine.getProperty('voices')
for voice in voices:
    if 'english' in voice.name.lower() or 'male' in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

# OpenAI API key (set your key here or use environment variable)
openai.api_key = os.getenv('OPENAI_API_KEY')

# Wikipedia API
wiki_wiki = wikipediaapi.Wikipedia(user_agent='HanryVoiceAssistant/1.0 (https://github.com/tohidshaikh426-art/Hanry)', language='en')

# Vosk model for offline recognition
vosk_model = vosk.Model("models/vosk-model-small-en-us-0.15")

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
chat_history = []
MAX_HISTORY = 8

def speak(text):
    print(f"Hanry: {text}")
    engine.say(text)
    engine.runAndWait()

def test_microphone():
    """Test microphone functionality"""
    speak("Testing microphone. Please say something.")
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio).lower()
            speak(f"I heard: {command}")
            return True
        except Exception as e:
            speak(f"Microphone test failed: {str(e)}")
            return False


def recognize_offline(audio):
    try:
        raw_data = audio.get_raw_data(convert_rate=16000, convert_width=2)
        recognizer = vosk.KaldiRecognizer(vosk_model, 16000)
        if recognizer.AcceptWaveform(raw_data):
            result = json.loads(recognizer.Result())
            return result.get("text", "").lower()
        return json.loads(recognizer.FinalResult()).get("text", "").lower()
    except Exception as e:
        print(f"Offline recognition error: {e}")
        return ""


def listen():
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.8

    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=6, phrase_time_limit=6)
        except sr.WaitTimeoutError:
            print("Listening timeout during capture.")
            return ""

    # Try offline recognition first
    text = recognize_offline(audio)
    if text:
        print(f"Offline recognized: {text}")
        return text

    print("Offline recognition returned nothing, trying online...")
    try:
        text = recognizer.recognize_google(audio).lower()
        print(f"Online recognized: {text}")
        return text
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Please speak clearly.")
        return ""
    except sr.RequestError:
        speak("Sorry, speech service is down.")
        return ""
    except Exception as e:
        print(f"Online recognition error: {e}")
        return ""


def classify_intent(command):
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
    elif "test" in command and ("microphone" in command or "mic" in command):
        return "test_microphone"
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
        system_prompt = (
            "You are Hanry, a highly intelligent AI assistant inspired by JARVIS. "
            "Speak with calm confidence, natural language, and a respectful tone. "
            "Address the user as 'Sir' and keep answers concise yet conversational. "
            "Use human-like phrasing, maintain polite formality, and make your responses feel smooth and friendly."
        )
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(chat_history[-MAX_HISTORY:])
        messages.append({"role": "user", "content": command})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=200,
            temperature=0.8,
            top_p=0.9
        )
        assistant_text = response.choices[0].message.content.strip()
        chat_history.append({"role": "user", "content": command})
        chat_history.append({"role": "assistant", "content": assistant_text})
        return assistant_text
    except Exception as e:
        print(f"AI response error: {e}")
        return "I apologize, Sir. I couldn't process that request right now."

def execute_command(command):
    intent = classify_intent(command)
    if intent == "open_app":
        app = command.replace("open", "").strip()
        try:
            if os.path.exists(app):
                os.startfile(app)
            else:
                subprocess.run(["cmd", "/c", "start", "", app], shell=True)
            speak(f"Opening {app} for you, Sir.")
        except Exception as e:
            print(f"Open app failed: {e}")
            speak("I couldn't open that application. Please check the name and try again.")
    elif intent == "search_web":
        query = command.replace("search", "").replace("google", "").strip()
        url = f"https://www.google.com/search?q={query}"
        pyautogui.hotkey('ctrl', 't')  # Open new tab
        pyautogui.typewrite(url)
        pyautogui.press('enter')
        speak(f"Right away, Sir. Searching for {query}.")
    elif intent == "shutdown":
        speak("I will shut down the system now. Please save your work, Sir.")
        os.system("shutdown /s /t 1")  # Windows shutdown
    elif intent == "time":
        time_str = get_time()
        speak(f"Certainly, Sir. {time_str}")
    elif intent == "weather":
        weather = get_weather()
        speak(f"Here is the current weather, Sir: {weather}")
    elif intent == "wikipedia":
        query = command.replace("wikipedia", "").replace("wiki", "").strip()
        info = search_wikipedia(query)
        speak(f"I found this information, Sir: {info}")
    elif intent == "test_microphone" or "test mic" in command:
        speak("Testing the microphone now, Sir.")
        test_microphone()
    elif intent == "exit":
        speak("Very well, Sir. I am signing off.")
        return False
    else:
        # Use AI for general queries
        response = ai_response(command)
        speak(response)
    return True


def wake_word_detected(command):
    return "hello" in command.lower()


def authenticate_user():
    # Basic authentication: for now, just check wake word
    # For advanced: implement voiceprint recognition (requires additional setup)
    speak("Yes, Sir. Hanry at your service. How may I assist you today?")
    return True


def main():
    speak("Voice assistant initialized. Say 'hello' to wake me up.")
    try:
        while True:
            command = listen()
            if wake_word_detected(command):
                if authenticate_user():
                    while True:
                        command = listen()
                        if not execute_command(command):
                            break
    except KeyboardInterrupt:
        speak("Shutting down gracefully. Goodbye.")

if __name__ == "__main__":
    main()