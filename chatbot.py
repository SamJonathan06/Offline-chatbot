import streamlit as st
import requests
import pyttsx3
import os
import uuid

# --- Configuration ---
MODEL_NAME = "tinyllama" 
OLLAMA_URL = "http://localhost:11434/api/chat"

# Set page config for layout
st.set_page_config(page_title="Offline ChatBot", page_icon="🤖", layout="wide")

# --- Custom CSS for Aesthetics ---
st.markdown("""
<style>
    /* Import modern font from Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

    /* Apply font globally */
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif !important;
        color: #ffffff !important;
    }

    /* Sleek Dark Themed Background */
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at 50% -20%, #2a2a35 0%, #0b0b0f 100%);
        background-attachment: fixed;
    }
    
    /* Make header transparent */
    [data-testid="stHeader"] {
        background-color: transparent !important;
    }
    
    /* The main content area */
    .block-container {
        background-color: transparent;
        padding: 2rem !important;
        margin-top: 2rem;
        color: #ffffff !important;
    }

    /* Title Styling */
    h1 {
        font-family: 'Poppins', sans-serif !important;
        color: #ffffff !important;
        text-align: center;
        font-weight: 600;
        margin-bottom: 0px;
        letter-spacing: 1px;
    }

    /* Style the chat input box */
    [data-testid="stChatInput"] {
        border: 1px solid #444455 !important;
        border-radius: 20px !important;
        background-color: rgba(20, 20, 25, 0.8) !important;
        color: #ffffff !important;
    }
    
    /* Fix input text color */
    [data-testid="stChatInputTextArea"] {
        color: #ffffff !important;
    }

    /* Transparent Sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(11, 11, 15, 0.95) !important;
        color: #ffffff !important;
    }

    /* Subtitle styling */
    .subtitle {
        text-align: center;
        color: #dddddd !important;
        font-weight: 300;
        margin-bottom: 30px;
        font-size: 1.1rem;
    }
    
    /* Ensure chat messages text is white */
    .stChatMessage p {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("Offline ChatBot")
st.markdown(f"<div class='subtitle'>Running completely offline using <b>{MODEL_NAME}</b> via Ollama.</div>", unsafe_allow_html=True)

# --- Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Functions ---
def get_ollama_response(messages):
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "stream": False
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        return response.json()["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"Error: Make sure Ollama is installed and running `ollama run {MODEL_NAME}`. Details: {e}"

def create_audio_file(text):
    """Converts text to an offline audio file using Windows built-in voices"""
    engine = pyttsx3.init()
    
    # Clean up the text so the bot doesn't read out loud markdown symbols like asterisk
    clean_text = text.replace("*", "").replace("#", "").replace("_", "")
    
    # Use a unique filename to prevent Streamlit caching issues
    audio_path = f"response_{uuid.uuid4().hex}.wav"
    
    # Save the spoken words to a file
    engine.save_to_file(clean_text, audio_path)
    engine.runAndWait()
    
    return audio_path

# --- UI: Display Chat History ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        
# --- UI: Chat Input ---
# Get text input or voice input
prompt = st.chat_input("What is on your mind?")
audio_value = st.audio_input("Or speak your mind (Voice Input)")

user_message = prompt

# If user recorded audio, convert it to text
if audio_value is not None:
    with st.spinner("Transcribing audio..."):
        try:
            import speech_recognition as sr
            import tempfile
            
            # Save the Streamlit audio bytes to a temporary WAV file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                tmp_file.write(audio_value.getvalue())
                tmp_path = tmp_file.name
                
            r = sr.Recognizer()
            with sr.AudioFile(tmp_path) as source:
                audio_data = r.record(source)
                # Using recognize_google for out-of-the-box compatibility without complex C++ installations.
                # For a strictly offline setup, you can replace this line with a local Whisper model call.
                user_message = r.recognize_google(audio_data)
                
            os.remove(tmp_path)
        except sr.UnknownValueError:
            st.warning("Could not understand the audio.")
            user_message = None
        except Exception as e:
            st.error(f"Speech recognition error: {e}")
            user_message = None

if user_message:
    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_message})
    with st.chat_message("user"):
        st.markdown(user_message)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking (locally)..."):
            # Get text response from AI
            response_text = get_ollama_response(st.session_state.messages)
            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})
            
        audio_file = None
        with st.spinner("Generating voice..."):
            # Convert text response to audio
            try:
                audio_file = create_audio_file(response_text)
            except Exception as e:
                st.error(f"Could not generate voice: {e}")
        
        # Play audio outside the spinner block so it definitely renders!
        if audio_file and os.path.exists(audio_file):
            try:
                # Read as bytes to avoid file locking and Streamlit caching issues
                with open(audio_file, "rb") as f:
                    audio_bytes = f.read()
                st.audio(audio_bytes, format='audio/wav')
                
                # Clean up the file after reading so they don't pile up
                try:
                    os.remove(audio_file)
                except:
                    pass 
            except Exception as e:
                st.error(f"Error reading audio file: {e}")