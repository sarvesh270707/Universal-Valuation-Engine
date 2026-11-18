import os
import re
import pytest

SECRET_PATTERNS = [
    (r"(?i)api[_-]?key\s*[:=]\s*['\"]([a-zA-Z0-9_\-]{16,})['\"]", "API Key"),
    (r"(?i)secret\s*[:=]\s*['\"]([a-zA-Z0-9_\-]{16,})['\"]", "Secret"),
    (r"ghp_[a-zA-Z0-9]{36}", "GitHub Token")
]

def test_no_hardcoded_secrets():
    flagged = []
    for root, dirs, files in os.walk("."):
        if ".git" in root or "tests" in root:
            continue
        for f in files:
            if f.endswith((".py", ".json", ".md", ".csv", ".txt")):
                p = os.path.join(root, f)
                try:
                    with open(p, "r", encoding="utf-8", errors="ignore") as fl:
                        content = fl.read()
                        for pat, lbl in SECRET_PATTERNS:
                            matches = re.findall(pat, content)
                            for m in matches:
                                if "example" not in str(m).lower() and "your_api_key" not in str(m).lower():
                                    flagged.append((p, lbl))
                except:
                    pass
    assert len(flagged) == 0, f"Found hardcoded secrets: {flagged}"

def test_no_sensitive_files_committed():
    forbidden_files = [".env", "id_rsa", "credentials.json", "secret.key"]
    found = []
    for root, dirs, files in os.walk("."):
        if ".git" in root:
            continue
        for f in files:
            if f in forbidden_files:
                found.append(os.path.join(root, f))
    assert len(found) == 0, f"Forbidden sensitive files found: {found}"
