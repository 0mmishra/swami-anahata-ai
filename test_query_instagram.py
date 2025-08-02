import chromadb
from chromadb.config import Settings

# ✅ Connect to the local persistent DB
client = chromadb.PersistentClient(path="./anahata_db")
collection = client.get_collection(name="instagram_posts")

# 🔍 Use a known caption fragment to test matching
query = "Masculinity was meant to be presence"

# 🔎 Perform similarity search
results = collection.query(
    query_texts=[query],
    n_results=5
)

# 🖨️ Print results nicely
print("🔍 Query:", query)
print("\n📄 Matching Results:\n")
for doc, meta, dist in zip(results["documents"][0], results["metadatas"][0], results["distances"][0]):
    print(f"→ {doc}\n   [Source: {meta['source']} | Score: {round(dist, 4)}]\n")
