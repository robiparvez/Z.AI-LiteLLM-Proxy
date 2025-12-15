@echo off
REM Start LiteLLM proxy with Z.AI configuration
REM This script loads environment variables from .env file

REM Check if .env file exists
if not exist .env (
    echo Error: .env file not found!
    echo Please create .env file from .env.example:
    echo   copy .env.example .env
    echo   REM Edit .env and add your ZAI_API_KEY
    exit /b 1
)

REM Load environment variables from .env file
for /f "usebackq tokens=1,* delims==" %%a in (".env") do (
    set "%%a=%%b"
)

REM Verify API key is set
if "%ZAI_API_KEY%"=="" (
    echo Error: ZAI_API_KEY not set in .env file!
    echo Please edit .env and add your API key from https://z.ai/model-api
    exit /b 1
)

echo Starting LiteLLM proxy on port 4000...
echo API Key loaded: %ZAI_API_KEY:~0,10%...
echo.

REM Start the proxy using uvx
uvx --from "litellm[proxy]" litellm --config z_ai_config.yaml --port 4000
