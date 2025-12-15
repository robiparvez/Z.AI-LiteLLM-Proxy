# Z.AI LiteLLM Proxy Setup Guide

## Overview

This guide will help you set up a complete LiteLLM proxy server to bridge z.ai's API with GitHub Copilot LLM Gateway's OpenAI-compatible format. This project provides a production-ready solution with automated startup scripts, secure configuration management, and support for multiple Z.AI GLM models.

## Prerequisites

- ✅ UV package manager installed
- ✅ LiteLLM installed (v1.80.7+ recommended)
- Z.AI API key from <https://z.ai/model-api>
- VS Code with GitHub Copilot and GitHub Copilot LLM Gateway extensions
- Python 3.11+ (specified in .python-version)

## 🔗 API Configuration

This proxy uses the official Z.AI API endpoint:

- **Base URL**: `https://api.z.ai/api/coding/paas/v4/`
- **Documentation**: [Z.AI API Docs](https://docs.litellm.ai/docs/providers/zai)

## Quick Start

### 1. Set Your API Key

**On Linux/macOS:**

```bash
export ZAI_API_KEY="your-actual-api-key-here"
```

**On Windows (PowerShell):**

```powershell
$env:ZAI_API_KEY="your-actual-api-key-here"
```

**On Windows (Command Prompt):**

```cmd
set ZAI_API_KEY=your-actual-api-key-here
```

**Or create a .env file:**

```bash
cp .env.example .env
# Edit .env and replace "your-actual-api-key-here" with your actual API key
```

### 2. Set Up Environment

Create a `.env` file with your API key:

```bash
cp .env.example .env
# Edit .env and replace "your-actual-api-key-here" with your actual API key
```

### 3. Start the Proxy

**Recommended - Use the startup scripts (automatically loads .env file):**

**Windows (Git Bash/Command Prompt):**

```bash
./start_proxy.bat
```

**Linux/macOS:**

```bash
chmod +x start_proxy.sh
./start_proxy.sh
```

**Startup Script Features:**

- **Automatic Environment Loading**: Scripts automatically load `.env` file
- **Configuration Validation**: Verify API key is set before starting
- **Error Handling**: Clear error messages for missing files or invalid configuration
- **Secure Key Display**: Shows only first 10 characters of API key for verification

**Alternative - Manual start (requires setting env vars first):**

**Linux/macOS:**

```bash
source .env && uvx --from 'litellm[proxy]' litellm --config z_ai_config.yaml --port 4000
```

**Windows (PowerShell):**

```powershell
Get-Content .env | ForEach-Object { if($_ -match '^([^=]+)=(.*)$') { [Environment]::SetEnvironmentVariable($matches[1], $matches[2], 'Process') } }
uvx --from 'litellm[proxy]' litellm --config z_ai_config.yaml --port 4000
```

You should see:

```text
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:4000
```

### 4. Test the Proxy (Optional)

In a new terminal:

```bash
curl http://localhost:4000/v1/models
```

You should see a JSON response listing your configured models.

### 5. Configure GitHub Copilot LLM Gateway

1. Open VS Code Settings (`Ctrl+,` or `Cmd+,`)
2. Search for **"Copilot LLM Gateway"**
3. Configure the following settings:
   - **Server URL**: `http://localhost:4000`
   - **API Key**: Leave empty (authentication is handled by the proxy)
   - **Default Max Tokens**: `32768`
   - **Default Max Output Tokens**: `4096`

### 6. Select Model in GitHub Copilot

1. Open GitHub Copilot Chat (`Ctrl+Alt+I` or `Cmd+Alt+I`)
2. Click the model selector dropdown
3. Click **"Manage Models..."**
4. Select **"LLM Gateway"** from the provider list
5. Enable the models you want to use (e.g., `glm-4.6`, `glm-4.5-flash`)

### 7. Start Coding

Your z.ai models should now be available in GitHub Copilot Chat.

## Available Models

The following Z.AI GLM models are pre-configured in `z_ai_config.yaml`:

- **glm-4.6** - Latest flagship model, 200K context, $0.60/$2.20 per 1M tokens
- **glm-4.5** - 128K context, $0.60/$2.20 per 1M tokens
- **glm-4.5-flash** - **FREE** tier model, 128K context
- **glm-4.5-air** - Lightweight model, 128K context, $0.20/$1.10 per 1M tokens

### Model Features

- **Streaming Support**: All models support both streaming and non-streaming responses
- **Context Length**: Models support up to 200K context window (glm-4.6)
- **Token Limits**: Configurable max_tokens (default: 4096)
- **OpenAI Compatible**: Full OpenAI API compatibility for seamless integration

### Other Available Z.AI Models

You can add any of these to `z_ai_config.yaml`:

- **glm-4.5v** - Vision model, $0.60/$1.80 per 1M tokens
- **glm-4.5-x** - Premium tier, $2.20/$8.90 per 1M tokens
- **glm-4.5-airx** - Fast lightweight, $1.10/$4.50 per 1M tokens
- **glm-4-32b-0414-128k** - 32B parameter model, $0.10/$0.10 per 1M tokens

See [Z.AI LiteLLM Documentation](https://docs.litellm.ai/docs/providers/zai) for the complete list.

## Important Configuration Notes

**Z.AI Provider Setup:**

- Z.AI models use the Z.AI API endpoint: `https://api.z.ai/api/coding/paas/v4/`
- In proxy configuration, set `custom_llm_provider: openai` for compatibility
- Model names are used directly (e.g., `glm-4.6`) without the `zai/` prefix
- For direct LiteLLM SDK usage (not via proxy), use the `zai/` prefix (e.g., `zai/glm-4.6`)

**SDK vs Proxy Usage:**

- **Direct SDK**: `completion(model="zai/glm-4.6", ...)` - requires `zai/` prefix
- **Via Proxy**: `completion(model="glm-4.6", ...)` - no prefix needed (configured in YAML)

## Configuration Files

- **`z_ai_config.yaml`** - Main configuration file for LiteLLM proxy with model definitions
- **`main.py`** - Example script showing direct SDK usage with streaming support
- **`pyproject.toml`** - UV project configuration with dependencies
- **`.env.example`** - Environment variable template for API key
- **`.gitignore`** - Git ignore patterns for version control
- **`.python-version`** - Python version specification (3.11+)
- **`start_proxy.bat`** - Windows startup script with environment loading
- **`start_proxy.sh`** - Linux/macOS startup script with environment loading

## Direct SDK Usage

The project includes `main.py` as an example of direct LiteLLM SDK usage:

```python
import os
from litellm import completion

# Example with zai/ prefix for direct SDK usage
response = completion(
    model="zai/glm-4.6",
    messages=[{"role": "user", "content": "Hello from LiteLLM!"}]
)

# Example with streaming
response = completion(
    model="zai/glm-4.5-flash",  # FREE tier
    messages=[{"role": "user", "content": "Count from 1 to 5"}],
    stream=True
)
```

**Note**: For direct SDK usage, use the `zai/` prefix. For proxy usage, model names are used without the prefix.

## Troubleshooting

### Proxy won't start

- Ensure port 4000 is not already in use
- Check that UV is properly installed: `uv --version`
- Verify the YAML file has correct indentation (use spaces, not tabs)

### Models not appearing in Copilot

- Run the test connection command in VS Code Command Palette: `Ctrl+Shift+P` → "GitHub Copilot LLM Gateway: Test Server Connection"
- Verify the proxy is running and accessible at `http://localhost:4000/v1/models`
- Check VS Code settings have the correct Server URL

### API Key errors

- Ensure `ZAI_API_KEY` environment variable is set in the terminal where you run the proxy
- The environment variable must be set **before** starting the proxy
- Don't include quotes in the actual API key value

### Connection refused errors

- Make sure the LiteLLM proxy is running
- Verify you're using `http://localhost:4000` (not `https`)
- Check firewall settings aren't blocking port 4000

## Alternative Model Configuration

To add more Z.AI models, edit `z_ai_config.yaml`:

```yaml
model_list:
  # Add any Z.AI GLM model using openai provider with custom api_base
  - model_name: glm-4.5v  # Vision model
    litellm_params:
      model: glm-4.5v
      api_base: https://api.z.ai/api/coding/paas/v4/
      api_key: os.environ/ZAI_API_KEY
      custom_llm_provider: openai
      max_tokens: 4096
```

**Note**: Z.AI models use the Z.AI API endpoint (`https://api.z.ai/api/coding/paas/v4/`) with `openai` as the provider for compatibility.

## Running as Background Service

**Linux/macOS with screen:**

```bash
screen -dmS litellm uv run litellm --config z_ai_config.yaml --port 4000
```

To reattach: `screen -r litellm`

**Linux/macOS with tmux:**

```bash
tmux new-session -d -s litellm uv run litellm --config z_ai_config.yaml --port 4000
```

To reattach: `tmux attach -t litellm`

## Additional Resources

- [LiteLLM Documentation](https://docs.litellm.ai/)
- [Z.AI API Documentation](https://z.ai/model-api)
- [GitHub Copilot LLM Gateway](https://marketplace.visualstudio.com/items?itemName=AndrewButson.github-copilot-llm-gateway)

## Notes

- Keep the proxy running whenever you want to use z.ai models in GitHub Copilot
- The proxy runs locally and forwards requests to z.ai's API
- Your API key is never exposed to VS Code, only to the local proxy
- You can modify `z_ai_config.yaml` to add/remove models as needed

## Project Structure

```plaintext
z-ai-llm-proxy/
├── README.md              # This file
├── z_ai_config.yaml       # LiteLLM configuration with model definitions
├── main.py                # Example usage script with streaming support
├── pyproject.toml         # UV project configuration
├── uv.lock                # Dependency lock file
├── .env.example           # Environment variable template
├── .gitignore             # Git ignore patterns
├── .python-version        # Python version specification (3.11+)
├── start_proxy.bat        # Windows startup script
├── start_proxy.sh         # Linux/macOS startup script
├── command.txt            # Quick command reference
└── .venv/                 # Virtual environment (auto-created)
```

## Key Features

### 🚀 Production Ready

- **Automated Startup Scripts**: Cross-platform scripts with environment validation
- **Secure Configuration**: Environment variable-based API key management
- **Error Handling**: Comprehensive validation and error messages
- **Multi-Platform Support**: Windows, Linux, and macOS compatibility

### 🔒 Security Features

- **Environment Protection**: API keys never exposed in source code
- **Input Validation**: Startup scripts verify configuration before launch
- **Secure Defaults**: No hardcoded credentials, proper .gitignore setup
- **Local Only**: Proxy runs locally, API key never leaves your machine

### 🛠️ Development Features

- **Modern Python**: Python 3.11+ requirement for latest features
- **UV Package Manager**: Fast, reliable dependency management
- **Complete Documentation**: Comprehensive setup and troubleshooting guides
- **Example Code**: Working examples showing both proxy and direct SDK usage

### 🔄 Integration Features

- **GitHub Copilot Compatible**: OpenAI API format for seamless integration
- **Multiple Models**: Support for 4 different GLM models with various capabilities
- **Streaming Support**: Real-time response streaming for interactive applications
- **Flexible Configuration**: Easy model addition and customization

## Next Steps

1. Get your API key from <https://z.ai/model-api>
2. Set the `ZAI_API_KEY` environment variable or create a `.env` file
3. Run `uv run litellm --config z_ai_config.yaml --port 4000`
4. Configure GitHub Copilot LLM Gateway in VS Code
5. Select your preferred z.ai model and start coding!
