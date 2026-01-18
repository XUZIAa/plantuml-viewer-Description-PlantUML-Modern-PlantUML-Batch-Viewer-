"""
图片生成器模块
负责批量生成图片的并发处理
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Callable
from diagram import PlantUMLDiagram


class ImageGenerator:
    """图片生成器"""
    
    def __init__(self, server_url: str = "http://www.plantuml.com/plantuml", max_workers: int = 5):
        self.server_url = server_url
        self.max_workers = max_workers
    
    def generate_batch(
        self, 
        diagrams: List[PlantUMLDiagram],
        progress_callback: Callable[[int, int, int], None] = None
    ) -> int:
        """
        批量生成图片
        
        Args:
            diagrams: 图表列表
            progress_callback: 进度回调函数 (当前索引, 成功数, 总数)
        
        Returns:
            成功生成的数量
        """
        total = len(diagrams)
        success_count = 0
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_index = {
                executor.submit(self._generate_single, diagram): i 
                for i, diagram in enumerate(diagrams)
            }
            
            for future in as_completed(future_to_index):
                index = future_to_index[future]
                try:
                    if future.result():
                        success_count += 1
                except Exception as e:
                    print(f"生成图片 {index} 失败: {e}")
                
                if progress_callback:
                    progress_callback(index, success_count, total)
        
        return success_count
    
    def _generate_single(self, diagram: PlantUMLDiagram) -> bool:
        """生成单个图片"""
        return diagram.generate_image(self.server_url)
