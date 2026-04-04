#!/bin/bash

# Docker Lab Setup Script - Kiểm tra môi trường Docker
echo "🐳 Docker Lab - Kiểm tra môi trường..."

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker chưa cài. Cài Docker Desktop (Mac/Windows) hoặc Docker Engine (Linux)."
    echo "   https://docs.docker.com/get-docker/"
    exit 1
fi
echo "✅ Docker: $(docker --version)"

# Check Docker Compose
if docker compose version &> /dev/null; then
    echo "✅ Docker Compose: $(docker compose version --short 2>/dev/null || docker compose version)"
elif command -v docker-compose &> /dev/null; then
    echo "✅ Docker Compose (standalone): $(docker-compose --version)"
else
    echo "⚠️  Docker Compose chưa có. Lab 3 cần Compose. Cài Docker Desktop (đã gồm Compose)."
fi

# Check Docker daemon
if ! docker info &> /dev/null; then
    echo "❌ Docker daemon không chạy. Khởi động Docker Desktop hoặc: sudo systemctl start docker"
    exit 1
fi
echo "✅ Docker daemon đang chạy"

# Optional: conda env for Jupyter
if conda info --envs 2>/dev/null | grep -q "datalab"; then
    echo "✅ Conda env 'datalab' đã có (có thể dùng cho Jupyter)"
else
    echo "📌 Tùy chọn: tạo env cho Jupyter: conda create -n datalab python=3.10 -y"
fi

echo ""
echo "📋 Next steps:"
echo "1. Mở Jupyter: jupyter lab"
echo "2. Chạy lần lượt: 01_docker_fundamentals.ipynb → 05_best_practices.ipynb"
echo "3. Các lệnh docker trong notebook chạy trên máy bạn (Docker phải bật)"
echo ""
