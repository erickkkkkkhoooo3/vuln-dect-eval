"""
Builds cases.json from data/manifest.json and data/snippets
Do not edit cases.json by hand, edit only manifest.json
"""

import json
from pathlib import Path

DATA = Path("data")

def main():
    manifest = json.loads((DATA/"manifest.json").read_text(encoding="utf-8"))

    cases = []
    for entry in manifest:
        code = (DATA /entry["file"]).read_text(encoding="utf-8")
        case = {key: value for key, value in entry.items() if key != "file"}

        case["code"] = code
        cases.append(case)

        out = DATA/"cases.json"
        out.write_text(json.dumps(cases, indent=2), encoding="utf-8")

        print(f"Wrote {len(cases)} cases to {out}")


if __name__ == "__main__":
    main()
