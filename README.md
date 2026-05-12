# 🤖 Tuesday — Autonomous AI Agent

> *"Good morning. It's Tuesday."*

**Tuesday** is a Jarvis-style autonomous AI agent designed to assist with tasks on your local machine, interact with LLMs, and orchestrate tools intelligently.

## 📁 Project Structure

```
Tuesday/
├── brain/              # 🧠 LLM integration & AI reasoning
│   ├── llm_client.py   #    Interface to talk to LLMs (OpenAI, local models, etc.)
│   ├── memory.py        #    Conversation history & context management
│   └── prompts/         #    System prompts & prompt templates
│       └── system_prompt.txt
│
├── tools/              # 🔧 Local OS tools & automation
│   ├── file_manager.py  #    Read, write, search files
│   ├── system_info.py   #    Get OS info, running processes, etc.
│   └── web_search.py    #    Web search & scraping capabilities
│
├── skills/             # 🎯 High-level composed skills
│   └── __init__.py      #    Skills that combine brain + tools
│
├── config/             # ⚙️ Configuration files
│   └── settings.py      #    App settings & constants
│
├── models/             # 🗂️ Local model storage (Git-ignored)
│   └── local/           #    Place .gguf / .bin model files here
│
├── tests/              # 🧪 Unit & integration tests
│   └── __init__.py
│
├── .env.example        # 📋 Template for environment variables (SAFE to commit)
├── .gitignore          # 🚫 Files Git should ignore
├── requirements.txt    # 📦 Python dependencies
├── main.py             # 🚀 Entry point — starts Tuesday
└── README.md           # 📖 You are here
```

## 🚀 Getting Started

1. **Clone the repo:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/Tuesday.git
   cd Tuesday
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate   # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your API keys:**
   ```bash
   copy .env.example .env
   # Edit .env and add your real API keys
   ```

5. **Run Tuesday:**
   ```bash
   python main.py
   ```

## 🔐 Security

- **NEVER** commit your `.env` file or any file containing API keys.
- Use `.env.example` as a template — it contains placeholder values only.
- The `.gitignore` is pre-configured to protect your secrets.

## 📜 License

MIT License — See LICENSE for details.
