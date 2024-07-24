"""
This module provides a command-line interface to list repositories in a GitHub organization.

It uses the GitHub API to fetch repository information, including the name, URL, owner, and size of each repository.
The user can provide a GitHub token and organization name as arguments. If not provided, the script will attempt to read them from environment variables.
The user can also provide a regular expression pattern to filter the repositories by their URLs.
The script can output either the full list of repositories or the filtered list, depending on the arguments provided.

Usage:
    python repos.py --token <token> --org <org> --pattern <pattern> --full
    python repos.py --token <token> --org <org> --pattern <pattern> --filtered

Arguments:
    --token: The GitHub token.
    --org: The GitHub organization.
    --pattern: The pattern to match repository URLs.
    --full: Print the full list of repositories.
    --filtered: Print the filtered list of repositories.

Environment Variables:
    GITHUB_ADMIN_TOKEN: The GitHub token.
"""

import argparse
import os
import re

from github import Github
from prettytable import PrettyTable
from termcolor import colored

# Create the parser
parser = argparse.ArgumentParser(
    description="List repositories in a GitHub organization"
)

# Add the arguments
parser.add_argument("--token", type=str, help="The GitHub token")
parser.add_argument("--org", type=str, help="The GitHub organization")
parser.add_argument("--pattern", type=str, help="The pattern to match repository URLs")
parser.add_argument(
    "--full", action="store_true", help="Print the full list of repositories"
)
parser.add_argument(
    "--filtered", action="store_true", help="Print the filtered list of repositories"
)

# Parse the arguments
args = parser.parse_args()

# Read the GitHub token from an environment variable if not provided as an argument
token = args.token if args.token else os.getenv("GITHUB_ADMIN_TOKEN")

# Create a Github instance using the token
g = Github(token)

# Get the organization
org = g.get_organization(args.org if args.org else "cprime-talent")

# Get all repos in the organization
repos = org.get_repos()

# Define the pattern for the repository URLs
pattern = args.pattern if args.pattern else r".*"

# Convert repos to a list of dictionaries so it can be output as JSON
repos_full_list = [
    {
        "name": repo.name,
        "url": repo.html_url,
        "owner": repo.owner.login,
        "size": repo.size,
    }
    for repo in repos
]

# Convert repos to a list of dictionaries so it can be output as JSON
# and filter the list to only include repos that match the pattern
repos_filtered_list = [
    {
        "name": repo.name,
        "url": repo.html_url,
        "owner": repo.owner.login,
        "size": repo.size,
    }
    for repo in repos
    if re.match(pattern, repo.html_url)
]


def display_table(repos_list: list[dict], title: str):
    """
    Display a table of repositories.

    Args:
        repos_list: A list of dictionaries containing repository information.
        title: The title of the table.
    """
    table = PrettyTable()
    table.field_names = ["Name", "URL", "Owner", "Size"]
    table.align = "l"  # Align columns to the left
    repos_list = sorted(repos_list, key=lambda x: x["name"])
    for repo in repos_list:
        table.add_row([repo["name"], repo["url"], repo["owner"], repo["size"]])
    print(f"\n{title}")
    print(colored(str(table), "green"))
    print("\n")


# Print the full list of repositories if the --full argument is provided
if args.full:
    display_table(repos_full_list, "Full list of repositories:")

# Print the filtered list of repositories if the --filtered argument is provided
if args.filtered:
    display_table(repos_filtered_list, "Filtered list of repositories:")
