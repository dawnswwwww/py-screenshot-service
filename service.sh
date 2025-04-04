#!/bin/bash

# 服务管理脚本
# 使用方法: ./service.sh {start|stop|restart|status}

# 服务名称
SERVICE_NAME="screenshot-service"
# PID 文件路径
PID_FILE=".venv/screenshot-service.pid"
# 服务端口
PORT=9143

# 检查虚拟环境是否激活
if [ -z "$VIRTUAL_ENV" ]; then
    echo "请先激活虚拟环境: source .venv/bin/activate"
    exit 1
fi

# 启动服务
start_service() {
    if [ -f "$PID_FILE" ]; then
        echo "服务已经在运行中 (PID: $(cat $PID_FILE))"
        exit 1
    fi
    
    echo "正在启动服务..."
    nohup uvicorn main:app --host 0.0.0.0 --port $PORT > screenshot-service.log 2>&1 &
    echo $! > $PID_FILE
    echo "服务已启动，PID: $(cat $PID_FILE)"
    echo "日志文件: screenshot-service.log"
}

# 停止服务
stop_service() {
    if [ ! -f "$PID_FILE" ]; then
        echo "服务未运行"
        exit 1
    fi
    
    PID=$(cat $PID_FILE)
    echo "正在停止服务 (PID: $PID)..."
    kill $PID
    rm $PID_FILE
    echo "服务已停止"
}

# 重启服务
restart_service() {
    stop_service
    sleep 2
    start_service
}

# 查看服务状态
status_service() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat $PID_FILE)
        if ps -p $PID > /dev/null; then
            echo "服务正在运行 (PID: $PID)"
            echo "服务地址: http://localhost:$PORT"
        else
            echo "服务进程已停止，但 PID 文件仍存在"
            rm $PID_FILE
        fi
    else
        echo "服务未运行"
    fi
}

# 主程序
case "$1" in
    start)
        start_service
        ;;
    stop)
        stop_service
        ;;
    restart)
        restart_service
        ;;
    status)
        status_service
        ;;
    *)
        echo "使用方法: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac

exit 0 