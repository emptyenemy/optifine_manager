import json
import shutil
from pathlib import Path

from modules.installed import (
    build_installation_dir_name,
    get_installed_build_path,
    get_minecraft_root,
    get_optifine_library_dir,
    get_default_versions_dir,
)


def delete_installed_build(build: dict, versions_dir: Path | None = None) -> list[str]:
    versions_dir = versions_dir or get_default_versions_dir()
    logs: list[str] = []
    deleted_version_id = build_installation_dir_name(build)

    logs.append(f"Подготовка удаления версии: {deleted_version_id}")
    logs.append(f"Каталог versions: {versions_dir}")

    build_dir = get_installed_build_path(build, versions_dir)
    if build_dir and build_dir.is_dir():
        logs.append(f"Удаляем папку версии: {build_dir}")
        shutil.rmtree(build_dir)
        logs.append("Папка версии удалена.")
    else:
        logs.append(f"Папка версии не найдена: {versions_dir / deleted_version_id}")

    library_dir = get_optifine_library_dir(build, versions_dir)
    if library_dir.is_dir():
        logs.append(f"Удаляем библиотеку OptiFine: {library_dir}")
        shutil.rmtree(library_dir)
        logs.append("Библиотека OptiFine удалена.")
    else:
        logs.append(f"Библиотека OptiFine не найдена: {library_dir}")

    logs.extend(_cleanup_launcher_profile(build, versions_dir))
    logs.append("Удаление завершено.")
    return logs


def _cleanup_launcher_profile(build: dict, versions_dir: Path) -> list[str]:
    logs: list[str] = []
    launcher_profiles_path = get_minecraft_root(versions_dir) / "launcher_profiles.json"
    if not launcher_profiles_path.is_file():
        logs.append(f"launcher_profiles.json не найден: {launcher_profiles_path}")
        return logs

    logs.append(f"Проверяем launcher_profiles.json: {launcher_profiles_path}")

    with launcher_profiles_path.open("r", encoding="utf-8") as file_obj:
        data = json.load(file_obj)

    deleted_version_id = build_installation_dir_name(build)
    profiles = data.get("profiles", {})
    profiles_to_delete = [
        profile_name
        for profile_name, profile in profiles.items()
        if profile.get("lastVersionId") == deleted_version_id
    ]

    if not profiles_to_delete:
        logs.append("Профили лаунчера для этой версии не найдены.")
    else:
        logs.append(f"Найдено профилей для удаления: {len(profiles_to_delete)}")

    for profile_name in profiles_to_delete:
        logs.append(f"Удаляем профиль лаунчера: {profile_name}")
        profiles.pop(profile_name, None)
        if data.get("selectedProfile") == profile_name:
            data["selectedProfile"] = "latest-release"
            logs.append("Сброшен selectedProfile на latest-release.")

    with launcher_profiles_path.open("w", encoding="utf-8") as file_obj:
        json.dump(data, file_obj, ensure_ascii=False, indent=2)

    logs.append("launcher_profiles.json обновлен.")
    return logs
