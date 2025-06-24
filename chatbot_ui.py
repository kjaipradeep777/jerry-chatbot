import streamlit as st
from chatbot_backend import get_intent, get_response

st.set_page_config(page_title="Jerry the Chatbot", page_icon="🤖", layout="centered")

st.title("🧠 Jerry the Chatbot")
st.markdown("#### Hi there! I'm Jerry 🤖 – your friendly assistant. Ask me anything!")

user_input = st.text_input("💬 You:", placeholder="Type your message here...")

if user_input:
    intent = get_intent(user_input)
    response = get_response(intent)
    st.markdown(f"**🧠 Jerry:** {response}")
