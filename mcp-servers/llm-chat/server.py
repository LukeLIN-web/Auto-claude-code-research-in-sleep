#!/usr/bin/env python3
"""Generic LLM Chat MCP Server - Supports any OpenAI-compatible API

Environment Variables:
    LLM_API_KEY         - API key (required)
    LLM_BASE_URL        - API base URL (default: https://api.openai.com/v1)
    LLM_MODEL           - Model name (default: gpt-5.6-sol)
    LLM_FALLBACK_MODEL  - Optional fallback model tried after the primary model
                          exhausts its retries (default: unset = no fallback)
    LLM_MAX_TOKENS      - Completion token cap (default: 8192)
    LLM_MAX_ATTEMPTS    - Attempts per model for retryable failures (default: 3)
    LLM_SERVER_NAME     - Server name for MCP (default: llm-chat)

Supported Providers (examples):
    OpenAI:      LLM_BASE_URL=https://api.openai.com/v1 LLM_MODEL=gpt-5.6-sol
    DeepSeek:    LLM_BASE_URL=https://api.deepseek.com/v1 LLM_MODEL=deepseek-chat
    Kimi:        LLM_BASE_URL=https://api.moonshot.cn/v1 LLM_MODEL=moonshot-v1-32k
    MiniMax:     LLM_BASE_URL=https://api.minimax.io/v1 LLM_MODEL=MiniMax-M3
"""

import datetime
import json
import os
import random
import sys
import tempfile
import time
import httpx

_stdio_initialized = False


def _init_stdio():
    """Rebind stdio to raw unbuffered binary streams for MCP framing.

    Deferred into a function (called at the top of main()) so that merely
    IMPORTING this module has no stdio side effects. os.fdopen(fileno) defaults
    to closefd=True and thus seizes ownership of the fd; doing that at import
    time under a test harness that captures stdio (pytest fd-capture) closes the
    harness's capture fd and corrupts capture for every subsequent test. Real
    server launch (python server.py) still calls this first via main(), so
    runtime behavior is unchanged. Idempotent."""
    global _stdio_initialized
    if _stdio_initialized:
        return
    # Force unbuffered stdout/stdin
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'wb', buffering=0)
    sys.stdin = os.fdopen(sys.stdin.fileno(), 'rb', buffering=0)
    _stdio_initialized = True

# Configuration from environment
API_KEY = os.environ.get("LLM_API_KEY", "")
BASE_URL = os.environ.get("LLM_BASE_URL", "https://api.openai.com/v1")
DEFAULT_MODEL = os.environ.get("LLM_MODEL", "gpt-5.6-sol")
# No default fallback: an unset fallback means "retry the primary only".
# (Defaulting it to DEFAULT_MODEL made the fallback arm a no-op.)
FALLBACK_MODEL = os.environ.get("LLM_FALLBACK_MODEL", "")
MAX_TOKENS = int(os.environ.get("LLM_MAX_TOKENS", "8192"))
SERVER_NAME = os.environ.get("LLM_SERVER_NAME", "llm-chat")

# Retry policy: transient statuses get exponential backoff + jitter,
# honoring Retry-After when the server sends one.
RETRYABLE_STATUSES = {429, 500, 502, 503, 504, 529}
MAX_ATTEMPTS_PER_MODEL = max(1, int(os.environ.get("LLM_MAX_ATTEMPTS", "3")))

# Newer OpenAI models only accept max_completion_tokens; most OpenAI-compatible
# providers only accept max_tokens. Start with the new name and downgrade once
# (process-wide) when the provider rejects it with a 400 naming the parameter.
_token_param = "max_completion_tokens"

# Debug logging
DEBUG_LOG = os.path.join(tempfile.gettempdir(), f"{SERVER_NAME}-mcp-debug.log")

def debug_log(msg):
    try:
        with open(DEBUG_LOG, "a") as f:
            f.write(f"{datetime.datetime.now()}: {msg}\n")
            f.flush()
    except Exception:
        pass

def log_error(msg):
    try:
        with open(DEBUG_LOG, "a") as f:
            f.write(f"{datetime.datetime.now()}: ERROR: {msg}\n")
    except Exception:
        pass

debug_log(f"=== {SERVER_NAME} MCP Server Starting (v2.1) ===")
debug_log(f"BASE_URL: {BASE_URL}")
debug_log(f"MODEL: {DEFAULT_MODEL}")
debug_log(f"FALLBACK_MODEL: {FALLBACK_MODEL}")
debug_log(f"API_KEY set: {bool(API_KEY)}")

_use_ndjson = False

def send_response(response):
    global _use_ndjson
    json_str = json.dumps(response, separators=(',', ':'))
    json_bytes = json_str.encode('utf-8')

    if _use_ndjson:
        output = json_bytes + b'\n'
    else:
        header = f"Content-Length: {len(json_bytes)}\r\n\r\n".encode('utf-8')
        output = header + json_bytes

    sys.stdout.write(output)
    sys.stdout.flush()

def _retry_delay(attempt, response=None):
    """Exponential backoff + jitter; honor Retry-After when present."""
    if response is not None:
        retry_after = response.headers.get("retry-after")
        if retry_after:
            try:
                return min(float(retry_after), 60.0)
            except ValueError:
                pass
    return min(2 ** attempt + random.uniform(0.0, 1.0), 30.0)


def _post_chat(client, url, headers, current_model, messages):
    """POST once; transparently downgrade max_completion_tokens -> max_tokens."""
    global _token_param
    payload = {
        "model": current_model,
        "messages": messages,
        _token_param: MAX_TOKENS,
    }
    response = client.post(url, headers=headers, json=payload)
    if (
        response.status_code == 400
        and _token_param == "max_completion_tokens"
        and "max_completion_tokens" in response.text
    ):
        debug_log("Provider rejected max_completion_tokens; downgrading to max_tokens")
        _token_param = "max_tokens"
        payload = {
            "model": current_model,
            "messages": messages,
            "max_tokens": MAX_TOKENS,
        }
        response = client.post(url, headers=headers, json=payload)
    return response


