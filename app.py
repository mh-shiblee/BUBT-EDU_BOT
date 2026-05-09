import streamlit as st
from chatbot.rag_chain import get_answer

# ─── Page config ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="BUBT Assistant",
    page_icon="🎓",
    layout="centered"
)

# ─── Header ───────────────────────────────────────────────────────────────────

st.title("🎓 BUBT Assistant")
st.caption("Ask me anything about Bangladesh University of Business and Technology")
with st.sidebar:
    st.image("https://bubt.edu.bd/storage/uploads/settings/vmqcNBkXRocUDX69tF9BGRzUbI7sFotaCympOxC3.png", width=200)
    st.markdown("### 📞 Contact BUBT")
    st.markdown("**Hotline:** 01810033733")
    st.markdown("**Website:** [bubt.edu.bd](https://bubt.edu.bd)")
    st.markdown("---")
    st.markdown("### 💡 Sample Questions")
    st.markdown("""
    - What is the tuition fee for CSE?
    - What documents are needed for admission?
    - What scholarships are available?
    - Tell me about the Debating Club
    - What is the grading system?
    - Where can I find the class routine?
    """)
    st.markdown("---")
    st.caption("Created by MH Shiblee with BUBT Data + Groq LLM")


st.markdown("""
    <style>
        .stChatMessage p {
            font-size: 1.05rem !important;
            line-height: 1.6 !important;
        }
        .stChatMessage li {
            font-size: 1.05rem !important;
            line-height: 1.6 !important;
        }
    </style>
""", unsafe_allow_html=True)


# ─── Initialize chat history in session state ─────────────────────────────────

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! I'm the BUBT Assistant. I can help you with information about admissions, programs, tuition fees, scholarships, clubs and more. How can I help you today?"
        },
        {
            "role": "assistant",
            "content": "💡 **Tip:** Please keep your questions as detailed and specific as possible. For example, instead of *'fees?'* try *'What is the total tuition fee for the CSE undergraduate program?'* — this helps me give you the most accurate answer!"
        }
    ]

# ─── Display chat history ─────────────────────────────────────────────────────

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ─── Handle user input ────────────────────────────────────────────────────────

if prompt := st.chat_input("Ask me about BUBT..."):

    # Show user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Save user message to session
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # Get answer from RAG chain
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = get_answer(prompt)
        st.markdown(answer)

    # Save assistant answer to session
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
