# ====================
# アプリインストール
# ====================
winget install Ollama.Ollama

# --------------------
# Ollamaモデル
# --------------------
ollama pull gemma3:4b          # 軽いベースライン用 ~3GB
ollama pull qwen2.5-coder:14b  # 強いベースライン用 ~9GB