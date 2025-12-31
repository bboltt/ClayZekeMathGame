"""
Database models for Minecraft Math Adventure
"""
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User account model"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    progress = db.relationship('QuestionProgress', backref='user', lazy=True, cascade='all, delete-orphan')
    sessions = db.relationship('GameSession', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class Question(db.Model):
    """Math question model"""
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    num1 = db.Column(db.Integer, nullable=False)
    num2 = db.Column(db.Integer, nullable=False)
    operation = db.Column(db.String(20), nullable=False, default='multiplication')
    answer = db.Column(db.Integer, nullable=False)

    # Relationships
    progress = db.relationship('QuestionProgress', backref='question', lazy=True)

    def __repr__(self):
        return f'<Question {self.num1}×{self.num2}={self.answer}>'


class QuestionProgress(db.Model):
    """Track user progress on individual questions with spaced repetition"""
    __tablename__ = 'question_progress'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)

    # Spaced Repetition Algorithm (SM-2)
    ease_factor = db.Column(db.Float, default=2.5)  # Difficulty multiplier
    interval = db.Column(db.Integer, default=0)  # Days until next review
    repetitions = db.Column(db.Integer, default=0)  # Consecutive correct answers

    # Statistics
    total_attempts = db.Column(db.Integer, default=0)
    correct_count = db.Column(db.Integer, default=0)
    wrong_count = db.Column(db.Integer, default=0)

    # Timing
    last_reviewed = db.Column(db.DateTime)
    next_review = db.Column(db.DateTime, default=datetime.utcnow)
    average_response_time = db.Column(db.Float, default=0.0)  # Seconds

    # Indexes for efficient querying
    __table_args__ = (
        db.Index('idx_user_next_review', 'user_id', 'next_review'),
    )

    def update_after_answer(self, is_correct, response_time):
        """Update progress using SM-2 spaced repetition algorithm"""
        self.total_attempts += 1

        # Update average response time
        if self.average_response_time == 0:
            self.average_response_time = response_time
        else:
            self.average_response_time = (self.average_response_time + response_time) / 2

        if is_correct:
            self.correct_count += 1
            self.repetitions += 1

            # Calculate next interval based on SM-2 algorithm
            if self.repetitions == 1:
                self.interval = 1
            elif self.repetitions == 2:
                self.interval = 6
            else:
                self.interval = int(self.interval * self.ease_factor)

            # Update ease factor
            quality = 4  # Good answer (0-5 scale)
            self.ease_factor = max(1.3, self.ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)))

        else:
            self.wrong_count += 1
            self.repetitions = 0
            self.interval = 0
            self.ease_factor = max(1.3, self.ease_factor - 0.2)

        self.last_reviewed = datetime.utcnow()
        self.next_review = datetime.utcnow() + timedelta(days=self.interval)

    def __repr__(self):
        return f'<QuestionProgress user={self.user_id} question={self.question_id}>'


class GameSession(db.Model):
    """Track user game sessions for time analytics"""
    __tablename__ = 'game_sessions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    ended_at = db.Column(db.DateTime)
    questions_answered = db.Column(db.Integer, default=0)
    correct_answers = db.Column(db.Integer, default=0)

    def duration_minutes(self):
        """Calculate session duration in minutes"""
        if self.ended_at:
            delta = self.ended_at - self.started_at
            return delta.total_seconds() / 60
        return 0

    def __repr__(self):
        return f'<GameSession user={self.user_id} at={self.started_at}>'
