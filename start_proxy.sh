#!/bin/bash
# Start LiteLLM proxy with Z.AI configuration
# This script loads environment variables from .env file

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Error: .env file not found!"
    echo "Please create .env file from .env.example:"
    echo "  cp .env.example .env"
    echo "  # Edit .env and add your ZAI_API_KEY"
    exit 1
fi

# Load environment variables from .env
set -a
source .env
set +a

# Verify API key is set
if [ -z "$ZAI_API_KEY" ]; then
    echo "Error: ZAI_API_KEY not set in .env file!"
    echo "Please edit .env and add your API key from https://z.ai/model-api"
    exit 1
fi

echo "Starting LiteLLM proxy on port 4000..."
echo "API Key loaded: ${ZAI_API_KEY:0:10}..."
echo ""

# Start the proxy using uvx
uvx --from 'litellm[proxy]' litellm --config z_ai_config.yaml --port 4000
