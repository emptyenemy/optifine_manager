from pathlib import Path
from tempfile import TemporaryDirectory

from modules.app_exit import exit_program
from modules.changelog import fetch_changelog_lines
from modules.console_ui import (
    choose_build,
    flush_input_buffer,
    format_build_label,
    init_console,
    print_error,
    print_info,
    print_section_header,
    print_success,
    print_warning,
    show_update_error,
    view_text,
    wait_for_enter,
    wait_for_retry_or_exit,
)
from modules.delete import delete_installed_build
from modules.direct_download_link import get_direct_download_link
from modules.download import download_file
from modules.installed import (
    get_installed_build_path,
    list_installed_minecraft_versions,
)
from modules.install import install_optifine_jar
from modules.http_client import OptiFineNetworkError
from modules.latest import get_available_builds
from modules.status import get_update_status


def run_once() -> bool:
    installed_minecraft_versions = list_installed_minecraft_versions()
    try:
        available_builds = get_available_builds(installed_minecraft_versions)
    except OptiFineNetworkError as exc:
        show_update_error(str(exc))
        if wait_for_retry_or_exit():
            return True
        flush_input_buffer()
        return exit_program()

    if not available_builds:
        print_error("Не найдено подходящих сборок OptiFine для локально установленных версий Minecraft.")
        wait_for_enter()
        return True

    status = get_update_status(available_builds)
    selection = choose_build(available_builds, status.installed_build_names, status)
    if not selection:
        return exit_program()

    action, selected_build = selection

    if action == 'changelog':
        try:
            changelog_url, changelog_lines = fetch_changelog_lines(selected_build)
        except Exception as e:
            print_error(f"Ошибка при загрузке changelog: {e}")
            wait_for_enter()
            return True

        view_text(
            "Список изменений",
            changelog_lines,
            footer=changelog_url,
        )
        return True

    if action == 'delete':
        print_section_header("Удаление OptiFine")
        print_info("Выбрана версия: " + format_build_label(selected_build))
        try:
            delete_logs = delete_installed_build(selected_build)
        except Exception as e:
            print_error(f"Ошибка при удалении OptiFine: {e}")
            wait_for_enter()
            return True

        for log_line in delete_logs:
            print_info(log_line)
        print_success("Выбранная версия OptiFine удалена.")
        return True

    installed_path = get_installed_build_path(selected_build)
    if installed_path:
        print_section_header("Установка OptiFine")
        print_success(f"Эта версия уже установлена: {installed_path}")
        return True

    print_section_header("Установка OptiFine")
    print_info("Выбрана версия: " + format_build_label(selected_build))

    adload_url = selected_build['mirror_url']
    print_info(f"Получаем прямую ссылку из {adload_url}...")
    try:
        direct_url = get_direct_download_link(adload_url)
    except Exception as e:
        print_error(f"Ошибка при получении прямой ссылки: {e}")
        wait_for_enter()
        return True

    print_info(f"Скачиваем: {direct_url}")
    with TemporaryDirectory(prefix="optifine-manager-") as temp_dir:
        try:
            jar_path = download_file(
                direct_url,
                Path(temp_dir),
                log_callback=print_info,
            )
        except Exception as e:
            print_error(f"Ошибка при скачивании файла: {e}")
            wait_for_enter()
            return True

        print_info(f"Запускаем установку из временного файла: {jar_path}")
        try:
            install_optifine_jar(jar_path)
        except Exception as e:
            print_error(f"Ошибка при установке OptiFine: {e}")
            wait_for_enter()
            return True

    installed_path = get_installed_build_path(selected_build)
    if not installed_path:
        print_error("Установка завершилась без ошибки, но версия не появилась в .minecraft.")
        wait_for_enter()
        return True

    print_success("OptiFine установлен. Временный .jar удален.")
    return True


def main():
    init_console()

    while run_once():
        pass


if __name__ == '__main__':
    main()
