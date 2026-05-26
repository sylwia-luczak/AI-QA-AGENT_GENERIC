#!/usr/bin/env python3
"""
Confluence CLI Tool
===================
Find pages, update content and append test scenarios/evidence
to Confluence Server / Data Center using a Personal Access Token (PAT).

Usage:
    python confluence_tool.py find --space DR "FTRS-3024"
    python confluence_tool.py get 1373940995
    python confluence_tool.py update 1373940995 --file /path/to/content.md
    python confluence_tool.py append 1373940995 --file /path/to/content.md

Configuration:
    Add CONFLUENCE_BASE_URL and CONFLUENCE_PAT to the .env file.
    Never commit .env to version control.
"""

import argparse
import os
import re
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

try:
    import truststore
    truststore.inject_into_ssl()
except ImportError:
    pass

load_dotenv(Path(__file__).parent / ".env")

CONFLUENCE_BASE_URL = os.environ.get("CONFLUENCE_BASE_URL", "").rstrip("/")
CONFLUENCE_PAT = os.environ.get("CONFLUENCE_PAT", "")


def _get_headers() -> dict:
    if not CONFLUENCE_PAT:
        print("ERROR: CONFLUENCE_PAT is not set. Check your .env file.", file=sys.stderr)
        sys.exit(1)
    if not CONFLUENCE_BASE_URL:
        print("ERROR: CONFLUENCE_BASE_URL is not set. Check your .env file.", file=sys.stderr)
        sys.exit(1)
    return {
        "Authorization": f"Bearer {CONFLUENCE_PAT}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def _handle_response(response: requests.Response, action: str) -> None:
    if response.status_code == 401:
        print("ERROR: Unauthorised. Check your CONFLUENCE_PAT.", file=sys.stderr)
        sys.exit(1)
    if response.status_code == 404:
        print(f"ERROR: Page not found.", file=sys.stderr)
        sys.exit(1)
    if not response.ok:
        print(f"ERROR: {action} failed — HTTP {response.status_code}", file=sys.stderr)
        print(response.text[:500], file=sys.stderr)
        sys.exit(1)


# ---------------------------------------------------------------------------
# Markdown → Confluence Storage Format converter
# ---------------------------------------------------------------------------

def _md_to_confluence(md_text: str) -> str:
    """
    Convert Markdown to Confluence storage format (XHTML-based).
    Handles: headings, bold/italic, code blocks (with language), inline code,
    tables, ordered/unordered lists, horizontal rules, paragraphs.
    """
    lines = md_text.splitlines()
    output: list[str] = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Fenced code block
        fence_match = re.match(r"^```(\w*)", line)
        if fence_match:
            lang = fence_match.group(1) or "none"
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                code_lines.append(lines[i])
                i += 1
            code_body = "\n".join(code_lines)
            output.append(
                f'<ac:structured-macro ac:name="code">'
                f'<ac:parameter ac:name="language">{lang}</ac:parameter>'
                f'<ac:parameter ac:name="linenumbers">false</ac:parameter>'
                f'<ac:plain-text-body><![CDATA[{code_body}]]></ac:plain-text-body>'
                f'</ac:structured-macro>'
            )
            i += 1
            continue

        # Heading
        heading_match = re.match(r"^(#{1,6})\s+(.*)", line)
        if heading_match:
            level = len(heading_match.group(1))
            text = _inline(heading_match.group(2))
            if level == 3:
                output.append(f'<h{level}><span style="color: rgb(0,82,204);">{text}</span></h{level}>')
            else:
                output.append(f"<h{level}>{text}</h{level}>")
            i += 1
            continue

        # Horizontal rule
        if re.match(r"^---+$", line.strip()):
            output.append("<hr/>")
            i += 1
            continue

        # Table
        if "|" in line and line.strip().startswith("|"):
            table_lines = []
            while i < len(lines) and "|" in lines[i] and lines[i].strip().startswith("|"):
                table_lines.append(lines[i])
                i += 1
            output.append(_table(table_lines))
            continue

        # Unordered list
        if re.match(r"^[-*]\s+", line):
            items = []
            while i < len(lines) and re.match(r"^[-*]\s+", lines[i]):
                items.append(_inline(re.sub(r"^[-*]\s+", "", lines[i])))
                i += 1
            output.append("<ul>" + "".join(f"<li>{item}</li>" for item in items) + "</ul>")
            continue

        # Ordered list
        if re.match(r"^\d+\.\s+", line):
            items = []
            while i < len(lines) and re.match(r"^\d+\.\s+", lines[i]):
                items.append(_inline(re.sub(r"^\d+\.\s+", "", lines[i])))
                i += 1
            output.append("<ol>" + "".join(f"<li>{item}</li>" for item in items) + "</ol>")
            continue

        # Empty line → skip (paragraphs handled implicitly)
        if not line.strip():
            output.append("")
            i += 1
            continue

        # Normal paragraph line
        output.append(f"<p>{_inline(line)}</p>")
        i += 1

    return "\n".join(output)


def _escape_xhtml(text: str) -> str:
    """Escape special XHTML characters in inline code content."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _inline(text: str) -> str:
    """Convert inline markdown (bold, italic, inline code, links) to storage format."""
    # Protect inline code first by replacing with placeholders, so bold/italic
    # regexes don't match across code spans (which causes invalid XHTML nesting).
    code_spans: list[str] = []

    def _stash_code(m: re.Match) -> str:
        code_spans.append(f"<code>{_escape_xhtml(m.group(1))}</code>")
        return f"\x00CODE{len(code_spans) - 1}\x00"

    text = re.sub(r"`([^`]+)`", _stash_code, text)
    # Bold (process before italic to avoid * ambiguity)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"__(.+?)__", r"<strong>\1</strong>", text)
    # Italic
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    text = re.sub(r"_(.+?)_", r"<em>\1</em>", text)
    # Restore inline code placeholders
    for idx, span in enumerate(code_spans):
        text = text.replace(f"\x00CODE{idx}\x00", span)
    # Links [text](url)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    # Strikethrough
    text = re.sub(r"~~(.+?)~~", r"<del>\1</del>", text)
    return text


def _table(table_lines: list[str]) -> str:
    """Convert markdown table to Confluence storage format."""
    html = ["<table><tbody>"]
    for idx, row in enumerate(table_lines):
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        # Skip separator row (---|---|---)
        if all(re.match(r"^[-: ]+$", c) for c in cells):
            continue
        tag = "th" if idx == 0 else "td"
        html.append("<tr>" + "".join(f"<{tag}>{_inline(c)}</{tag}>" for c in cells) + "</tr>")
    html.append("</tbody></table>")
    return "\n".join(html)


# ---------------------------------------------------------------------------
# API commands
# ---------------------------------------------------------------------------

def find_pages(space_key: str, query: str) -> None:
    """Search for pages in a Confluence space by title."""
    url = f"{CONFLUENCE_BASE_URL}/rest/api/content"
    params = {
        "spaceKey": space_key,
        "title": query,
        "expand": "version,space",
        "limit": 20,
    }
    response = requests.get(url, headers=_get_headers(), params=params, timeout=30)
    _handle_response(response, "Search")

    results = response.json().get("results", [])
    if not results:
        print(f"No pages found in space '{space_key}' matching '{query}'")
        return

    print(f"\nFound {len(results)} page(s) in space '{space_key}':\n")
    for page in results:
        page_id = page["id"]
        title = page["title"]
        version = page.get("version", {}).get("number", "?")
        print(f"  ID: {page_id}  v{version}  {title}")
        print(f"  URL: {CONFLUENCE_BASE_URL}/spaces/{space_key}/pages/{page_id}")
        print()


def get_page(page_id: str) -> None:
    """Display page info and a preview of the current content."""
    url = f"{CONFLUENCE_BASE_URL}/rest/api/content/{page_id}"
    params = {"expand": "body.storage,version,space,ancestors"}
    response = requests.get(url, headers=_get_headers(), params=params, timeout=30)
    _handle_response(response, "Get page")

    data = response.json()
    space = data.get("space", {}).get("key", "?")
    title = data.get("title", "?")
    version = data.get("version", {}).get("number", "?")
    body_preview = data.get("body", {}).get("storage", {}).get("value", "")[:600]

    sep = "=" * 70
    print(sep)
    print(f"  PAGE ID : {page_id}")
    print(f"  Title   : {title}")
    print(f"  Space   : {space}")
    print(f"  Version : {version}")
    print(sep)
    print("\nContent preview (storage format):\n")
    print(body_preview)
    print(f"\n  URL: {CONFLUENCE_BASE_URL}/spaces/{space}/pages/{page_id}")
    print(sep)


def _get_current_version(page_id: str) -> tuple[int, str, str]:
    """Return (version_number, title, space_key) for a page."""
    url = f"{CONFLUENCE_BASE_URL}/rest/api/content/{page_id}"
    response = requests.get(url, headers=_get_headers(), params={"expand": "version,space"}, timeout=30)
    _handle_response(response, "Fetch page metadata")
    data = response.json()
    return (
        data["version"]["number"],
        data["title"],
        data["space"]["key"],
    )


def update_page(page_id: str, md_content: str) -> None:
    """Replace the full page body with converted markdown content."""
    version, title, space = _get_current_version(page_id)
    new_version = version + 1
    storage_body = _md_to_confluence(md_content)

    payload = {
        "version": {"number": new_version},
        "title": title,
        "type": "page",
        "body": {
            "storage": {
                "value": storage_body,
                "representation": "storage",
            }
        },
    }

    url = f"{CONFLUENCE_BASE_URL}/rest/api/content/{page_id}"
    response = requests.put(url, headers=_get_headers(), json=payload, timeout=30)
    _handle_response(response, "Update page")

    print(f"Page updated successfully (v{new_version})")
    print(f"URL: {CONFLUENCE_BASE_URL}/spaces/{space}/pages/{page_id}")


def append_to_page(page_id: str, md_content: str) -> None:
    """Append markdown content to the bottom of an existing page."""
    url = f"{CONFLUENCE_BASE_URL}/rest/api/content/{page_id}"
    response = requests.get(
        url, headers=_get_headers(),
        params={"expand": "body.storage,version,space"},
        timeout=30,
    )
    _handle_response(response, "Fetch page for append")

    data = response.json()
    version = data["version"]["number"]
    title = data["title"]
    space = data["space"]["key"]
    existing_body = data["body"]["storage"]["value"]

    appended_body = _md_to_confluence(md_content)
    new_body = existing_body + "\n" + appended_body

    payload = {
        "version": {"number": version + 1},
        "title": title,
        "type": "page",
        "body": {
            "storage": {
                "value": new_body,
                "representation": "storage",
            }
        },
    }

    resp = requests.put(url, headers=_get_headers(), json=payload, timeout=30)
    _handle_response(resp, "Append to page")

    print(f"Content appended successfully (v{version + 1})")
    print(f"URL: {CONFLUENCE_BASE_URL}/spaces/{space}/pages/{page_id}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Confluence CLI Tool — find pages, update and append content via PAT",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python confluence_tool.py find --space DR "FTRS-3024"
  python confluence_tool.py get 1373940995
  python confluence_tool.py update 1373940995 --file /Users/sylwia/scripts/FTRS-3024_test_plan.md
  python confluence_tool.py append 1373940995 --file /Users/sylwia/scripts/FTRS-3024_evidence.md
        """,
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # find
    find_p = subparsers.add_parser("find", help="Search for pages in a space by title")
    find_p.add_argument("--space", required=True, metavar="SPACE_KEY", help="Confluence space key, e.g. DR")
    find_p.add_argument("query", metavar="QUERY", help="Partial page title to search for")

    # get
    get_p = subparsers.add_parser("get", help="Display page info and content preview")
    get_p.add_argument("page_id", metavar="PAGE_ID", help="Confluence page ID")

    # update
    update_p = subparsers.add_parser("update", help="Replace page content with markdown file")
    update_p.add_argument("page_id", metavar="PAGE_ID", help="Confluence page ID")
    update_p.add_argument("--file", required=True, metavar="FILE", help="Path to markdown file")

    # append
    append_p = subparsers.add_parser("append", help="Append markdown content to an existing page")
    append_p.add_argument("page_id", metavar="PAGE_ID", help="Confluence page ID")
    append_p.add_argument("--file", required=True, metavar="FILE", help="Path to markdown file")

    args = parser.parse_args()

    if args.command == "find":
        find_pages(args.space, args.query)

    elif args.command == "get":
        get_page(args.page_id)

    elif args.command in ("update", "append"):
        md_path = Path(args.file)
        if not md_path.exists():
            print(f"ERROR: File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
        md_content = md_path.read_text(encoding="utf-8")
        if args.command == "update":
            update_page(args.page_id, md_content)
        else:
            append_to_page(args.page_id, md_content)


if __name__ == "__main__":
    main()
