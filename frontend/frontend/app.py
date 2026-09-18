"""
Streamlit chat UI for the Academic RAG backend.

Run with:
    streamlit run app.py
after the backend is up (uvicorn app.main:app --reload) and .env points
API_BASE_URL at it.
"""
import streamlit as st

from api_client import API_BASE_URL, APIError, ask_question, check_health

st.set_page_config(page_title="Academic RAG Assistant", page_icon="📚", layout="centered")

if "messages" not in st.session_state:
    st.session_state.messages = []  # list of {role, content, sources?}

# --- Sidebar: connection status ---
with st.sidebar:
    st.header("Backend")
    st.caption(f"API_BASE_URL: `{API_BASE_URL}`")
    if st.button("Check connection", use_container_width=True):
        st.session_state["_health_checked"] = True

    if st.session_state.get("_health_checked"):
        if check_health():
            st.success("Backend is reachable and healthy.")
        else:
            st.error("Backend is not reachable. Is uvicorn running on that URL?")

    st.divider()
    if st.button("Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.title("📚 Academic RAG Assistant")
st.caption("Ask a question grounded in your indexed documents.")

# --- Chat history ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander(f"Sources ({len(msg['sources'])})"):
                for src in msg["sources"]:
                    st.markdown(f"- {src}")

# --- Chat input ---
question = st.chat_input("Ask a question about your documents...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                result = ask_question(question)
                st.markdown(result.answer)
                if result.sources:
                    with st.expander(f"Sources ({len(result.sources)})"):
                        for src in result.sources:
                            st.markdown(f"- {src}")

                st.session_state.messages.append(
                    {"role": "assistant", "content": result.answer, "sources": result.sources}
                )
            except APIError as exc:
                friendly_msg = f"⚠️ {exc}"
                st.error(friendly_msg)
                st.session_state.messages.append({"role": "assistant", "content": friendly_msg})
