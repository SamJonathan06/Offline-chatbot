# 🤖 Local Offline Voice Chatbot

A fully functional, 100% offline AI chatbot equipped with voice recognition and Text-to-Speech (TTS) capabilities.

## 🎯 The Problem Solved
Cloud-based AI models often raise privacy concerns and require constant internet connectivity. This project solves that by utilizing local LLMs for inference, ensuring that conversations remain entirely private and accessible without an internet connection. It also addresses accessibility by providing both text and voice interaction modalities.

## 🛠️ Tools & Technologies
*   **UI Framework:** Streamlit (Python)
*   **Local LLM Engine:** Ollama (running the `tinyllama` model)
*   **Voice Output:** `pyttsx3` (Offline Text-to-Speech)
*   **Voice Input:** `SpeechRecognition` library
*   **Language:** Python

## ✨ Key Features & Techniques
*   **100% Offline Processing:** All data processing, including AI inference, happens locally on the machine.
*   **Voice Integration:** 
    *   Converts user speech to text for input.
    *   Generates dynamic audio files for the AI's response using Windows built-in voices.
*   **Custom UI Styling:** Utilizes injected CSS within Streamlit to create a modern, dark-themed UI with custom fonts (Poppins).
*   **Contextual Chat:** Maintains conversation history within the Streamlit session state for continuous dialogue.
*   **Error Handling:** Robust try/except blocks to gracefully handle missing dependencies or audio processing failures.

## 🚀 How to Run Locally
**Prerequisites:** 
You must have [Ollama](https://ollama.com/) installed and the TinyLlama model downloaded (`ollama pull tinyllama`).

1. Clone the repository: `git clone <https://github.com/SamJonathan06/Offline-chatbot.git>`
2. Navigate to the directory: `cd chatbot-project`
3. Install dependencies: `pip install streamlit requests pyttsx3 SpeechRecognition`
4. Run the app: `streamlit run `chatbot.py``
