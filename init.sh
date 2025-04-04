#!/bin/bash

# 检查是否安装了 Python
if ! command -v python3 &> /dev/null; then
    echo "Python3 未安装，请先安装 Python3"
    exit 1
fi

# 检查是否安装了 pip
if ! command -v pip3 &> /dev/null; then
    echo "pip3 未安装，请先安装 pip3"
    exit 1
fi

# 创建虚拟环境
echo "创建虚拟环境..."
python3 -m venv .venv

# 激活虚拟环境
echo "激活虚拟环境..."
source .venv/bin/activate

# 安装项目依赖
echo "安装项目依赖..."
pip install -e .

# 安装 Playwright Chromium
echo "安装 Playwright Chromium..."
playwright install chromium

echo "初始化完成！"
echo "使用以下命令启动服务："
echo "source .venv/bin/activate"
echo "uvicorn main:app --reload --port 9143" 