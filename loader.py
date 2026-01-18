"""
文件加载器模块
负责从各种来源加载 PlantUML 代码
"""

import pyperclip
from pathlib import Path
from typing import List
from diagram import PlantUMLDiagram


class DiagramLoader:
    """图表加载器"""
    
    SUPPORTED_EXTENSIONS = {'.puml', '.plantuml', '.pu', '.txt'}
    
    @staticmethod
    def load_from_clipboard() -> PlantUMLDiagram:
        """从剪贴板加载"""
        code = pyperclip.paste()
        return PlantUMLDiagram(code, "剪贴板")
    
    @staticmethod
    def load_from_file(filepath: str) -> PlantUMLDiagram:
        """从文件加载"""
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
        return PlantUMLDiagram(code, filepath)
    
    @classmethod
    def load_from_folder(cls, folder_path: str) -> List[PlantUMLDiagram]:
        """从文件夹批量加载"""
        folder = Path(folder_path)
        diagrams = []
        
        for ext in cls.SUPPORTED_EXTENSIONS:
            for filepath in folder.rglob(f"*{ext}"):
                try:
                    diagram = cls.load_from_file(str(filepath))
                    diagrams.append(diagram)
                except Exception as e:
                    print(f"加载文件失败 {filepath}: {e}")
        
        return diagrams
