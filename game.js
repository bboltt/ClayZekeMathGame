// Minecraft Math Game - Multiplication Module
class MathGame {
    constructor() {
        this.score = 0;
        this.streak = 0;
        this.totalAnswered = 0;
        this.currentQuestion = null;
        this.achievements = {
            firstCorrect: false,
            streak5: false,
            streak10: false,
            master50: false
        };

        // DOM elements
        this.questionEl = document.getElementById('question');
        this.answerInput = document.getElementById('answer-input');
        this.submitBtn = document.getElementById('submit-btn');
        this.newQuestionBtn = document.getElementById('new-question-btn');
        this.feedbackEl = document.getElementById('feedback');
        this.scoreEl = document.getElementById('score');
        this.streakEl = document.getElementById('streak');
        this.totalEl = document.getElementById('total');
        this.achievementList = document.getElementById('achievement-list');

        this.init();
    }

    init() {
        // Event listeners
        this.submitBtn.addEventListener('click', () => this.checkAnswer());
        this.newQuestionBtn.addEventListener('click', () => this.generateQuestion());
        this.answerInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.checkAnswer();
            }
        });

        // Generate first question
        this.generateQuestion();
        this.answerInput.focus();
    }

    generateQuestion() {
        // Generate random single-digit numbers (1-9)
        const num1 = Math.floor(Math.random() * 9) + 1;
        const num2 = Math.floor(Math.random() * 9) + 1;

        this.currentQuestion = {
            num1: num1,
            num2: num2,
            answer: num1 * num2
        };

        // Display question
        this.questionEl.textContent = `${num1} × ${num2} = ?`;

        // Clear previous answer and feedback
        this.answerInput.value = '';
        this.feedbackEl.textContent = '';
        this.feedbackEl.className = 'feedback';
        this.answerInput.focus();
    }

    checkAnswer() {
        const userAnswer = parseInt(this.answerInput.value);

        // Validate input
        if (isNaN(userAnswer) || this.answerInput.value === '') {
            this.showFeedback('Please enter a number! ⛏️', false);
            return;
        }

        this.totalAnswered++;
        this.updateStats();

        if (userAnswer === this.currentQuestion.answer) {
            this.handleCorrectAnswer();
        } else {
            this.handleIncorrectAnswer();
        }
    }

    handleCorrectAnswer() {
        this.score++;
        this.streak++;
        this.updateStats();

        const messages = [
            '✨ Awesome! You mined a diamond! 💎',
            '🎉 Correct! You built a masterpiece! 🏰',
            '⭐ Great job! Steve is proud! 🎮',
            '🔥 Perfect! You defeated the Creeper! 💚',
            '🌟 Excellent! You found the treasure! 🗝️',
            '👏 Amazing! You crafted success! ⚒️'
        ];

        const randomMessage = messages[Math.floor(Math.random() * messages.length)];
        this.showFeedback(randomMessage, true);

        // Check achievements
        this.checkAchievements();

        // Auto-generate new question after a delay
        setTimeout(() => {
            this.generateQuestion();
        }, 1500);
    }

    handleIncorrectAnswer() {
        this.streak = 0;
        this.updateStats();

        const correctAnswer = this.currentQuestion.answer;
        const messages = [
            `💥 Oops! The answer is ${correctAnswer}. Try again! 🎯`,
            `🧨 Not quite! It's ${correctAnswer}. Keep mining! ⛏️`,
            `❌ The answer is ${correctAnswer}. Don't give up! 💪`,
            `🔴 Close! The correct answer is ${correctAnswer}. 🎮`
        ];

        const randomMessage = messages[Math.floor(Math.random() * messages.length)];
        this.showFeedback(randomMessage, false);

        // Keep the same question visible for learning
        // User can click "New Question" when ready
    }

    showFeedback(message, isCorrect) {
        this.feedbackEl.textContent = message;
        this.feedbackEl.className = `feedback ${isCorrect ? 'correct' : 'incorrect'}`;
    }

    updateStats() {
        this.scoreEl.textContent = this.score;
        this.streakEl.textContent = this.streak;
        this.totalEl.textContent = this.totalAnswered;
    }

    checkAchievements() {
        const achievementElements = this.achievementList.children;

        // First Correct
        if (!this.achievements.firstCorrect && this.score >= 1) {
            this.achievements.firstCorrect = true;
            this.unlockAchievement(achievementElements[0], '🌟 First Correct!');
        }

        // Streak of 5
        if (!this.achievements.streak5 && this.streak >= 5) {
            this.achievements.streak5 = true;
            this.unlockAchievement(achievementElements[1], '🔥 Streak of 5');
        }

        // Streak of 10
        if (!this.achievements.streak10 && this.streak >= 10) {
            this.achievements.streak10 = true;
            this.unlockAchievement(achievementElements[2], '💎 Streak of 10');
        }

        // Master - 50 correct
        if (!this.achievements.master50 && this.score >= 50) {
            this.achievements.master50 = true;
            this.unlockAchievement(achievementElements[3], '👑 Master (50 correct)');
        }
    }

    unlockAchievement(element, text) {
        element.textContent = text;
        element.classList.remove('locked');
        element.classList.add('unlocked');

        // Play achievement sound effect (visual feedback)
        setTimeout(() => {
            element.style.transform = 'scale(1)';
        }, 500);
    }
}

// Initialize game when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const game = new MathGame();
    console.log('🎮 Minecraft Math Game Loaded! Good luck! ⛏️');
});
