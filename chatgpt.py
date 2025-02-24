import openai
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page title
st.title("Chatbot Basic")

# Create OpenAI client by setting the API key
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Set up session state
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

# Set up chat messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response from OpenAI
    with st.chat_message("assistant"):
        try:
            response = openai.ChatCompletion.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True
            )

            # Handle streaming response
            full_response = ""
            for chunk in response:
                full_response += chunk['choices'][0]['delta'].get('content', '')

            st.markdown(full_response)

            # Display response
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error(f"⚠️ Error: {str(e)}")