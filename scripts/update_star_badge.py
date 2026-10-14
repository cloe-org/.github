#!/usr/bin/env python3
"""Update the Shields.io endpoint payload with the organization's public stars."""

import json
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ORG = os.environ.get("GITHUB_ORG", "cloe-org")
TOKEN = os.environ.get("GITHUB_TOKEN")
OUTPUT = Path(os.environ.get("STAR_BADGE_OUTPUT", "badge/star-badge.json"))


def fetch_repositories(page):
    url = f"https://api.github.com/orgs/{ORG}/repos?type=public&per_page=100&page={page}"
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "cloe-org-star-badge"}
    if TOKEN:
        headers["Authorization"] = "Bearer " + TOKEN

    request = Request(url, headers=headers)
    try:
        with urlopen(request) as response:
            return json.load(response)
    except (HTTPError, URLError) as error:
        raise RuntimeError(f"Unable to fetch repositories from GitHub: {error}") from error


def main():
    stars = 0
    page = 1
    while True:
        repositories = fetch_repositories(page)
        if not repositories:
            break
        stars += sum(repository["stargazers_count"] for repository in repositories)
        page += 1

    badge = {
        "schemaVersion": 1,
        "label": "Org stars",
        "message": f"★ {stars}",
        "color": "blue",
    }
    output = json.dumps(badge, indent=2) + "\n"
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    if not OUTPUT.exists() or OUTPUT.read_text() != output:
        OUTPUT.write_text(output)
    print(f"Total stars for {ORG}: {stars}")


if __name__ == "__main__":
    main()
