# Kids Educational Flashcards Web App — Project & Session Log

## 📌 Project Overview
An interactive, mobile-first educational Flash Cards application designed for kids to learn World Countries, Capitals, Maps, Flags, and future subjects (Currencies, Science, Solar System, etc.).

* **Location:** `g:\My Drive\Flash Cards`
* **Live App URL:** `https://kuldeeptyagivet.github.io/flash-cards/`
* **Local Dev Server:** `http://localhost:8000/`
* **GitHub Repository:** `https://github.com/kuldeeptyagivet/flash-cards`

---

## 🏗️ Architecture & Component Design

### 1. Real Geographic Vector Maps & Data (`decks/Countries-Capital/`)
* **[`decks/Countries-Capital/data.json`](file:///g:/My%20Drive/Flash%20Cards/decks/Countries-Capital/data.json)**: Full dataset containing 196 countries, capitals, continents, ISO 2-letter codes, flag emojis, and lat/long coordinates.
* **[`decks/Countries-Capital/maps/`](file:///g:/My%20Drive/Flash%20Cards/decks/Countries-Capital/maps/)**: 196 **Real Geographic SVG Vector Maps** generated from official Natural Earth GeoJSON border boundaries (`in.svg`, `us.svg`, `fr.svg`, `br.svg`, `jp.svg`) with auto-calibrated viewports and glowing capital markers.

### 2. Deck Selection Hub & Search Bar (`index.html`)
* **Landing Page Hub**: Shows a prominent **Search Bar** (`🔍 Search decks...`) and grid of deck cards.
* **Deck Card**: Tapping **Countries & Capitals** loads the dataset and opens the 3D Flashcard & Quiz experience.
* **Navigation**: Includes a `← Back to Decks` button to return to the Hub anytime.

---

## 📜 Session History & Progress Log

### Session 1: 2026-08-11
* **Status:** Completed Real Geographic SVG Map integration, GitHub Repository setup, and GitHub Pages deployment.
* **Accomplished:**
  * Replaced initial placeholder shapes with **100% authentic, real geographical border polygons** for all 196 countries generated via Natural Earth GeoJSON vector data.
  * Re-organized dataset and vector SVG maps under `decks/Countries-Capital/`.
  * Designed and built the Home Deck Selection Hub with live search bar filtering across available decks.
  * Added "← Back to Decks" header navigation.
  * Created public GitHub repo `kuldeeptyagivet/flash-cards` and enabled GitHub Pages at `https://kuldeeptyagivet.github.io/flash-cards/`.
  * Pushed updated code and verified live deployment.

---

## 🚀 How to Run & Deploy

1. **Local Development:**
   Run in terminal:
   ```bash
   python -m http.server 8000 --directory "g:\My Drive\Flash Cards"
   ```
   Open `http://localhost:8000/` on mobile or desktop.

2. **Live URL:**
   Open `https://kuldeeptyagivet.github.io/flash-cards/` on any mobile phone or browser.

3. **Cloudflare Pages (`flash.examsindia.org`):**
   * Connect `kuldeeptyagivet/flash-cards` to Cloudflare Pages and set custom domain `flash.examsindia.org`.
