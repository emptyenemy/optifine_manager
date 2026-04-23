import os
import re
from pathlib import Path


def get_default_versions_dir() -> Path:
    appdata = os.environ.get('APPDATA')
    if appdata:
        return Path(appdata) / '.minecraft' / 'versions'

    return Path.home() / 'AppData' / 'Roaming' / '.minecraft' / 'versions'


def normalize_minecraft_version(version_name: str) -> str:
    return version_name.removeprefix("Minecraft ").strip()


def build_optifine_suffix(build_name: str) -> str:
    return build_name.strip().replace(" ", "_")


def build_installation_dir_name(build: dict) -> str:
    minecraft_version = normalize_minecraft_version(build['minecraft_version'])
    optifine_suffix = build_optifine_suffix(build['file'])
    return f"{minecraft_version}-{optifine_suffix}"


def build_optifine_edition(build_name: str) -> str:
    return build_name.removeprefix("OptiFine ").strip().replace(" ", "_")


def build_library_version(build: dict) -> str:
    minecraft_version = normalize_minecraft_version(build['minecraft_version'])
    edition = build_optifine_edition(build['file'])
    return f"{minecraft_version}_{edition}"


def get_installed_build_path(build: dict, versions_dir: Path | None = None) -> Path | None:
    versions_dir = versions_dir or get_default_versions_dir()
    build_dir = versions_dir / build_installation_dir_name(build)
    if build_dir.is_dir():
        return build_dir
    return None


def get_minecraft_root(versions_dir: Path | None = None) -> Path:
    versions_dir = versions_dir or get_default_versions_dir()
    return versions_dir.parent


def get_optifine_library_dir(build: dict, versions_dir: Path | None = None) -> Path:
    minecraft_root = get_minecraft_root(versions_dir)
    library_version = build_library_version(build)
    return minecraft_root / "libraries" / "optifine" / "OptiFine" / library_version


def list_installed_minecraft_versions(versions_dir: Path | None = None) -> set[str]:
    versions_dir = versions_dir or get_default_versions_dir()
    if not versions_dir.is_dir():
        return set()

    installed_versions = set()

    for item in versions_dir.iterdir():
        if not item.is_dir():
            continue

        if "-OptiFine_" in item.name:
            continue

        version_json = item / f"{item.name}.json"
        if version_json.is_file():
            installed_versions.add(item.name)

    return installed_versions


def list_installed_optifine_builds(versions_dir: Path | None = None) -> list[dict]:
    versions_dir = versions_dir or get_default_versions_dir()
    if not versions_dir.is_dir():
        return []

    pattern = re.compile(r'^(?P<minecraft_version>[^-]+)-(?P<file>OptiFine_.+)$')
    installed_builds = []

    for item in versions_dir.iterdir():
        if not item.is_dir():
            continue

        match = pattern.match(item.name)
        if not match:
            continue

        installed_builds.append({
            'minecraft_version': match.group('minecraft_version'),
            'file': match.group('file').replace('_', ' '),
            'path': item,
        })

    return installed_builds
