#!/bin/bash

echo "🐳 Testing Docker Build & Run"
echo "============================="

# Build the image
echo "📦 Building Docker image..."
docker build -t health-monitor-test .

if [ $? -eq 0 ]; then
    echo "✅ Docker build successful!"
    
    echo ""
    echo "🚀 Starting container on port 8000..."
    echo "Access your app at: http://localhost:8000"
    echo "Press Ctrl+C to stop"
    echo ""
    
    # Run the container
    docker run -p 8000:8000 --name health-monitor-test-container health-monitor-test
else
    echo "❌ Docker build failed!"
    exit 1
fi
