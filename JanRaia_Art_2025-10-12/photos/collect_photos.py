#!/usr/bin/env python3
import json
from pathlib import Path

# Папка с фотографиями
folder = Path(r"C:\Users\JanTar\Documents\GitHub\Art\JanRaia_Art_2025-10-12\photos")

# Разрешённые расширения
exts = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".heic", ".heif"}

# Список объектов
files = []
for p in folder.rglob("*"):
    if p.is_file() and p.suffix.lower() in exts:
        files.append({
            "filename": p.name,
            "path": str(p),
            "relative": str(p.relative_to(folder.parent)),
        })

# Сохраняем JSON рядом
outfile = folder / "images_index.json"
with open(outfile, "w", encoding="utf-8") as f:
    json.dump(files, f, ensure_ascii=False, indent=2)

print(f"✅ Сохранено {len(files)} файлов в {outfile}")
