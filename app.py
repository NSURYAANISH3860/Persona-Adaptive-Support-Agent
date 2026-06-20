import streamlit as st
from src.classifier import classify_customer_persona
from src.rag_pipeline import LocalRAGPipeline
from src.generator import generate_adaptive_response
from google.genai import errors

st.set_page_config(page_title="Persona-Adaptive Support", layout="wide")
st.title("🤖 Intelligent Customer Support Agent")

@st.cache_resource
def init_system():
    pipeline = LocalRAGPipeline()
    pipeline.load_and_ingest_all()
    return pipeline

pipeline = init_system()

# Chat UI
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("How can we help you today?")

if user_input:
    # Display user msg
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.spinner("Analyzing request..."):
        try:
            # 1. Classify
            classification = classify_customer_persona(user_input)
            persona = classification.get("persona", "Frustrated User")
            
            # 2. Retrieve
            context = pipeline.retrieve_context(user_input)
            
            # 3. Generate
            result = generate_adaptive_response(user_input, persona, context)

            # Display Response
            with st.chat_message("assistant"):
                st.markdown(f"**Detected Persona:** `{persona}`")
                st.markdown(result["response"])
                
                # Clean UI for escalations (No JSON!)
                if result["escalated"]:
                    st.warning("⚠️ This issue requires human intervention.")
                    if st.button("📞 Connect to Human Agent"):
                        st.success("Connecting you to the next available support specialist... Please hold.")

            # Save assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": result["response"]})

        # Graceful handling for Google 503 Server Errors
        except errors.APIError as e:
            st.error("⚠️ The AI server is currently experiencing high traffic. Please wait a few seconds and try again.")
        except Exception as e:
            st.error(f"⚠️ An unexpected error occurred: {e}")