<h1 align="center">🤖 KnowledgeSystem 📚</h1>

## 🚀 Project Description

KnowledgeSystem is an intelligent knowledge management platform that leverages LLMs (Large Language Models) to provide conversational retrieval, context-aware responses, and seamless integration with vector stores. Built with Python and Flask, it offers a modern web interface for users to interact with their knowledge base.

---

## 🏗️ Project Structure

```text
KnowledgeSystem/
├── LICENSE
├── README.md
├── requirements.txt
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── main.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── vectore_store.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── llm_service.py
│   │   └── storage_service.py
│   ├── static/
│   │   └── style.css
│   └── templates/
│       └── index.html
└── vector_db/
```

---

## 🛠️ Installation

1. **Clone the repository:**
	```bash
	git clone https://github.com/yourusername/KnowledgeSystem.git
	cd KnowledgeSystem
	```
2. **Create a virtual environment (recommended):**
	```bash
	python3 -m venv .venv
	source .venv/bin/activate
	```
	Or using [uv](https://github.com/astral-sh/uv):
	```bash
	uv venv --python 3.11 .venv
	source .venv/bin/activate
	uv pip install -r requirements.txt
	```
3. **Install Python requirements:**
	```bash
	pip install -r requirements.txt
	```
4. **Set up environment variables:**
	- Copy `.env-example` to `.env` and fill in your API keys and settings.

---



## 🧩 Architecture Overview

Below is a high-level architecture diagram of the application:

```
╭──────────────────────────────╮
│      User Interface          │
│        (HTML/CSS)           │
╰─────────────┬────────────────╯
		  │
		  ▼
	╭───────────────────────╮
	│     Flask App         │
	│     (main.py)         │
	╰─────┬─────┬─────┬─────╯
		│     │     │
		▼     ▼     ▼
   ╭────────────╮ ╭───────────────╮ ╭────────────────────╮
   │  LLM       │ │  Vector Store │ │ Templates/Static   │
   │  Service   │ │               │ │ Files              │
   ╰────┬───────╯ ╰──────┬────────╯ ╰─────────┬──────────╯
	  │                │                    │
	  ▼                ▼                    ▼
  ╭────────────╮   ╭──────────────╮     ╭──────────────╮
  │ OpenAI API │   │ Storage      │     │ style.css    │
  ╰────────────╯   │ Service      │     │ index.html   │
			 ╰──────────────╯     ╰──────────────╯
```

---

## 📄 Usage

1. Start the Flask app:
	```bash
	python app/main.py
	```
2. Open your browser and navigate to `http://localhost:5000`
3. Interact with the knowledge system via the web interface.

---

## ✨ Features

- Conversational AI with context memory
- Vector store integration for efficient retrieval
- Modular and extensible service architecture
- Simple, modern web UI

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📜 License

This project is licensed under the terms of the MIT License.
