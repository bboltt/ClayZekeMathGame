# Minecraft Math Adventure 🎮⛏️

A fun, Minecraft-themed multiplication learning platform with spaced repetition algorithm, user authentication, and progress tracking!

## ✨ Features

### 🎯 Core Learning Features
- **Spaced Repetition Algorithm**: Based on the SM-2 algorithm for optimal learning
- **Adaptive Question Selection**: Questions adapt based on your performance
- **Progress Tracking**: Detailed statistics on accuracy, time spent, and improvement
- **User Accounts**: Each learner has their own profile and progress
- **Time Analytics**: Track how long you spend on each session

### 🎨 Minecraft Theme
- Authentic Minecraft characters (Steve, Creeper)
- Blocky, pixel-art design
- Minecraft-themed feedback messages
- Animated characters and blocks
- Grass block footer and decorative elements

### 📊 Dashboard & Analytics
- Overall accuracy percentage
- Total questions answered
- Time spent learning
- Questions due for review
- Session history
- Performance graphs

### 🏆 Achievements System
- 🪵 First Block Mined!
- 🔥 5 Block Streak
- 💎 Diamond Miner (10 streak)
- 👑 Minecraft Master (50 correct)

## 🚀 Technology Stack

**Backend:**
- Python Flask
- SQLAlchemy ORM
- PostgreSQL (production) / SQLite (development)
- Flask-Login for authentication
- Werkzeug for password hashing

**Frontend:**
- HTML5 / CSS3
- Vanilla JavaScript
- Responsive design
- No framework dependencies!

**Deployment:**
- Render.com (free tier)
- Gunicorn WSGI server
- PostgreSQL database

## 📁 Project Structure

```
ClayZekeMathGame/
├── app.py                  # Main Flask application
├── models.py               # Database models
├── requirements.txt        # Python dependencies
├── render.yaml            # Render deployment config
├── .env.example           # Environment variables template
├── templates/             # HTML templates
│   ├── base.html          # Base template
│   ├── index.html         # Landing page
│   ├── login.html         # Login page
│   ├── signup.html        # Registration page
│   ├── dashboard.html     # User dashboard
│   ├── play.html          # Main game page
│   ├── 404.html          # 404 error page
│   └── 500.html          # 500 error page
├── static/                # Static assets
│   ├── css/
│   │   └── style.css      # Minecraft-themed styles
│   └── js/
│       └── game.js        # Game logic
├── README.md             # This file
└── DEPLOYMENT_RENDER.md  # Deployment guide
```

## 🎮 How to Use

### For Users

1. **Visit the website** (deployed URL)
2. **Create an account** (username, email, password)
3. **Start playing!**
4. **Check your dashboard** to see progress
5. **Come back daily** - the spaced repetition algorithm will optimize your learning!

### For Developers

#### Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/bboltt/ClayZekeMathGame.git
   cd ClayZekeMathGame
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Run the application:**
   ```bash
   python app.py
   ```

6. **Visit:** `http://localhost:5000`

#### Running Tests

```bash
# Create a test account
python -c "from app import app, db; from models import User; app.app_context().push(); user = User(username='test', email='test@test.com'); user.set_password('test123'); db.session.add(user); db.session.commit(); print('Test user created!')"
```

## 🌐 Deployment

See [DEPLOYMENT_RENDER.md](DEPLOYMENT_RENDER.md) for complete deployment instructions to Render.com (100% FREE!).

**Quick Deploy:**
1. Push code to GitHub
2. Create Render account
3. Create PostgreSQL database
4. Create Web Service
5. Set environment variables
6. Deploy!

Your app will be live at: `https://your-app-name.onrender.com`

## 🧠 Spaced Repetition Algorithm

The app uses the **SuperMemo SM-2** algorithm:

1. **Ease Factor**: Tracks how "easy" each question is for the user
2. **Interval**: Days until next review
3. **Repetitions**: Consecutive correct answers

**How it works:**
- Answer correctly → interval increases exponentially
- Answer incorrectly → interval resets, ease factor decreases
- Questions you struggle with appear more frequently
- Mastered questions appear less often

## 📈 Future Enhancements

Planned features for future versions:
- ➕ Addition module
- ➖ Subtraction module
- ➗ Division module
- 🎯 Difficulty levels
- ⏱️ Timed challenges
- 👥 Multiplayer mode
- 📱 Mobile app
- 🎵 Sound effects
- 🌍 Leaderboards

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

Created with ❤️ for young learners everywhere!

## 🙏 Acknowledgments

- Inspired by Minecraft
- SuperMemo SM-2 algorithm for spaced repetition
- Built with Flask and modern web technologies

## 📞 Support

For issues or questions:
- Open an issue on GitHub
- Check [DEPLOYMENT_RENDER.md](DEPLOYMENT_RENDER.md) for deployment help

---

**Start learning multiplication the fun way!** 🎮⛏️💎

## Screenshots

*Coming soon! Deploy and add screenshots of:*
- Landing page
- Login page
- Dashboard
- Game interface
- Achievements

## Live Demo

After deployment, your live app will be accessible at:
```
https://your-app-name.onrender.com
```

Enjoy building knowledge, one block at a time! 🧱
