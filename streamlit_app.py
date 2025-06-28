import streamlit as st
from main import get_frontend_answer
import time

st.set_page_config(page_title="Frontend Expert Chat", page_icon="💬")

st.title("💬 Frontend Expert AI")
st.caption("Ask anything about HTML, CSS, JavaScript, React, etc.")

# Initialize chat history if it doesn't exist yet
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if user_query := st.chat_input("Ask your frontend question..."):
    # Store user message
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    # Agent response
    with st.chat_message("assistant"):
        with st.spinner("Typing..."):
            response = get_frontend_answer(user_query)
            placeholder = st.empty()
            typed_text = ""
            for char in response:
                typed_text += char
                placeholder.markdown(typed_text)
                time.sleep(0.010)  # Adjust for typing speed

    # Store assistant message
    st.session_state.messages.append({"role": "assistant", "content": response})
