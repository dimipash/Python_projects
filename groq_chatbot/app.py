import streamlit as st
from groq import Groq
import pathlib

# Page configuration
st.set_page_config(
    page_title="Groq Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Load CSS
def load_css(css_file):
    with open(css_file) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load the CSS file
css_path = pathlib.Path(__file__).parent / "style.css"
load_css(css_path)

# creates groq client
client = Groq(api_key=st.secrets.get("GROQ_API_KEY"))

# Page Header
st.markdown("""
    <div class="main-header">
        <h1>🤖 Groq Chatbot</h1>
        <p>Powered by Llama 3.3 70B Versatile - Running on Groq's Lightning-Fast Infrastructure</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("Chats")


# Session State
if "default_model" not in st.session_state:
    st.session_state["default_model"] = "llama-3.3-70b-versatile"

if "messages" not in st.session_state:
    st.session_state["messages"] = []

print(st.session_state)


# Display the messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


# Chat input for user message
if prompt := st.chat_input():
    # append message to message collection
    st.session_state.messages.append({"role": "user", "content": prompt})

    # display the new message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display the assistant response from the model
    with st.chat_message("assistant"):
        # place holder for the response text
        response_text = st.empty()

        # Call the Groq API
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=st.session_state.messages,
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )

        full_response = ""

        for chunk in completion:
            chunk_content = chunk.choices[0].delta.content or ""
            full_response += chunk_content
            response_text.markdown(full_response + "▌")
        
        response_text.markdown(full_response)

        # add full response to the messages
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )
