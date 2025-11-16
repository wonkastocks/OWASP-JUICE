#!/bin/bash

# Setup script for 20 container support
echo "🐳 Setting up support for 20 Juice Shop containers..."

# Check current containers
echo "Current Docker containers:"
docker ps -a | grep juice-user || echo "No juice-user containers found"

# Create containers 6-20 if they don't exist
for i in {6..20}; do
    PORT=$((3000 + $i))
    NAME="juice-user$i"
    
    # Check if container exists
    if docker ps -a | grep -q "$NAME"; then
        echo "Container $NAME already exists"
    else
        echo "Creating container $NAME on port $PORT..."
        docker run -d \
            --name $NAME \
            --restart unless-stopped \
            -p $PORT:3000 \
            -e NODE_ENV=ctf \
            bkimminich/juice-shop:latest
        
        if [ $? -eq 0 ]; then
            echo "✅ Container $NAME created successfully"
        else
            echo "❌ Failed to create container $NAME"
        fi
    fi
done

echo ""
echo "📊 Container Status:"
docker ps --format "table {{.Names}}\t{{.Ports}}\t{{.Status}}" | grep juice-user

echo ""
echo "✅ Setup complete! You now have capacity for 20 containers (ports 3001-3020)"
echo ""
echo "Note: Containers 6-20 have been created but are optional."
echo "You can manage them through the admin panel."