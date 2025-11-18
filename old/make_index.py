from pathlib import Path
import json, re, urllib.parse

# ⚙️ Настройки
USER = "xkbn7779090-cmyk"
REPO = "Art"
BRANCH = "main"
CREATED_IN = "Limburg, Netherlands"
YEAR = 2025
REGION = "LN"

# 💾 Основной каталог
root = Path("images")
base_url = f"https://raw.githubusercontent.com/{USER}/{REPO}/{BRANCH}/images"

# 💰 Базовые цены по размеру
price_map = {
    "20x20": 110,
    "25x25": 130,
    "30x24": 150,
    "40x40": 180,
    "50x50": 250,
    "60x50": 280,
    "70x50": 320,
    "70x100": 380,
    "100x70": 420,
    "120x40": 450
}

data = []

# 🧩 Собираем все файлы
for p in sorted(root.glob("*.jpg")):
    name = p.stem

    # Пример имени: #100_main_20x20_C
    m = re.match(r"#?(\d+)_.*?(\d+x\d+)_?(C|CB)", name)
    if not m:
        print(f"⚠️ Пропущено (непонятное имя): {name}")
        continue

    num, size, material = m.groups()
    size_cm = size.replace("x", "×") + " cm"
    mat_full = "Oil on canvas, stretched on stretcher frame" if material == "C" else "Oil on canvas board"

    title = f"#{num} Untitled {size} {('canvas' if material=='C' else 'board')}"
    sku = f"{REGION}-{YEAR}-{size}-{num}_Untitled_{size}_{material}"
    price = f"€{price_map.get(size, 200)}"

    url = f"{base_url}/{urllib.parse.quote(p.name)}"

    item = {
        "Title": title,
        "SKU": sku,
        "Size": size_cm,
        "Material": mat_full,
        "Created in": CREATED_IN,
        "Price": price,
        "Image link": url,
        "Description (EN)": "",
        "Description (RU)": ""
    }

    data.append(item)

# 📁 Запись в JSON
Path("index.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"✅ Создан index.json ({len(data)} записей)")
