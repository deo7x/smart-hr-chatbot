# from langchain_community.vectorstores import Chroma
# from langchain_community.document_loaders import Docx2txtLoader,DirectoryLoader, TextLoader, PyPDFLoader
# from langchain_community.embeddings import OllamaEmbeddings


# # Load documents from folder
# loader = DirectoryLoader(
#     r"C:\Skyview\Development\RASA HR AI\smart-hr-chatbot\HR_AI\policy_docs",
#     glob="**/*.docx",
#     loader_cls=Docx2txtLoader

# )
# docs = loader.load()

# # If PDFs: loader = DirectoryLoader("docs", glob="**/*.pdf", loader_cls=PyPDFLoader)

# # Create embeddings using Ollama (Llama2-based embeddings)
# embeddings = OllamaEmbeddings(model="llama2")

# # Create Chroma DB and persist
# db = Chroma.from_documents(docs, embeddings, persist_directory="vector_db")
# db.persist()

# print("✅ Documents indexed in ChromaDB")






import time
from threading import Thread
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import Docx2txtLoader, DirectoryLoader, TextLoader, PyPDFLoader
from langchain_community.embeddings import OllamaEmbeddings

# ---------------- Stopwatch Function ----------------
def stopwatch(task_name: str, func, *args, **kwargs):
    """
    Runs a function while showing an increasing timer.
    Returns the result of the function.
    """
    seconds = 0
    done = False
    result = None  # <-- Store function result

    def wrapper():
        nonlocal done, result
        result = func(*args, **kwargs)   # <-- Capture result
        done = True
        return result

    thread = Thread(target=wrapper)
    thread.start()

    # Show stopwatch until task completes
    while not done:
        mins, secs = divmod(seconds, 60)
        timer = f"{mins:02d}:{secs:02d}"
        print(f"{task_name} ⏱ {timer}", end="\r")
        time.sleep(1)
        seconds += 1

    thread.join()
    print(f"{task_name} ✅ Completed in {seconds} sec")
    return result   # <-- Return the captured result

# ---------------- Document Loading ----------------
def load_documents():
    loader = DirectoryLoader(
        r"C:\Skyview\Development\RASA HR AI\smart-hr-chatbot\HR_AI\policy_docs",
        glob="**/*.docx",
        loader_cls=Docx2txtLoader
    )
    docs = loader.load()
    print(f"📂 Loaded {len(docs)} documents")
    return docs

# ---------------- Embedding + Chroma ----------------
def create_chroma_db(docs):
    embeddings = OllamaEmbeddings(model="llama2")
    db = Chroma.from_documents(docs, embeddings, persist_directory="vector_db")
    db.persist()
    print(f"💾 Stored {len(docs)} documents in ChromaDB")
    return db

# ---------------- Main ----------------
if __name__ == "__main__":
    docs = stopwatch("📄 Loading Documents", load_documents)
    db = stopwatch("🔎 Creating ChromaDB", create_chroma_db, docs)

    print("🎉 All documents indexed in ChromaDB successfully!")
