from PIL import Image, ImageDraw, ImageFont
import qrcode
import os
from typing import Optional
from pathlib import Path

class ImageCompositeService:
    def __init__(self, storage_service):
        self.storage_service = storage_service
        self.font_path = os.path.join(os.path.dirname(__file__), "..", "assets", "fonts", "NotoSansSC-Regular.ttf")
        self.watermark_text = "Powered by webbuilder.site"
        
    async def composite_image(self, screenshot_path: str, url: str, output_path: Optional[str] = None) -> str:
        """
        合成截图、二维码和水印
        :param screenshot_path: 原始截图路径
        :param url: 要生成二维码的URL
        :param output_path: 输出路径，如果为None则自动生成
        :return: 合成后的图片路径
        """
        
        file_path = Path(self.storage_service.base_path) / screenshot_path
        
        # 打开原始截图
        screenshot = Image.open(file_path)
        
        # 生成二维码
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        # 计算新图片的尺寸
        qr_size = 200  # 二维码大小
        padding = 20   # 内边距
        watermark_height = 40  # 水印高度
        
        new_width = max(screenshot.width, qr_size + 2 * padding)
        new_height = screenshot.height + qr_size + watermark_height + 3 * padding
        
        # 创建新图片
        composite = Image.new('RGB', (new_width, new_height), 'white')
        
        # 粘贴原始截图
        composite.paste(screenshot, ((new_width - screenshot.width) // 2, padding))
        
        # 调整二维码大小并粘贴
        qr_img = qr_img.resize((qr_size, qr_size))
        qr_position = ((new_width - qr_size) // 2, screenshot.height + 2 * padding)
        composite.paste(qr_img, qr_position)
        
        # 添加水印
        try:
            font = ImageFont.truetype(self.font_path, 20)
        except:
            font = ImageFont.load_default()
            
        draw = ImageDraw.Draw(composite)
        text_width = draw.textlength(self.watermark_text, font=font)
        text_position = ((new_width - text_width) // 2, new_height - watermark_height)
        draw.text(text_position, self.watermark_text, font=font, fill='gray')
        
        
        # 保存合成后的图片
        if output_path is None:
            output_path = self._generate_output_path(file_path)
        
        directory = os.path.dirname(file_path)
        
            
        composite.save(os.path.join(directory, output_path))
            
        return output_path
    
    def _generate_output_path(self, original_path: str) -> str:
        """生成输出路径"""
        filename = os.path.basename(original_path)
        name, ext = os.path.splitext(filename)
        return f"{name}_composite{ext}"