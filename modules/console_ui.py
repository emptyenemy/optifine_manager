import os
import time
from colorama import Fore, Style, init
from pyfiglet import Figlet

from modules.installed import build_installation_dir_name

WINDOW_SIZE = 12
FIGLET = Figlet()
VERSION_LINE = "v1.00 by @emptyenemy"
BANNER_LINES = (
    FIGLET.renderText("OptiFine").rstrip().splitlines()
    + FIGLET.renderText("Manager").rstrip().splitlines()
)


def init_console() -> None:
    init(autoreset=True)


def print_banner() -> None:
    for line in BANNER_LINES:
        print(Fore.BLUE + Style.BRIGHT + line)

    print(Style.DIM + VERSION_LINE)
    print("")


def format_build_label(build: dict) -> str:
    minecraft_version = build['minecraft_version'].removeprefix("Minecraft ").strip()
    release_type = 'preview' if build['release_type'] == 'preview' else 'release'
    return f"{minecraft_version} | {build['file']} | {release_type} | {build['date']}"


def print_error(message: str) -> None:
    print(Fore.RED + message)


def print_success(message: str) -> None:
    print(Fore.GREEN + message)


def print_warning(message: str) -> None:
    print(Fore.YELLOW + message)


def print_info(message: str) -> None:
    print(message)


def print_section_header(title: str) -> None:
    print(Fore.BLUE + Style.BRIGHT + title)


def view_text(title: str, lines: list[str], footer: str | None = None) -> None:
    import msvcrt

    _clear_console()
    print(Fore.BLUE + Style.BRIGHT + title)
    if footer:
        print(Style.DIM + footer)
    print("")

    for line in lines:
        print(line)

    print("")
    print(Style.DIM + "Esc — назад")

    while True:
        key = msvcrt.getwch()
        if key in ("\x00", "\xe0"):
            msvcrt.getwch()
            continue
        if key == "\x1b":
            return


def wait_for_enter(prompt: str = "Нажмите Enter, чтобы продолжить...") -> None:
    print("")
    input(prompt)
    flush_input_buffer()


def print_update_status(status) -> None:
    if not status.latest_build:
        print_error("Не удалось получить список версий OptiFine.")
        return

    print(Fore.BLUE + Style.BRIGHT + "Проверка обновлений")

    if status.is_latest_installed:
        print_success("У вас установлена последняя версия!")
        return

    if status.latest_installed_build:
        print_warning("Доступна новая версия OptiFine!")
        return

    print(Fore.YELLOW + "Не удалось найти установленный OptiFine.")


def show_update_error(message: str) -> None:
    _clear_console()
    print_banner()
    print(Fore.BLUE + Style.BRIGHT + "Проверка обновлений")
    print_error(message)
    print("")
    print(Style.DIM + "Enter — повторить, Esc — выход")


def wait_for_retry_or_exit() -> bool:
    import msvcrt

    flush_input_buffer()

    while True:
        key = msvcrt.getwch()
        if key in ("\x00", "\xe0"):
            msvcrt.getwch()
            continue
        if key in ("\r", "\n"):
            flush_input_buffer()
            return True
        if key == "\x1b":
            flush_input_buffer()
            return False


def choose_build(
    builds: list[dict],
    installed_build_names: set[str],
    status=None,
) -> tuple[str, dict] | None:
    if not builds:
        return None

    selected_index = 0
    flush_input_buffer()

    while True:
        _render_build_selector(builds, selected_index, installed_build_names, status)
        action = _read_action()

        if action == 'up':
            selected_index = max(0, selected_index - 1)
        elif action == 'down':
            selected_index = min(len(builds) - 1, selected_index + 1)
        elif action == 'enter':
            _clear_console()
            return 'install', builds[selected_index]
        elif action == 'delete':
            selected_build = builds[selected_index]
            if build_installation_dir_name(selected_build) not in installed_build_names:
                continue
            _clear_console()
            return 'delete', selected_build
        elif action == 'changelog':
            _clear_console()
            return 'changelog', builds[selected_index]
        elif action == 'quit':
            _clear_console()
            return None


def _render_build_selector(
    builds: list[dict],
    selected_index: int,
    installed_build_names: set[str],
    status=None,
) -> None:
    _clear_console()
    print_banner()
    if status is not None:
        print_update_status(status)
        print("")

    print(Fore.BLUE + Style.BRIGHT + "Список версий")

    start_index = max(0, selected_index - WINDOW_SIZE // 2)
    end_index = min(len(builds), start_index + WINDOW_SIZE)
    start_index = max(0, end_index - WINDOW_SIZE)

    for index in range(start_index, end_index):
        build = builds[index]
        is_selected = index == selected_index
        is_installed = build_installation_dir_name(build) in installed_build_names

        prefix = Fore.BLUE + "> " if is_selected else "  "
        status = Fore.GREEN + " [установлено]" if is_installed else ""
        label = format_build_label(build)

        if is_selected:
            print(prefix + Fore.BLUE + Style.BRIGHT + label + status)
        else:
            print(prefix + label + status)

    print("")
    print(
        Style.DIM
        + "↑/↓ — перемещение, "
        + "Enter — установить, "
        + "Space — список изменений, "
        + "Delete — удалить, "
        + "Esc — выход"
    )


def _read_action() -> str | None:
    import msvcrt

    key = msvcrt.getwch()

    if key == '\x1b':
        return 'quit'
    if key == ' ':
        return 'changelog'
    if key in ('\r', '\n'):
        return 'enter'
    if key in ('w', 'W'):
        return 'up'
    if key in ('s', 'S'):
        return 'down'

    if key in ('\x00', '\xe0'):
        arrow = msvcrt.getwch()
        if arrow == 'H':
            return 'up'
        if arrow == 'P':
            return 'down'
        if arrow == 'S':
            return 'delete'

    return None


def flush_input_buffer(settle_ms: float = 0.06) -> None:
    import msvcrt

    deadline = time.perf_counter() + settle_ms
    while time.perf_counter() < deadline:
        drained = False
        while msvcrt.kbhit():
            key = msvcrt.getwch()
            if key in ('\x00', '\xe0') and msvcrt.kbhit():
                msvcrt.getwch()
            drained = True

        if drained:
            deadline = time.perf_counter() + settle_ms
        else:
            time.sleep(0.01)


def clear_console() -> None:
    _clear_console()


def _clear_console() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')
