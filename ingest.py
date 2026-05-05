from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# 設定
DOCS_DIR = r"C:\git_mirai006\llm-rag\cfn-docs-text"
CHROMA_DIR = r"C:\git_mirai006\llm-rag\chroma_db"

print("ドキュメント読み込み中...")
loader = DirectoryLoader(
    DOCS_DIR,
    glob="**/*.txt",
    loader_cls=TextLoader,
    loader_kwargs={"encoding": "utf-8"},
    show_progress=True,
)
docs = loader.load()
print(f"読み込み完了: {len(docs)}件")

# チャンク分割
splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=64,
)
chunks = splitter.split_documents(docs)
print(f"チャンク数: {len(chunks)}")

# Embedding モデル（多言語対応・CUDA）
print("Embeddingモデル読み込み中...")
embeddings = HuggingFaceEmbeddings(
    model_name="intfloat/multilingual-e5-large",
    model_kwargs={"device": "cuda"},
    encode_kwargs={"batch_size": 128},
)

# Chroma に取り込み（バッチ処理）
print("Chromaに取り込み中...")
BATCH = 1000
for i in range(0, len(chunks), BATCH):
    batch = chunks[i:i+BATCH]
    if i == 0:
        db = Chroma.from_documents(
            batch,
            embeddings,
            persist_directory=CHROMA_DIR,
        )
    else:
        db.add_documents(batch)
    print(f"  {min(i+BATCH, len(chunks))}/{len(chunks)} チャンク完了")

print("完了！")