"""
Minecraft Math Adventure - Flask Application
A spaced-repetition based math learning platform with Minecraft theme
"""
import os
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Question, QuestionProgress, GameSession
from sqlalchemy import func
import random

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'minecraft-math-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///minecraft_math.db')

# Fix for Render.com PostgreSQL URL
if app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgres://'):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ============================================================================
# Database Initialization
# ============================================================================

def init_questions():
    """Initialize multiplication questions (1-9 × 1-9)"""
    if Question.query.count() == 0:
        questions = []
        for num1 in range(1, 10):
            for num2 in range(1, 10):
                question = Question(
                    num1=num1,
                    num2=num2,
                    operation='multiplication',
                    answer=num1 * num2
                )
                questions.append(question)
        db.session.bulk_save_objects(questions)
        db.session.commit()
        print("✅ Initialized 81 multiplication questions")


# ============================================================================
# Authentication Routes
# ============================================================================

@app.route('/')
def index():
    """Landing page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        # Validation
        if not username or not email or not password:
            flash('All fields are required!', 'error')
            return render_template('signup.html')

        if len(password) < 6:
            flash('Password must be at least 6 characters!', 'error')
            return render_template('signup.html')

        # Check if user exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'error')
            return render_template('signup.html')

        if User.query.filter_by(email=email).first():
            flash('Email already registered!', 'error')
            return render_template('signup.html')

        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash(f'Welcome to Minecraft Math, {username}!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user, remember=True)
            flash(f'Welcome back, {username}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password!', 'error')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out!', 'info')
    return redirect(url_for('index'))


# ============================================================================
# Game Routes
# ============================================================================

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard with statistics"""
    # Get user statistics
    total_questions = QuestionProgress.query.filter_by(user_id=current_user.id).count()
    total_attempts = db.session.query(func.sum(QuestionProgress.total_attempts)).filter_by(user_id=current_user.id).scalar() or 0
    total_correct = db.session.query(func.sum(QuestionProgress.correct_count)).filter_by(user_id=current_user.id).scalar() or 0
    total_wrong = db.session.query(func.sum(QuestionProgress.wrong_count)).filter_by(user_id=current_user.id).scalar() or 0

    # Calculate accuracy
    accuracy = (total_correct / total_attempts * 100) if total_attempts > 0 else 0

    # Get recent sessions
    recent_sessions = GameSession.query.filter_by(user_id=current_user.id).order_by(GameSession.started_at.desc()).limit(5).all()

    # Total time spent
    total_time_minutes = sum(s.duration_minutes() for s in GameSession.query.filter_by(user_id=current_user.id).all())

    # Questions due for review
    questions_due = QuestionProgress.query.filter(
        QuestionProgress.user_id == current_user.id,
        QuestionProgress.next_review <= datetime.utcnow()
    ).count()

    stats = {
        'total_questions_practiced': total_questions,
        'total_attempts': total_attempts,
        'total_correct': total_correct,
        'total_wrong': total_wrong,
        'accuracy': round(accuracy, 1),
        'total_time_minutes': round(total_time_minutes, 1),
        'questions_due': questions_due,
        'recent_sessions': recent_sessions
    }

    return render_template('dashboard.html', stats=stats, user=current_user)


@app.route('/play')
@login_required
def play():
    """Main game page"""
    return render_template('play.html', user=current_user)


@app.route('/mistakes')
@login_required
def review_mistakes():
    """Review questions answered incorrectly"""
    # Get all questions with at least one wrong answer
    mistakes = QuestionProgress.query.filter(
        QuestionProgress.user_id == current_user.id,
        QuestionProgress.wrong_count > 0
    ).order_by(QuestionProgress.wrong_count.desc()).all()

    return render_template('mistakes.html', mistakes=mistakes, user=current_user)


# ============================================================================
# API Routes
# ============================================================================

@app.route('/api/start-session', methods=['POST'])
@login_required
def start_session():
    """Start a new game session"""
    session = GameSession(user_id=current_user.id)
    db.session.add(session)
    db.session.commit()
    return jsonify({'session_id': session.id})


@app.route('/api/end-session', methods=['POST'])
@login_required
def end_session():
    """End current game session"""
    session_id = request.json.get('session_id')
    session = GameSession.query.get(session_id)
    if session and session.user_id == current_user.id:
        session.ended_at = datetime.utcnow()
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'error': 'Session not found'}), 404


@app.route('/api/get-question', methods=['GET'])
@login_required
def get_question():
    """Get next question using spaced repetition algorithm"""
    # First, try to get questions due for review
    due_progress = QuestionProgress.query.filter(
        QuestionProgress.user_id == current_user.id,
        QuestionProgress.next_review <= datetime.utcnow()
    ).order_by(QuestionProgress.next_review).first()

    if due_progress:
        question = due_progress.question
    else:
        # Get a new question or one with low accuracy
        practiced_question_ids = [p.question_id for p in QuestionProgress.query.filter_by(user_id=current_user.id).all()]

        # Try to find an unpracticed question
        unpracticed = Question.query.filter(~Question.id.in_(practiced_question_ids)).first() if practiced_question_ids else None

        if unpracticed:
            question = unpracticed
        else:
            # Get a question with low accuracy
            weak_progress = QuestionProgress.query.filter_by(user_id=current_user.id).order_by(
                (QuestionProgress.correct_count / (QuestionProgress.total_attempts + 1))
            ).first()

            if weak_progress:
                question = weak_progress.question
            else:
                # Fallback: random question
                question = Question.query.order_by(func.random()).first()

    return jsonify({
        'id': question.id,
        'num1': question.num1,
        'num2': question.num2,
        'operation': question.operation
    })


@app.route('/api/submit-answer', methods=['POST'])
@login_required
def submit_answer():
    """Submit answer and update progress"""
    data = request.json
    question_id = data.get('question_id')
    user_answer = data.get('answer')
    response_time = data.get('response_time', 0)  # Seconds
    session_id = data.get('session_id')

    question = Question.query.get(question_id)
    if not question:
        return jsonify({'error': 'Question not found'}), 404

    is_correct = (user_answer == question.answer)

    # Get or create progress record
    progress = QuestionProgress.query.filter_by(
        user_id=current_user.id,
        question_id=question_id
    ).first()

    if not progress:
        progress = QuestionProgress(
            user_id=current_user.id,
            question_id=question_id
        )
        db.session.add(progress)

    # Update progress with spaced repetition
    progress.update_after_answer(is_correct, response_time)

    # Update session statistics
    if session_id:
        session = GameSession.query.get(session_id)
        if session and session.user_id == current_user.id:
            session.questions_answered += 1
            if is_correct:
                session.correct_answers += 1

    db.session.commit()

    return jsonify({
        'correct': is_correct,
        'correct_answer': question.answer,
        'next_review_days': progress.interval
    })


@app.route('/api/stats', methods=['GET'])
@login_required
def get_stats():
    """Get current user statistics"""
    total_correct = db.session.query(func.sum(QuestionProgress.correct_count)).filter_by(user_id=current_user.id).scalar() or 0
    total_attempts = db.session.query(func.sum(QuestionProgress.total_attempts)).filter_by(user_id=current_user.id).scalar() or 0

    return jsonify({
        'total_correct': total_correct,
        'total_attempts': total_attempts,
        'username': current_user.username
    })


# ============================================================================
# Error Handlers
# ============================================================================

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


# ============================================================================
# Initialize Database
# ============================================================================

with app.app_context():
    db.create_all()
    init_questions()
    print("✅ Database initialized!")


# ============================================================================
# Run Application
# ============================================================================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
