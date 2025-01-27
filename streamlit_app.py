import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
from datasets import load_dataset
from gtts import gTTS
import os
import re
import random

# Enable Dark Mode and Custom CSS
st.markdown(
    """
    <style>
        body {
            background-color: #121212;
            color: white;
        }
        .css-1d391kg {
            background-color: #333;
        }
        .stButton > button {
            background-color: #6200ee;
            color: white;
        }
        .stTextInput input {
            background-color: #333;
            color: white;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Load models and datasets
try:
    code_llama_model = AutoModelForCausalLM.from_pretrained("meta-llama/CodeLlama-7B-Python")
    code_llama_tokenizer = AutoTokenizer.from_pretrained("meta-llama/CodeLlama-7B-Python")
except Exception as e:
    st.error(f"Error loading model: {e}")
    code_llama_model = None
    code_llama_tokenizer = None

try:
    wordlist_dataset = load_dataset("Canstralian/Wordlists")
except Exception as e:
    st.error(f"Error loading Wordlist dataset: {e}")
    wordlist_dataset = None

# Initialize chat history storage
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you?"}]

# Function to validate the prompt using regular expressions
def validate_prompt(prompt: str) -> bool:
    """
    Validates if the input prompt is not empty and meets some basic format rules.
    Args:
        prompt (str): The input prompt to be validated.
    Returns:
        bool: True if the prompt is valid, False otherwise.
    """
    # Improved validation: Allow alphanumeric characters, spaces, and punctuation
    if re.match(r'^[A-Za-z0-9\s\.,;!?(){}[\]]+$', prompt):
        return True
    return False

# Function to convert text to speech
def text_to_speech(text: str) -> None:
    """
    Converts text to speech using gTTS and saves it as an MP3 file.
    Args:
        text (str): The text to be converted to speech.
    """
    try:
        tts = gTTS(text, lang='en')
        tts.save("response.mp3")
        os.system("mpg321 response.mp3")
    except Exception as e:
        st.error(f"Error generating speech: {e}")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Function to generate chatbot response
def generate_response(prompt: str) -> str:
    """
    Generates a response from the assistant based on the user input.
    Args:
        prompt (str): The user's input prompt.
    Returns:
        str: The generated response from the assistant.
    """
    if code_llama_model and code_llama_tokenizer:
        if "python" in prompt.lower():
            # Use the Code Llama model for code-related queries
            inputs = code_llama_tokenizer(prompt, return_tensors="pt")
            outputs = code_llama_model.generate(**inputs, max_length=150, num_return_sequences=1)
            response = code_llama_tokenizer.decode(outputs[0], skip_special_tokens=True)
        else:
            response = "I'm here to assist with your queries."
    else:
        response = "Model not loaded. Please try again later."

    if "osint" in prompt.lower():
        # Respond with dataset-based OSINT information
        response = "OSINT data analysis coming soon!"
    elif "wordlist" in prompt.lower() and wordlist_dataset:
        # Fetch and display a random entry from the Wordlist dataset
        wordlist_entry = random.choice(wordlist_dataset["train"])["text"]
        response = f"Here's a random wordlist entry: {wordlist_entry}"

    return response

# User input handling
if prompt := st.chat_input():
    # Validate user input
    if validate_prompt(prompt):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        # Generate and display response with smooth animations
        with st.chat_message("assistant"):
            with st.spinner("Assistant is typing..."):
                response = generate_response(prompt)
                st.write(response)
        
        # Text-to-Speech integration for the assistant's response
        text_to_speech(response)

        # Store the assistant's response
        st.session_state.messages.append({"role": "assistant", "content": response})
    else:
        st.warning("Invalid input. Please ensure your input contains only valid characters.")

# User Feedback Section
feedback = st.selectbox("How was your experience?", ["😊 Excellent", "😐 Okay", "😕 Poor"])
if feedback:
    st.success(f"Thank you for your feedback: {feedback}", icon="✅")