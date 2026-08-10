"""Load the REAL mcp-servers/llm-chat/server.py for tests.

Historically this file carried a hand-maintained copy of the server logic
because importing the server rebound stdio at module level. The server has
since deferred that into _init_stdio() (called from main() only), so importing
it is side-effect free — the copy was removed to restore a single source of
truth. Patch targets like ``tests._llm_chat_helpers.API_KEY`` resolve to the
real server module via the sys.modules replacement below.
"""

import importlib.util
import sys
from pathlib import Path

_SERVER_PATH = Path(__file__).resolve().parent.parent / "mcp-servers" / "llm-chat" / "server.py"
_spec = importlib.util.spec_from_file_location(__name__, _SERVER_PATH)
_module = importlib.util.module_from_spec(_spec)
sys.modules[__name__] = _module
_spec.loader.exec_module(_module)
