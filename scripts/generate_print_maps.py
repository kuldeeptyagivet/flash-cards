import os
import json
import math

BASE_DIR = r'g:\My Drive\Flash Cards'
DECKS_DIR = os.path.join(BASE_DIR, 'decks', 'Countries-Capital')
PRINT_MAPS_DIR = os.path.join(DECKS_DIR, 'maps-print')
SCRATCH_DIR = os.path.join(BASE_DIR, 'scratch')

os.makedirs(PRINT_MAPS_DIR, exist_ok=True)

with open(os.path.join(SCRATCH_DIR, 'countries.geojson'), 'r', encoding='utf-8') as f:
    geojson_data = json.load(f)

# Official Survey of India boundary (includes PoK + Aksai Chin), simplified.
with open(os.path.join(SCRATCH_DIR, 'india-composite-simplified.geojson'), 'r', encoding='utf-8') as f:
    india_composite = json.load(f)
india_geometry = india_composite['features'][0]['geometry']

for feat in geojson_data['features']:
    props = feat['properties']
    iso2 = (props.get('ISO_A2') or props.get('POSTAL') or '').lower()
    if iso2 == 'in':
        feat['geometry'] = india_geometry
        break

with open(os.path.join(DECKS_DIR, 'data.json'), 'r', encoding='utf-8') as f:
    country_dataset = json.load(f)

def project(lon, lat, width=800, height=500):
    x = (lon + 180.0) * (width / 360.0)
    lat_rad = math.radians(max(min(lat, 84.0), -84.0))
    merc_n = math.log(math.tan((math.pi / 4.0) + (lat_rad / 2.0)))
    y = (height / 2.0) - (width * merc_n / (2.0 * math.pi))
    return round(x, 2), round(y, 2)

feature_map = {}
for feat in geojson_data['features']:
    props = feat['properties']
    iso2 = (props.get('ISO_A2') or props.get('POSTAL') or '').lower()
    iso3 = (props.get('ISO_A3') or props.get('ADM0_A3') or '').lower()
    name = (props.get('NAME') or props.get('ADMIN') or '').lower()
    if iso2 and iso2 != '-99':
        feature_map[iso2] = feat
    if iso3 and iso3 != '-99':
        feature_map[iso3] = feat
    if name:
        feature_map[name] = feat

def geom_to_svg_path(geometry):
    gtype = geometry['type']
    coords = geometry['coordinates']
    polys = [coords] if gtype == 'Polygon' else (coords if gtype == 'MultiPolygon' else [])
    paths = []
    all_points = []
    for poly in polys:
        for ring in poly:
            r_path = []
            for i, p in enumerate(ring):
                sx, sy = project(p[0], p[1], 800, 500)
                all_points.append((sx, sy))
                cmd = "M" if i == 0 else "L"
                r_path.append(f"{cmd} {sx} {sy}")
            r_path.append("Z")
            paths.append(" ".join(r_path))
    return " ".join(paths), all_points

success_count = 0

for item in country_dataset:
    iso = item['iso']
    cap_lat = item['lat']
    cap_lon = item['lon']

    cap_x, cap_y = project(cap_lon, cap_lat, 800, 500)
    feat = feature_map.get(iso) or feature_map.get(item['country'].lower())

    if feat:
        path_d, points = geom_to_svg_path(feat['geometry'])
    else:
        path_d, points = "", []

    if points:
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        min_x, max_x = min(min_x, cap_x), max(max_x, cap_x)
        min_y, max_y = min(min_y, cap_y), max(max_y, cap_y)
        width = max(max_x - min_x, 15)
        height = max(max_y - min_y, 15)
        pad_x = max(width * 0.12, 6)
        pad_y = max(height * 0.12, 6)
        vx, vy = min_x - pad_x, min_y - pad_y
        vw, vh = width + pad_x * 2, height + pad_y * 2
    else:
        box = 60
        vx, vy, vw, vh = cap_x - 30, cap_y - 30, box, box
        path_d = f"M {cap_x-20} {cap_y-10} L {cap_x+20} {cap_y-10} L {cap_x+10} {cap_y+20} L {cap_x-15} {cap_y+15} Z"

    svg_str = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vx:.2f} {vy:.2f} {vw:.2f} {vh:.2f}" '
        f'width="100%" height="100%">'
        f'<path d="{path_d}" fill="#E0E7FF" stroke="#4338CA" stroke-width="{vw*0.012:.2f}" stroke-linejoin="round"/>'
        f'<circle cx="{cap_x:.2f}" cy="{cap_y:.2f}" r="{max(vw*0.03, 1.6):.2f}" fill="#DC2626" stroke="#FFFFFF" stroke-width="{vw*0.006:.2f}"/>'
        f'</svg>'
    )

    with open(os.path.join(PRINT_MAPS_DIR, f"{iso}.svg"), 'w', encoding='utf-8') as f_out:
        f_out.write(svg_str)
    success_count += 1

print(f"Generated {success_count} lightweight print maps in {PRINT_MAPS_DIR}")
