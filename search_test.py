from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

CHROMA_DIR = r"C:\git_mirai006\llm-rag\chroma_db"

embeddings = HuggingFaceEmbeddings(
    model_name="intfloat/multilingual-e5-large",
    model_kwargs={"device": "cuda"},
    encode_kwargs={"batch_size": 128},
)

db = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)

# 日本語で検索
query = "query: サブネットの設定方法は？"
results = db.similarity_search(query, k=3)

for i, doc in enumerate(results):
    print(f"\n--- 結果 {i+1} ---")
    print(f"ソース: {doc.metadata.get('source', 'N/A')}")
    print(doc.page_content[:300])python search_test.py