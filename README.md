# 🎓 BUBT AI Assistant

An AI-powered chatbot for Bangladesh University of Business and Technology (BUBT) that answers questions about admissions, programs, tuition fees, scholarships, clubs and more.

---

## 🌐 Live Demo
👉 [Click here to try the chatbot]([https://your-app-url.streamlit.app](https://bubt-edubot-di3zq54wuzczu7canb2j5c.streamlit.app/))

---

## 📌 Features

- 🎯 Answers questions about BUBT programs, fees, and admissions
- 💰 Provides detailed tuition fee breakdown for all programs
- 🏆 Explains scholarship and waiver criteria
- 📋 Lists required documents for admission
- 🏛️ Provides information about all 12 BUBT student clubs
- 🔗 Shares direct links to important university pages
- 💬 Remembers conversation context for follow-up questions
- 🚫 Handles out-of-scope questions gracefully

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python |
| AI Model | Llama 3.1 8B via Groq API |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| Vector Search | FAISS |
| Text Processing | LangChain Text Splitters |
| UI | Streamlit |
| Deployment | Streamlit Community Cloud |

---

## 🏗️ Architecture

University Data (JSON)
│
▼
Text Conversion (json_to_text.py)
│
▼
Chunking (LangChain RecursiveCharacterTextSplitter)
│
▼
Embedding (sentence-transformers → all-MiniLM-L6-v2)
│
▼
Vector Storage (FAISS → index.faiss + index.pkl)
User Question
│
▼
Embed Question (same model)
│
▼
Search FAISS (find top 6 relevant chunks)
│
▼
Build Prompt (context + conversation history)
│
▼
Groq LLM (llama-3.1-8b-instant)
│
▼
Answer displayed in Streamlit UI

## 🚀 Run Locally

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/BUBT-Chatbot.git
cd BUBT-Chatbot
```

**2. Create virtual environment**
```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Mac/Linux
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up environment variables**

Create a `.env` file in the root folder:
GROQ_API_KEY=your_groq_api_key_here
Get your free Groq API key at 👉 https://console.groq.com

**5. Run the app**
```bash
streamlit run app.py
```

---

## 💡 Sample Questions
What is the tuition fee for CSE?
What documents are needed for admission?
What scholarships are available at BUBT?
Tell me about the Debating Club
What is the grading system?
Where can I find the class routine?
What are the graduate programs offered?
What is the waiver for freedom fighters?

## 🙏 Acknowledgements

- [Groq](https://groq.com) for the free LLM API
- [Sentence Transformers](https://www.sbert.net) for the embedding model
- [FAISS](https://github.com/facebookresearch/faiss) by Meta for vector search
- [Streamlit](https://streamlit.io) for the UI and free deployment
- [BUBT](https://bubt.edu.bd) for the university information


this is personal learning project to learn about RAG,ChatBot,VectorDB etc.
