/* Quiz Mode Engine */
class QuizEngine {
  constructor(dataset) {
    this.dataset = dataset;
    this.score = 0;
    this.streak = 0;
    this.currentQuestion = null;
  }

  generateQuestion() {
    if (!this.dataset || this.dataset.length < 4) return null;

    // Pick random target country
    const target = this.dataset[Math.floor(Math.random() * this.dataset.length)];
    
    // Pick 3 wrong options
    const wrongOptions = [];
    while (wrongOptions.length < 3) {
      const candidate = this.dataset[Math.floor(Math.random() * this.dataset.length)];
      if (candidate.iso !== target.iso && !wrongOptions.includes(candidate.capital)) {
        wrongOptions.push(candidate.capital);
      }
    }

    // Shuffle options
    const options = [target.capital, ...wrongOptions].sort(() => 0.5 - Math.random());

    this.currentQuestion = {
      country: target.country,
      flag: target.flag,
      correctCapital: target.capital,
      iso: target.iso,
      options: options
    };

    return this.currentQuestion;
  }

  checkAnswer(selectedCapital) {
    if (!this.currentQuestion) return false;
    const isCorrect = selectedCapital === this.currentQuestion.correctCapital;
    if (isCorrect) {
      this.score += 10;
      this.streak += 1;
    } else {
      this.streak = 0;
    }
    return isCorrect;
  }
}
