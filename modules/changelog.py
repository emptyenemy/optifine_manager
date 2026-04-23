from urllib.parse import urljoin

from modules.http_client import fetch_text_sync


def get_changelog_url(build: dict) -> str:
    return urljoin("https://optifine.net/", build["changelog_url"])


def fetch_changelog_lines(build: dict) -> tuple[str, list[str]]:
    changelog_url = get_changelog_url(build)
    text = fetch_text_sync(changelog_url, timeout=30).replace("\r", "")
    lines = [line.rstrip() for line in text.split("\n")]

    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()

    if not lines:
        return changelog_url, ["Changelog пуст."]

    return changelog_url, _extract_single_version_changelog(lines)


def _extract_single_version_changelog(lines: list[str]) -> list[str]:
    selected_lines = []
    seen_header = False

    for line in lines:
        if line.startswith("OptiFine "):
            if seen_header:
                break
            seen_header = True

        if seen_header:
            selected_lines.append(line)

    while selected_lines and not selected_lines[-1].strip():
        selected_lines.pop()

    return selected_lines or lines
