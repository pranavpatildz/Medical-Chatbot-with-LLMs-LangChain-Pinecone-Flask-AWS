from dotenv import load_dotenv
import os
from src.helper import load_pdf_files, filter_to_minimal_docs, text_split, download_embeddings
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore

load_dotenv()

# ✅ API KEY (DO NOT use os.getenv with key string)
PINECONE_API_KEY = os.environ["PINECONE_API_KEY"]

# 1️⃣ Load & process documents
extracted_data = load_pdf_files(
    r"D:\Medical Chatbot\Medical-Chatbot-with-LLMs-LangChain-Pinecone-Flask-AWS\data"
)
minimal_docs = filter_to_minimal_docs(extracted_data)
texts_chunk = text_split(minimal_docs)

print(f"📄 PDFs loaded: {len(extracted_data)}")
print(f"✂️ Text chunks created: {len(texts_chunk)}")

# 2️⃣ Load embeddings
embeddings = download_embeddings()
print("🧠 Embeddings loaded")

# 3️⃣ Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
index_name = "medical-chatbot"

# 4️⃣ Create index if not exists
if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )

# 5️⃣ 🔥 UPSERT DOCUMENTS (THIS WAS MISSING)
vectorstore = PineconeVectorStore.from_documents(
    documents=texts_chunk,
    embedding=embeddings,
    index_name=index_name,
)

print("✅ Documents successfully upserted into Pinecone")