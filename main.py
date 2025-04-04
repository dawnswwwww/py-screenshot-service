from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
from services.screenshot_service import ScreenshotService
from storage.storage import LocalStorageService
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()
storage_service = LocalStorageService()
screenshot_service = ScreenshotService(storage_service)
storage_base_url = os.getenv("STORAGE_BASE_URL")

# 挂载静态文件目录
app.mount("/static/screenshots", StaticFiles(directory=storage_base_url), name="screenshots")

def get_image_url(request: Request, image_path: str) -> str:
    """获取完整的图片URL"""
    service_host = os.getenv("SERVICE_HOST")
    if service_host:
        return f"{service_host}static/screenshots/{image_path}"
    else:
        # 如果未配置 SERVICE_HOST，则使用请求的 host
        return f"{request.base_url}static/screenshots/{image_path}"

class ScreenshotRequest(BaseModel):
    url: str
    width: int = 1920
    height: int = 1080

class FullPageScreenshotRequest(BaseModel):
    url: str
    width: int = 1920

class BatchScreenshotRequest(BaseModel):
    requests: List[ScreenshotRequest]

class BatchFullPageScreenshotRequest(BaseModel):
    requests: List[FullPageScreenshotRequest]

@app.post("/screenshot")
async def take_screenshot(request: Request, screenshot_request: ScreenshotRequest):
    result = await screenshot_service.take_screenshot(
        screenshot_request.url, 
        screenshot_request.width, 
        screenshot_request.height
    )
    return {
        "img_url": get_image_url(request, result["img_url"]),
        "share_url": get_image_url(request, result["share_url"])
    }

@app.post("/full-page-screenshot")
async def take_full_page_screenshot(request: Request, full_page_request: FullPageScreenshotRequest):
    result = await screenshot_service.take_full_page_screenshot(full_page_request.url, full_page_request.width)
    return {
        "img_url": get_image_url(request, result["img_url"]),
        "share_url": get_image_url(request, result["share_url"])
    }

@app.post("/batch-screenshot")
async def batch_take_screenshot(request: Request, batch_request: BatchScreenshotRequest):
    results = await screenshot_service.batch_take_screenshot(
        [req.dict() for req in batch_request.requests]
    )
    return {
        "results": [{
            "url": result["url"],
            "img_url": get_image_url(request, result["img_url"]),
            "share_url": get_image_url(request, result["share_url"])
        } for result in results]
    }

@app.post("/batch-full-page-screenshot")
async def batch_take_full_page_screenshot(request: Request, batch_request: BatchFullPageScreenshotRequest):
    results = await screenshot_service.batch_take_full_page_screenshot(
        [req.dict() for req in batch_request.requests]
    )
    return {
        "results": [{
            "url": result["url"],
            "img_url": get_image_url(request, result["img_url"]),
            "share_url": get_image_url(request, result["share_url"])
        } for result in results]
    }
