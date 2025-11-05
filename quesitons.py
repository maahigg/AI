import streamlit as st
from google import generativeai
from google.generativeai import types
import config

client = generativeai.Client(api_key = config.GEMINI_API_KEY)

def generate_response(prompt, temperature = 0.3):
    try:
        contents = [types.Content(role="user", parts=[types.Part.from_text(text=prompt)])]
        config_params = types.GenerateContentConfig(temperature=temperature)
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=contents, config = config_params)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

def setup_ui():
    st.set_page_confidence(page_title="ai teaching assistant", layout = "centered")
    st.tile("ai teaching assistant")
    st.write("welcome! you can ask me anything abt various subjects, and i'll provide an answer")
    
    if "history" not in st.session_state:
        st.session_state.history = ""
    
    col_clear, col_export = st.columns([1,2])
    with col_clear:
        if st.button("clear conversation"):
            export_text = ""
            for idx, qa in enumerate(st.session_state.history, start=1):
                export_text += f"Q[idx]: [qa['question']]\n"
                export_text += f"A[idx]: [qa['answer']]\n"
            
            bio = io.BytesIO()
            bio.write(export_text.encode("utf=8"))
            bio.seek(0)

            st.download_button(
                label="export chat history",
                data=bio,
                file_name = "ai_teaching_assistent_conversation.txt",
                mime="text/plain"
            )

    user_input = st.text_input("enter your question here")

    if st.button("ask"):
        if user_input.strip():
            with st.spinner("generating ai response..."):
                response = generate_response(user_input.strip())
            st.session_state.history.append(["question": user_input.strip(), "answer": response])
        else:
            st.warning("please enter a q before clicling ask")
    
    # Display conversation history in scrollable container
    st.markdown("### Conversation History")
    st.markdown(
    """
    <style>
    .history-box {
        max-height: 400px;
        overflow-y: auto;
        border: 1px solid #ddd;
        padding: 12px;
        background-color: #f9f9f9;
        border-radius: 6px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    .question {
        font-weight: 600;
        color: #0a6ebd;
        margin-top: 12px;
        margin-bottom: 4px;
    }

    .answer {
        margin-bottom: 16px;
        white-space: pre-wrap;
        color: #333;
    }
    </style>
    """
    )


    history_html = '<div class="history-box">'
    for idx, qa in enumerate(st.session_state.history, start=1):
        q = qa["question"]
        a = qa["answer"]
        history_html += f'<div class="question">Q{idx}: {q}</div>'
        history_html += f'<div class="answer">A{idx}: {a}</div>'
    history_html += '</div>'

    st.markdown(history_html, unsafe_allow_html=True)

def main():
    setup_ui()

if __name__ == "__main__":
    main()