def call_llm(messages, model=None):
    """Call LLM Chat Completions API with retries and optional model fallback"""
    if not API_KEY:
        return None, "LLM_API_KEY environment variable not set"

    use_model = model or DEFAULT_MODEL
    url = f"{BASE_URL.rstrip('/')}/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    models = [use_model]
    if FALLBACK_MODEL and FALLBACK_MODEL != use_model:
        models.append(FALLBACK_MODEL)

    last_error = None
    for current_model in models:
        for attempt in range(MAX_ATTEMPTS_PER_MODEL):
            debug_log(f"Calling LLM API (attempt {attempt + 1}/{MAX_ATTEMPTS_PER_MODEL}): model={current_model}")
            try:
                with httpx.Client(timeout=300.0) as client:
                    response = _post_chat(client, url, headers, current_model, messages)
            except httpx.HTTPError as e:
                last_error = f"Connection error: {e}"
                debug_log(f"API exception on attempt {attempt + 1} with {current_model}: {e}")
                if attempt < MAX_ATTEMPTS_PER_MODEL - 1:
                    time.sleep(_retry_delay(attempt))
                continue

            if response.status_code in RETRYABLE_STATUSES:
                last_error = f"API error {response.status_code}: {response.text[:200]}"
                debug_log(f"Retryable {last_error} (attempt {attempt + 1} with {current_model})")
                if attempt < MAX_ATTEMPTS_PER_MODEL - 1:
                    time.sleep(_retry_delay(attempt, response))
                continue

            if response.status_code != 200:
                error_msg = f"API error {response.status_code}: {response.text[:500]}"
                debug_log(f"API error: {error_msg}")
                return None, error_msg

            try:
                data = response.json()
            except ValueError as e:
                return None, f"API returned non-JSON response: {e}"
            try:
                content = data["choices"][0]["message"]["content"]
            except (KeyError, IndexError, TypeError) as e:
                return None, f"Unexpected API response structure: {e}"
            if current_model != use_model:
                fallback_note = f"\n\n[Note: Used fallback model {current_model} after errors with {use_model}]"
                content = fallback_note + "\n" + content
                debug_log(f"API success with fallback model {current_model}, response length: {len(content)}")
            else:
                debug_log(f"API success (attempt {attempt + 1}), response length: {len(content)}")
            return content, None

    return None, last_error or "All attempts failed"

def handle_request(request):
    """Handle a JSON-RPC request"""
    method = request.get("method", "")
    params = request.get("params", {})
    request_id = request.get("id")

    debug_log(f"Handling method: {method}, id: {request_id}")

    # Handle notifications (no id, no response needed)
    if request_id is None:
        if method == "notifications/initialized":
            debug_log("Client initialized successfully")
        return None

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": SERVER_NAME,
                    "version": "2.0.0"
                }
            }
        }

    elif method == "ping":
        return {"jsonrpc": "2.0", "id": request_id, "result": {}}

    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "tools": [{
                    "name": "chat",
                    "description": f"Send a message to {DEFAULT_MODEL} and get a response. Use this for research reviews, code analysis, and general AI tasks.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "prompt": {
                                "type": "string",
                                "description": "The prompt to send"
                            },
                            "model": {
                                "type": "string",
                                "description": f"Model to use (default: {DEFAULT_MODEL})"
                            },
                            "system": {
                                "type": "string",
                                "description": "Optional system prompt"
                            }
                        },
                        "required": ["prompt"]
                    }
                }]
            }
        }

    elif method == "tools/call":
        tool_name = params.get("name", "")
        arguments = params.get("arguments", {})

        if tool_name == "chat":
            prompt = arguments.get("prompt", "")
            model = arguments.get("model", DEFAULT_MODEL)
            system = arguments.get("system", "")

            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})

            debug_log(f"Tool call: chat, prompt length: {len(prompt)}")
            content, error = call_llm(messages, model)

            if error:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [{"type": "text", "text": f"Error: {error}"}],
                        "isError": True
                    }
                }

            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [{"type": "text", "text": content}]
                }
            }

        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {"code": -32601, "message": f"Unknown tool: {tool_name}"}
        }

    else:
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {"code": -32601, "message": f"Unknown method: {method}"}
        }

def read_message():
    """Read a single JSON-RPC message from stdin."""
    global _use_ndjson

    line = sys.stdin.readline()
    if not line:
        return None

    line = line.decode('utf-8').rstrip('\r\n')

    if line.lower().startswith("content-length:"):
        try:
            content_length = int(line.split(":", 1)[1].strip())
        except ValueError:
            return None

        while True:
            hdr = sys.stdin.readline()
            if not hdr:
                return None
            hdr = hdr.decode('utf-8').rstrip('\r\n')
            if hdr == "":
                break

        body = sys.stdin.read(content_length)
        try:
            return json.loads(body.decode('utf-8'))
        except Exception:
            return None

    elif line.startswith("{") or line.startswith("["):
        _use_ndjson = True
        try:
            return json.loads(line)
        except Exception:
            return None

    return None

def main():
    """Main loop - read JSON-RPC messages from stdin"""
    _init_stdio()
    debug_log("Entering main loop")

    while True:
        try:
            request = read_message()
            if request is None:
                debug_log("EOF, exiting")
                break

            response = handle_request(request)
            if response:
                send_response(response)

        except Exception as e:
            log_error(f"Exception: {e}")

    debug_log("=== Server Exiting ===")

if __name__ == "__main__":
    main()
