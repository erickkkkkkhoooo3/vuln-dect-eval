import json
import re
from pathlib import Path

CASES = json.loads(Path("data/cases.json").read_text(encoding="utf-8"))
REQUIRED = {"id", "language", "code", "vulnerable", "cwe", "source", "notes"}
LEAK = re.compile(r"FLAW|FIX|\bbad\w*|\bgood\w*|CWE|juliet", re.IGNORECASE)


def test_required_fields():
    for case in CASES:
        assert REQUIRED <= case.keys(), case.get("id")


def test_ids_are_unique():
    ids = [case["id"] for case in CASES]
    assert len(ids) == len(set(ids))


def test_labels_are_consistent():
    for case in CASES:
        if case["vulnerable"]:
            assert re.fullmatch(r"CWE-\d+", case["cwe"]), case["id"]
        else:
            assert case["cwe"] is None, case["id"]


def test_no_answer_leaks_in_code():
    for case in CASES:
        match = LEAK.search(case["code"])
        assert match is None, f"{case['id']} contains '{match.group()}'"


def test_roughly_half_safe():
    safe = sum(not case["vulnerable"] for case in CASES)
    assert 0.4 <= safe / len(CASES) <= 0.6


def test_at_least_three_cwes():
    cwes = {case["cwe"] for case in CASES if case["vulnerable"]}
    assert len(cwes) >= 3