import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import io
import re
import config

try:
    client = genai.Client(api_key=config.GEMINI_API_KEY)
except Exception as e:
    st.error(f"❌ Could not initialize Gemini client: {e}")

def generate_response(prompt: str, temperature: float = 0.3):
    try:
        contents = [types.Content(role="user", parts=[types.Part.from_text(text=prompt)])]
        cfg = types.GenerateContentConfig(temperature=temperature)
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=contents, config=cfg
        )
        return response.text
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

def run_ai_teaching_assistant():
    st.title("🎓 AI Teaching Assistant")
    st.write("Ask me anything about your subjects and I’ll give a clear, helpful answer!")

    if "history_ata" not in st.session_state:
        st.session_state.history_ata = []

    col_clear, col_export = st.columns([1, 2])

    with col_clear:
        if st.button("🧹 Clear Conversation", key="clear_ata"):
            st.session_state.history_ata = []
            st.success("Conversation cleared!")

    with col_export:
        if st.session_state.history_ata:
            export_text = ""
            for idx, qa in enumerate(st.session_state.history_ata, start=1):
                export_text += f"Q{idx}: {qa['question']}\n"
                export_text += f"A{idx}: {qa['answer']}\n\n"
            bio = io.BytesIO(export_text.encode("utf-8"))
            bio.seek(0)
            st.download_button(
                label="💾 Export Chat History",
                data=bio,
                file_name="AI_Teaching_Assistant_Conversation.txt",
                mime="text/plain",
            )

    user_input = st.text_input("💬 Enter your question here:", key="input_ata")

    if st.button("Ask", key="ask_ata"):
        if user_input.strip():
            with st.spinner("🤖 Thinking..."):
                answer = generate_response(user_input.strip(), temperature=0.3)
            st.session_state.history_ata.append(
                {"question": user_input.strip(), "answer": answer}
            )
            st.experimental_rerun()
        else:
            st.warning("Please enter a question before clicking *Ask*.")

    if st.session_state.history_ata:
        st.markdown("### 🗂 Conversation History")
        for idx, qa in enumerate(st.session_state.history_ata, start=1):
            st.markdown(f"**Q{idx}:** {qa['question']}")
            st.markdown(f"**A{idx}:** {qa['answer']}")

