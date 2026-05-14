# 🤖 Tuesday — Complete Project Setup Guide

---

## 1. What Is Version Control? (The Simple Analogy)

Imagine you're writing a novel. Every night before bed, you photocopy your entire manuscript and label it **"Draft — May 12"**. The next night, another copy: **"Draft — May 13"**.

If you accidentally delete a whole chapter on May 14, no problem — you grab the May 13 copy and you're back in business.

**That's version control.**

- **Git** is the photocopier — it lives on *your* computer and takes snapshots (called **commits**) of your project.
- **GitHub** is a safe deposit box in the cloud — you send copies of your snapshots there so they're backed up and shareable.

| Concept | Real-World Analogy |
|---|---|
| **Git** | Your personal photocopier |
| **Commit** | One labeled photocopy of your manuscript |
| **Repository (repo)** | The binder holding all your photocopies |
| **GitHub** | The bank vault where you store a backup binder |
| **Push** | Sending your latest copies to the vault |
| **Pull** | Grabbing the latest copies from the vault |
| **.gitignore** | A sticky note saying "DON'T photocopy these pages" |

---

## 2. What Was Just Created ✅

I've already created everything for you. Here's your full project tree:

```
c:\My_Projects\My_Projects\Tuesday\
│
├── 🧠 brain/                    ← The AI's "thinking" module
│   ├── __init__.py
│   ├── llm_client.py            ← Talks to LLMs (OpenAI, Gemini, etc.)
│   ├── memory.py                ← Remembers conversation history
│   └── prompts/
│       └── system_prompt.txt    ← Tuesday's personality definition
│
├── 🔧 tools/                    ← Local OS automation
│   ├── __init__.py
│   ├── file_manager.py          ← Read/write/list files
│   ├── system_info.py           ← OS info, environment
│   └── web_search.py            ← Web search (placeholder)
│
├── 🎯 skills/                   ← High-level skills (brain + tools combined)
│   └── __init__.py
│
├── ⚙️ config/                   ← Configuration
│   ├── __init__.py
│   └── settings.py              ← App constants & .env loader
│
├── 🗂️ models/local/             ← Where you'll put local AI models (git-ignored)
│   └── .gitkeep
│
├── 🧪 tests/                    ← Future tests go here
│   └── __init__.py
│
├── 📋 .env.example              ← API key template (SAFE to commit)
├── 🚫 .gitignore                ← Tells Git what NOT to upload
├── 📦 requirements.txt          ← Python packages
├── 🚀 main.py                   ← Entry point — run this to start Tuesday
└── 📖 README.md                 ← Project documentation
```

---

## 3. The `.gitignore` Explained — Protecting Your Secrets

> [!CAUTION]
> If you accidentally push an API key to GitHub, **anyone on the internet can find and use it**, potentially running up hundreds of dollars in charges. The `.gitignore` is your safety net.

Your `.gitignore` blocks these categories:

| Category | What it blocks | Why |
|---|---|---|
| **API Keys & Secrets** | `.env`, `secrets/`, `*.key` | Your passwords & billing keys |
| **Python junk** | `__pycache__/`, `venv/`, `*.pyc` | Auto-generated files, not your code |
| **Node.js junk** | `node_modules/` | Downloaded packages (huge, reproducible) |
| **IDE files** | `.idea/`, `*.swp` | Your personal editor settings |
| **OS clutter** | `.DS_Store`, `Thumbs.db` | Mac/Windows hidden files |
| **AI model files** | `models/local/*.bin`, `*.gguf` | Too large for Git (multi-GB) |

### The `.env.example` vs `.env` Pattern

```
.env.example  ← Template with FAKE keys     → ✅ COMMITTED to Git (safe)
.env          ← Your REAL keys               → ❌ NEVER committed (git-ignored)
```

To set up your real keys:
```powershell
# In the VS Code terminal:
copy .env.example .env
# Then open .env and replace the placeholder values with your real API keys
```

---

## 4. Git Is Already Initialized ✅

I've already run these commands for you:

```powershell
# ✅ DONE — Initialize the repository
git init

# ✅ DONE — Stage all files
git add -A

# ✅ DONE — Create the first commit
git commit -m "Initial commit: Tuesday AI Agent project structure"
```

Your local Git repo is ready with **18 files committed**.

---

## 5. Connecting to GitHub (You Do This Part)

### Step 1: Create the GitHub Repository

1. Go to [github.com/new](https://github.com/new)
2. Set **Repository name** to: `Tuesday`
3. Set visibility to **Private** (recommended for a project with API key handling)
4. **⚠️ Do NOT** check "Add a README" or "Add .gitignore" — we already have those
5. Click **Create repository**

### Step 2: Link & Push (Run These in VS Code Terminal)

After creating the repo, GitHub will show you a URL. Run these commands in your VS Code terminal:

```powershell
# Replace YOUR_USERNAME with your actual GitHub username
git remote add origin https://github.com/YOUR_USERNAME/Tuesday.git

# Rename the branch to 'main' (modern convention)
git branch -M main

# Push your code to GitHub
git push -u origin main
```

> [!NOTE]
> If this is your first time pushing, GitHub will ask you to log in. A browser window will open — just sign in and authorize.

### Step 3: Verify

After pushing, refresh your GitHub repo page. You should see all your files there — but **NOT** a `.env` file (because `.gitignore` is protecting you).

---

## 6. The Daily Git Workflow

From now on, every time you make meaningful changes, run this in your VS Code terminal:

```powershell
# See what changed
git status

# Stage all changes
git add -A

# Save a snapshot with a descriptive message
git commit -m "Add: basic LLM client for OpenAI"

# Send it to GitHub
git push
```

> [!TIP]
> Write commit messages like mini journal entries. Future-you will thank present-you.
> - ✅ `"Add: conversation memory with context window"`
> - ✅ `"Fix: crash when API key is missing"`
> - ❌ `"stuff"` or `"update"`

---

## 7. Quick Reference — Commands You'll Use Most

| Command | What it does |
|---|---|
| `git status` | Shows what files have changed |
| `git add -A` | Stages ALL changes for the next commit |
| `git commit -m "message"` | Saves a snapshot locally |
| `git push` | Uploads your commits to GitHub |
| `git pull` | Downloads the latest from GitHub |
| `git log --oneline -5` | Shows your last 5 commits |

---

## 8. Next Steps

Your project is ready to build on. Here's a suggested roadmap:

1. **🔐 Set up `.env`** — Copy `.env.example` to `.env` and add your real API keys
2. **🧠 Wire up the brain** — Implement `brain/llm_client.py` with real OpenAI/Gemini calls
3. **🎤 Add voice I/O** — Give Tuesday ears and a mouth
4. **🔧 Build more tools** — App launcher, clipboard manager, email reader
5. **🎯 Compose skills** — Chain brain + tools into powerful workflows

---

> *Good morning. It's Tuesday. Let's build something extraordinary.* 🤖
