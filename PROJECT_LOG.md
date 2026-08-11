# Kids Educational Flashcards Web App — Project & Session Log

## 📌 Project Overview
An interactive, mobile-first educational Flash Cards application designed for kids to learn World Countries, Capitals, Maps, Flags, and future subjects (Currencies, Science, Solar System, etc.).

* **Location:** `g:\My Drive\Flash Cards`
* **Live App URL:** `https://kuldeeptyagivet.github.io/flash-cards/`
* **Local Dev Server:** `http://localhost:8000/`
* **GitHub Repository:** `https://github.com/kuldeeptyagivet/flash-cards`

---

## 🏗️ Architecture & Component Design

### 1. Dual-View SVG Vector Maps (`decks/Countries-Capital/maps/`)
* **Zoomed Real Country Shape**: Real geographic border polygon for the selected country with a glowing capital city marker.
* **Mini World Locator Inset Map**: Positioned in the top-right corner of every SVG card, showing the entire world map with a glowing yellow/gold beacon indicating exactly where that country sits on planet Earth.

### 2. Deck Selection Hub & Search Bar (`index.html`)
* **Landing Page Hub**: Shows a prominent **Search Bar** (`🔍 Search decks...`) and grid of deck cards.
* **Deck Card**: Tapping **Countries & Capitals** loads the dataset and opens the 3D Flashcard & Quiz experience.
* **Navigation**: Includes a `← Back to Decks` button to return to the Hub anytime.

---

## 📜 Session History & Progress Log

### Session 1: 2026-08-11
* **Status:** Added Dual-View World Locator Inset Maps to all 196 flashcards.
* **Accomplished:**
  * Embedded a **Mini World Locator Inset Map** in the top-right corner of all 196 SVG vector maps.
  * Replaced initial placeholder shapes with 100% authentic, real geographical border polygons generated via Natural Earth GeoJSON vector data.
  * Re-organized dataset and vector SVG maps under `decks/Countries-Capital/`.
  * Designed and built the Home Deck Selection Hub with live search bar filtering across available decks.
  * Created public GitHub repo `kuldeeptyagivet/flash-cards` and enabled GitHub Pages at `https://kuldeeptyagivet.github.io/flash-cards/`.
  * Pushed updated code and verified live deployment.
