#!/bin/bash

# S3 Lab Setup Script
echo "🚀 Setting up S3 Lab environment..."

# Check if conda environment exists
if conda info --envs | grep -q "datalab"; then
    echo "✅ Found datalab conda environment"
else
    echo "📦 Creating datalab conda environment with Python 3.10..."
    conda create -n datalab python=3.10 -y
fi

# Activate conda environment
echo "📦 Activating datalab environment..."
source $(conda info --base)/etc/profile.d/conda.sh
conda activate datalab

# Install requirements
echo "📥 Installing S3 lab dependencies..."
pip install -r requirements.txt

# Register Jupyter kernel (optional)
python -m ipykernel install --user --name=datalab --display-name="S3 Lab (datalab)" 2>/dev/null || true

echo "✅ S3 Lab setup completed!"
echo ""
echo "📋 Next steps:"
echo "1. Start MinIO: docker compose up -d"
echo "2. MinIO Console: http://localhost:9001 (minioadmin / minioadmin)"
echo "3. S3 API endpoint: http://localhost:9000"
echo "4. Start Jupyter: jupyter lab"
echo "5. Open notebooks: 01_s3_fundamentals.ipynb → 04_data_pipeline_integration.ipynb"
echo ""
