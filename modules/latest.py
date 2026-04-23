from datetime import datetime

from modules.installed import normalize_minecraft_version
from modules.optifine import parse_optifine_versions


def parse_build_date(build: dict) -> datetime:
    return datetime.strptime(build['date'], "%d.%m.%Y")


def _annotate_build(build: dict, minecraft_version: str, release_type: str) -> dict:
    annotated = build.copy()
    annotated['minecraft_version'] = minecraft_version
    annotated['release_type'] = release_type
    return annotated


def _pick_best_build(section: dict) -> dict | None:
    minecraft_version = section['minecraft_version']
    release_builds = [
        _annotate_build(build, minecraft_version, 'release')
        for build in section['main']
    ]
    if release_builds:
        return max(release_builds, key=parse_build_date)

    preview_builds = [
        _annotate_build(build, minecraft_version, 'preview')
        for build in section['previews']
    ]
    if preview_builds:
        return max(preview_builds, key=parse_build_date)

    return None


def get_available_builds(installed_minecraft_versions: set[str] | None = None) -> list[dict]:
    versions = parse_optifine_versions()
    builds = []

    for section in versions:
        normalized_version = normalize_minecraft_version(section['minecraft_version'])
        if installed_minecraft_versions is not None and normalized_version not in installed_minecraft_versions:
            continue

        best_build = _pick_best_build(section)
        if best_build:
            builds.append(best_build)

    builds.sort(key=parse_build_date, reverse=True)
    return builds


def get_latest_build() -> dict | None:
    builds = get_available_builds()
    if not builds:
        return None
    return builds[0]
