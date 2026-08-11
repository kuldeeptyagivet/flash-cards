import os
import shutil

BASE_DIR = r'g:\My Drive\Flash Cards'
DECKS_DIR = os.path.join(BASE_DIR, 'decks')
CC_DIR = os.path.join(DECKS_DIR, 'Countries-Capital')
CC_MAPS_DIR = os.path.join(CC_DIR, 'maps')

os.makedirs(CC_MAPS_DIR, exist_ok=True)

# Copy data.json
old_json = os.path.join(BASE_DIR, 'data', 'countries-capitals.json')
new_json = os.path.join(CC_DIR, 'data.json')
if os.path.exists(old_json):
    shutil.copy2(old_json, new_json)
    print(f"Copied data to {new_json}")

# Copy maps
old_maps_dir = os.path.join(BASE_DIR, 'assets', 'maps', 'countries')
if os.path.exists(old_maps_dir):
    for f in os.listdir(old_maps_dir):
        if f.endswith('.svg'):
            shutil.copy2(os.path.join(old_maps_dir, f), os.path.join(CC_MAPS_DIR, f))
    print(f"Copied SVG maps to {CC_MAPS_DIR}")

# Create decks manifest decks.json
manifest = [
    {
        "id": "countries-capital",
        "title": "Countries & Capitals",
        "category": "Geography",
        "icon": "🌍",
        "badge": "196 Cards",
        "description": "Learn 196 world countries, capital cities, continents, and interactive vector maps!",
        "dataPath": "decks/Countries-Capital/data.json",
        "mapsPath": "decks/Countries-Capital/maps/"
    }
]

manifest_path = os.path.join(DECKS_DIR, 'manifest.json')
with open(manifest_path, 'w', encoding='utf-8') as f:
    import json
    json.dump(manifest, f, indent=2)

print(f"Created decks manifest at {manifest_path}")
