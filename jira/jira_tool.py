#!/usr/bin/env python3
"""
Jira CLI Tool
=============
Fetch ticket details and post comments to Jira Server / Data Center
using a Personal Access Token (PAT).

Usage:
    python jira_tool.py fetch FTRS-1234
    python jira_tool.py comment FTRS-1234 "Your comment text here"
    python jira_tool.py comment FTRS-1234 --file path/to/comment.md

Configuration:
    Copy .env.example to .env and fill in your values.
    Never commit .env to version control.
"""

import argparse
import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

try:
    import truststore
    truststore.inject_into_ssl()  # Use macOS/system native trust store
except ImportError:
    pass

# Load .env from the same directory as this script
load_dotenv(Path(__file__).parent / ".env")

JIRA_BASE_URL = os.environ.get("JIRA_BASE_URL", "").rstrip("/")
JIRA_PAT = os.environ.get("JIRA_PAT", "")

FIELDS = "summary,description,status,issuetype,priority,assignee,reporter,labels,comment,subtasks,issuelinks,fixVersions,customfield_10016"


def _get_headers() -> dict:
    if not JIRA_PAT:
        print("ERROR: JIRA_PAT is not set. Check your .env file.", file=sys.stderr)
        sys.exit(1)
    if not JIRA_BASE_URL:
        print("ERROR: JIRA_BASE_URL is not set. Check your .env file.", file=sys.stderr)
        sys.exit(1)
    return {
        "Authorization": f"Bearer {JIRA_PAT}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def _get_ssl_verify() -> bool | str:
    """Use REQUESTS_CA_BUNDLE if explicitly set, otherwise let truststore handle it."""
    cert_path = os.environ.get("REQUESTS_CA_BUNDLE")
    if cert_path and Path(cert_path).exists():
        return cert_path
    return True


def fetch_ticket(ticket_id: str) -> None:
    """Fetch and display full ticket details including all comments."""
    url = f"{JIRA_BASE_URL}/rest/api/2/issue/{ticket_id}"
    params = {"fields": FIELDS}

    response = requests.get(
        url,
        headers=_get_headers(),
        params=params,
        verify=_get_ssl_verify(),
        timeout=30,
    )

    if response.status_code == 404:
        print(f"ERROR: Ticket {ticket_id} not found.", file=sys.stderr)
        sys.exit(1)
    if response.status_code == 401:
        print("ERROR: Unauthorised. Check your JIRA_PAT.", file=sys.stderr)
        sys.exit(1)
    response.raise_for_status()

    data = response.json()
    fields = data.get("fields", {})

    _print_ticket(ticket_id, fields)


def _print_ticket(ticket_id: str, fields: dict) -> None:
    separator = "=" * 70

    print(separator)
    print(f"  TICKET: {ticket_id}")
    print(separator)
    print(f"  Title    : {fields.get('summary', 'N/A')}")
    print(f"  Type     : {_nested(fields, 'issuetype', 'name')}")
    print(f"  Status   : {_nested(fields, 'status', 'name')}")
    print(f"  Priority : {_nested(fields, 'priority', 'name')}")
    print(f"  Assignee : {_nested(fields, 'assignee', 'displayName') or 'Unassigned'}")
    print(f"  Reporter : {_nested(fields, 'reporter', 'displayName')}")

    labels = fields.get("labels", [])
    if labels:
        print(f"  Labels   : {', '.join(labels)}")

    print()
    print("--- DESCRIPTION " + "-" * 54)
    description = fields.get("description") or "(no description)"
    print(description)

    # Subtasks
    subtasks = fields.get("subtasks", [])
    if subtasks:
        print()
        print("--- SUBTASKS " + "-" * 57)
        for sub in subtasks:
            status = _nested(sub, "fields", "status", "name")
            print(f"  [{status}]  {sub.get('key')} — {_nested(sub, 'fields', 'summary')}")

    # Linked issues
    links = fields.get("issuelinks", [])
    if links:
        print()
        print("--- LINKED ISSUES " + "-" * 52)
        for link in links:
            link_type = _nested(link, "type", "name")
            if "outwardIssue" in link:
                issue = link["outwardIssue"]
                direction = _nested(link, "type", "outward")
            else:
                issue = link.get("inwardIssue", {})
                direction = _nested(link, "type", "inward")
            key = issue.get("key", "?")
            summary = _nested(issue, "fields", "summary")
            status = _nested(issue, "fields", "status", "name")
            print(f"  {link_type} ({direction}): [{status}] {key} — {summary}")

    # Comments
    comments = fields.get("comment", {}).get("comments", [])
    if comments:
        print()
        print("--- COMMENTS " + "-" * 57)
        for i, comment in enumerate(comments, 1):
            author = _nested(comment, "author", "displayName")
            created = comment.get("created", "")[:10]
            body = comment.get("body", "")
            comment_id = comment.get("id", "?")
            print(f"\n  [{i}] id:{comment_id}  {author} \u2014 {created}")
            print(f"  {body}")
    else:
        print()
        print("--- COMMENTS (none) " + "-" * 50)

    print()
    print(separator)
    print(f"  URL: {JIRA_BASE_URL}/browse/{ticket_id}")
    print(separator)


def _nested(obj: dict, *keys: str) -> str:
    """Safely traverse nested dict keys."""
    for key in keys:
        if not isinstance(obj, dict):
            return "N/A"
        obj = obj.get(key, {})
    return obj if isinstance(obj, str) else "N/A"


def edit_comment(ticket_id: str, comment_id: str, comment_text: str) -> None:
    """Edit an existing comment on a Jira ticket."""
    url = f"{JIRA_BASE_URL}/rest/api/2/issue/{ticket_id}/comment/{comment_id}"
    payload = {"body": comment_text}

    response = requests.put(
        url,
        headers=_get_headers(),
        json=payload,
        verify=_get_ssl_verify(),
        timeout=30,
    )

    if response.status_code == 404:
        print(f"ERROR: Comment {comment_id} not found on {ticket_id}.", file=sys.stderr)
        sys.exit(1)
    if response.status_code == 401:
        print("ERROR: Unauthorised. Check your JIRA_PAT.", file=sys.stderr)
        sys.exit(1)
    response.raise_for_status()

    print(f"Comment {comment_id} updated successfully.")
    print(f"View: {JIRA_BASE_URL}/browse/{ticket_id}")


def post_comment(ticket_id: str, comment_text: str) -> None:
    """Post a comment to a Jira ticket."""
    url = f"{JIRA_BASE_URL}/rest/api/2/issue/{ticket_id}/comment"
    payload = {"body": comment_text}

    response = requests.post(
        url,
        headers=_get_headers(),
        json=payload,
        verify=_get_ssl_verify(),
        timeout=30,
    )

    if response.status_code == 404:
        print(f"ERROR: Ticket {ticket_id} not found.", file=sys.stderr)
        sys.exit(1)
    if response.status_code == 401:
        print("ERROR: Unauthorised. Check your JIRA_PAT.", file=sys.stderr)
        sys.exit(1)
    response.raise_for_status()

    comment_id = response.json().get("id")
    print(f"Comment posted successfully (id: {comment_id})")
    print(f"View: {JIRA_BASE_URL}/browse/{ticket_id}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Jira CLI Tool — fetch tickets and post comments via PAT",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python jira_tool.py fetch FTRS-1234
  python jira_tool.py comment FTRS-1234 "Testing completed. All scenarios passed."
  python jira_tool.py comment FTRS-1234 --file /Users/sylwia/scripts/FTRS-1234_comment.md
  python jira_tool.py edit FTRS-1234 123456 --file /Users/sylwia/scripts/FTRS-1234_comment.md
        """,
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # fetch subcommand
    fetch_parser = subparsers.add_parser("fetch", help="Fetch and display ticket details")
    fetch_parser.add_argument("ticket_id", metavar="TICKET", help="Jira ticket ID, e.g. FTRS-1234")

    # edit subcommand
    edit_parser = subparsers.add_parser("edit", help="Edit an existing comment on a ticket")
    edit_parser.add_argument("ticket_id", metavar="TICKET", help="Jira ticket ID, e.g. FTRS-1234")
    edit_parser.add_argument("comment_id", metavar="COMMENT_ID", help="Jira comment ID (shown in fetch output)")
    edit_group = edit_parser.add_mutually_exclusive_group(required=True)
    edit_group.add_argument("text", nargs="?", metavar="TEXT", help="New comment text (inline)")
    edit_group.add_argument("--file", metavar="FILE", help="Path to a file containing the new comment text")

    # comment subcommand
    comment_parser = subparsers.add_parser("comment", help="Post a comment to a ticket")
    comment_parser.add_argument("ticket_id", metavar="TICKET", help="Jira ticket ID, e.g. FTRS-1234")
    comment_group = comment_parser.add_mutually_exclusive_group(required=True)
    comment_group.add_argument("text", nargs="?", metavar="TEXT", help="Comment text (inline)")
    comment_group.add_argument("--file", metavar="FILE", help="Path to a file containing the comment text")

    args = parser.parse_args()

    if args.command == "fetch":
        fetch_ticket(args.ticket_id)

    elif args.command == "edit":
        if args.file:
            comment_path = Path(args.file)
            if not comment_path.exists():
                print(f"ERROR: File not found: {args.file}", file=sys.stderr)
                sys.exit(1)
            comment_text = comment_path.read_text(encoding="utf-8")
        else:
            comment_text = args.text

        if not comment_text or not comment_text.strip():
            print("ERROR: Comment text is empty.", file=sys.stderr)
            sys.exit(1)

        edit_comment(args.ticket_id, args.comment_id, comment_text)

    elif args.command == "comment":
        if args.file:
            comment_path = Path(args.file)
            if not comment_path.exists():
                print(f"ERROR: File not found: {args.file}", file=sys.stderr)
                sys.exit(1)
            comment_text = comment_path.read_text(encoding="utf-8")
        else:
            comment_text = args.text

        if not comment_text or not comment_text.strip():
            print("ERROR: Comment text is empty.", file=sys.stderr)
            sys.exit(1)

        post_comment(args.ticket_id, comment_text)


if __name__ == "__main__":
    main()
