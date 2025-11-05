import streamlit as st
import os
from google import genai
from google.genai import types

# --- 1. GEMINI CLIENT AND GENERATION FUNCTION ---
# Note: Ensure GEMINI_API_KEY is set in your environment
try:
    # Attempt to initialize the client
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
except Exception:
    # Handle the case where the key might not be available
    client = None

def generate_gemini_response(prompt, temperature=0.3):
    """Generate a response from Gemini API."""
    if not client:
        return "API Client not initialized. Please ensure GEMINI_API_KEY is set."
    try:
        contents = [types.Content(role="user", parts=[types.Part.from_text(text=prompt)])]
        config_params = types.GenerateContentConfig(temperature=temperature)
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=contents, config=config_params
        )
        return response.text
    except Exception as e:
        return f"Error during API call: {str(e)}"

def generate_response_with_role(prompt, model_role):
    """Generates the AI response based on the prompt and selected role."""
    full_prompt = f"Role: You are a {model_role}. {prompt}"
    return generate_gemini_response(full_prompt)


# --- 2. INPUT HANDLING LOGIC ---

def handle_input():
    """Handles the user input and updates the chat history."""
    # Check for non-empty input to avoid adding blank entries
    if st.session_state.user_input.strip():
        user_prompt = st.session_state.user_input
        model_role = st.session_state.model_role
        
        # 1. Get AI Response
        with st.spinner(f"AI ({model_role}) is thinking..."):
             ai_response = generate_response_with_role(user_prompt, model_role)

        # 2. Update History
        st.session_state.history.insert(0, { # Insert at the front for reverse display
            "question": user_prompt,
            "answer": ai_response,
            "role": model_role
        })
        
        # 3. Clear Input
        st.session_state.user_input = ""


# --- 3. UI SETUP AND HISTORY DISPLAY ---

def display_history():
    """Displays the conversation history using native Streamlit components."""
    # Use an expander to collapse the history for tidiness
    with st.expander("Conversation History", expanded=True):
        # Iterate over history (reversed order is common for chat apps)
        for idx, qa in enumerate(st.session_state.history):
            q = qa["question"]
            a = qa["answer"]
            role = qa["role"]
            
            # Display Question (Q)
            st.info(f"**Q{len(st.session_state.history) - idx} ({role}):** {q}")
            
            # Display Answer (A)
            st.success(f"**A{len(st.session_state.history) - idx}:** {a}")
            st.divider() # Separator

def setup_ui():
    """Sets up the Streamlit application UI."""
    st.set_page_config(page_title="Role-Based Chatbot", layout="wide")
    st.title("🤖 Role-Based Chatbot")

    # Initialize session state
    if "history" not in st.session_state:
        st.session_state.history = []
    if "model_role" not in st.session_state:
        st.session_state.model_role = "General Assistant"

    # Sidebar for Model Role Selection
    st.sidebar.title("Configuration")
    st.session_state.model_role = st.sidebar.selectbox(
        "Select AI Role:",
        ["Teacher", "Expert Scientist", "Business Leader", "Peer Student", "General Assistant"],
        key="role_selector"
    )
    st.sidebar.caption("The AI's response style changes based on the selected role.")

    # Chat Input
    st.text_input(
        f"Ask a question to the {st.session_state.model_role}...",
        key="user_input",
        on_change=handle_input
    )

    # Display History
    display_history()

# --- MAIN EXECUTION BLOCK ---

if __name__ == "__main__":
    setup_ui()