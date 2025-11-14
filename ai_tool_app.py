import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import io, re, config

client = genai.Client(api_key=config.GEMINI_API_KEY)

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

def generate_image(prompt: str):
    try:
        contents = [types.Content(role="user", parts=[types.Part.from_text(text=prompt)])]
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=contents
        )
        if hasattr(response, "image") and response.image:
            img = Image.open(BytesIO(response.image))
            return img
        else:
            return None
    except Exception as e:
        st.error(f"⚠️ Image Generation Error: {str(e)}")
        return None

def is_prompt_safe(prompt: str) -> bool:
    forbidden = ["violence", "weapon", "blood", "gun", "hate", "nude", "kill"]
    pattern = re.compile("|".join(forbidden), re.IGNORECASE)
    return not bool(pattern.search(prompt))

def run_ai_teaching_assistant():
    st.title("🎓 AI Teaching Assistant")
    st.write("Ask me anything about your subjects and I’ll explain clearly.")
    if "history_ata" not in st.session_state:
        st.session_state.history_ata = []
    user_input = st.text_input("💬 Enter your question here:")
    if st.button("Ask", key="ask_ata"):
        if user_input.strip():
            with st.spinner("🤖 Thinking..."):
                ans = generate_response(user_input.strip())
            st.session_state.history_ata.append(
                {"question": user_input.strip(), "answer": ans}
            )
            st.experimental_rerun()
        else:
            st.warning("⚠️ Please enter a question first.")
    if st.session_state.history_ata:
        st.markdown("### 🗂 Conversation History")
        for idx, qa in enumerate(st.session_state.history_ata, 1):
            st.markdown(f"**Q{idx}:** {qa['question']}")
            st.markdown(f"**A{idx}:** {qa['answer']}")

def run_math_mastermind():
    st.title("🔢 Math Mastermind")
    st.write("Enter any math problem and I’ll solve it step by step.")
    if "history_math" not in st.session_state:
        st.session_state.history_math = []
    with st.form("math_form"):
        math_input = st.text_area("🧮 Enter your math question:")
        submitted = st.form_submit_button("Solve Problem")
    if submitted:
        if math_input.strip():
            prompt = f"You are a Math Mastermind. Explain this problem step by step:\n\n{math_input.strip()}"
            with st.spinner("🧠 Solving..."):
                solution = generate_response(prompt, temperature=0.2)
            st.session_state.history_math.append(
                {"problem": math_input.strip(), "solution": solution}
            )
            st.experimental_rerun()
        else:
            st.warning("Please enter a math problem.")
    if st.session_state.history_math:
        st.markdown("### 🧾 Previous Problems")
        for idx, qa in enumerate(st.session_state.history_math, 1):
            st.markdown(f"**Problem {idx}:** {qa['problem']}")
            st.markdown(f"**Solution:** {qa['solution']}")

def run_safe_image_generator():
    st.title("🖼️ Safe AI Image Generator")
    st.write("Generate AI images safely by describing what you’d like to see.")
    if "images" not in st.session_state:
        st.session_state.images = []
    with st.form("image_form"):
        image_prompt = st.text_input("🎨 Describe the image:")
        generate = st.form_submit_button("Generate Image")
    if generate:
        if not image_prompt.strip():
            st.warning("Please enter an image description.")
        elif not is_prompt_safe(image_prompt):
            st.error("⚠️ Unsafe prompt detected. Please revise your description.")
        else:
            with st.spinner("🧩 Generating Image..."):
                img = generate_image(image_prompt.strip())
            if img:
                st.image(img, caption="AI-Generated Image", use_container_width=True)
                st.session_state.images.append(img)
            else:
                st.error("❌ No image generated. Try a simpler prompt.")

def main():
    st.sidebar.title("🧰 AI Toolbox")
    feature = st.sidebar.selectbox(
        "Select a Feature",
        ["AI Teaching Assistant", "Math Mastermind", "Safe AI Image Generator"],
    )
    if feature == "AI Teaching Assistant":
        run_ai_teaching_assistant()
    elif feature == "Math Mastermind":
        run_math_mastermind()
    elif feature == "Safe AI Image Generator":
        run_safe_image_generator()

if __name__ == "__main__":
    main()
