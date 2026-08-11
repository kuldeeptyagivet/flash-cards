/* Flash Cards Core App Controller */
document.addEventListener('DOMContentLoaded', () => {
  let fullDataset = [];
  let currentDeck = [];
  let currentIndex = 0;
  let activeMapsPath = 'decks/Countries-Capital/maps/';
  let starredSet = new Set(JSON.parse(localStorage.getItem('starred_countries') || '[]'));
  let quizInstance = null;

  // DOM Elements
  const deckHubView = document.getElementById('deckHubView');
  const flashcardStage = document.getElementById('flashcardStage');
  const quizStage = document.getElementById('quizStage');
  const backDecksBtn = document.getElementById('backDecksBtn');
  const modeSwitcher = document.getElementById('modeSwitcher');
  const filterBar = document.getElementById('filterBar');
  const deckSearchInput = document.getElementById('deckSearchInput');
  const homeLogoBtn = document.getElementById('homeLogoBtn');

  const cardWrapper = document.getElementById('cardWrapper');
  const countryNameEl = document.getElementById('countryName');
  const flagEmojiEl = document.getElementById('flagEmoji');
  const continentBadgeEl = document.getElementById('continentBadge');
  const capitalNameEl = document.getElementById('capitalName');
  const cardMapEl = document.getElementById('cardMap');
  const cardCounterEl = document.getElementById('cardCounter');
  const starBtn = document.getElementById('starBtn');
  const speakFrontBtn = document.getElementById('speakFrontBtn');
  const speakBackBtn = document.getElementById('speakBackBtn');
  
  const prevBtn = document.getElementById('prevBtn');
  const nextBtn = document.getElementById('nextBtn');
  
  const filterChips = document.querySelectorAll('.filter-chip');
  const modeBtns = document.querySelectorAll('.mode-btn');

  // Deck Hub Search Filter
  if (deckSearchInput) {
    deckSearchInput.addEventListener('input', (e) => {
      const query = e.target.value.toLowerCase().trim();
      const deckCards = document.querySelectorAll('.deck-card');
      deckCards.forEach(card => {
        const text = card.textContent.toLowerCase();
        if (text.includes(query)) {
          card.style.display = 'flex';
        } else {
          card.style.display = 'none';
        }
      });
    });
  }

  // Open Deck
  const deckCards = document.querySelectorAll('.deck-card[data-deck-path]');
  deckCards.forEach(card => {
    card.addEventListener('click', () => {
      const dataPath = card.dataset.deckPath;
      activeMapsPath = card.dataset.mapsPath || 'decks/Countries-Capital/maps/';
      loadDeck(dataPath);
    });
  });

  function loadDeck(dataPath) {
    fetch(dataPath)
      .then(res => res.json())
      .then(data => {
        fullDataset = data;
        currentDeck = [...fullDataset];
        quizInstance = new QuizEngine(fullDataset);
        
        // Show Flashcards View
        deckHubView.style.display = 'none';
        flashcardStage.style.display = 'flex';
        backDecksBtn.style.display = 'flex';
        modeSwitcher.style.display = 'flex';
        filterBar.style.display = 'flex';
        
        renderCard(0);
      })
      .catch(err => console.error("Error loading deck data:", err));
  }

  // Back to Decks Hub
  function showHomeHub() {
    deckHubView.style.display = 'flex';
    flashcardStage.style.display = 'none';
    quizStage.classList.remove('active');
    backDecksBtn.style.display = 'none';
    modeSwitcher.style.display = 'none';
    filterBar.style.display = 'none';
  }

  if (backDecksBtn) backDecksBtn.addEventListener('click', showHomeHub);
  if (homeLogoBtn) homeLogoBtn.addEventListener('click', showHomeHub);

  // Render Card
  function renderCard(index) {
    if (!currentDeck.length) {
      countryNameEl.textContent = "No cards found";
      capitalNameEl.textContent = "N/A";
      flagEmojiEl.textContent = "❓";
      cardCounterEl.textContent = "0 / 0";
      cardMapEl.src = "";
      return;
    }

    currentIndex = (index + currentDeck.length) % currentDeck.length;
    const item = currentDeck[currentIndex];

    // Reset flip
    cardWrapper.classList.remove('flipped');

    // Populate text
    countryNameEl.textContent = item.country;
    flagEmojiEl.textContent = item.flag;
    continentBadgeEl.textContent = item.continent;
    capitalNameEl.textContent = item.capital;
    cardCounterEl.textContent = `${currentIndex + 1} / ${currentDeck.length}`;

    // Load SVG Map from subfolder
    cardMapEl.src = `${activeMapsPath}${item.iso}.svg`;

    // Star state
    if (starredSet.has(item.iso)) {
      starBtn.classList.add('starred');
      starBtn.textContent = '★';
    } else {
      starBtn.classList.remove('starred');
      starBtn.textContent = '☆';
    }
  }

  // Flip Card
  cardWrapper.addEventListener('click', (e) => {
    if (e.target.closest('.action-btn')) return;
    cardWrapper.classList.toggle('flipped');
  });

  // Navigation
  prevBtn.addEventListener('click', () => renderCard(currentIndex - 1));
  nextBtn.addEventListener('click', () => renderCard(currentIndex + 1));

  // Touch Swipe Gestures
  let touchStartX = 0;
  cardWrapper.addEventListener('touchstart', (e) => {
    touchStartX = e.changedTouches[0].screenX;
  }, { passive: true });

  cardWrapper.addEventListener('touchend', (e) => {
    let touchEndX = e.changedTouches[0].screenX;
    if (touchStartX - touchEndX > 50) {
      renderCard(currentIndex + 1); // Swipe left -> Next
    } else if (touchEndX - touchStartX > 50) {
      renderCard(currentIndex - 1); // Swipe right -> Prev
    }
  }, { passive: true });

  // Star / Bookmark Toggle
  starBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    const item = currentDeck[currentIndex];
    if (!item) return;

    if (starredSet.has(item.iso)) {
      starredSet.delete(item.iso);
    } else {
      starredSet.add(item.iso);
    }
    localStorage.setItem('starred_countries', JSON.stringify([...starredSet]));
    renderCard(currentIndex);
  });

  // Audio Speech Pronunciation
  speakFrontBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    const item = currentDeck[currentIndex];
    if (item && window.speechEngine) {
      window.speechEngine.speak(item.country);
    }
  });

  speakBackBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    const item = currentDeck[currentIndex];
    if (item && window.speechEngine) {
      window.speechEngine.speak(item.capital);
    }
  });

  // Filter Chips (Continents & Starred)
  filterChips.forEach(chip => {
    chip.addEventListener('click', () => {
      filterChips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');

      const filter = chip.dataset.filter;
      if (filter === 'all') {
        currentDeck = [...fullDataset];
      } else if (filter === 'starred') {
        currentDeck = fullDataset.filter(item => starredSet.has(item.iso));
      } else {
        currentDeck = fullDataset.filter(item => item.continent === filter);
      }
      renderCard(0);
    });
  });

  // Mode Switcher (Cards vs Quiz)
  modeBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      modeBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const mode = btn.dataset.mode;
      if (mode === 'cards') {
        flashcardStage.style.display = 'flex';
        quizStage.classList.remove('active');
        renderCard(currentIndex);
      } else if (mode === 'quiz') {
        flashcardStage.style.display = 'none';
        quizStage.classList.add('active');
        loadNextQuizQuestion();
      }
    });
  });

  // Quiz Mode Logic
  function loadNextQuizQuestion() {
    if (!quizInstance) return;
    const q = quizInstance.generateQuestion();
    if (!q) return;

    document.getElementById('quizCountryName').textContent = `${q.flag} ${q.country}`;
    document.getElementById('quizScore').textContent = `Score: ${quizInstance.score} ⭐`;
    document.getElementById('quizStreak').textContent = `Streak: ${quizInstance.streak} 🔥`;

    const optionsContainer = document.getElementById('quizOptions');
    optionsContainer.innerHTML = '';

    q.options.forEach(opt => {
      const optBtn = document.createElement('button');
      optBtn.className = 'option-btn';
      optBtn.textContent = opt;

      optBtn.addEventListener('click', () => {
        const isCorrect = quizInstance.checkAnswer(opt);
        if (isCorrect) {
          optBtn.classList.add('correct');
          if (window.speechEngine) window.speechEngine.speak("Correct! " + opt);
        } else {
          optBtn.classList.add('wrong');
          if (window.speechEngine) window.speechEngine.speak("Oops! The capital is " + q.correctCapital);
        }

        // Disable all buttons after pick
        const allBtns = optionsContainer.querySelectorAll('.option-btn');
        allBtns.forEach(b => {
          b.disabled = true;
          if (b.textContent === q.correctCapital) {
            b.classList.add('correct');
          }
        });

        // Load next question after delay
        setTimeout(() => loadNextQuizQuestion(), 1600);
      });

      optionsContainer.appendChild(optBtn);
    });
  }
});
