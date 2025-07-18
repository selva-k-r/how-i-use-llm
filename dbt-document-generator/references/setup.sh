#!/bin/bash
# Setup script for dbt Documentation Automation

echo "🚀 Setting up dbt Documentation Automation..."

# Check if we're in a dbt project
if [ ! -f "dbt_project.yml" ]; then
    echo "❌ dbt_project.yml not found. Please run this script from your dbt project root."
    exit 1
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Create config file from example
if [ ! -f "config.yml" ]; then
    echo "📝 Creating config.yml from example..."
    cp config.example.yml config.yml
    echo "✅ Please edit config.yml with your OpenAI API key"
fi

# Check if manifest.json exists
if [ ! -f "target/manifest.json" ]; then
    echo "⚠️  manifest.json not found. Running dbt compile..."
    dbt compile
fi

# Check if OpenAI API key is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  OPENAI_API_KEY environment variable not set."
    echo "    Please set it with: export OPENAI_API_KEY='your-api-key'"
    echo "    Or add it to your config.yml file"
fi

echo "✅ Setup complete! Run 'python dbt_doc_automation.py' to start"
