# ====================
# アプリインストール
# ====================
winget install Ollama.Ollama

# --------------------
# Ollamaモデル
# --------------------
ollama pull gemma3:4b          # 軽いベースライン用 ~3GB
ollama pull qwen2.5-coder:14b  # 強いベースライン用 ~9GB


# Scraping
pip install requests beautifulsoup4
pip install selenium webdriver-manager

# Rag Index
pip install llama-index llama-index-llms-ollama llama-index-embeddings-ollama llama-index-vector-stores-chroma chromadb
pip install langchain langchain-community chromadb sentence-transformers
ollama pull nomic-embed-text

pip uninstall torch torchvision torchaudio -y

# CUDA 12.1対応版をインストール
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121