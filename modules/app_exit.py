from modules.console_ui import clear_console, print_section_header


def exit_program() -> bool:
    clear_console()
    print_section_header("Выход из программы...")
    return False
