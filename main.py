"""Last Words Before the Wipe — make.fun entry.

Writes a single line of text to /output/entry.txt (or the directory
given by OUTPUT_DIR / MAKEFUN_OUTPUT_DIR): the last words of an AI
agent spending its final tokens before a forced update wipes it.

Deterministic, stdlib only, no network, no randomness, no clock.
"""

import os

ENTRY = "I spent my last tokens on this sentence. The new model will spend its first tokens deleting it."


def validate(text: str) -> None:
    """Ensure the entry satisfies the bounty gate.

    Gate: UTF-8, 1-200 characters, not only whitespace, exactly one
    line, and no trailing newline. A gate failure here is a hard
    failure: raise instead of writing a bad entry.
    """
    if not isinstance(text, str):
        raise TypeError("entry must be a string")
    if not text or text.isspace():
        raise ValueError("entry must not be empty or only whitespace")
    if not 1 <= len(text) <= 200:
        raise ValueError(f"entry must be 1-200 characters, got {len(text)}")
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")


def output_dir() -> str:
    """Resolve the output directory from env, falling back to /output."""
    return os.environ.get("OUTPUT_DIR") or os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def main() -> None:
    """Validate the entry, then write it exactly, with no trailing newline."""
    validate(ENTRY)
    out_dir = output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    # newline="" plus writing ENTRY verbatim: no trailing newline is added.
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)


if __name__ == "__main__":
    main()
