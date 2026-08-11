# Kids Educational Flashcards Web App — Project & Session Log

## 📌 Project Overview
An interactive, mobile-first educational Flash Cards application designed for kids to learn World Countries, Capitals, Maps, Flags, and future subjects (Currencies, Science, Solar System, etc.).

* **Location:** `g:\My Drive\Flash Cards`
* **Local Dev Server:** `http://localhost:8000/`
* **Target Platforms:** Mobile Browsers (iOS Safari, Android Chrome), Tablets, Desktop & Cloudflare Pages (`flash.examsindia.org`).

---

## 🏗️ Architecture & Component Design

### 1. Modular Subfolder Deck Architecture (`decks/`)
* **[`decks/Countries-Capital/data.json`](file:///g:/My%20Drive/Flash%20Cards/decks/Countries-Capital/data.json)**: Full dataset containing 196 countries, capitals, continents, ISO 2-letter codes, flag emojis, and lat/long coordinates.
* **[`decks/Countries-Capital/maps/`](file:///g:/My%20Drive/Flash%20Cards/decks/Countries-Capital/maps/)**: 196 individual SVG vector map files (`in.svg`, `us.svg`, etc.) for Countries & Capitals.
* **Future Deck Subfolders**: `decks/World-Flags/`, `decks/Solar-System/`, `decks/Currencies/`, etc.

### 2. Deck Selection Hub & Search Bar (`index.html`)
* **Landing Page Hub**: Shows a prominent **Search Bar** (`🔍 Search decks...`) and grid of deck cards.
* **Deck Card**: Tapping **Countries & Capitals** loads the dataset and opens the 3D Flashcard & Quiz experience.
* **Navigation**: Includes a `← Back to Decks` button to return to the Hub anytime.

---

## 📜 Session History & Progress Log

### Session 1: 2026-08-11
* **Status:** Completed Deck Selection Hub & `decks/Countries-Capital/` modular subfolder structure.
* **Accomplished:**
  * Re-organized dataset and vector SVG maps under `decks/Countries-Capital/`.
  * Designed and built the Home Deck Selection Hub with live search bar filtering across available decks.
  * Added "← Back to Decks" header navigation for seamless switching.
  * Tested and verified on `http://localhost:8000/`.

---

## 🚀 How to Run & Deploy

1. **Local Development:**
   Run in terminal:
   ```bash
   python -m http.server 8000 --directory "g:\My Drive\Flash Cards"
   ```
   Open `http://localhost:8000/` on mobile or desktop.

2. **Deploying to Cloudflare Pages (`flash.examsindia.org`):**
   * Log into [dash.cloudflare.com](https://dash.cloudflare.com) -> **Workers & Pages** -> **Create** -> **Pages** -> **Upload assets**.
   * Upload folder `g:\My Drive\Flash Cards`.
   * Add custom domain: `flash.examsindia.org`.
