import streamlit as st
import requests

st.title("Chatbot Basic")

chat_url = "http://127.0.0.1:8000/chat/"

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input from user
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        payload = {
            "messages": [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]
        }
        headers = {
            "Content-Type": "application/json"
        }

        # Make the request to the FastAPI backend
        response = requests.post(chat_url, json=payload, headers=headers)
        
        # Check for errors in the response
        if response.status_code == 403:
            st.error("Quota exceeded. Please check your plan and billing details.")
        elif response.status_code != 200:
            st.error(f"Error: {response.json().get('detail', 'Unknown error occurred.')}")
        else:
            assistant_message = response.json().get("reply", "No reply found")
            st.markdown(assistant_message)
            st.session_state.messages.append({"role": "assistant", "content": assistant_message})