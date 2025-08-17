import os
import docx
import chromadb
from chromadb.utils import embedding_functions

# ==========================
# 1. Setup ChromaDB Client
# ==========================
client = chromadb.PersistentClient(path="./chroma_db")  # will create folder if not exists
collection = client.get_or_create_collection(name="policy_docs")

# Embedding function (local model, no API needed)
embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# ==========================
# 2. Load .docx files from folder
# ==========================
folder_path = "Policy_Data"  # change path if needed

def read_docx(file_path):
    """Read all paragraphs from a .docx file and return as single string."""
    doc = docx.Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])

# Loop through all .docx files and add to ChromaDB
for filename in os.listdir(folder_path):
    filepath = os.path.join(folder_path, filename)

    if os.path.isfile(filepath) and filename.endswith(".docx"):
        text = read_docx(filepath)

        # Add to ChromaDB
        collection.add(
            documents=[text],
            ids=[filename],  # using filename as unique ID
        )
        print(f"✅ Saved: {filename}")

# ==========================
# 3. Verify saved docs
# ==========================
print("\n📂 Total documents in collection:", collection.count())

# Optional: run a test query
query_text = "Leave Policy"  # example query
results = collection.query(
    query_texts=[query_text],
    n_results=3
)
print("\n🔎 Query Results:", results)
