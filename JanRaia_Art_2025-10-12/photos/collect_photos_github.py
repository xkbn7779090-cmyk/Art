#!/usr/bin/env python3
import json
from pathlib import Path

# === Настройки ===
# Локальная папка с фотографиями
folder = Path(r"C:\Users\JanTar\Documents\GitHub\Art\JanRaia_Art_2025-10-12\photos")

# Введи свои данные для формирования ссылки
GITHUB_OWNER  = "xkbn7779090-cmyk"   # твой GitHub логин или организация
GITHUB_REPO   = "Art"                # название репозитория
GITHUB_BRANCH = "main"               # имя ветки
GITHUB_FOLDER = "JanRaia_Art_2025-10-12/photos"  # путь в репозитории

# Разрешённые расширения
exts = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".heic", ".heif"}

# === Сбор файлов ===
files = []
for p in folder.rglob("*"):
    if p.is_file() and p.suffix.lower() in exts:
        rel = f"{GITHUB_FOLDER}/{p.name}"
        raw_url = f"https://raw.githubusercontent.com/{GITHUB_OWNER}/{GITHUB_REPO}/{GITHUB_BRANCH}/{rel}"
        files.append({
            "filename": p.name,
            "raw_url": raw_url,
            "relative_repo_path": rel
        })

# === Сохранение ===
outfile = folder / "images_index.json"
with open(outfile, "w", encoding="utf-8") as f:
    json.dump(files, f, ensure_ascii=False, indent=2)

print(f"✅ Сохранено {len(files)} файлов в {outfile}")
