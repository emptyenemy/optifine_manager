from dataclasses import dataclass
from pathlib import Path

from modules.installed import build_installation_dir_name, get_default_versions_dir


@dataclass(slots=True)
class UpdateStatus:
    versions_dir: Path
    latest_build: dict | None
    latest_installed_build: dict | None
    installed_build_names: set[str]

    @property
    def is_latest_installed(self) -> bool:
        if not self.latest_build:
            return False
        return build_installation_dir_name(self.latest_build) in self.installed_build_names

    @property
    def has_updates(self) -> bool:
        return self.latest_build is not None and not self.is_latest_installed


def get_update_status(
    available_builds: list[dict],
    versions_dir: Path | None = None,
) -> UpdateStatus:
    versions_dir = versions_dir or get_default_versions_dir()
    installed_build_names = {
        item.name
        for item in versions_dir.iterdir()
        if item.is_dir()
    } if versions_dir.is_dir() else set()

    latest_build = available_builds[0] if available_builds else None
    latest_installed_build = next(
        (
            build
            for build in available_builds
            if build_installation_dir_name(build) in installed_build_names
        ),
        None,
    )

    return UpdateStatus(
        versions_dir=versions_dir,
        latest_build=latest_build,
        latest_installed_build=latest_installed_build,
        installed_build_names=installed_build_names,
    )
