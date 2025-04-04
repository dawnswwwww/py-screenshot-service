@echo off

REM 检查是否安装了 Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python 未安装，请先安装 Python
    pause
    exit /b 1
)

REM 检查是否安装了 pip
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo pip 未安装，请先安装 pip
    pause
    exit /b 1
)

REM 创建虚拟环境
echo 创建虚拟环境...
python -m venv .venv

REM 激活虚拟环境
echo 激活虚拟环境...
call .venv\Scripts\activate.bat

REM 安装项目依赖
echo 安装项目依赖...
pip install -e .

REM 安装 Playwright Chromium
echo 安装 Playwright Chromium...
playwright install chromium

echo 初始化完成！
echo 使用以下命令启动服务：
echo .venv\Scripts\activate.bat
echo uvicorn main:app --reload --port 9143

pause 