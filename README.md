# Health Monitor - Deployment Guide

A containerized health monitoring application that checks the status of your API endpoints and provides a web interface for monitoring.

## 🚀 Quick Deploy (Free Options)

### Option 1: Railway (Recommended - Easiest)

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/quickstart)

1. **Fork/Clone this repository**
2. **Visit [Railway.app](https://railway.app)** and sign up with GitHub
3. **Click "New Project" → "Deploy from GitHub repo"**
4. **Select this repository**
5. **Railway will automatically detect the Dockerfile and deploy**
6. **Your app will be live at `https://your-app-name.railway.app`**

**Cost**: Free tier includes 512MB RAM, $5/month credit

### Option 2: Render

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

1. **Fork this repository to your GitHub**
2. **Visit [Render.com](https://render.com)** and sign up
3. **Click "New" → "Web Service"**
4. **Connect your GitHub repo**
5. **Render will use the `render.yaml` configuration**
6. **Your app will be live at `https://your-app-name.onrender.com`**

**Cost**: Free tier (sleeps after 15min inactivity)

### Option 3: Heroku

1. **Install Heroku CLI**
2. **Create `Procfile`**: `web: python tempt.py`
3. **Deploy**:
   ```bash
   heroku create your-health-monitor
   git add .
   git commit -m "Deploy health monitor"
   git push heroku main
   ```

**Cost**: Free tier discontinued, starts at $7/month

## 🐳 Local Docker Development

### Build and Run Locally

```bash
# Build the Docker image
docker build -t health-monitor .

# Run the container
docker run -p 8000:8000 health-monitor
```

### Docker Compose (Optional)

```yaml
# docker-compose.yml
version: '3.8'
services:
  health-monitor:
    build: .
    ports:
      - "8000:8000"
    environment:
      - PORT=8000
    restart: unless-stopped
```

```bash
docker-compose up -d
```

## 🌐 Features

- **Real-time Health Monitoring**: Checks API status every 60 seconds
- **Manual Health Checks**: Trigger immediate checks via web interface
- **History Tracking**: Keeps last 100 health check results
- **Auto-refresh**: Web interface updates every 30 seconds
- **REST API**: JSON endpoints for programmatic access
- **Responsive UI**: Works on desktop and mobile

## 📡 API Endpoints

- `GET /` - Web interface
- `GET /api/status` - JSON status
- `POST /trigger-health-check` - Manual health check

## ⚙️ Configuration

The app monitors: `https://ariaibot-2693c651aa05.herokuapp.com/health`

To monitor a different endpoint, modify the URL in `tempt.py`:

```python
# Line 23 in tempt.py
with urllib.request.urlopen("YOUR_API_ENDPOINT", timeout=10) as response:
```

## 🔧 Environment Variables

- `PORT`: Server port (default: 8000)

## 📊 Monitoring

- **Health Check Endpoint**: `/api/status`
- **Uptime Monitoring**: Built-in health checks
- **Auto-restart**: Configured for all platforms

## 🛡️ Security

- Runs as non-root user in container
- No sensitive data stored
- HTTPS ready for production

## 📈 Scaling

For high-traffic scenarios:
- Use Railway Pro ($20/month) for better performance
- Consider Redis for health check history storage
- Add authentication if needed

## 🎯 Perfect For

- API uptime monitoring
- Service health dashboards
- DevOps monitoring tools
- Microservice health checks

---

**🚀 Deploy in under 2 minutes with Railway!**
