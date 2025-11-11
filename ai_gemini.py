import streamlit as st
from google import genai
from google.genai import types
import config

client = genai.Client(api_key=config.GEMINI_API_KEY)

def generate_response(prompt, temperature=0.3):
    try:
        contents = [types.Content(role="user", parts=[types.Part.from_text(text=prompt)])]
        config_params = types.GenerateContentConfig(temperature=temperature)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=contents,
            config=config_params,
        )
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

def setup_ui():
    st.title("🎓 Enhanced AI Teaching Assistant")
    st.write("Ask questions and get AI responses tailored by role. Your conversation history is saved below!")

    if "conversation" not in st.session_state:
        st.session_state.conversation = []

    role = st.selectbox("Select AI Role", ["Teacher", "Expert", "Friendly Helper"])
    user_input = st.text_input("Enter your question here:")

    if st.button("Ask"):
        if user_input.strip() != "":
            prompt = f"You are a {role}. Please answer the following question:\n{user_input}"
            response = generate_response(prompt)
            st.session_state.conversation.append({"question": user_input, "answer": response})

    if st.button("Clear Conversation"):
        st.session_state.conversation = []

    for i, chat in enumerate(st.session_state.conversation):
        st.markdown(f"**You:** {chat['question']}")
        st.markdown(f"**{role}:** {chat['answer']}")
        st.markdown("---")

def main():
    setup_ui()

if __name__ == "__main__":
    main()
