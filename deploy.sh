#!/bin/bash

# Health Monitor Deployment Script
echo "🚀 Health Monitor Deployment Setup"
echo "=================================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📝 Initializing Git repository..."
    git init
    echo "tempt.py" > .gitignore
    echo "Dockerfile" >> .gitignore
    echo ".dockerignore" >> .gitignore
    echo "railway.json" >> .gitignore
    echo "render.yaml" >> .gitignore
    echo "README_DEPLOYMENT.md" >> .gitignore
    echo "deploy.sh" >> .gitignore
fi

# Create a clean deployment directory
echo "📁 Creating deployment directory..."
mkdir -p health-monitor-deploy
cd health-monitor-deploy

# Copy necessary files
cp ../tempt.py .
cp ../Dockerfile .
cp ../.dockerignore .
cp ../railway.json .
cp ../render.yaml .
cp ../README_DEPLOYMENT.md ./README.md

# Create .gitignore for deployment
cat > .gitignore << EOF
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
.venv/
venv/
.DS_Store
*.log
EOF

# Initialize git if needed
if [ ! -d ".git" ]; then
    git init
    git add .
    git commit -m "Initial commit: Health Monitor App"
fi

echo ""
echo "✅ Deployment setup complete!"
echo ""
echo "📋 Next Steps:"
echo "1. Push to GitHub:"
echo "   cd health-monitor-deploy"
echo "   git remote add origin https://github.com/YOUR_USERNAME/health-monitor.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "2. Deploy to Railway:"
echo "   - Visit https://railway.app"
echo "   - Click 'New Project' → 'Deploy from GitHub repo'"
echo "   - Select your health-monitor repository"
echo "   - Railway will auto-deploy!"
echo ""
echo "3. Deploy to Render:"
echo "   - Visit https://render.com"
echo "   - Click 'New' → 'Web Service'"
echo "   - Connect your GitHub repo"
echo "   - Render will use render.yaml config"
echo ""
echo "🌐 Your app will be publicly accessible once deployed!"

cd ..
echo "📁 Files ready in: ./health-monitor-deploy/"
