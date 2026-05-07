---
description: "Full project overview for the Hanry voice assistant. Use when working on any file in this repo so the agent understands architecture, components, and behavior without repeated explanation."
applyTo: ["**/*"]
---

# Hanry Voice Assistant Overview

This repository contains a Python voice assistant project named **Hanry**.
The assistant is designed to run on Windows, listen for voice commands, and execute tasks using both offline and online speech recognition.

## Project Files
- `main.py` - core assistant implementation
- `README.md` - usage, setup, and features
- `requirements.txt` - dependency list
- `agent-overview.instructions.md` - project summary for the agent
- `copilot-instructions.md` - additional agent context
- `models/vosk-model-small-en-us-0.15/` - offline Vosk speech model

## Core Functionality

### Voice Input and Recognition
- Primary wake word: **"hello"**
- Uses `speech_recognition` for microphone access
- Offline recognition: `vosk` with Vosk English model
- Online fallback: Google Speech Recognition via `recognize_google`
- Microphone is tested with ambient noise adjustment and capture timeout

### Command Flow
1. `listen()` captures audio
2. `wake_word_detected(command)` checks for "hello"
3. `authenticate_user()` acknowledges the user
4. `listen()` captures the next command
5. `classify_intent(command)` determines intent
6. `execute_command(command)` performs the action

### Supported Intents
- `open_app` - opens applications or files
- `search_web` - opens a browser search
- `shutdown` - shuts down Windows
- `time` - reports the current time
- `weather` - returns weather via `wttr.in`
- `wikipedia` - searches Wikipedia via `wikipediaapi`
- `test_microphone` - runs a microphone check
- `exit` - stops the assistant
- `general` - uses OpenAI GPT for conversational replies

### AI and Personality
- Uses `openai` GPT-3.5 via `ChatCompletion`
- System prompt is configured for a Jarvis-like assistant
- Responses are designed to be polite, confident, and natural
- Conversation history is preserved for follow-up context

### Text-to-Speech
- Uses `pyttsx3`
- Sets a voice if an English or male voice is available
- Speaks responses aloud and prints them to console

## Important Setup Notes
- The OpenAI API key must be provided via environment variable: `OPENAI_API_KEY`
- No API keys should be hard-coded in source files
- The Vosk model must be present at `models/vosk-model-small-en-us-0.15`
- The assistant is Windows-specific for application launching and shutdown commands

## Development and Enhancement Notes
- The wake word is intentionally simple: `hello`
- The system prefers offline recognition first to reduce latency and dependency on network
- If offline recognition fails, it falls back to online Google speech recognition
- `execute_command()` should be extended safely and with care for system access
- Use this file to understand the system without asking the user for repeated explanations

## Agent Guidance
- Always use this project overview as the primary context for code changes
- Do not prompt the user to re-explain the application behavior
- Assume the current codebase is the authoritative implementation of Hanry
- Prefer improvements that make voice recognition and natural conversation more reliable and intuitive
