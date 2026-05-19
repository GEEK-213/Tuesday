# Day 7: Terminal Executor

## Why `subprocess.run` over `os.system`?

When giving an AI agent the ability to execute terminal commands, it is crucial to use Python's built-in `subprocess.run` instead of the older `os.system`. 

Here are the main reasons:
1. **Output Capture**: `os.system` only returns the exit code of the command, not the actual output (stdout/stderr). `subprocess.run` with `capture_output=True` allows us to capture the text output and feed it back into the AI agent's memory.
2. **Timeouts**: `subprocess.run` supports a `timeout` parameter. Since AI agents might hallucinate or run blocking commands (like starting a server or a continuous ping), we need to enforce a strict timeout (e.g., 10 seconds) to prevent the agent from hanging indefinitely.
3. **Control**: `subprocess` provides far more control over input, output, error streams, and environment variables compared to `os.system`.

## Security Implications of `shell=True`

In our implementation, we use `shell=True` inside `subprocess.run`. 

**What does it do?**
When `shell=True` is passed, the command is executed through the shell (like bash, powershell, or cmd). This allows the agent to use shell features like pipes (`|`), redirections (`>`), and environment variable expansion seamlessly.

**The Calculated Risk:**
Using `shell=True` is generally discouraged in production applications where untrusted user input is passed directly to the shell, as it opens up the application to shell injection vulnerabilities. 
However, in a local development environment where the AI agent is the one generating the commands (and we are monitoring its actions), this is a calculated risk. We trade strict security for flexibility and power, allowing the agent to perform complex shell operations much like a human developer would. To mitigate risks, we ensure commands are bounded by strict timeouts.
