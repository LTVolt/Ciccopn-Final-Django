import argparse
from pathlib import Path
import re

# We only touch SQL string literals, preserving SQL structure.
SQL_STRING_RE = re.compile(r"'((?:[^'\\]|\\.|'')*)'")

MOJIBAKE_MARKERS = (
    "├",
    "┬",
    "Ã",
    "Â",
    "╟",
    "╣",
    "╜",
)


def maybe_fix_literal(text: str) -> str:
    if not any(marker in text for marker in MOJIBAKE_MARKERS):
        return text

    # SQL escaped apostrophes are doubled: ''
    sql_unescaped = text.replace("''", "'")

    try:
        fixed = sql_unescaped.encode("cp850").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return text

    # Restore SQL apostrophe escaping
    return fixed.replace("'", "''")


def fix_sql_dump(content: str) -> tuple[str, int]:
    fixed_count = 0

    def repl(match: re.Match) -> str:
        nonlocal fixed_count
        inner = match.group(1)
        fixed_inner = maybe_fix_literal(inner)
        if fixed_inner != inner:
            fixed_count += 1
        return f"'{fixed_inner}'"

    fixed_content = SQL_STRING_RE.sub(repl, content)
    return fixed_content, fixed_count


def read_sql_text(path: Path) -> str:
    raw = path.read_bytes()

    # UTF-16 LE with BOM (common when redirecting native output in Windows PowerShell)
    if raw.startswith(b"\xff\xfe"):
        return raw.decode("utf-16")

    # UTF-8 with BOM
    if raw.startswith(b"\xef\xbb\xbf"):
        return raw.decode("utf-8-sig")

    # Fallback UTF-8
    return raw.decode("utf-8", errors="replace")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fix mojibake accents in MySQL dump generated/imported with wrong DOS codepage handling."
    )
    parser.add_argument("input", help="Path to input SQL dump")
    parser.add_argument("output", help="Path to output fixed SQL dump")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    content = read_sql_text(input_path)
    fixed_content, fixed_count = fix_sql_dump(content)
    output_path.write_text(fixed_content, encoding="utf-8", newline="\n")

    print(f"Done. Literals fixed: {fixed_count}")
    print(f"Output file: {output_path}")


if __name__ == "__main__":
    main()
