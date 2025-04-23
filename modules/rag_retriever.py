import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
import whisper

# 🔁 PATHS
FAISS_PATH = "data/vector_store/faiss_index"

# ------------------ PART 1: General Knowledge Setup ------------------

def get_general_finance_knowledge():
    """
    Predefined general finance knowledge base.
    """
    texts = [
        "The primary goal of financial management is to maximize shareholder wealth by making sound investment and financing decisions.",
        "Financial statements include the balance sheet, income statement, and cash flow statement.",
        "The balance sheet provides a snapshot of a company’s financial position at a specific point in time.",
        "Cash flow statements show the inflows and outflows of cash, categorized into operating, investing, and financing activities.",
        "Profitability ratios such as gross margin and net profit margin help assess a company’s financial performance.",
        "Working capital management involves managing current assets and liabilities to ensure a company can meet its short-term obligations.",
        "Capital budgeting is the process of evaluating and selecting long-term investments that are in line with the firm's goal of shareholder wealth maximization.",
    ]
    return [Document(page_content=text) for text in texts]

def setup_general_vector_store():
    """
    Embed and store general finance knowledge into FAISS.
    """
    documents = get_general_finance_knowledge()
    return setup_vector_store(documents)

# ------------------ PART 2: Document Embedding & Search ------------------

def setup_vector_store(documents, save_index=True):
    """
    Embed documents and store them in FAISS vector DB.
    """
    embed = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = FAISS.from_documents(documents, embed)
    if save_index:
        save_vector_store(db)
    return db

def save_vector_store(vector_store):
    """
    Save the FAISS vector store to local path.
    """
    vector_store.save_local(FAISS_PATH)

def load_vector_store():
    """
    Load FAISS vector store from local path.
    """
    index_path = os.path.join(FAISS_PATH, "index.faiss")
    if os.path.exists(index_path):
        embed = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        try:
            return FAISS.load_local(FAISS_PATH, embed, allow_dangerous_deserialization=True)
        except Exception as e:
            print("⚠️ Failed to load FAISS index:", e)
            return None
    else:
        return None

def query_vector_store(question, vector_store=None, k=1):
    """
    Perform semantic search with the input question.
    """
    if not vector_store:
        vector_store = load_vector_store()
        if not vector_store:
            print("🧠 No user-uploaded vector store found. Using general financial knowledge base...")
            vector_store = setup_general_vector_store()

    result = vector_store.similarity_search(question, k=k)
    return result[0].page_content if result else "❌ No relevant information found."

# ------------------ PART 3: Audio Input → Semantic Answer ------------------

def transcribe_audio(audio_path):
    """
    Transcribe speech to text using OpenAI Whisper.
    """
    try:
        model = whisper.load_model("base")  # Options: tiny, base, small, medium, large
        result = model.transcribe(audio_path)
        return result['text']
    except Exception as e:
        return f"❌ Failed to transcribe audio: {e}"

def query_from_audio(audio_path):
    """
    Convert audio → question → vector search → answer.
    """
    question = transcribe_audio(audio_path)
    if "❌" in question:
        return question
    print(f"🎤 Transcribed Question: {question}")
    return query_vector_store(question)
