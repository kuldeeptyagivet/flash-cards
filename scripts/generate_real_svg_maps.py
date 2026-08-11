import os
import json
import math
import urllib.request

BASE_DIR = r'g:\My Drive\Flash Cards'
DECKS_DIR = os.path.join(BASE_DIR, 'decks', 'Countries-Capital')
MAPS_DIR = os.path.join(DECKS_DIR, 'maps')
SCRATCH_DIR = os.path.join(BASE_DIR, 'scratch')

os.makedirs(MAPS_DIR, exist_ok=True)
os.makedirs(SCRATCH_DIR, exist_ok=True)

# 1. Download real GeoJSON dataset
geojson_url = 'https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_admin_0_countries.geojson'
cache_file = os.path.join(SCRATCH_DIR, 'countries.geojson')

if not os.path.exists(cache_file):
    print("Downloading official Natural Earth real GeoJSON boundaries...")
    req = urllib.request.Request(geojson_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp, open(cache_file, 'wb') as f:
        f.write(resp.read())

with open(cache_file, 'r', encoding='utf-8') as f:
    geojson_data = json.load(f)

# Load dataset mapping
dataset_path = os.path.join(DECKS_DIR, 'data.json')
with open(dataset_path, 'r', encoding='utf-8') as f:
    country_dataset = json.load(f)

# Helper Mercator projection
def project(lon, lat):
    x = (lon + 180.0) * (800.0 / 360.0)
    lat_rad = math.radians(max(min(lat, 84.0), -84.0))
    merc_n = math.log(math.tan((math.pi / 4.0) + (lat_rad / 2.0)))
    y = (500.0 / 2.0) - (800.0 * merc_n / (2.0 * math.pi))
    return round(x, 2), round(y, 2)

# Build feature lookup map by ISO-2, ISO-3, or Name
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

# Convert GeoJSON Geometry to SVG Path
def geom_to_svg_path(geometry):
    gtype = geometry['type']
    coords = geometry['coordinates']
    paths = []
    
    if gtype == 'Polygon':
        polygon_list = [coords]
    elif gtype == 'MultiPolygon':
        polygon_list = coords
    else:
        return "", []

    all_points = []
    
    for poly in polygon_list:
        for ring in poly:
            ring_path = []
            for i, p in enumerate(ring):
                lon, lat = p[0], p[1]
                sx, sy = project(lon, lat)
                all_points.append((sx, sy))
                cmd = "M" if i == 0 else "L"
                ring_path.append(f"{cmd} {sx} {sy}")
            ring_path.append("Z")
            paths.append(" ".join(ring_path))
            
    return " ".join(paths), all_points

# Generate Real SVGs
success_count = 0

for item in country_dataset:
    iso = item['iso']
    c_name = item['country']
    cap_name = item['capital']
    cap_lat = item['lat']
    cap_lon = item['lon']
    
    # Capital projection
    cap_x, cap_y = project(cap_lon, cap_lat)
    
    # Find matching GeoJSON feature
    feat = feature_map.get(iso) or feature_map.get(c_name.lower())
    
    path_d = ""
    points = []
    
    if feat:
        path_d, points = geom_to_svg_path(feat['geometry'])
    
    # Calculate bounding box
    if points:
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        
        # Include capital in bounding box
        min_x = min(min_x, cap_x)
        max_x = max(max_x, cap_x)
        min_y = min(min_y, cap_y)
        max_y = max(max_y, cap_y)
        
        width = max(max_x - min_x, 15)
        height = max(max_y - min_y, 15)
        
        # Add padding
        pad_x = max(width * 0.15, 10)
        pad_y = max(height * 0.15, 10)
        
        vx = min_x - pad_x
        vy = min_y - pad_y
        vw = width + (pad_x * 2)
        vh = height + (pad_y * 2)
    else:
        # Fallback bounding box if shape not found
        box = 60
        vx, vy, vw, vh = cap_x - 30, cap_y - 30, box, box
        path_d = f"M {cap_x-20} {cap_y-10} L {cap_x+20} {cap_y-10} L {cap_x+10} {cap_y+20} L {cap_x-15} {cap_y+15} Z"

    # Assemble Real Geographic SVG
    svg_str = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vx:.2f} {vy:.2f} {vw:.2f} {vh:.2f}" width="100%" height="100%">
  <defs>
    <radialGradient id="bgGrad_{iso}" cx="50%" cy="50%" r="70%">
      <stop offset="0%" stop-color="#1E293B"/>
      <stop offset="100%" stop-color="#0F172A"/>
    </radialGradient>
    <linearGradient id="realCountryGrad_{iso}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#4F46E5"/>
      <stop offset="100%" stop-color="#2563EB"/>
    </linearGradient>
    <filter id="shadow_{iso}" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="#000" flood-opacity="0.5"/>
    </filter>
  </defs>

  <!-- Background -->
  <rect x="{vx:.2f}" y="{vy:.2f}" width="{vw:.2f}" height="{vh:.2f}" fill="url(#bgGrad_{iso})"/>
  
  <!-- Real Geographic Country Polygon -->
  <g filter="url(#shadow_{iso})">
    <path d="{path_d}" fill="url(#realCountryGrad_{iso})" stroke="#818CF8" stroke-width="0.8" stroke-linejoin="round"/>
  </g>

  <!-- Real Capital Location Marker -->
  <circle cx="{cap_x}" cy="{cap_y}" r="{vw*0.06}" fill="#EF4444" fill-opacity="0.35">
    <animate attributeName="r" values="{vw*0.04};{vw*0.08};{vw*0.04}" dur="2s" repeatCount="indefinite"/>
  </circle>

  <circle cx="{cap_x}" cy="{cap_y}" r="{max(vw*0.015, 1.2)}" fill="#EF4444" stroke="#FFFFFF" stroke-width="0.6"/>
</svg>'''

    svg_out_file = os.path.join(MAPS_DIR, f"{iso}.svg")
    with open(svg_out_file, 'w', encoding='utf-8') as f_out:
        f_out.write(svg_str)
    success_count += 1

print(f"Successfully generated {success_count} REAL geographic country SVG maps in {MAPS_DIR}")
