# Day 6: Implementing a File Reader for Tuesday

Today, we've given Tuesday the ability to read files! This is a massive upgrade. It means that when Tuesday needs to debug code, analyze configurations, or understand a specific document, she can now open the file directly and read its contents.

However, giving an AI the ability to read files from your hard drive introduces two important challenges that we needed to address: Security and Memory Limits.

## Security: Preventing "Directory Traversal Attacks"

Imagine if you told an AI, "Please read the file `my_code.py`." The AI opens it, reads it, and helps you. Great!
But what if a malicious user (or a confused AI) tried to read this instead:
`../../../../etc/passwd` (on Linux/Mac) or `../../../../Windows/System32/config/SAM` (on Windows).

This is known as a **Directory Traversal Attack** (or "Path Traversal"). By using `../` (which means "go up one folder"), an attacker can break out of the project folder and start accessing sensitive files anywhere on your computer—including passwords, private keys, or personal documents.

### How We Protected Tuesday

We added a strict "sandbox" rule to Tuesday's `read_file` tool:
1. Tuesday is **only** allowed to read files that are inside her `workspace/` directory or the current project directory.
2. Before opening any file, the tool checks the absolute path of the requested file. 
3. If the path tries to escape the allowed folders, the tool instantly blocks the request and returns an "Access Denied" error.

This ensures that Tuesday remains helpful without compromising the security of your computer.

## Efficiency: Context Window Limits

You might wonder: *Why make Tuesday read files one by one? Why not just give her the entire project codebase all at once?*

This comes down to how AI models process information, specifically their **Context Window Limit**.

### What is a Context Window?
An AI's context window is like its short-term memory. It dictates how many words (or "tokens") it can remember and process at any given moment. 

If your project has 50 files, and each file is 500 lines long, sending the entire project to the AI would quickly exceed its memory limit. Even if the AI's context window is massive, dumping thousands of lines of irrelevant code has negative side effects:
- **It's Slow:** The AI has to read and process a massive wall of text before answering.
- **It's Expensive:** API costs are usually calculated based on the number of tokens processed. Sending 100,000 tokens for a simple question gets very expensive, very fast.
- **It's Distracting:** The more irrelevant code you give the AI, the higher the chance it gets confused or misses the specific bug you are trying to fix.

### The Tool-Based Solution
Instead of forcing Tuesday to memorize the entire project, we give her a `[READ_FILE]` tool. 

Now, when you ask her to fix a bug in `main.py`, she doesn't need to look at the database config or the UI styling. She simply says, *"I need to read `main.py`,"* grabs exactly the information she needs, and gives you a fast, focused, and accurate answer. 
