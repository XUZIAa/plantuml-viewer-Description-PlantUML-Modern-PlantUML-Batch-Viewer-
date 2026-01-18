"""
项目管理模块
负责项目的创建、打开和管理
"""

import json
import os
import time
from pathlib import Path
from typing import Optional, List


class ProjectManager:
    """项目管理器"""
    
    CONFIG_FILE = ".plantuml_project.json"
    IMAGES_DIR = "images"
    CODES_DIR = "codes"
    
    def __init__(self):
        self.current_project_path: Optional[Path] = None
        self.project_config = {}
    
    def create_project(self, project_path: str, project_name: str) -> bool:
        """创建新项目"""
        try:
            project_dir = Path(project_path)
            project_dir.mkdir(parents=True, exist_ok=True)
            
            # 创建项目子目录
            (project_dir / self.IMAGES_DIR).mkdir(exist_ok=True)
            (project_dir / self.CODES_DIR).mkdir(exist_ok=True)
            
            # 创建项目配置文件
            config = {
                "name": project_name,
                "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "version": "1.0"
            }
            
            config_file = project_dir / self.CONFIG_FILE
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            
            self.current_project_path = project_dir
            self.project_config = config
            
            return True
        except Exception as e:
            print(f"创建项目失败: {e}")
            return False
    
    def open_project(self, project_path: str) -> bool:
        """打开现有项目"""
        try:
            project_dir = Path(project_path)
            
            if not project_dir.exists():
                return False
            
            # 检查是否是有效的项目目录
            config_file = project_dir / self.CONFIG_FILE
            if not config_file.exists():
                # 如果没有配置文件，创建一个
                config = {
                    "name": project_dir.name,
                    "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "version": "1.0"
                }
                with open(config_file, 'w', encoding='utf-8') as f:
                    json.dump(config, f, ensure_ascii=False, indent=2)
            else:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            
            # 确保子目录存在
            (project_dir / self.IMAGES_DIR).mkdir(exist_ok=True)
            (project_dir / self.CODES_DIR).mkdir(exist_ok=True)
            
            self.current_project_path = project_dir
            self.project_config = config
            
            return True
        except Exception as e:
            print(f"打开项目失败: {e}")
            return False
    
    def get_images_dir(self) -> Optional[Path]:
        """获取图片目录"""
        if self.current_project_path:
            return self.current_project_path / self.IMAGES_DIR
        return None
    
    def get_codes_dir(self) -> Optional[Path]:
        """获取代码目录"""
        if self.current_project_path:
            return self.current_project_path / self.CODES_DIR
        return None
    
    def get_project_name(self) -> str:
        """获取项目名称"""
        return self.project_config.get("name", "未命名项目")
    
    def get_project_path(self) -> Optional[Path]:
        """获取项目路径"""
        return self.current_project_path
    
    def list_recent_projects(self, max_count: int = 10) -> List[str]:
        """列出最近打开的项目"""
        recent_file = Path.home() / ".plantuml_recent_projects.json"
        
        if not recent_file.exists():
            return []
        
        try:
            with open(recent_file, 'r', encoding='utf-8') as f:
                recent = json.load(f)
            return recent[:max_count]
        except:
            return []
    
    def add_to_recent(self, project_path: str):
        """添加到最近项目列表"""
        recent_file = Path.home() / ".plantuml_recent_projects.json"
        
        try:
            if recent_file.exists():
                with open(recent_file, 'r', encoding='utf-8') as f:
                    recent = json.load(f)
            else:
                recent = []
            
            # 移除重复项
            if project_path in recent:
                recent.remove(project_path)
            
            # 添加到开头
            recent.insert(0, project_path)
            
            # 只保留最近10个
            recent = recent[:10]
            
            with open(recent_file, 'w', encoding='utf-8') as f:
                json.dump(recent, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存最近项目失败: {e}")
