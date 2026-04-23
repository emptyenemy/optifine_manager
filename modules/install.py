import subprocess
from pathlib import Path


def install_optifine_jar(jar_path: str | Path, timeout_seconds: int = 120) -> str:
    jar_path = Path(jar_path)

    process = subprocess.run(
        ["java", "-cp", str(jar_path), "optifine.Installer"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        timeout=timeout_seconds,
        check=False,
    )

    output = process.stdout.strip()
    if process.returncode != 0:
        if output:
            raise RuntimeError(
                f"Silent-установка OptiFine завершилась с кодом {process.returncode}.\n{output}"
            )
        raise RuntimeError(
            f"Silent-установка OptiFine завершилась с кодом {process.returncode}."
        )

    return output


def main():
    raise SystemExit("Этот модуль используется через main.py.")


if __name__ == '__main__':
    main()
