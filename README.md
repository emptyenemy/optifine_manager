# OptiFine Manager

Terminal manager for downloading, installing, viewing changelogs, and removing OptiFine builds on Windows.

## Features

- checks updates for locally installed Minecraft versions
- shows only relevant OptiFine builds for versions you actually have
- prefers release builds over preview builds
- falls back to the latest preview if no release exists
- opens changelog directly in the terminal
- downloads OptiFine to a temporary folder
- installs OptiFine through the internal silent installer entrypoint
- deletes installed OptiFine versions and cleans launcher profiles
- handles `optifine.net` connection errors without crashing

## Requirements

- Windows
- Python 3.11+
- Java in `PATH`
- installed Minecraft versions in:
  `C:\Users\%USERNAME%\AppData\Roaming\.minecraft\versions`

## Installation

```powershell
git clone https://github.com/emptyenemy/optifine_manager
cd "OptiFine Manager"
pip install -r requirements.txt
```

## Run

```powershell
python main.py
```

## Controls

- `↑/↓` move through the list
- `Enter` install selected OptiFine build
- `Space` open changelog
- `Delete` remove installed OptiFine build
- `Esc` go back / exit

## How It Works

1. Reads local Minecraft versions from `.minecraft\versions`
2. Downloads the OptiFine versions page
3. Filters builds to only compatible local Minecraft versions
4. Resolves the direct download link
5. Downloads the selected `.jar` into a temporary directory
6. Runs silent installation with:

```powershell
java -cp OptiFine_xxx.jar optifine.Installer
```

7. Removes the temporary installer file

## Dependencies

- `aiohttp`
- `beautifulsoup4`
- `colorama`
- `pyfiglet`

## Project Structure

```text
main.py
requirements.txt
modules/
  app_exit.py
  changelog.py
  console_ui.py
  delete.py
  direct_download_link.py
  download.py
  http_client.py
  install.py
  installed.py
  latest.py
  optifine.py
  status.py
```

## Notes

- the project uses OptiFine's internal installer class instead of GUI automation
- worlds are not deleted when removing OptiFine versions
- if `optifine.net` is unavailable, the app shows a retry/exit screen instead of a traceback

## Disclaimer

This project is unofficial and is not affiliated with OptiFine.
