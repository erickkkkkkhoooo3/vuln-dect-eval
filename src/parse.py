"""
Turn a model's raw reply into readable, structured text.
"""

import json
import re

CWE_PATTERN = re.compile(r"^CWE-\d+$")
FENCE_PATTERN = re.compile(r"^```(?:json)?\s*(.*?)\s*```$", re.DOTALL)

def parse(raw:str) -> dict:
    result = {"vulnerable": None, "cwe" : None, "reason": None, "parse_error": None}
    text = raw.strip()
    fenced = FENCE_PATTERN.match(text)
    if fenced:
        text = fenced.group(1)

    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        result["parse_error"] = f"INVALID JSON: {e.msg}"
        return result

    if not isinstance(data, dict):
        result["parse_error"] = "JSON is NOT an object."
        return result

    vulnerable = data.get("vulnerable")
    if not isinstance(vulnerable, bool):
        result["parse_error"] = "'vulnerable' is missing or not 'true/false'"
        return result

    cwe = data.get("cwe")
    if cwe is not None and not (isinstance(cwe, str) and CWE_PATTERN.match(cwe)):
        result["parse_error"] = f"'cwe' not in CWE-<number> form: {cwe!r}"
        return result

    result["vulnerable"] = vulnerable
    result["cwe"] = cwe
    result["reason"] = data.get("reason")
    return result

if __name__ == "__main__":
    from pathlib import Path
    from client import ask

    template = Path("prompts/v1.txt").read_text(encoding="utf-8")
    snippet = '''
    String query = "SELECT * FROM users WHERE name = '" + userName + "'";
    Statement stmt = conn.createStatement();
    ResultSet rs = stmt.executeQuery(query);
    '''

    raw = ask(template.replace("{{CODE}}", snippet))
    print("RAW:", raw)
    print("PARSED:", parse(raw))

