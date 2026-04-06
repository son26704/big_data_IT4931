#!/bin/bash

# Spark Lab Setup Script
echo "🚀 Setting up Spark Lab Environment..."

# Use the currently active Python environment (venv recommended)
if [ -n "${VIRTUAL_ENV:-}" ]; then
    echo "📦 Using active virtual environment: $VIRTUAL_ENV"
else
    echo "⚠️ No active virtual environment detected."
    echo "   Recommended: source ../.venv/bin/activate"
fi

python3 -m pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data/{batch,streaming,ml}
mkdir -p logs
mkdir -p checkpoints

# Set permissions
echo "🔐 Setting permissions..."
chmod +x scripts/*.sh 2>/dev/null || true

# Create environment file
echo "⚙️ Creating environment configuration..."
cat > .env << EOF
# Spark Configuration
SPARK_MASTER_URL=spark://localhost:7077
SPARK_APP_NAME=SparkLab

# Database Configuration
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=spark_lab
POSTGRES_USER=spark_user
POSTGRES_PASSWORD=spark_password

# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_TOPIC_PREFIX=spark_lab

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379

# Jupyter Configuration
JUPYTER_PORT=8888
JUPYTER_TOKEN=spark-lab-2024
EOF

echo "✅ Spark Lab setup completed!"
echo ""
echo "🎯 Next steps:"
echo "1. Start the cluster: docker compose up -d"
echo "2. Access Spark Master UI: http://localhost:8080"
echo "3. Access Jupyter Lab: http://localhost:8888"
echo "4. Check logs: docker compose logs -f"
echo ""
echo "📚 Available services:"
echo "   - Spark Master: localhost:8080"
echo "   - Jupyter Lab: localhost:8888"
echo "   - Kafka: localhost:9092"
echo "   - PostgreSQL: localhost:5432"
echo "   - Redis: localhost:6379"
