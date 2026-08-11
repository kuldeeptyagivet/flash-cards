import os
import json
import math
import urllib.request

BASE_DIR = r'g:\My Drive\Flash Cards'
DECKS_DIR = os.path.join(BASE_DIR, 'decks', 'Countries-Capital')
MAPS_DIR = os.path.join(DECKS_DIR, 'maps')
SCRATCH_DIR = os.path.join(BASE_DIR, 'scratch')

# Load GeoJSON
cache_file = os.path.join(SCRATCH_DIR, 'countries.geojson')
with open(cache_file, 'r', encoding='utf-8') as f:
    geojson_data = json.load(f)

# Load country dataset
dataset_path = os.path.join(DECKS_DIR, 'data.json')
with open(dataset_path, 'r', encoding='utf-8') as f:
    country_dataset = json.load(f)

# Global Mercator Projection (0..800 x 0..500)
def project(lon, lat, width=800, height=500):
    x = (lon + 180.0) * (width / 360.0)
    lat_rad = math.radians(max(min(lat, 84.0), -84.0))
    merc_n = math.log(math.tan((math.pi / 4.0) + (lat_rad / 2.0)))
    y = (height / 2.0) - (width * merc_n / (2.0 * math.pi))
    return round(x, 2), round(y, 2)

# Build feature lookup map
feature_map = {}
world_all_paths = []

# Pre-generate simplified world paths for the mini inset map
for feat in geojson_data['features']:
    props = feat['properties']
    iso2 = (props.get('ISO_A2') or props.get('POSTAL') or '').lower()
    iso3 = (props.get('ISO_A3') or props.get('ADM0_A3') or '').lower()
    name = (props.get('NAME') or props.get('ADMIN') or '').lower()
    
    if iso2 and iso2 != '-99': feature_map[iso2] = feat
    if iso3 and iso3 != '-99': feature_map[iso3] = feat
    if name: feature_map[name] = feat

    # Generate world paths
    gtype = feat['geometry']['type']
    coords = feat['geometry']['coordinates']
    polys = [coords] if gtype == 'Polygon' else (coords if gtype == 'MultiPolygon' else [])
    
    for poly in polys:
        for ring in poly:
            r_path = []
            for i, p in enumerate(ring):
                sx, sy = project(p[0], p[1], 800, 500)
                cmd = "M" if i == 0 else "L"
                r_path.append(f"{cmd} {sx} {sy}")
            r_path.append("Z")
            world_all_paths.append(" ".join(r_path))

world_combined_svg_d = " ".join(world_all_paths)

