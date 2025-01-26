import streamlit as st
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
from hugchat import hugchat
import os

# Streamlit page config
st.set_page_config(page_title="HugChat - An LLM-powered Streamlit app")

# Sidebar contents
with st.sidebar:
    st.title('🤗💬 HugChat App')
    st.markdown('''
    ## About
    This app is an LLM-powered chatbot built using:
    - [Streamlit](https://streamlit.io/)
    - [HugChat](https://github.com/Soulter/hugging-chat-api)
    - [OpenAssistant/oasst-sft-6-llama-30b-xor](https://huggingface.co/OpenAssistant/oasst-sft-6-llama-30b-xor) LLM model
    
    💡 Note: No API key required!
    ''')
    add_vertical_space(5)
    st.write('Made with ❤️ by [Data Professor](https://youtube.com/dataprofessor)')

# Initialize chatbot and session state
if 'chatbot' not in st.session_state:
    # Create ChatBot instance
    st.session_state.chatbot = hugchat.ChatBot()

if 'generated' not in st.session_state:
    st.session_state['generated'] = ["I'm HugChat, How may I help you?"]

if 'past' not in st.session_state:
    st.session_state['past'] = ['Hi!']

# Layout of input/response containers
input_container = st.container()
colored_header(label='', description='', color_name='blue-30')
response_container = st.container()

# User input
def get_text():
    return st.text_input("You: ", "", key="input")

with input_container:
    user_input = get_text()

# AI Response Generation
def generate_response(prompt):
    try:
        response = st.session_state.chatbot.chat(prompt)
        return response
    except Exception as e:
        return f"An error occurred: {e}"

# Display conversation
with response_container:
    if user_input:
        response = generate_response(user_input)
        st.session_state.past.append(user_input)
        st.session_state.generated.append(response)

    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state['past'][i], is_user=True, key=f"{i}_user")
            message(st.session_state["generated"][i], key=f"{i}")