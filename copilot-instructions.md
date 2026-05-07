---
description: "Advanced Voice Assistant project: Python-based AI voice assistant named Hanry with speech recognition, NLP, OpenAI integration, and system commands. Use when: working on voice assistant features, AI conversation, NLP intent classification, command execution, or extending Hanry-like functionality."
---

# Voice Assistant Project Overview

This workspace contains an advanced Python-based AI voice assistant project named Hanry. The assistant runs on a laptop with full system access and responds to wake words "Hey Hanry" or "Hanry".

## Project Structure
- `main.py`: Main script with advanced voice assistant logic
- `README.md`: Project documentation and setup instructions
- `requirements.txt`: Python dependencies (including OpenAI, spaCy, Wikipedia)
- `copilot-instructions.md`: This file for agent context
- `assistant_memory.json`: User memory file (created at runtime)

## Key Components
- **Speech Recognition**: Uses `speech_recognition` with Google Speech API
- **Text-to-Speech**: Uses `pyttsx3` for voice output
- **Natural Language Processing**: Uses `spaCy` for intent classification
- **AI Conversation**: Uses `OpenAI GPT-3.5` for general responses
- **Wake Word Detection**: Responds to "hey hanry" or "hanry"
- **Command Execution**: System commands, web search, time/weather/Wikipedia
- **Memory System**: JSON-based user preference storage
- **System Integration**: `pyautogui` for shortcuts, `subprocess` for apps

## Advanced Features
- **Intent Classification**: Automatically categorizes user commands
- **Conversational AI**: Fallback to GPT for non-command queries
- **Time Queries**: Current time reporting
- **Weather Information**: Real-time weather via wttr.in API
- **Wikipedia Search**: Knowledge retrieval from Wikipedia
- **Persistent Memory**: Remembers user interactions (expandable)

## Current Commands/Intents
- Open applications
- Web/Google search
- System shutdown
- Time queries
- Weather queries
- Wikipedia search
- Exit/quit
- General conversation (AI-powered)

## Security Considerations
- Full system access - use with caution
- Wake word authentication only (basic)
- Recommended: Voiceprint recognition for security
- OpenAI API key required for AI features

## Extension Possibilities
- Voiceprint authentication
- Mobile integration (Flutter/React Native)
- Advanced NLP with more intents
- Integration with smart home devices
- Multi-language support
- Voice emotion detection
- Server-client architecture
- Custom skill plugins

## Development Notes
- Windows-specific system commands
- Requires OpenAI API key (set via environment variable)
- spaCy model: en_core_web_sm (auto-downloads)
- Rate limited by Google Speech API and OpenAI
- Memory stored in JSON for simplicity (upgrade to database for production)</content>
<parameter name="filePath">c:\Users\Asus\OneDrive\Desktop\Voice assistant\copilot-instructions.md