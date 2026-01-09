from dotenv import load_dotenv
import os
from pinecone import Pinecone

load_dotenv()

key = os.getenv("PINECONE_API_KEY")
print("KEY FOUND:", bool(key))

pc = Pinecone(api_key=key)

print("INDEXES:", pc.list_indexes())
