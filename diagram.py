"""
PlantUML 图表模型
负责图表数据的管理和图片生成
"""

import requests
from PIL import Image
import io
from typing import Optional
from encoder import PlantUMLEncoder


class PlantUMLDiagram:
    """PlantUML 图表对象"""
    
    def __init__(self, code: str, source: str = "", image_path: str = ""):
        self.code = code.strip()
        self.source = source
        self.image_path = image_path  # 已保存的图片路径
        self.image: Optional[Image.Image] = None
        
    def generate_image(self, server_url: str = "http://www.plantuml.com/plantuml") -> bool:
        """生成图片"""
        try:
            encoded = PlantUMLEncoder.encode(self.code)
            url = f"{server_url}/png/{encoded}"
            
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            self.image = Image.open(io.BytesIO(response.content))
            return True
        except Exception as e:
            print(f"生成图片失败: {e}")
            return False
    
    def save_image(self, filepath: str) -> bool:
        """保存图片到文件"""
        if not self.image:
            return False
        try:
            self.image.save(filepath)
            self.image_path = filepath
            return True
        except Exception as e:
            print(f"保存图片失败: {e}")
            return False
    
    def load_image(self) -> bool:
        """从已保存的路径加载图片"""
        if not self.image_path:
            return False
        
        # 检查路径是否存在
        if not Path(self.image_path).exists():
            print(f"图片文件不存在: {self.image_path}")
            self.image_path = ""  # 清除无效路径
            return False
        
        try:
            self.image = Image.open(self.image_path)
            return True
        except Exception as e:
            print(f"加载图片失败: {e}")
            self.image_path = ""  # 清除无效路径
            return False
    
    def to_dict(self) -> dict:
        """转换为字典用于序列化"""
        return {
            'code': self.code,
            'source': self.source,
            'image_path': self.image_path
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'PlantUMLDiagram':
        """从字典创建对象"""
        return cls(
            code=data.get('code', ''),
            source=data.get('source', ''),
            image_path=data.get('image_path', '')
        )
