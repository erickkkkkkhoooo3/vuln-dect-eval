from parse import parse
def test_clean_json():
    r = parse('{"vulnerable": true, "cwe": "CWE-89", "reason": "x"}')
    assert r["vulnerable"] is True
    assert r["cwe"] == "CWE-89"
    assert r["parse_error"] is None


def test_safe_with_null_cwe():
    r = parse('{"vulnerable": false, "cwe": null, "reason": "x"}')
    assert r["vulnerable"] is False
    assert r["cwe"] is None
    assert r["parse_error"] is None


def test_fenced_json_is_accepted():
    r = parse('```json\n{"vulnerable": true, "cwe": "CWE-78", "reason": "x"}\n```')
    assert r["cwe"] == "CWE-78"
    assert r["parse_error"] is None


def test_prose_around_json_is_an_error():
    r = parse('Here is my answer: {"vulnerable": true, "cwe": "CWE-89"}')
    assert r["vulnerable"] is None
    assert r["parse_error"] is not None


def test_string_true_is_an_error():
    r = parse('{"vulnerable": "true", "cwe": "CWE-89"}')
    assert r["parse_error"] is not None


def test_bad_cwe_format_is_an_error():
    r = parse('{"vulnerable": true, "cwe": "SQL injection"}')
    assert r["parse_error"] is not None


def test_empty_reply_is_an_error():
    assert parse("")["parse_error"] is not None


def test_json_list_is_an_error():
    assert parse("[1, 2]")["parse_error"] is not None
