import asyncio
from pathlib import Path
from typing import Callable

import aiohttp


class OptiFineNetworkError(RuntimeError):
    pass


async def fetch_text(url: str, timeout: float = 30) -> str:
    client_timeout = aiohttp.ClientTimeout(total=timeout)
    try:
        async with aiohttp.ClientSession(timeout=client_timeout) as session:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.text()
    except (aiohttp.ClientError, asyncio.TimeoutError) as exc:
        raise OptiFineNetworkError("Не удалось установить соединение с OptiFine.") from exc


def fetch_text_sync(url: str, timeout: float = 30) -> str:
    return asyncio.run(fetch_text(url, timeout=timeout))


async def download_to_path(
    url: str,
    target_path: Path,
    timeout: float = 300,
    metadata_callback: Callable[[int | None], None] | None = None,
    progress_callback: Callable[[int, int | None], None] | None = None,
) -> Path:
    client_timeout = aiohttp.ClientTimeout(total=timeout)
    try:
        async with aiohttp.ClientSession(timeout=client_timeout) as session:
            async with session.get(url) as response:
                response.raise_for_status()
                if metadata_callback is not None:
                    metadata_callback(response.content_length)

                downloaded = 0
                with target_path.open("wb") as file_obj:
                    async for chunk in response.content.iter_chunked(8192):
                        if chunk:
                            file_obj.write(chunk)
                            downloaded += len(chunk)
                            if progress_callback is not None:
                                progress_callback(downloaded, response.content_length)
    except (aiohttp.ClientError, asyncio.TimeoutError) as exc:
        raise OptiFineNetworkError("Не удалось установить соединение с OptiFine.") from exc
    return target_path


def download_to_path_sync(
    url: str,
    target_path: Path,
    timeout: float = 300,
    metadata_callback: Callable[[int | None], None] | None = None,
    progress_callback: Callable[[int, int | None], None] | None = None,
) -> Path:
    return asyncio.run(
        download_to_path(
            url,
            target_path,
            timeout=timeout,
            metadata_callback=metadata_callback,
            progress_callback=progress_callback,
        )
    )
