# Duke Pilot


**duke-pilot** is a personal, self-hosted alternative to GitHub Copilot — built as a learning project to explore how LLM-based code assistants work under the hood. It uses FastAPI, local models (like [Qwen](https://huggingface.co/Qwen)), document embedding, and modular processing pipelines. Designed to run on your own server via Docker.

---

## 🚀 Features

- ⚙️ FastAPI-based REST API for LLM-driven code and document assistance
- 🧾 Document ingestion pipeline: supports PDFs, images, text, and more
- 🧠 Embedding and retrieval via a chunked docstore backend
- 🔌 Pluggable LLM support (default: Qwen, others via Hugging Face)
- 🐳 Dockerized for easy local or server deployment
- 💬 [Coming Soon] Minimal chat interface for interaction

---

## 📦 Project Structure

```

.
├── docker-compose.yaml       # Runs the full app + doc store
├── duke\_pilot/               # Main application
│   ├── api/                  # FastAPI endpoints for chat, docstore, parser
│   ├── docstore/             # In-memory or persistent vector storage
│   ├── processors/           # File parsers, chunkers, embedding logic
│   ├── prompter/             # Prompt templates and model wiring
│   └── utils/                # Pathing, UUID, and helper functions

````

---

## ⚡ Getting Started

### 🔧 Prerequisites

- Docker and Docker Compose
- (Optional) GPU for faster model inference

### 🐳 Run with Docker

```bash
docker-compose up --build
````

Once running, the FastAPI app will be available at [http://localhost:8000](http://localhost:8000).

### 🔗 API Docs

Visit [http://localhost:8000/docs](http://localhost:8000/docs) for the Swagger UI.

---

## 🧠 Model Configuration

By default, duke-pilot uses the [Qwen](https://huggingface.co/Qwen) model from Hugging Face. You can modify `prompter/model.py` to use any Hugging Face-compatible LLM with minimal changes.

---

## 📂 Document Support

The document processor currently supports:

* `.pdf`, `.txt`, `.docx`, `.png`, `.jpg`, `.md`, etc.
* Automatic semantic chunking and embedding
* Parsed text is stored and indexed for retrieval-based prompting

---

## 🧪 Development

To run locally outside Docker:

```bash
uv sync
uv run uvicorn duke_pilot.main:app --reload
```

---

## 🎯 Roadmap

* [ ] Add simple web chat UI
* [ ] Add user auth
* [ ] Model hot-swap support via config
* [ ] Optimized chunk deduplication

---

## 🤝 Contributing

This is a personal learning project, I will likely drop this after the end of this weekend. It's just something to have a little fun with.

---

## 📄 License

MIT License

