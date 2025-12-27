# Deployment Guide

This guide will help you deploy the Minecraft Math Adventure game to the web using GitHub Pages.

## Quick Deployment Steps

### Option 1: Deploy from Branch Directly (Easiest - Recommended)

Deploy directly from the current branch:

1. **Go to Repository Settings:**
   - Navigate to your GitHub repository
   - Click "Settings" → "Pages"

2. **Configure Source:**
   - Under "Source", select "Deploy from a branch"
   - Choose your branch: `claude/minecraft-math-game-HzS8q`
   - Select folder: `/ (root)`
   - Click "Save"

3. **Wait for deployment:**
   - GitHub will automatically build and deploy
   - Your site will be available at: `https://bboltt.github.io/ClayZekeMathGame/`

### Option 2: Deploy via Main Branch (Using GitHub Actions)

For automatic deployment using GitHub Actions:

1. **Create and merge to main branch via GitHub:**
   - Go to your repository on GitHub
   - Click "Pull requests" → "New pull request"
   - Set base to `main` and compare to `claude/minecraft-math-game-HzS8q`
   - Create and merge the pull request

2. **Enable GitHub Pages:**
   - Go to repository "Settings" → "Pages"
   - Under "Source", select "GitHub Actions"
   - The workflow will automatically deploy

3. **Access your game:**
   - Your site will be live at: `https://bboltt.github.io/ClayZekeMathGame/`

## Verification

After deployment:
1. Visit your GitHub Pages URL
2. You should see the Minecraft Math Adventure game
3. Test the multiplication questions
4. Try answering correctly and incorrectly to verify feedback
5. Check that achievements unlock properly

## Updating the Game

To update the deployed game:
1. Make changes to your files
2. Commit and push to the branch
3. GitHub Pages will automatically rebuild (if using Actions)
4. Changes will be live in a few minutes

## Custom Domain (Optional)

To use a custom domain:
1. Add a `CNAME` file with your domain name
2. Configure DNS settings with your domain provider
3. Update GitHub Pages settings to use custom domain

## Troubleshooting

**Game not loading:**
- Check that all files (index.html, styles.css, game.js) are in the root directory
- Verify GitHub Pages is enabled in repository settings
- Check browser console for errors

**Changes not appearing:**
- Wait 2-3 minutes for GitHub Pages to rebuild
- Clear browser cache (Ctrl+Shift+R or Cmd+Shift+R)
- Check that files are properly committed and pushed

**404 Error:**
- Ensure repository is public (or you have GitHub Pro for private repos)
- Verify the correct branch is selected in Pages settings
- Check that index.html exists in the root directory

## Repository Structure

```
ClayZekeMathGame/
├── index.html          # Main game page
├── styles.css          # Minecraft-themed styling
├── game.js            # Game logic
├── README.md          # Project documentation
├── DEPLOYMENT.md      # This file
└── .github/
    └── workflows/
        └── deploy.yml # GitHub Actions deployment workflow
```

Enjoy sharing your math game with your child! 🎮⛏️
