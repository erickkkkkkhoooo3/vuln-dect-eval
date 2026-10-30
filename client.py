"""
Thin wrapper around the Anthropic API.
Exposes one function, ask(),
which sends a prompt and returns the raw text reply; parsing happens in parse.py. 
Enforces a per-run call budget (MAX_CALLS) as a guard against runaway loops.
"""

import os
from dotenv import load_dotenv
from anthropic import Anthropic 

load_dotenv()

MAX_CALLS = int(os.environ.get("MAX_CALLS", 50))

_calls_made = 0

class CallBudgetExceeded(Exception):
    pass

_client = Anthropic(
    api_key=os.environ["ANTHROPIC_API_KEY"],
    max_retries = 2,
    timeout = 30,
)

def ask(prompt: str, model: str = "claude-sonnet-5-5") -> str: 
    """Send one prompt, return the model's raw text reply."""
    global _calls_made
    if _calls_made >= MAX_CALLS:
        raise CallBudgetExceeded(f"Hit MAX_CALLS={MAX_CALLS}; stopping.")
    _calls_made += 1

    response = _client.messages.create(
    model = model,
    max_tokens = 1024,
    messages = [{"role": "user", "content" : prompt}],
    )

    return response.content[0].text

if __name__ == "__main__":
    snippet = '''
String query = "SELECT * FROM users WHERE name = '" + userName + "'";
...
'''
print(ask(f"Is this Java code vulnerable? If so, what CWE?\n\n{snippet}\n"))

