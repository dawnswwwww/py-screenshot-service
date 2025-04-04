# 截图服务

这是一个基于 Playwright 的截图服务，提供网页截图和长截图功能。

## 功能特性

- 普通网页截图（可指定宽高）
- 全页面长截图（可指定宽度）
- 批量截图支持
- 可扩展的存储服务（目前支持本地存储）

## 快速开始

### 使用初始化脚本（推荐）

#### Linux/macOS

```bash
chmod +x init.sh
./init.sh
```

#### Windows

双击运行 `init.bat`

### 手动安装

1. 安装依赖：

```bash
pip install -e .
```

2. 安装 Playwright Chromium 浏览器：

```bash
playwright install chromium
```

## 服务管理

### Linux/macOS

使用 `service.sh` 脚本管理服务：

```bash
# 启动服务
./service.sh start

# 停止服务
./service.sh stop

# 重启服务
./service.sh restart

# 查看服务状态
./service.sh status
```

服务日志文件：`screenshot-service.log`

## API 接口

### 1. 普通截图

POST `http://localhost:9143/screenshot`

请求参数：

```json
{
  "url": "https://example.com",
  "width": 1920,
  "height": 1080
}
```

响应：

```json
{
  "image_url": "/path/to/screenshot.png"
}
```

### 2. 长截图

POST `http://localhost:9143/full-page-screenshot`

请求参数：

```json
{
  "url": "https://example.com",
  "width": 1920
}
```

响应：

```json
{
  "image_url": "/path/to/screenshot.png"
}
```

### 3. 批量普通截图

POST `http://localhost:9143/batch-screenshot`

请求参数：

```json
{
  "requests": [
    {
      "url": "https://example.com",
      "width": 1920,
      "height": 1080
    },
    {
      "url": "https://example.org",
      "width": 1280,
      "height": 720
    }
  ]
}
```

响应：

```json
{
  "results": [
    {
      "url": "https://example.com",
      "image_url": "/path/to/screenshot1.png"
    },
    {
      "url": "https://example.org",
      "image_url": "/path/to/screenshot2.png"
    }
  ]
}
```

### 4. 批量长截图

POST `http://localhost:9143/batch-full-page-screenshot`

请求参数：

```json
{
  "requests": [
    {
      "url": "https://example.com",
      "width": 1920
    },
    {
      "url": "https://example.org",
      "width": 1280
    }
  ]
}
```

响应：

```json
{
  "results": [
    {
      "url": "https://example.com",
      "image_url": "/path/to/screenshot1.png"
    },
    {
      "url": "https://example.org",
      "image_url": "/path/to/screenshot2.png"
    }
  ]
}
```

## 存储服务

目前使用本地文件系统存储截图，可以通过实现 `StorageService` 协议来扩展支持其他存储方式（如 OSS、CDN 等）。
