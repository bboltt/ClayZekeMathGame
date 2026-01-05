// Minecraft Math Game - Frontend Logic
class MathGame {
    constructor() {
        this.score = 0;
        this.streak = 0;
        this.totalAnswered = 0;
        this.currentQuestion = null;
        this.sessionId = null;
        this.questionStartTime = null;
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

    async init() {
        // Start session
        await this.startSession();

        // Event listeners
        this.submitBtn.addEventListener('click', () => this.checkAnswer());
        this.newQuestionBtn.addEventListener('click', () => this.generateQuestion());
        this.answerInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.checkAnswer();
            }
        });

        // Load user stats
        await this.loadStats();

        // Generate first question
        await this.generateQuestion();
        this.answerInput.focus();

        // End session on page unload
        window.addEventListener('beforeunload', () => this.endSession());
    }

    async startSession() {
        try {
            const response = await fetch('/api/start-session', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
            const data = await response.json();
            this.sessionId = data.session_id;
        } catch (error) {
            console.error('Failed to start session:', error);
        }
    }

    async endSession() {
        if (this.sessionId) {
            try {
                await fetch('/api/end-session', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ session_id: this.sessionId })
                });
            } catch (error) {
                console.error('Failed to end session:', error);
            }
        }
    }

    async loadStats() {
        try {
            const response = await fetch('/api/stats');
            const data = await response.json();
            this.score = data.total_correct;
            this.totalAnswered = data.total_attempts;
            this.updateStats();
        } catch (error) {
            console.error('Failed to load stats:', error);
        }
    }

    async generateQuestion() {
        try {
            const response = await fetch('/api/get-question');
            const question = await response.json();

            this.currentQuestion = question;
            this.questionStartTime = Date.now();

            // Display question
            this.questionEl.textContent = `${question.num1} × ${question.num2} = ?`;

            // Clear previous answer and feedback
            this.answerInput.value = '';
            this.feedbackEl.textContent = '';
            this.feedbackEl.className = 'feedback';
            this.answerInput.focus();
        } catch (error) {
            console.error('Failed to generate question:', error);
            this.questionEl.textContent = 'Error loading question';
        }
    }

    async checkAnswer() {
        const userAnswer = parseInt(this.answerInput.value);

        // Validate input
        if (isNaN(userAnswer) || this.answerInput.value === '') {
            this.showFeedback('Please enter a number! ⛏️', false);
            return;
        }

        // Calculate response time in seconds
        const responseTime = (Date.now() - this.questionStartTime) / 1000;

        try {
            const response = await fetch('/api/submit-answer', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    question_id: this.currentQuestion.id,
                    answer: userAnswer,
                    response_time: responseTime,
                    session_id: this.sessionId
                })
            });

            const result = await response.json();
            this.totalAnswered++;

            if (result.correct) {
                this.handleCorrectAnswer(result);
            } else {
                this.handleIncorrectAnswer(result);
            }

            this.updateStats();
            this.checkAchievements();
        } catch (error) {
            console.error('Failed to submit answer:', error);
            this.showFeedback('Error submitting answer', false);
        }
    }

    handleCorrectAnswer(result) {
        this.score++;
        this.streak++;

        const messages = [
            '💎 Perfect! You mined diamonds! 💎',
            '🧱 Correct! Block placed successfully! 🧱',
            '⛏️ Great mining! Steve approves! 🧑‍🌾',
            '🟩 Excellent! Creeper defeated! 🟩',
            '🔥 You crafted the answer! 🔥',
            '⚔️ Victory! Another block conquered! ⚔️',
            '🪵 You chopped the right answer! 🪵',
            '🏰 Amazing! Castle built correctly! 🏰'
        ];

        const randomMessage = messages[Math.floor(Math.random() * messages.length)];
        let message = randomMessage;

        if (result.next_review_days > 0) {
            message += ` Next review in ${result.next_review_days} day(s)!`;
        }

        this.showFeedback(message, true);

        // Auto-generate new question after a delay
        setTimeout(() => {
            this.generateQuestion();
        }, 1500);
    }

    handleIncorrectAnswer(result) {
        this.streak = 0;

        const correctAnswer = result.correct_answer;
        const messages = [
            `🟩 Creeper says: It's ${correctAnswer}! Try again! 🟩`,
            `⛏️ Wrong block! The answer is ${correctAnswer}. Keep mining! ⛏️`,
            `🧱 Oops! Break block ${correctAnswer} instead! 🧱`,
            `🧑‍🌾 Steve says: It's ${correctAnswer}. Keep crafting! 🧑‍🌾`,
            `🔴 Block not found! The answer is ${correctAnswer}! 🔴`
        ];

        const randomMessage = messages[Math.floor(Math.random() * messages.length)];
        this.showFeedback(randomMessage, false);
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
            this.unlockAchievement(achievementElements[0], '🪵 First Block Mined!');
        }

        // Streak of 5
        if (!this.achievements.streak5 && this.streak >= 5) {
            this.achievements.streak5 = true;
            this.unlockAchievement(achievementElements[1], '🔥 5 Block Streak');
        }

        // Streak of 10
        if (!this.achievements.streak10 && this.streak >= 10) {
            this.achievements.streak10 = true;
            this.unlockAchievement(achievementElements[2], '💎 Diamond Miner (10)');
        }

        // Master - 50 correct
        if (!this.achievements.master50 && this.score >= 50) {
            this.achievements.master50 = true;
            this.unlockAchievement(achievementElements[3], '👑 Minecraft Master (50)');
        }
    }

    unlockAchievement(element, text) {
        element.textContent = text;
        element.classList.remove('locked');
        element.classList.add('unlocked');
    }
}

// Initialize game when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const game = new MathGame();
    console.log('🎮 Minecraft Math Game Loaded! Good luck! ⛏️');
});
