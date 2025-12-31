# Deployment Guide - Render.com

Complete guide to deploy Minecraft Math Adventure to Render (100% FREE tier available!)

## Prerequisites

- GitHub account
- Render account (sign up at https://render.com - free!)
- Your code pushed to GitHub repository

## Step-by-Step Deployment

### 1. Push Your Code to GitHub

Make sure all files are committed and pushed to your GitHub repository:

```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

### 2. Create a Render Account

1. Go to https://render.com
2. Click "Get Started" or "Sign Up"
3. **Sign up with GitHub** (easiest method)
4. Authorize Render to access your repositories

### 3. Create PostgreSQL Database

1. In Render Dashboard, click "New +" → "PostgreSQL"
2. Fill in:
   - **Name**: `minecraft-math-db`
   - **Database**: `minecraft_math`
   - **User**: `minecraft_user`
   - **Region**: Choose closest to you
   - **Plan**: **Free** ✅
3. Click "Create Database"
4. Wait 2-3 minutes for database to be created
5. **Copy the "Internal Database URL"** - you'll need this!

### 4. Create Web Service

1. Click "New +" → "Web Service"
2. Click "Build and deploy from a Git repository"
3. Select your repository: `ClayZekeMathGame`
4. Click "Connect"

5. **Configure the service:**
   - **Name**: `minecraft-math-game` (or your choice - this becomes your URL!)
   - **Region**: Same as your database
   - **Branch**: `main`
   - **Root Directory**: (leave empty)
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: **Free** ✅

6. **Add Environment Variables:**
   Click "Advanced" → "Add Environment Variable"

   Add these:
   - **SECRET_KEY**: Click "Generate" button (Render creates a secure random key)
   - **DATABASE_URL**: Paste the Internal Database URL you copied earlier

7. Click "Create Web Service"

### 5. Wait for Deployment

- First deployment takes 3-5 minutes
- Watch the logs in real-time
- You'll see messages like:
  ```
  ✅ Database initialized!
  ✅ Initialized 81 multiplication questions
  ```

### 6. Get Your URL!

Once deployment succeeds, you'll see:

```
🎉 Your app is live at: https://minecraft-math-game.onrender.com
```

**That's your URL!** Share it with anyone!

## Testing Your Deployment

1. Visit your URL: `https://your-app-name.onrender.com`
2. Click "Start Learning" to create an account
3. Sign up with a test account
4. Play a few questions
5. Check the dashboard

## Important Notes

### Free Tier Limitations

✅ **Completely Free**
✅ **Unlimited users**
✅ **PostgreSQL database included**

⚠️ **Cold Starts:**
- App sleeps after 15 minutes of inactivity
- First visit after sleep: 30-60 second wait
- After that: instant until it sleeps again

### Keeping Your App Awake (Optional)

If you want to avoid cold starts, you have options:

**Option 1: Upgrade to Paid ($7/month)**
- No cold starts
- Always instant
- More resources

**Option 2: Use a Ping Service (Free)**
- Use services like UptimeRobot or Cron-job.org
- Ping your app every 14 minutes
- Keeps it awake during active hours

## Updating Your App

When you make changes:

1. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Update feature"
   git push origin main
   ```

2. Render automatically detects changes and redeploys!
3. Wait 2-3 minutes for new version to be live

## Monitoring

### View Logs
1. Go to Render Dashboard
2. Click on your web service
3. Click "Logs" tab
4. See real-time application logs

### Check Database
1. Click on your database in Dashboard
2. View connection info
3. Monitor usage

## Troubleshooting

### App Won't Start

**Check logs for errors:**
- Missing dependencies? Update `requirements.txt`
- Database connection error? Verify DATABASE_URL is set correctly

### Database Issues

**Reset database (WARNING: Deletes all data):**
1. Go to database in Dashboard
2. Click "Delete Database"
3. Create new database
4. Update DATABASE_URL in web service

### App is Slow

**First load after sleep:**
- Normal! Free tier sleeps after 15min
- Subsequent loads are fast

**Always slow:**
- Check logs for errors
- Database might need indexing (already done in our code!)

## Custom Domain (Optional)

Want `mathgame.com` instead of `.onrender.com`?

1. Buy a domain (Namecheap, Google Domains, etc.)
2. In Render Dashboard → your service → "Settings"
3. Add custom domain
4. Update DNS records at your domain provider
5. Render handles SSL automatically!

## Security Best Practices

✅ **Already implemented:**
- Password hashing
- SQL injection protection (SQLAlchemy)
- CSRF protection
- Secure session management

🔒 **Additional tips:**
- Never commit `.env` file (already in .gitignore)
- Use Render's generated SECRET_KEY
- Regularly update dependencies

## Cost Breakdown

| Resource | Plan | Cost |
|----------|------|------|
| Web Service | Free | $0 |
| PostgreSQL | Free | $0 |
| **TOTAL** | | **$0/month** |

For personal/educational use with your child, the free tier is perfect!

## Support

- **Render Docs**: https://render.com/docs
- **Flask Docs**: https://flask.palletsprojects.com/
- **PostgreSQL Docs**: https://www.postgresql.org/docs/

## Your Live URLs

After deployment, your URLs will be:
- **Game**: `https://your-app-name.onrender.com`
- **Login**: `https://your-app-name.onrender.com/login`
- **Signup**: `https://your-app-name.onrender.com/signup`
- **Dashboard**: `https://your-app-name.onrender.com/dashboard`
- **Play**: `https://your-app-name.onrender.com/play`

## Next Steps

1. Share the URL with your child
2. Have them create an account
3. Start learning multiplication!
4. Check their progress in the dashboard
5. Watch the spaced repetition algorithm work its magic!

Enjoy your FREE Minecraft Math Adventure! 🎮⛏️💎
