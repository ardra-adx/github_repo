#!/usr/bin/env python3
"""
GitHub Repository Analyzer
--------------------------------
  • Counts total lines of code (selected extensions or *all* text files)
  • Lists languages used (bytes & %)
  • Reports contributor count
  • Aggregates commits per ISO week
  • Prints basic repository facts

Usage
-----
$ pip install PyGithub
$ export GITHUB_TOKEN=<your‑token>           # optional but recommended
$ python github_repo_analyzer.py tensorflow/tensorflow
"""

import argparse
import base64
import os
import sys
from collections import defaultdict
from datetime import datetime, timezone

from github import Github, GithubException

# ---------- configurable -------------
DEFAULT_EXTENSIONS = {
    ".py", ".js", ".ts", ".java", ".c", ".cpp",
    ".go", ".rb", ".rs", ".php", ".html", ".css",
}


def get_github_client():
    token = os.getenv("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")
    return Github(token) if token else Github()


def fetch_repo(client, full_name: str):
    try:
        return client.get_repo(full_name)
    except GithubException as err:
        sys.exit(f"Could not fetch '{full_name}': {err}")


# ---------- commits per week ----------
def commits_per_week(repo):
    """Return dict {'YYYY-Www': count} using ISO calendar weeks."""
    counts = defaultdict(int)
    try:
        for commit in repo.get_commits():
            dt = commit.commit.author.date.replace(tzinfo=timezone.utc)
            year, week, _ = dt.isocalendar()
            key = f"{year}-W{week:02}"
            counts[key] += 1
    except GithubException as err:
        print(f"Commit history truncated: {err}")
    return dict(counts)


# ---------- lines of code -------------
def list_all_contents(repo, path=""):
    """Breadth‑first traversal of the Contents API (rate‑limit‑friendly)."""
    queue, files = [path], []
    while queue:
        current = queue.pop(0)
        for item in repo.get_contents(current):
            if item.type == "dir":
                queue.append(item.path)
            else:
                files.append(item)
    return files


def count_loc(repo, extensions=DEFAULT_EXTENSIONS):
    total = 0
    for file in list_all_contents(repo):
        if extensions and not any(file.name.endswith(ext) for ext in extensions):
            continue
        try:
            data = base64.b64decode(file.content)
            total += len(data.splitlines())
        except Exception:
            continue  # skip binary or decoding failures
    return total


# ---------- pretty printing -----------
def human_date(dt):
    return dt.strftime("%Y-%m-%d")


def print_banner(title):
    print(f"\n{title}")
    print("-" * len(title))


def main():
    parser = argparse.ArgumentParser(description="Analyze a public GitHub repository.")
    parser.add_argument("repo", help="Repository in owner/name format")
    parser.add_argument(
        "--all-ext",
        action="store_true",
        help="Count LOC for every file GitHub flags as text (ignore extension filter)",
    )
    args = parser.parse_args()

    gh = get_github_client()
    repo = fetch_repo(gh, args.repo)

    # ----- basic facts -----
    print_banner(" Repository Info")
    print(f"Name           : {repo.full_name}")
    print(f"Description    : {repo.description or '—'}")
    print(f"Default branch : {repo.default_branch}")
    print(f"Created        : {human_date(repo.created_at)}")
    print(f"Stars        : {repo.stargazers_count}")
    print(f"Forks        : {repo.forks_count}")

    # ----- contributors -----
    try:
        contributors = repo.get_contributors().totalCount
    except GithubException:
        contributors = "Unavailable"
    print(f"👥 Contributors : {contributors}")

    # ----- languages -----
    print_banner("Languages Used")
    try:
        langs = repo.get_languages()
        total_bytes = sum(langs.values())
        for lang, size in sorted(langs.items(), key=lambda x: x[1], reverse=True):
            pct = 100 * size / total_bytes if total_bytes else 0
            print(f"{lang:<15} {size:>10} bytes  ({pct:5.2f}%)")
    except GithubException as err:
        print(f" {err}")

    # ----- commits per week -----
    print_banner(" Commits per ISO Week")
    weekly = commits_per_week(repo)
    for week in sorted(weekly):
        print(f"{week}: {weekly[week]}")

    # ----- lines of code -----
    print_banner(" Lines of Code")
    ext_filter = set() if args.all_ext else DEFAULT_EXTENSIONS
    loc = count_loc(repo, ext_filter)
    ext_note = "all file types" if args.all_ext else "selected extensions"
    print(f"Total LOC ({ext_note}): {loc}")

    print("\n Analysis complete!")


if __name__ == "__main__":
    main()
