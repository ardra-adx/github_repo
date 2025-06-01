# github_repo
A command‑line Python script that inspects any public (or private) GitHub repository and prints a compact report with:

-Repository facts (description, stars, forks, dates)
-Contributors count
-Programming languages used (
-Commits per ISO week (activity timeline)
-Lines‑of‑code (LOC) for common source extensions, or for all text files when --all-ext is used


import
python
PyGitHub
GitHub token (optional but recommended)


#code
python github_repo_analyzer.py <owner>/<repo>

#Functions

get_github_client()-Creates and returns a Github client using a token if available.

fetch_repo(client, full_name)-Fetches the repository object using full repo name (owner/repo).

commits_per_week(repo)-Counts commits per ISO week (e.g., 2023-W10) using commit timestamps.

list_all_contents(repo, path="")-Recursively traverses all files in the repository (rate-limit-friendly).

count_loc(repo, extensions)-Counts total lines of code in the repository based on allowed extensions.

human_date(dt)-Formats a datetime object into a human-readable YYYY-MM-DD format.

print_banner(title)-Helper to display section banners in the console.

main()

-Parses arguments
-Initializes GitHub client
-Fetches repository
-Prints info, contributors, language breakdown, commit stats, and LOC.


















![Screenshot from 2025-05-31 18-40-37](https://github.com/user-attachments/assets/b2dadf41-df22-46de-b49b-8321958c4c5b)
