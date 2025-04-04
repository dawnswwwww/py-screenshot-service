from abc import ABC, abstractmethod
from pathlib import Path
import uuid
from typing import Protocol
import os


default_base_path = "screenshots"
storage_base_url = os.getenv("STORAGE_BASE_URL", default_base_path)

class StorageService(Protocol):
    def save(self, data: bytes, extension: str = "png") -> str:
        """保存数据并返回访问URL"""
        ...

class LocalStorageService:
    def __init__(self, base_path: str = storage_base_url):
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)
        
    def save(self, data: bytes, extension: str = "png") -> str:
        filename = f"{uuid.uuid4()}.{extension}"
        file_path = self.base_path / filename
        file_path.write_bytes(data)
        return filename  # 只返回文件名，不包含目录 