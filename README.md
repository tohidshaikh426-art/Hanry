# Voice Assistant

A Python-based AI voice assistant named Hanry, designed to run on your laptop with full system access. It responds only to your wake word "Hey Hanry" and can execute various commands.

## Features
- Speech recognition and text-to-speech
- Wake word detection ("Hey Hanry" or "Hanry")
- Advanced natural language processing with spaCy
- AI-powered conversational responses using OpenAI GPT
- System commands (open apps, search web, shutdown)
- Time and weather information
- Wikipedia search
- User memory persistence
- User authentication via wake word (expandable to voice recognition)

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Download spaCy model: `python -m spacy download en_core_web_sm`
3. Set OpenAI API key: Set environment variable `OPENAI_API_KEY` or edit `main.py`
4. Run the assistant: `python main.py`

## New Advanced Features
- **Conversational AI**: Uses OpenAI GPT-3.5 for general queries and responses
- **Intent Classification**: Automatically detects command types using NLP
- **Time Queries**: Ask "what time is it?"
- **Weather Information**: Ask "what's the weather?"
- **Wikipedia Search**: Ask "wikipedia [topic]"
- **Memory System**: Remembers user preferences (expandable)

## Security Warning
This assistant has full system access. Use at your own risk. Ensure it's only activated by authorized users. For better security, implement voiceprint authentication.

## Extending to Mobile
For mobile phones:
- Use frameworks like Flutter or React Native for cross-platform apps.
- Integrate with mobile APIs for system control.
- For voice recognition, use platform-specific libraries (e.g., Android SpeechRecognizer).
- Consider a server-client architecture where the laptop runs the main AI and mobile connects via API.

## Customization
- Add more commands in `execute_command` function.
- Improve authentication with libraries like `pyaudio` for voice analysis.
- Expand memory system for user preferences.
- Add more APIs for additional services.