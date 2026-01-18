"""
现代化启动窗口 - 使用 CustomTkinter
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox, simpledialog
from pathlib import Path
from project_manager import ProjectManager

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class ModernStartupWindow:
    """现代化启动窗口"""
    
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("PlantUML 快速预览工具")
        self.root.geometry("800x600")
        
        self.project_manager = ProjectManager()
        self.selected_project_path = None
        
        self._setup_ui()
        self._load_recent_projects()
    
    def _setup_ui(self):
        """构建界面"""
        # 配置主窗口背景色
        self.root.configure(fg_color=("#F3F4F6", "#111827"))
        
        # 主容器
        main_container = ctk.CTkFrame(self.root, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=40, pady=40)
        
        # 顶部标题区域
        header = ctk.CTkFrame(main_container, fg_color="transparent")
        header.pack(fill="x", pady=(0, 30))
        
        # Logo/标题组合
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(anchor="center")
        
        ctk.CTkLabel(
            title_frame,
            text="PlantUML",
            font=("Segoe UI", 32, "bold"),
            text_color=("#3B82F6", "#60A5FA")
        ).pack(side="left")
        
        ctk.CTkLabel(
            title_frame,
            text=" Viewer",
            font=("Segoe UI", 32),
            text_color=("#1F2937", "#F9FAFB")
        ).pack(side="left")
        
        ctk.CTkLabel(
            header,
            text="选择或创建一个项目开始工作",
            font=("Segoe UI", 14),
            text_color=("#6B7280", "#9CA3AF")
        ).pack(pady=(10, 0))
        
        # 内容区域 - 左右分栏
        content_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        content_frame.pack(fill="both", expand=True)
        
        # 左侧：操作卡片
        left_card = ctk.CTkFrame(
            content_frame, 
            corner_radius=15,
            width=260, # 固定宽度
            fg_color=("#FFFFFF", "#1F2937"),
            border_width=1,
            border_color=("#E5E7EB", "#374151")
        )
        left_card.pack(side="left", fill="both", expand=False, padx=(0, 10))
        left_card.pack_propagate(False) # 保持固定宽度
        
        ctk.CTkLabel(
            left_card, text="开始", font=("Segoe UI", 16, "bold"),
            text_color=("#111827", "#F9FAFB")
        ).pack(anchor="w", padx=20, pady=20)
        
        def create_action_btn(parent, text, icon, cmd, color):
            btn = ctk.CTkButton(
                parent,
                text=f"{icon}  {text}",
                command=cmd,
                height=50,
                corner_radius=10,
                font=("Segoe UI", 14, "bold"),
                fg_color=color,
                hover_color=("#2563EB", "#3B82F6") if color == "#3B82F6" else ("#059669", "#10B981"),
                anchor="w"
            )
            btn.pack(fill="x", padx=20, pady=10)
            return btn
            
        create_action_btn(left_card, "创建新项目", "➕", self._create_project, "#10B981")
        create_action_btn(left_card, "打开现有项目", "📂", self._open_project, "#3B82F6")
        
        # 底部退出按钮
        ctk.CTkButton(
            left_card,
            text="退出应用",
            command=self._exit_app,
            height=40,
            corner_radius=10,
            font=("Segoe UI", 13),
            fg_color="transparent",
            text_color=("#6B7280", "#9CA3AF"),
            hover_color=("#F3F4F6", "#374151"),
            border_width=1,
            border_color=("#E5E7EB", "#4B5563")
        ).pack(side="bottom", fill="x", padx=20, pady=20)

        # 右侧：最近项目卡片
        right_card = ctk.CTkFrame(
            content_frame, 
            corner_radius=15,
            fg_color=("#FFFFFF", "#1F2937"),
            border_width=1,
            border_color=("#E5E7EB", "#374151")
        )
        right_card.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        ctk.CTkLabel(
            right_card, text="最近打开的项目", font=("Segoe UI", 16, "bold"),
            text_color=("#111827", "#F9FAFB")
        ).pack(anchor="w", padx=20, pady=20)
        
        self.recent_frame_scroll = ctk.CTkScrollableFrame(
            right_card,
            corner_radius=0,
            fg_color="transparent"
        )
        self.recent_frame_scroll.pack(fill="both", expand=True, padx=5, pady=(0, 20))
        
        self.recent_items = []
    
    def _load_recent_projects(self):
        """加载最近项目"""
        recent = self.project_manager.list_recent_projects()
        
        for project_path in recent:
            if Path(project_path).exists():
                self._add_recent_item(project_path)
    
    def _add_recent_item(self, project_path: str):
        """添加最近项目项"""
        path_obj = Path(project_path)
        
        # 列表项容器
        item_frame = ctk.CTkFrame(
            self.recent_frame_scroll, 
            corner_radius=8,
            fg_color="transparent",
            border_width=0
        )
        item_frame.pack(fill="x", padx=0, pady=2)
        
        # 内部内容按钮（点击整个区域即可打开）
        # 这里为了交互方便，我们做一个整块的按钮效果，或者保留原有布局
        # 考虑到习惯，还是分左右结构：左边信息，右边显式按钮，但优化样式
        
        content_frame = ctk.CTkFrame(
            item_frame, 
            fg_color=("#F3F4F6", "#374151"),  # 显式背景色，浅灰/深灰
            corner_radius=8
        )
        content_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # 左侧图标
        icon_label = ctk.CTkLabel(
            content_frame, 
            text="📁", 
            font=("Segoe UI", 18),
            width=40,
            text_color=("#3B82F6", "#60A5FA") # 蓝色图标
        )
        icon_label.pack(side="left", padx=(5, 10))
        
        # 右侧按钮 (先 pack 以防被挤压)
        ctk.CTkButton(
            content_frame,
            text="打开",
            command=lambda p=project_path: self._open_recent_project(p),
            width=60,
            height=28,
            corner_radius=6,
            font=("Segoe UI", 12),
            fg_color=("#E5E7EB", "#4B5563"),
            text_color=("#1F2937", "#F9FAFB"),
            hover_color=("#D1D5DB", "#6B7280")
        ).pack(side="right", padx=10)
        
        # 中间信息 (占据剩余空间)
        info_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True)
        
        # 确保有名称显示
        display_name = path_obj.name if path_obj.name else str(path_obj)
        
        ctk.CTkLabel(
            info_frame,
            text=display_name,
            font=("Segoe UI", 14, "bold"),
            anchor="w",
            text_color=("#1F2937", "#F9FAFB")
        ).pack(anchor="w", pady=(2, 0))
    
    def _create_project(self):
        """创建新项目"""
        project_dir = filedialog.askdirectory(title="选择项目位置")
        if not project_dir:
            return
        
        # 创建输入对话框
        dialog = ctk.CTkInputDialog(
            text="请输入项目名称:",
            title="创建项目"
        )
        project_name = dialog.get_input()
        
        if not project_name:
            return
        
        project_path = Path(project_dir) / project_name
        
        if project_path.exists():
            if not messagebox.askyesno("确认", "该文件夹已存在，是否使用现有文件夹？"):
                return
        
        if self.project_manager.create_project(str(project_path), project_name):
            self.project_manager.add_to_recent(str(project_path))
            self.selected_project_path = str(project_path)
            self.root.destroy()
        else:
            messagebox.showerror("错误", "创建项目失败")
    
    def _open_project(self):
        """打开现有项目"""
        project_dir = filedialog.askdirectory(title="选择项目文件夹")
        if not project_dir:
            return
        
        if self.project_manager.open_project(project_dir):
            self.project_manager.add_to_recent(project_dir)
            self.selected_project_path = project_dir
            self.root.destroy()
        else:
            messagebox.showerror("错误", "打开项目失败")
    
    def _open_recent_project(self, project_path: str):
        """打开最近项目"""
        if not Path(project_path).exists():
            messagebox.showerror("错误", "项目路径不存在")
            return
        
        if self.project_manager.open_project(project_path):
            self.project_manager.add_to_recent(project_path)
            self.selected_project_path = project_path
            self.root.destroy()
        else:
            messagebox.showerror("错误", "打开项目失败")
    
    def _exit_app(self):
        """退出应用"""
        self.selected_project_path = None
        self.root.destroy()
    
    def show(self) -> tuple:
        """显示窗口"""
        self.root.mainloop()
        return self.selected_project_path, self.project_manager
