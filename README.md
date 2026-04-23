# OptiFine Manager

![OptiFine Manager](https://i.imgur.com/CS09vii.png)

[Русский](README.md) | [English](README_EN.md)

Терминальный менеджер для загрузки, установки, просмотра changelog и удаления сборок OptiFine на Windows.

## Возможности

- проверяет обновления для локально установленных версий Minecraft
- показывает только те сборки OptiFine, которые соответствуют имеющимся версиям
- отдаёт предпочтение release-сборкам перед preview-сборками
- откатывается на последнюю preview-сборку, если release отсутствует
- открывает changelog прямо в терминале
- загружает OptiFine во временную папку
- устанавливает OptiFine через внутреннюю точку входа тихого установщика
- удаляет установленные версии OptiFine и чистит профили лаунчера
- корректно обрабатывает ошибки соединения с `optifine.net` без падений

## Требования

- Windows
- Python 3.11+
- Java в `PATH`
- установленные версии Minecraft в:
  `C:\Users\%USERNAME%\AppData\Roaming\.minecraft\versions`

## Установка

```powershell
git clone https://github.com/emptyenemy/optifine_manager
cd "OptiFine Manager"
pip install -r requirements.txt
```

## Запуск

```powershell
python main.py
```

## Управление

- `↑/↓` перемещение по списку
- `Enter` установить выбранную сборку OptiFine
- `Space` открыть changelog
- `Delete` удалить установленную сборку OptiFine
- `Esc` назад / выход

## Как это работает

1. Читает локальные версии Minecraft из `.minecraft\versions`
2. Загружает страницу версий OptiFine
3. Фильтрует сборки, оставляя только совместимые с локальными версиями Minecraft
4. Получает прямую ссылку на скачивание
5. Загружает выбранный `.jar` во временную папку
6. Запускает тихую установку командой:

```powershell
java -cp OptiFine_xxx.jar optifine.Installer
```

7. Удаляет временный файл установщика

## Зависимости

- `aiohttp`
- `beautifulsoup4`
- `colorama`
- `pyfiglet`

## Структура проекта

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

## Примечания

- проект использует внутренний класс установщика OptiFine вместо автоматизации GUI
- миры не удаляются при удалении версий OptiFine
- если `optifine.net` недоступен, приложение показывает экран повтора/выхода вместо трейсбэка

## Дисклеймер

Этот проект неофициальный и не связан с OptiFine.
