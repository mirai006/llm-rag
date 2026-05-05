from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama

CHROMA_DIR = r"C:\git_mirai006\llm-rag\chroma_db"
#MODEL = "qwen2.5-coder:14b"  # gemma3:4b に変えてもOK
MODEL = "gemma3:4b" 

embeddings = HuggingFaceEmbeddings(
    model_name="intfloat/multilingual-e5-large",
    model_kwargs={"device": "cuda"},
    encode_kwargs={"batch_size": 128},
)

db = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
llm = Ollama(model=MODEL)

def ask(question):
    # 検索
    docs = db.similarity_search(f"query: {question}", k=5)
    context = "\n\n".join([doc.page_content for doc in docs])
    sources = list(set([doc.metadata.get('source', '') for doc in docs]))

    # プロンプト
    prompt = f"""以下のAWS CloudFormationドキュメントを参考に、質問に日本語で答えてください。

ドキュメント:
{context}

質問: {question}

回答:"""

    response = llm.invoke(prompt)
    print(f"\n回答:\n{response}")
    print(f"\n参照ソース:")
    for s in sources:
        print(f"  - {s}")

# 対話ループ
while True:
    question = input("\n質問を入力してください (終了: q): ")
    if question.lower() == 'q':
        break
    ask(question)