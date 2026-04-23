from pathlib import Path
from typing import Callable
from urllib.parse import parse_qs, urlparse

from modules.http_client import download_to_path_sync


def resolve_filename(download_url: str) -> str:
    query = parse_qs(urlparse(download_url).query)
    filename = query.get('f', [None])[0]
    if filename:
        return filename

    path_name = Path(urlparse(download_url).path).name
    if path_name:
        return path_name

    raise RuntimeError("Не удалось определить имя файла для скачивания.")


def _format_size(size_in_bytes: int) -> str:
    units = ["B", "KB", "MB", "GB"]
    size = float(size_in_bytes)

    for unit in units:
        if size < 1024 or unit == units[-1]:
            if unit == "B":
                return f"{int(size)} {unit}"
            return f"{size:.2f} {unit}"
        size /= 1024

    return f"{size_in_bytes} B"


def download_file(
    download_url: str,
    target_dir: Path | None = None,
    log_callback: Callable[[str], None] | None = None,
) -> Path:
    target_dir = target_dir or Path.cwd()
    target_dir.mkdir(parents=True, exist_ok=True)
    log_callback = log_callback or (lambda _: None)

    file_name = resolve_filename(download_url)
    target_path = target_dir / file_name
    last_percent_step = -1
    last_unknown_reported_mb = 0

    log_callback(f"Подготовка скачивания файла: {file_name}")
    log_callback(f"Каталог скачивания: {target_dir}")
    log_callback(f"Итоговый путь файла: {target_path}")

    def handle_metadata(total_bytes: int | None) -> None:
        if total_bytes:
            log_callback(f"Размер файла: {_format_size(total_bytes)}")

    def handle_progress(downloaded_bytes: int, total_bytes: int | None) -> None:
        nonlocal last_percent_step, last_unknown_reported_mb

        if total_bytes:
            percent = int((downloaded_bytes / total_bytes) * 100)
            percent_step = min(10, percent // 10)
            if percent_step > last_percent_step:
                last_percent_step = percent_step
                log_callback(
                    "Скачано: "
                    f"{min(percent_step * 10, 100)}% "
                    f"({_format_size(downloaded_bytes)} / {_format_size(total_bytes)})"
                )
            return

        downloaded_mb = downloaded_bytes // (1024 * 1024)
        if downloaded_mb > last_unknown_reported_mb:
            last_unknown_reported_mb = downloaded_mb
            log_callback(f"Скачано: {_format_size(downloaded_bytes)}")

    downloaded_path = download_to_path_sync(
        download_url,
        target_path,
        metadata_callback=handle_metadata,
        progress_callback=handle_progress,
    )
    log_callback(f"Скачивание завершено: {downloaded_path}")
    log_callback(f"Финальный размер: {_format_size(downloaded_path.stat().st_size)}")
    return downloaded_path