# Convert GeoJSON Geometry to SVG Path & Points
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
    c_name = item['country']
    cap_name = item['capital']
    cap_lat = item['lat']
    cap_lon = item['lon']
    
    cap_x, cap_y = project(cap_lon, cap_lat, 800, 500)
    feat = feature_map.get(iso) or feature_map.get(c_name.lower())
    
    path_d = ""
    points = []
    
    if feat:
        path_d, points = geom_to_svg_path(feat['geometry'])
    
    if points:
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        
        min_x = min(min_x, cap_x)
        max_x = max(max_x, cap_x)
        min_y = min(min_y, cap_y)
        max_y = max(max_y, cap_y)
        
        width = max(max_x - min_x, 15)
        height = max(max_y - min_y, 15)
        
        pad_x = max(width * 0.15, 10)
        pad_y = max(height * 0.15, 10)
        
        vx = min_x - pad_x
        vy = min_y - pad_y
        vw = width + (pad_x * 2)
        vh = height + (pad_y * 2)
    else:
        box = 60
        vx, vy, vw, vh = cap_x - 30, cap_y - 30, box, box
        path_d = f"M {cap_x-20} {cap_y-10} L {cap_x+20} {cap_y-10} L {cap_x+10} {cap_y+20} L {cap_x-15} {cap_y+15} Z"

    # Inset Map Parameters in top-right of viewBox
    inset_w = vw * 0.32
    inset_h = vh * 0.24
    inset_x = vx + vw - inset_w - (vw * 0.03)
    inset_y = vy + (vh * 0.03)
    
    # Scale world map (0..800 x 0..500) into inset (inset_x..inset_x+inset_w x inset_y..inset_y+inset_h)
    scale_x = inset_w / 800.0
    scale_y = inset_h / 500.0
    
    # World locator dot inside inset
    dot_inset_x = inset_x + (cap_x * scale_x)
    dot_inset_y = inset_y + (cap_y * scale_y)

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

  <!-- Card Background -->
  <rect x="{vx:.2f}" y="{vy:.2f}" width="{vw:.2f}" height="{vh:.2f}" fill="url(#bgGrad_{iso})"/>
  
  <!-- Main Zoomed Real Geographic Country Polygon -->
  <g filter="url(#shadow_{iso})">
    <path d="{path_d}" fill="url(#realCountryGrad_{iso})" stroke="#818CF8" stroke-width="{vw*0.006:.2f}" stroke-linejoin="round"/>
  </g>

  <!-- Capital City Marker -->
  <circle cx="{cap_x:.2f}" cy="{cap_y:.2f}" r="{vw*0.05:.2f}" fill="#EF4444" fill-opacity="0.35">
    <animate attributeName="r" values="{vw*0.03:.2f};{vw*0.07:.2f};{vw*0.03:.2f}" dur="2s" repeatCount="indefinite"/>
  </circle>
  <circle cx="{cap_x:.2f}" cy="{cap_y:.2f}" r="{max(vw*0.015, 1.2):.2f}" fill="#EF4444" stroke="#FFFFFF" stroke-width="0.6"/>

  <!-- MINI WORLD LOCATOR INSET MAP (Top-Right) -->
  <g id="worldInset">
    <!-- Inset Frame -->
    <rect x="{inset_x:.2f}" y="{inset_y:.2f}" width="{inset_w:.2f}" height="{inset_h:.2f}" rx="{vw*0.02:.2f}" fill="#0F172A" fill-opacity="0.9" stroke="#475569" stroke-width="{vw*0.005:.2f}"/>
    
    <!-- Mini World Map Path -->
    <g transform="translate({inset_x:.2f}, {inset_y:.2f}) scale({scale_x:.6f}, {scale_y:.6f})">
      <path d="{world_combined_svg_d}" fill="#334155" stroke="none"/>
    </g>

    <!-- World Locator Pin Highlight for this Country -->
    <circle cx="{dot_inset_x:.2f}" cy="{dot_inset_y:.2f}" r="{inset_w*0.08:.2f}" fill="#F59E0B" fill-opacity="0.6">
      <animate attributeName="r" values="{inset_w*0.05:.2f};{inset_w*0.12:.2f};{inset_w*0.05:.2f}" dur="1.5s" repeatCount="indefinite"/>
    </circle>
    <circle cx="{dot_inset_x:.2f}" cy="{dot_inset_y:.2f}" r="{inset_w*0.04:.2f}" fill="#F59E0B" stroke="#FFFFFF" stroke-width="0.4"/>

    <!-- Inset Label -->
    <text x="{inset_x + inset_w/2:.2f}" y="{inset_y + inset_h - (vh*0.015):.2f}" font-family="system-ui, sans-serif" font-size="{vh*0.025:.2f}" font-weight="bold" fill="#94A3B8" text-anchor="middle">WORLD MAP</text>
  </g>
</svg>'''

    svg_out_file = os.path.join(MAPS_DIR, f"{iso}.svg")
    with open(svg_out_file, 'w', encoding='utf-8') as f_out:
        f_out.write(svg_str)
    success_count += 1

print(f"Successfully generated {success_count} Dual-View (Real Country + World Inset Locator) SVG maps!")
