from playwright.async_api import async_playwright
from typing import Optional, List, Dict
from storage.storage import StorageService
import asyncio
from services.image_composite_service import ImageCompositeService

class ScreenshotService:
    def __init__(self, storage_service: StorageService):
        self.storage_service = storage_service
        self.image_composite_service = ImageCompositeService(storage_service)
        
    async def _take_screenshot(self, url: str, width: int = 1920, height: int = 1080, full_page: bool = False) -> Dict[str, str]:
        """通用的截图方法
        
        Args:
            url: 要截图的网页地址
            width: 视口宽度
            height: 视口高度
            full_page: 是否截取整个页面
            
        Returns:
            包含原始截图和合成图片路径的字典
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.set_viewport_size({"width": width, "height": height})
            await page.goto(url)
            screenshot_bytes = await page.screenshot(full_page=full_page)
            await browser.close()
            
            # 保存原始截图
            original_path = self.storage_service.save(screenshot_bytes)
            
            # 合成图片（添加二维码和水印）
            composite_path = await self.image_composite_service.composite_image(original_path, url)
            
            return {
                "img_url": original_path,
                "share_url": composite_path
            }
            
    async def take_screenshot(self, url: str, width: int = 1920, height: int = 1080) -> Dict[str, str]:
        """截取当前视口大小的截图
        
        Args:
            url: 要截图的网页地址
            width: 视口宽度
            height: 视口高度
            
        Returns:
            包含原始截图和合成图片路径的字典
        """
        return await self._take_screenshot(url, width, height, full_page=False)
            
    async def take_full_page_screenshot(self, url: str, width: int = 1920) -> Dict[str, str]:
        """截取整个页面的截图
        
        Args:
            url: 要截图的网页地址
            width: 视口宽度
            
        Returns:
            包含原始截图和合成图片路径的字典
        """
        return await self._take_screenshot(url, width, height=1080, full_page=True)

    async def batch_take_screenshot(self, requests: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """批量截取当前视口大小的截图（并发处理）
        
        Args:
            requests: 截图请求列表，每个请求包含 url、width、height
            
        Returns:
            截图结果列表，每个结果包含 url、原始图片路径和合成图片路径
        """
        async def process_request(req: Dict[str, str]) -> Dict[str, str]:
            url = req.get("url")
            width = int(req.get("width", 1920))
            height = int(req.get("height", 1080))
            result = await self.take_screenshot(url, width, height)
            return {
                "url": url,
                "img_url": result["img_url"],
                "share_url": result["share_url"]
            }
            
        # 并发处理所有请求
        tasks = [process_request(req) for req in requests]
        results = await asyncio.gather(*tasks)
        return results

    async def batch_take_full_page_screenshot(self, requests: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """批量截取整个页面的截图（并发处理）
        
        Args:
            requests: 截图请求列表，每个请求包含 url、width
            
        Returns:
            截图结果列表，每个结果包含 url、原始图片路径和合成图片路径
        """
        async def process_request(req: Dict[str, str]) -> Dict[str, str]:
            url = req.get("url")
            width = int(req.get("width", 1920))
            result = await self.take_full_page_screenshot(url, width)
            return {
                "url": url,
                "img_url": result["img_url"],
                "share_url": result["share_url"]
            }
            
        # 并发处理所有请求
        tasks = [process_request(req) for req in requests]
        results = await asyncio.gather(*tasks)
        return results 