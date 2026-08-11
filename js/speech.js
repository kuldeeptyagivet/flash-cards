/* Web Speech API Audio Pronunciation Module */
class SpeechEngine {
  constructor() {
    this.synth = window.speechSynthesis;
    this.isSupported = 'speechSynthesis' in window;
  }

  speak(text, lang = 'en-US') {
    if (!this.isSupported) {
      console.warn("Speech Synthesis is not supported in this browser.");
      return;
    }

    // Cancel any ongoing speech
    this.synth.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = lang;
    utterance.rate = 0.9; // Slightly slower for kids to hear clearly
    utterance.pitch = 1.0;

    this.synth.speak(utterance);
  }
}

window.speechEngine = new SpeechEngine();
