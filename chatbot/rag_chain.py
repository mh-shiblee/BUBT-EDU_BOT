import os
import pickle
import faiss
import numpy as np
from groq import Groq
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import streamlit as st

# ─── Load environment variables ───────────────────────────────────────────────

load_dotenv()

# ─── Paths ────────────────────────────────────────────────────────────────────

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FAISS_INDEX_PATH = os.path.join(BASE_DIR, "..", "vector_store", "index.faiss")
CHUNKS_PATH = os.path.join(BASE_DIR, "..", "vector_store", "index.pkl")

# ─── Cached resource loaders ──────────────────────────────────────────────────


@st.cache_resource
def load_embedding_model():
    print("Loading embedding model...")
    return SentenceTransformer("all-MiniLM-L6-v2")


@st.cache_resource
def load_faiss_index():
    print("Loading FAISS index...")
    index = faiss.read_index(FAISS_INDEX_PATH)
    with open(CHUNKS_PATH, "rb") as f:
        chunks = pickle.load(f)
    print(f"Loaded {len(chunks)} chunks from FAISS!")
    return index, chunks


@st.cache_resource
def load_groq_client():
    return Groq(api_key=os.getenv("GROQ_API_KEY"))

# ─── Load everything ──────────────────────────────────────────────────────────


model = load_embedding_model()
index, chunks = load_faiss_index()
groq_client = load_groq_client()

# ─── Conversation history ─────────────────────────────────────────────────────

conversation_history = []

# ─── Contextualize question using recent history ──────────────────────────────


def contextualize_question(question, history):
    if not history:
        return question

    # Take last 2 exchanges (4 messages)
    recent = history[-4:]
    history_text = ""
    for msg in recent:
        role = "User" if msg["role"] == "user" else "Bot"
        history_text += f"{role}: {msg['content']}\n"

    combined = f"{history_text}User: {question}"
    return combined

# ─── Retrieve relevant chunks from FAISS ─────────────────────────────────────


def retrieve_context(question, history, n_results=6):
    # Contextualize question with history
    search_query = contextualize_question(question, history)

    # Embed the search query
    question_vector = model.encode([search_query])
    question_vector = np.array(question_vector).astype("float32")

    # Search FAISS for top n_results closest vectors
    distances, indices = index.search(question_vector, n_results)

    # Use indices to fetch original text chunks
    # indices is a 2D array so we take indices[0]
    retrieved_chunks = [chunks[i] for i in indices[0] if i < len(chunks)]

    # Join retrieved chunks into one context string
    context = "\n\n".join(retrieved_chunks)
    return context

# ─── Ask Groq with context and history ───────────────────────────────────────


def ask_groq(question, context, history):
    system_prompt = """You are an official assistant for Bangladesh University of Business and Technology (BUBT).
Your job is to help students and applicants with information about BUBT only.

Note: "cost", "tuition fee", "program fee", "course fee" and "price" all mean the same thing.
Always check the context for fee related information when asked about cost or price.

Answer questions using ONLY the context provided. If a relevant link exists in the context, always include it.

Follow these rules strictly:

1. BUBT information questions → answer from context only, never make up facts.

2. General knowledge or career advice questions (like "is CSE hard?" or "career scope of BBA") →
   Say: "That's a great question! For personalized academic advice, I recommend speaking directly
   with BUBT's academic advisors. You can reach them at 01810033733 or visit the campus."

3. Sensitive or opinion based questions (like ragging, campus safety, 
   bullying, university comparisons, personal opinions about BUBT) →
   Say: "I'm only able to provide official information..."

4. Completely unrelated questions (weather, politics, sports etc) →
   Say: "I'm BUBT's assistant and can only help with questions about the university.
   Is there anything about admissions, programs, or fees I can help you with?"

Keep all responses friendly, professional and concise.
If the context contains a relevant link or URL related to the question, always include it in your answer."""

    # Build messages list
    messages = [{"role": "system", "content": system_prompt}]

    # Add conversation history (last 10 messages = 5 exchanges)
    if history:
        messages.extend(history[-10:])

    # Add current question with context
    current_message = f"""Context:
{context}

Question: {question}"""

    messages.append({"role": "user", "content": current_message})

    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages
    )

    return response.choices[0].message.content

# ─── Main function ────────────────────────────────────────────────────────────


def get_answer(question):
    global conversation_history

    # Retrieve context using history aware search
    context = retrieve_context(question, conversation_history)

    # Get answer from Groq
    answer = ask_groq(question, context, conversation_history)

    # Save exchange to history
    conversation_history.append({"role": "user", "content": question})
    conversation_history.append({"role": "assistant", "content": answer})

    return answer

 # ─── Terminal test ────────────────────────────────────────────────────────────


# if __name__ == "__main__":
#     print("BUBT Chatbot ready! Type 'exit' to quit.\n")
#     while True:
#         question = input("You: ")
#         if question.lower() == "exit":
#             break
#         answer = get_answer(question)
#         print(f"\nBot: {answer}\n")
