# Agent Sandboxing: Safe File Writing

When building autonomous AI agents with the ability to write to the local file system, security and safety must be primary concerns. Providing an AI agent unrestricted access to the root directory is dangerous and can lead to unintended consequences.

## The Risks of Unrestricted Write Access
If an agent can write anywhere on your disk, a simple misunderstanding or hallucination by the LLM could result in:
- Overwriting critical system files.
- Modifying project source code unintentionally, breaking the application.
- Dropping malicious payloads if the LLM is somehow prompted to do so.

## The Sandboxing Solution
To mitigate these risks, we employ "Agent Sandboxing." Sandboxing involves restricting the AI's operations to an isolated environment or a designated folder.

For Tuesday, we achieve this by hardcoding a dedicated `workspace/` directory in the `file_writer.py` tool.

1. **Isolation**: By forcing all file writes into `workspace/`, we ensure that the AI cannot accidentally modify anything outside of this specific, safe location.
2. **Simplified Monitoring**: We know exactly where to look for the AI's outputs.
3. **Control**: The code dynamically resolves the path and appends the AI's intended filename exclusively to the `workspace/` directory, entirely preventing modifications to sensitive project files.

By containing the agent's reach, we gain the utility of autonomous file creation without sacrificing system security.
