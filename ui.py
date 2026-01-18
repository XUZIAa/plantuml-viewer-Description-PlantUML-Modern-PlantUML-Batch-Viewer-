"""
现代化用户界面完整版 - 使用 CustomTkinter
包含所有功能的完整实现
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox, Menu
from PIL import Image, ImageTk
from typing import List, Optional
import threading
from pathlib import Path
import pyperclip
from queue import Queue
import shutil
import tkinter as tk

from diagram import PlantUMLDiagram
from loader import DiagramLoader
from generator import ImageGenerator
from project_manager import ProjectManager

# 默认浅色主题
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class ModernPlantUMLViewer:
    """现代化 PlantUML 查看器 - 完整功能版"""
    
    def __init__(self, root: ctk.CTk, project_manager):
        self.root = root
        self.project_manager = project_manager
        
        # 窗口设置
        project_name = self.project_manager.get_project_name()
        self.root.title(f"PlantUML 快速预览工具 - {project_name}")
        self.root.geometry("1600x900")
        
        # 数据
        self.diagrams: List[PlantUMLDiagram] = []
        self.current_index = 0
        self.is_generating = False
        self.current_theme = "light"  # 当前主题，默认浅色
        
        self.loader = DiagramLoader()
        self.generator = ImageGenerator(max_workers=10)
        self.zoom_level = 1.0
        
        # 任务队列
        self.task_queue = Queue()
        
        self._setup_ui()
        self._load_project_codes()
        self._start_ui_updater()
    
    def _setup_ui(self):
        """构建界面"""
        # 配置主窗口背景色 - 使用更现代的色调
        self.root.configure(fg_color=("#F3F4F6", "#111827"))
        
        self._create_menubar()
        self._create_header()
        self._create_main_content()
        self._create_statusbar()
        self._create_context_menu()  # 创建右键菜单
    
    def _create_menubar(self):
        """创建系统原生菜单栏"""
        # 创建主菜单
        menubar = Menu(self.root)
        self.root.configure(menu=menubar)
        
        # 文件菜单
        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="从剪贴板加载", command=self.load_from_clipboard, accelerator="Ctrl+V")
        file_menu.add_command(label="打开文件...", command=self.load_from_file, accelerator="Ctrl+O")
        file_menu.add_command(label="打开文件夹...", command=self.load_from_folder)
        file_menu.add_separator()
        file_menu.add_command(label="保存当前图片...", command=self.save_current_image, accelerator="Ctrl+S")
        file_menu.add_command(label="批量保存图片...", command=self.save_all_images)
        file_menu.add_separator()
        file_menu.add_command(label="导出代码...", command=self.export_code)
        file_menu.add_command(label="导出所有代码...", command=self.export_all_codes)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.close_window, accelerator="Alt+F4")
        
        # 编辑菜单
        edit_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="编辑", menu=edit_menu)
        edit_menu.add_command(label="编辑当前代码", command=self.edit_current_code, accelerator="F2")
        edit_menu.add_command(label="复制代码", command=self.copy_code, accelerator="Ctrl+C")
        edit_menu.add_separator()
        edit_menu.add_command(label="搜索...", command=self.search_diagrams, accelerator="Ctrl+F")
        edit_menu.add_separator()
        edit_menu.add_command(label="删除当前", command=self.delete_current, accelerator="Delete")
        edit_menu.add_command(label="清空全部", command=self.clear_all)
        
        # 生成菜单
        gen_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="生成", menu=gen_menu)
        gen_menu.add_command(label="生成当前", command=self.generate_current_image, accelerator="F5")
        gen_menu.add_command(label="生成全部", command=self.generate_all_images, accelerator="Ctrl+F5")
        gen_menu.add_separator()
        gen_menu.add_command(label="重新生成失败项", command=self.regenerate_failed)
        
        # 查看菜单
        view_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="查看", menu=view_menu)
        view_menu.add_command(label="上一个", command=self.prev_diagram, accelerator="Ctrl+Up")
        view_menu.add_command(label="下一个", command=self.next_diagram, accelerator="Ctrl+Down")
        view_menu.add_separator()
        view_menu.add_command(label="放大", command=self.zoom_in, accelerator="Ctrl++")
        view_menu.add_command(label="缩小", command=self.zoom_out, accelerator="Ctrl+-")
        view_menu.add_command(label="重置缩放", command=self.zoom_reset, accelerator="Ctrl+0")
        view_menu.add_separator()
        view_menu.add_command(label="切换主题", command=self.toggle_theme, accelerator="Ctrl+T")
        
        # 项目菜单
        proj_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="项目", menu=proj_menu)
        proj_menu.add_command(label="打开项目文件夹", command=self.open_project_folder)
        proj_menu.add_command(label="统计信息", command=self.show_statistics)
        
        # 帮助菜单
        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="帮助", menu=help_menu)
        help_menu.add_command(label="快速开始", command=self.show_quick_start)
        help_menu.add_command(label="快捷键列表", command=self.show_shortcuts)
        help_menu.add_separator()
        help_menu.add_command(label="关于", command=self.show_about)
        
        # 绑定快捷键
        self._bind_shortcuts()
    
    def _create_menu_button(self, parent, text, command):
        """创建菜单按钮"""
        btn = ctk.CTkButton(
            parent, text=text, command=command,
            width=60, height=30, corner_radius=6,
            fg_color="transparent",
            hover_color=("#E0E0E0", "#3B3B3B"),
            text_color=("#000000", "#FFFFFF"),
            font=("Microsoft YaHei UI", 12)
        )
        btn.pack(side="left", padx=2)
    
    def _show_file_menu(self):
        """显示文件菜单"""
        menu = Menu(self.root, tearoff=0, bg="#FFFFFF", fg="#212529", 
                   activebackground="#007BFF", activeforeground="#FFFFFF", font=("Microsoft YaHei UI", 10))
        menu.add_command(label="从剪贴板加载", command=self.load_from_clipboard, accelerator="Ctrl+V")
        menu.add_command(label="打开文件...", command=self.load_from_file, accelerator="Ctrl+O")
        menu.add_command(label="打开文件夹...", command=self.load_from_folder)
        menu.add_separator()
        menu.add_command(label="保存当前图片...", command=self.save_current_image, accelerator="Ctrl+S")
        menu.add_command(label="批量保存图片...", command=self.save_all_images)
        menu.add_separator()
        menu.add_command(label="导出代码...", command=self.export_code)
        menu.add_command(label="导出所有代码...", command=self.export_all_codes)
        menu.add_separator()
        menu.add_command(label="关闭", command=self.close_window, accelerator="Alt+F4")
        menu.post(self.root.winfo_pointerx(), self.root.winfo_pointery())
    
    def _show_edit_menu(self):
        """显示编辑菜单"""
        menu = Menu(self.root, tearoff=0, bg="#FFFFFF", fg="#212529",
                   activebackground="#007BFF", activeforeground="#FFFFFF", font=("Microsoft YaHei UI", 10))
        menu.add_command(label="编辑当前代码", command=self.edit_current_code, accelerator="F2")
        menu.add_command(label="复制代码", command=self.copy_code, accelerator="Ctrl+C")
        menu.add_separator()
        menu.add_command(label="搜索...", command=self.search_diagrams, accelerator="Ctrl+F")
        menu.add_separator()
        menu.add_command(label="删除当前", command=self.delete_current, accelerator="Delete")
        menu.add_command(label="清空全部", command=self.clear_all)
        menu.post(self.root.winfo_pointerx(), self.root.winfo_pointery())
    
    def _show_generate_menu(self):
        """显示生成菜单"""
        menu = Menu(self.root, tearoff=0, bg="#FFFFFF", fg="#212529",
                   activebackground="#007BFF", activeforeground="#FFFFFF", font=("Microsoft YaHei UI", 10))
        menu.add_command(label="生成当前", command=self.generate_current_image, accelerator="F5")
        menu.add_command(label="生成全部", command=self.generate_all_images, accelerator="Ctrl+F5")
        menu.add_separator()
        menu.add_command(label="重新生成失败项", command=self.regenerate_failed)
        menu.post(self.root.winfo_pointerx(), self.root.winfo_pointery())
    
    def _show_view_menu(self):
        """显示查看菜单"""
        menu = Menu(self.root, tearoff=0, bg="#FFFFFF", fg="#212529",
                   activebackground="#007BFF", activeforeground="#FFFFFF", font=("Microsoft YaHei UI", 10))
        menu.add_command(label="上一个", command=self.prev_diagram, accelerator="Ctrl+Up")
        menu.add_command(label="下一个", command=self.next_diagram, accelerator="Ctrl+Down")
        menu.add_separator()
        menu.add_command(label="放大", command=self.zoom_in, accelerator="Ctrl++")
        menu.add_command(label="缩小", command=self.zoom_out, accelerator="Ctrl+-")
        menu.add_command(label="重置缩放", command=self.zoom_reset, accelerator="Ctrl+0")
        menu.add_separator()
        menu.add_command(label="切换主题", command=self.toggle_theme, accelerator="Ctrl+T")
        menu.post(self.root.winfo_pointerx(), self.root.winfo_pointery())
    
    def _show_project_menu(self):
        """显示项目菜单"""
        menu = Menu(self.root, tearoff=0, bg="#FFFFFF", fg="#212529",
                   activebackground="#007BFF", activeforeground="#FFFFFF", font=("Microsoft YaHei UI", 10))
        menu.add_command(label="打开项目文件夹", command=self.open_project_folder)
        menu.add_command(label="切换项目", command=self.close_window)
        menu.add_separator()
        menu.add_command(label="统计信息", command=self.show_statistics)
        menu.post(self.root.winfo_pointerx(), self.root.winfo_pointery())
    
    def _show_help_menu(self):
        """显示帮助菜单"""
        menu = Menu(self.root, tearoff=0, bg="#FFFFFF", fg="#212529",
                   activebackground="#007BFF", activeforeground="#FFFFFF", font=("Microsoft YaHei UI", 10))
        menu.add_command(label="快速开始", command=self.show_quick_start)
        menu.add_command(label="快捷键列表", command=self.show_shortcuts)
        menu.add_separator()
        menu.add_command(label="关于", command=self.show_about)
        menu.post(self.root.winfo_pointerx(), self.root.winfo_pointery())
    
    def show_quick_start(self):
        """显示快速开始"""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("快速开始")
        dialog.geometry("500x450")
        dialog.resizable(False, False)
        
        # 统一背景色
        dialog.configure(fg_color=("#F3F4F6", "#111827"))
        
        # 设置为模态窗口
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 居中显示
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'{width}x{height}+{x}+{y}')
        
        # 主容器
        main_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # 标题
        ctk.CTkLabel(
            main_frame,
            text="快速开始指南",
            font=("Segoe UI", 20, "bold"),
            text_color=("#111827", "#F9FAFB")
        ).pack(pady=(10, 20))
        
        # 内容框
        content_frame = ctk.CTkFrame(
            main_frame, 
            fg_color=("#FFFFFF", "#1F2937"), 
            corner_radius=15,
            border_width=1,
            border_color=("#E5E7EB", "#374151")
        )
        content_frame.pack(fill="both", expand=True, pady=10)
        
        steps = [
            ("📁 导入", "点击顶部 '打开' 或从剪贴板导入代码"),
            ("⚡ 生成", "点击 '生成当前' 或 '全部生成' 渲染图片"),
            ("💾 保存", "生成后可保存为 PNG 图片文件"),
            ("🔍 搜索", "使用左侧搜索框快速查找图表"),
            ("📏 调整", "拖动中间分隔条调整布局大小")
        ]
        
        for icon, text in steps:
            step_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
            step_frame.pack(fill="x", padx=20, pady=12)
            
            ctk.CTkLabel(
                step_frame,
                text=icon,
                font=("Segoe UI", 16),
                width=30
            ).pack(side="left")
            
            ctk.CTkLabel(
                step_frame,
                text=text,
                font=("Segoe UI", 13),
                text_color=("#4B5563", "#D1D5DB"),
                anchor="w"
            ).pack(side="left", padx=10)
        
        # 确定按钮
        ctk.CTkButton(
            main_frame,
            text="开始使用",
            command=dialog.destroy,
            width=120,
            height=35,
            corner_radius=8,
            font=("Segoe UI", 13, "bold"),
            fg_color="#3B82F6",
            hover_color="#2563EB"
        ).pack(pady=(20, 10))
        
        dialog.wait_window()
    
    def show_about(self):
        """显示关于"""
        about_window = ctk.CTkToplevel(self.root)
        about_window.title("关于")
        about_window.geometry("500x550")
        about_window.resizable(False, False)
        
        # 统一背景色
        about_window.configure(fg_color=("#F3F4F6", "#111827"))
        
        # 设置为模态窗口
        about_window.transient(self.root)
        about_window.grab_set()
        
        # 居中显示
        about_window.update_idletasks()
        width = about_window.winfo_width()
        height = about_window.winfo_height()
        x = (about_window.winfo_screenwidth() // 2) - (width // 2)
        y = (about_window.winfo_screenheight() // 2) - (height // 2)
        about_window.geometry(f'{width}x{height}+{x}+{y}')
        
        # 主容器
        main_frame = ctk.CTkFrame(about_window, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # 标题 Logo
        ctk.CTkLabel(
            main_frame,
            text="PlantUML Viewer",
            font=("Segoe UI", 24, "bold"),
            text_color=("#3B82F6", "#60A5FA")
        ).pack(pady=(20, 5))
        
        ctk.CTkLabel(
            main_frame,
            text="v2.0.0",
            font=("Segoe UI", 12),
            text_color=("#6B7280", "#9CA3AF")
        ).pack(pady=(0, 15))
        
        # 信息卡片
        info_card = ctk.CTkFrame(
            main_frame, 
            fg_color=("#FFFFFF", "#1F2937"), 
            corner_radius=15,
            border_width=1,
            border_color=("#E5E7EB", "#374151")
        )
        info_card.pack(fill="both", expand=True, pady=10)
        
        # 作者信息
        info_frame = ctk.CTkFrame(info_card, fg_color="transparent")
        info_frame.pack(fill="x", pady=20)
        
        ctk.CTkLabel(
            info_frame,
            text="作者：许",
            font=("Segoe UI", 14, "bold"),
            text_color=("#111827", "#F9FAFB")
        ).pack(pady=(5, 5))
        
        ctk.CTkLabel(
            info_frame,
            text="pursue_everything@163.com",
            font=("Segoe UI", 12),
            text_color=("#3B82F6", "#60A5FA")
        ).pack(pady=2)
        
        ctk.CTkLabel(
            info_frame,
            text="2026年1月18日",
            font=("Segoe UI", 12),
            text_color=("#6B7280", "#9CA3AF")
        ).pack(pady=2)
        
        # 免责声明
        warning_frame = ctk.CTkFrame(info_card, fg_color=("#FEF3C7", "#78350F"), corner_radius=8)
        warning_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            warning_frame,
            text="本软件完全免费，严禁商业用途",
            font=("Segoe UI", 12, "bold"),
            text_color=("#92400E", "#FEF3C7"),
            justify="center"
        ).pack(pady=10)
        
        # 技术栈
        tech_frame = ctk.CTkFrame(info_card, fg_color="transparent")
        tech_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            tech_frame,
            text="Powered by",
            font=("Segoe UI", 11, "italic"),
            text_color=("#6B7280", "#9CA3AF")
        ).pack()
        
        ctk.CTkLabel(
            tech_frame,
            text="Python • CustomTkinter • Pillow",
            font=("Segoe UI", 11),
            text_color=("#4B5563", "#D1D5DB")
        ).pack(pady=2)
        
        # 确定按钮
        ctk.CTkButton(
            main_frame,
            text="关闭",
            command=about_window.destroy,
            width=120,
            height=35,
            corner_radius=8,
            font=("Segoe UI", 13),
            fg_color=("#E5E7EB", "#374151"),
            text_color=("#111827", "#F9FAFB"),
            hover_color=("#D1D5DB", "#4B5563")
        ).pack(pady=(10, 10))
        
        # 等待窗口关闭
        about_window.wait_window()
    
    def _create_header(self):
        """创建现代化顶部导航栏"""
        # 头部容器 - 增加高度和阴影感（通过颜色区分）
        self.header = ctk.CTkFrame(
            self.root, 
            height=70, 
            corner_radius=0, 
            fg_color=("#FFFFFF", "#1F2937")
        )
        self.header.pack(fill="x", padx=0, pady=0)
        self.header.pack_propagate(False)  # 固定高度
        
        # 1. 左侧 Logo 区域
        logo_frame = ctk.CTkFrame(self.header, fg_color="transparent")
        logo_frame.pack(side="left", padx=20, pady=10)
        
        # 标题
        ctk.CTkLabel(
            logo_frame, 
            text="PlantUML", 
            font=("Segoe UI", 20, "bold"),
            text_color=("#3B82F6", "#60A5FA")  # 品牌蓝
        ).pack(side="left")
        
        ctk.CTkLabel(
            logo_frame, 
            text=" Viewer", 
            font=("Segoe UI", 20),
            text_color=("#374151", "#E5E7EB")
        ).pack(side="left")

        # 2. 中间工具栏区域 - 使用分组卡片样式
        tools_frame = ctk.CTkFrame(self.header, fg_color="transparent")
        tools_frame.pack(side="left", fill="y", padx=40, pady=12)
        
        # 辅助函数：创建图标按钮
        def create_tool_btn(parent, text, command, color=None, hover_color=None, width=100):
            if color is None:
                color = "transparent"
                text_color = ("#4B5563", "#D1D5DB")
                hover = ("#F3F4F6", "#374151")
            else:
                text_color = "#FFFFFF"
                hover = hover_color
                
            return ctk.CTkButton(
                parent, 
                text=text, 
                command=command,
                width=width, 
                height=36, 
                corner_radius=8, 
                font=("Segoe UI", 13, "bold" if color != "transparent" else "normal"),
                fg_color=color,
                hover_color=hover,
                text_color=text_color
            )

        # 文件组
        file_group = ctk.CTkFrame(tools_frame, fg_color="transparent")
        file_group.pack(side="left", padx=5)
        
        create_tool_btn(file_group, "📋 剪贴板", self.load_from_clipboard, width=90).pack(side="left", padx=2)
        create_tool_btn(file_group, "📄 打开文件", self.load_from_file, width=90).pack(side="left", padx=2)
        create_tool_btn(file_group, "📂 打开文件夹", self.load_from_folder, width=100).pack(side="left", padx=2)
        
        # 分隔线
        ctk.CTkFrame(tools_frame, width=1, height=20, fg_color=("#E5E7EB", "#4B5563")).pack(side="left", padx=15, pady=10)
        
        # 生成组
        gen_group = ctk.CTkFrame(tools_frame, fg_color="transparent")
        gen_group.pack(side="left", padx=5)
        
        self.generate_current_btn = create_tool_btn(
            gen_group, "⚡ 生成当前", self.generate_current_image,
            color="#10B981", hover_color="#059669", width=110
        )
        self.generate_current_btn.pack(side="left", padx=2)
        
        self.generate_all_btn = create_tool_btn(
            gen_group, "⚡ 全部", self.generate_all_images,
            color="transparent", width=80
        )
        self.generate_all_btn.pack(side="left", padx=2)
        self.generate_all_btn.configure(text_color=("#10B981", "#10B981"), border_width=1, border_color=("#10B981", "#10B981"))

        # 分隔线
        ctk.CTkFrame(tools_frame, width=1, height=20, fg_color=("#E5E7EB", "#4B5563")).pack(side="left", padx=15, pady=10)
        
        # 保存组
        save_group = ctk.CTkFrame(tools_frame, fg_color="transparent")
        save_group.pack(side="left", padx=5)
        
        create_tool_btn(save_group, "💾 保存", self.save_current_image, width=80).pack(side="left", padx=2)
        create_tool_btn(save_group, "💾 批量", self.save_all_images, width=80).pack(side="left", padx=2)

        # 3. 右侧功能区
        right_frame = ctk.CTkFrame(self.header, fg_color="transparent")
        right_frame.pack(side="right", padx=20)
        
        self.theme_btn = create_tool_btn(right_frame, "☀️", self.toggle_theme, width=40)
        self.theme_btn.pack(side="left", padx=5)
        
        # 更多菜单按钮
        self.menu_btn = create_tool_btn(right_frame, "⋮", self.show_app_menu, width=40)
        self.menu_btn.pack(side="left", padx=5)

    def show_app_menu(self):
        """显示应用菜单"""
        menu = Menu(
            self.root, tearoff=0,
            bg="#FFFFFF", fg="#212529",
            activebackground="#3B82F6", activeforeground="#FFFFFF",
            font=("Segoe UI", 10)
        )
        menu.add_command(label="📊 项目统计", command=self.show_statistics)
        menu.add_separator()
        menu.add_command(label="📁 打开项目文件夹", command=self.open_project_folder)
        menu.add_command(label="📤 导出所有代码", command=self.export_all_codes)
        menu.add_separator()
        menu.add_command(label="⌨️ 快捷键列表", command=self.show_shortcuts)
        menu.add_command(label="📖 快速开始", command=self.show_quick_start)
        menu.add_separator()
        menu.add_command(label="ℹ️ 关于", command=self.show_about)
        
        # 在按钮下方显示
        try:
            x = self.menu_btn.winfo_rootx()
            y = self.menu_btn.winfo_rooty() + self.menu_btn.winfo_height() + 5
            menu.tk_popup(x, y)
        finally:
            menu.grab_release()

    def _create_main_content(self):
        """创建主内容区 - 卡片式布局"""
        # 主容器 - 提供边距
        main_container = ctk.CTkFrame(self.root, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 左侧卡片 - 列表
        self.left_panel = ctk.CTkFrame(
            main_container, 
            width=280, 
            corner_radius=15,
            fg_color=("#FFFFFF", "#1F2937"),
            border_width=1,
            border_color=("#E5E7EB", "#374151")
        )
        self.left_panel.pack(side="left", fill="y", padx=(0, 0))
        self.left_panel.pack_propagate(False)
        
        # 分隔条 - 隐形但在视觉上增加间距
        self.separator = ctk.CTkFrame(
            main_container, 
            width=16, 
            corner_radius=0,
            fg_color="transparent",
            cursor="sb_h_double_arrow"
        )
        self.separator.pack(side="left", fill="y")
        self.separator.bind("<Button-1>", self._start_resize)
        self.separator.bind("<B1-Motion>", self._do_resize)
        self.separator.bind("<ButtonRelease-1>", self._end_resize)
        
        # 装饰性分隔线
        ctk.CTkFrame(self.separator, width=4, height=40, corner_radius=2, fg_color=("#D1D5DB", "#4B5563")).place(relx=0.5, rely=0.5, anchor="center")

        # 右侧容器 - 不再是一个单一卡片，而是包含两个垂直排列的卡片
        self.right_panel = ctk.CTkFrame(main_container, fg_color="transparent")
        self.right_panel.pack(side="left", fill="both", expand=True)
        
        # 构建左侧内容
        self._create_left_panel()
        
        # 构建右侧内容
        self._create_right_panel()
        
        self._is_resizing = False
    
    def _create_left_panel(self):
        """创建左侧面板"""
        # 顶部标题区
        header = ctk.CTkFrame(self.left_panel, fg_color="transparent", height=60)
        header.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(
            header, text="图表列表", font=("Segoe UI", 16, "bold"),
            text_color=("#111827", "#F9FAFB")
        ).pack(side="left")
        
        self.count_label = ctk.CTkLabel(
            header, text="(0)", font=("Segoe UI", 14),
            text_color=("#6B7280", "#9CA3AF")
        )
        self.count_label.pack(side="left", padx=8)
        
        # 搜索框 - 现代化样式
        search_container = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        search_container.pack(fill="x", padx=15, pady=5)
        
        self.search_entry = ctk.CTkEntry(
            search_container, 
            placeholder_text="🔍 搜索代码或文件名...",
            height=40,
            corner_radius=10,
            border_width=1,
            font=("Segoe UI", 13),
            fg_color=("#F9FAFB", "#374151"),
            border_color=("#E5E7EB", "#4B5563"),
            text_color=("#111827", "#F9FAFB")
        )
        self.search_entry.pack(fill="x")
        self.search_entry.bind('<Return>', lambda e: self.search_diagrams())
        
        # 列表区域
        self.list_frame = ctk.CTkScrollableFrame(
            self.left_panel,
            fg_color="transparent",
            corner_radius=0
        )
        self.list_frame.pack(fill="both", expand=True, padx=5, pady=10)
        self.list_items = []
    
    def _create_right_panel(self):
        """创建右侧面板"""
        # 1. 代码区域卡片
        self.code_container = ctk.CTkFrame(
            self.right_panel, 
            corner_radius=15, 
            height=250,
            fg_color=("#FFFFFF", "#1F2937"),
            border_width=1,
            border_color=("#E5E7EB", "#374151")
        )
        self.code_container.pack(fill="x", expand=False)
        self.code_container.pack_propagate(False)
        
        # 代码区Header
        code_header = ctk.CTkFrame(self.code_container, height=40, fg_color="transparent")
        code_header.pack(fill="x", padx=15, pady=5)
        
        ctk.CTkLabel(
            code_header, text="Code Editor", font=("Segoe UI", 13, "bold"),
            text_color=("#6B7280", "#9CA3AF")
        ).pack(side="left", pady=5)
        
        ctk.CTkButton(
            code_header, text="✏️ 编辑", command=self.edit_current_code,
            width=70, height=28, corner_radius=6, 
            font=("Segoe UI", 12), fg_color=("#F3F4F6", "#374151"),
            text_color=("#111827", "#F9FAFB"), hover_color=("#E5E7EB", "#4B5563")
        ).pack(side="right")

        self.code_textbox = ctk.CTkTextbox(
            self.code_container, wrap="word", font=("JetBrains Mono", 12),
            corner_radius=8,
            fg_color=("#F9FAFB", "#111827"),
            text_color=("#111827", "#D1D5DB"),
            border_width=1,
            border_color=("#E5E7EB", "#374151")
        )
        self.code_textbox.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # 分隔条
        self.separator_v = ctk.CTkFrame(
            self.right_panel, height=16, fg_color="transparent",
            cursor="sb_v_double_arrow"
        )
        self.separator_v.pack(fill="x")
        self.separator_v.bind("<Button-1>", self._start_resize_vertical)
        self.separator_v.bind("<B1-Motion>", self._do_resize_vertical)
        self.separator_v.bind("<ButtonRelease-1>", self._end_resize_vertical)
        
        # 装饰性横线
        ctk.CTkFrame(self.separator_v, width=40, height=4, corner_radius=2, fg_color=("#D1D5DB", "#4B5563")).place(relx=0.5, rely=0.5, anchor="center")
        
        # 2. 图片预览卡片
        self.image_container = ctk.CTkFrame(
            self.right_panel, 
            corner_radius=15,
            fg_color=("#FFFFFF", "#1F2937"),
            border_width=1,
            border_color=("#E5E7EB", "#374151")
        )
        self.image_container.pack(fill="both", expand=True)
        
        # 工具栏浮层 (Overlay) - 放在 Image Container 的顶部
        img_tools = ctk.CTkFrame(self.image_container, fg_color="transparent", height=40)
        img_tools.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkLabel(
            img_tools, text="Preview", font=("Segoe UI", 13, "bold"),
            text_color=("#6B7280", "#9CA3AF")
        ).pack(side="left")
        
        # 缩放按钮组
        zoom_frame = ctk.CTkFrame(img_tools, fg_color=("#F3F4F6", "#374151"), corner_radius=8)
        zoom_frame.pack(side="right")
        
        def create_zoom_btn(text, cmd):
            return ctk.CTkButton(
                zoom_frame, text=text, command=cmd,
                width=32, height=28, corner_radius=6,
                fg_color="transparent", hover_color=("#E5E7EB", "#4B5563"),
                text_color=("#111827", "#F9FAFB"), font=("Segoe UI", 14)
            )
            
        create_zoom_btn("－", self.zoom_out).pack(side="left", padx=2, pady=2)
        create_zoom_btn("1:1", self.zoom_reset).pack(side="left", padx=2, pady=2)
        create_zoom_btn("＋", self.zoom_in).pack(side="left", padx=2, pady=2)
        
        # 图片显示区域
        self.image_display_frame = ctk.CTkFrame(
            self.image_container, 
            fg_color=("#F9FAFB", "#111827"), # 稍微深一点的背景衬托图片
            corner_radius=8
        )
        self.image_display_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        self.image_label = ctk.CTkLabel(
            self.image_display_frame, text="",
            text_color=("#9CA3AF", "#6B7280")
        )
        self.image_label.pack(fill="both", expand=True)
        
        self._is_resizing_v = False
    
    def _start_resize(self, event):
        """开始调整左右大小"""
        self._is_resizing = True
        self._resize_start_x = event.x_root
        self._resize_start_width = self.left_panel.winfo_width()
    
    def _do_resize(self, event):
        """调整左右大小"""
        if not self._is_resizing:
            return
        delta = event.x_root - self._resize_start_x
        new_width = max(200, min(800, self._resize_start_width + delta))
        self.left_panel.configure(width=new_width)
    
    def _end_resize(self, event):
        """结束调整左右大小"""
        self._is_resizing = False
    
    def _start_resize_vertical(self, event):
        """开始调整上下大小"""
        self._is_resizing_v = True
        self._resize_start_y = event.y_root
        self._resize_start_height = self.code_container.winfo_height()
    
    def _do_resize_vertical(self, event):
        """调整上下大小"""
        if not self._is_resizing_v:
            return
        delta = event.y_root - self._resize_start_y
        new_height = max(150, min(600, self._resize_start_height + delta))
        self.code_container.configure(height=new_height)
    
    def _end_resize_vertical(self, event):
        """结束调整上下大小"""
        self._is_resizing_v = False
    
    def _create_statusbar(self):
        """创建状态栏"""
        statusbar = ctk.CTkFrame(
            self.root, 
            height=30, 
            corner_radius=0,
            fg_color=("#E5E7EB", "#1F2937") # 底部深色条
        )
        statusbar.pack(fill="x", padx=0, pady=0)
        
        self.status_label = ctk.CTkLabel(
            statusbar, text="就绪", font=("Segoe UI", 11), anchor="w",
            text_color=("#4B5563", "#9CA3AF")
        )
        self.status_label.pack(side="left", padx=20, pady=2)
        
        self.progress_bar = ctk.CTkProgressBar(
            statusbar, width=200, height=8, corner_radius=4,
            progress_color=("#3B82F6", "#3B82F6")
        )
        self.progress_bar.pack(side="right", padx=20, pady=11)
        self.progress_bar.set(0)
    
    def _start_ui_updater(self):
        """启动UI更新线程"""
        def update_ui():
            while True:
                try:
                    task = self.task_queue.get(timeout=0.1)
                    if task:
                        func, args = task
                        self.root.after(0, func, *args)
                except:
                    pass
        threading.Thread(target=update_ui, daemon=True).start()

    # ==================== 文件加载功能 ====================
    
    def load_from_clipboard(self):
        """从剪贴板加载"""
        try:
            # 先读取剪贴板内容
            code = pyperclip.paste()
            if not code or not code.strip():
                messagebox.showwarning("警告", "剪贴板为空")
                return
            
            # 弹出对话框询问文件名
            dialog = ctk.CTkInputDialog(
                text="请输入文件名（不含扩展名）:",
                title="保存为文件"
            )
            filename = dialog.get_input()
            
            if not filename:
                return
            
            # 确保文件名合法
            filename = filename.strip()
            if not filename:
                return
            
            # 添加 .puml 扩展名
            if not filename.endswith(('.puml', '.plantuml', '.pu')):
                filename = filename + '.puml'
            
            # 保存到项目 codes 目录
            codes_dir = self.project_manager.get_codes_dir()
            if not codes_dir:
                messagebox.showerror("错误", "项目目录不存在")
                return
            
            filepath = codes_dir / filename
            
            # 检查文件是否已存在
            if filepath.exists():
                if not messagebox.askyesno("确认", f"文件 {filename} 已存在，是否覆盖？"):
                    return
            
            # 保存文件
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(code)
            
            # 加载文件
            diagram = self.loader.load_from_file(str(filepath))
            self.diagrams.append(diagram)
            self._update_list()
            self.update_status(f"已从剪贴板创建文件: {filename}")
            messagebox.showinfo("成功", f"文件已保存: {filename}")
            
        except Exception as e:
            messagebox.showerror("错误", f"加载失败: {e}")
    
    def load_from_file(self):
        """从文件加载"""
        filepaths = filedialog.askopenfilenames(
            title="选择 PlantUML 文件",
            filetypes=[("PlantUML 文件", "*.puml *.plantuml *.pu"), ("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        if not filepaths:
            return
        
        codes_dir = self.project_manager.get_codes_dir()
        for filepath in filepaths:
            try:
                source_path = Path(filepath)
                target_path = codes_dir / source_path.name
                if target_path.exists():
                    if not messagebox.askyesno("确认", f"文件 {source_path.name} 已存在，是否覆盖？"):
                        continue
                shutil.copy2(filepath, target_path)
                diagram = self.loader.load_from_file(str(target_path))
                self.diagrams.append(diagram)
            except Exception as e:
                messagebox.showerror("错误", f"加载文件失败 {filepath}: {e}")
        self._update_list()
        self.update_status(f"已加载 {len(filepaths)} 个文件")
    
    def load_from_folder(self):
        """从文件夹加载"""
        folder = filedialog.askdirectory(title="选择文件夹")
        if not folder:
            return
        diagrams = self.loader.load_from_folder(folder)
        if not diagrams:
            messagebox.showinfo("提示", "未找到 PlantUML 文件")
            return
        codes_dir = self.project_manager.get_codes_dir()
        imported_count = 0
        for diagram in diagrams:
            try:
                source_path = Path(diagram.source)
                target_path = codes_dir / source_path.name
                if not target_path.exists():
                    shutil.copy2(diagram.source, target_path)
                diagram.source = str(target_path)
                self.diagrams.append(diagram)
                imported_count += 1
            except Exception as e:
                print(f"导入文件失败 {diagram.source}: {e}")
        self._update_list()
        self.update_status(f"已从文件夹导入 {imported_count} 个文件")
    
    def _load_project_codes(self):
        """加载项目中的代码"""
        codes_dir = self.project_manager.get_codes_dir()
        if not codes_dir or not codes_dir.exists():
            return
        puml_files = list(codes_dir.glob("*.puml")) + list(codes_dir.glob("*.plantuml")) + list(codes_dir.glob("*.pu"))
        if not puml_files:
            return
        for filepath in puml_files:
            try:
                diagram = self.loader.load_from_file(str(filepath))
                self.diagrams.append(diagram)
            except Exception as e:
                print(f"加载文件失败 {filepath}: {e}")
        self._update_list()
        if puml_files:
            self.update_status(f"已加载项目中的 {len(puml_files)} 个文件")

    # ==================== 图片生成功能 ====================
    
    def generate_current_image(self):
        """生成当前图片"""
        if not self.diagrams:
            messagebox.showwarning("警告", "没有可生成的图表")
            return
        if self.current_index >= len(self.diagrams):
            return
        if self.is_generating:
            messagebox.showinfo("提示", "正在生成中")
            return
        threading.Thread(target=self._generate_current_thread, daemon=True).start()
    
    def generate_all_images(self):
        """生成所有图片"""
        if not self.diagrams:
            messagebox.showwarning("警告", "没有可生成的图表")
            return
        if self.is_generating:
            messagebox.showinfo("提示", "正在生成中")
            return
        threading.Thread(target=self._generate_images_thread, daemon=True).start()
    
    def _generate_current_thread(self):
        """生成当前图片线程"""
        self.is_generating = True
        self.root.after(0, self._disable_generate_buttons)
        diagram = self.diagrams[self.current_index]
        self.root.after(0, self.update_status, "正在生成当前图片...")
        success = diagram.generate_image(self.generator.server_url)
        self.root.after(0, self._current_generation_complete, success)
    
    def _generate_images_thread(self):
        """生成所有图片线程"""
        self.is_generating = True
        self.root.after(0, self._disable_generate_buttons)
        def progress_callback(index, success, total):
            progress = ((index + 1) / total)
            self.root.after(0, self._update_progress, progress, index + 1, total, success)
        success_count = self.generator.generate_batch(self.diagrams, progress_callback)
        self.root.after(0, self._generation_complete, success_count, len(self.diagrams))
    
    def _current_generation_complete(self, success: bool):
        """当前图片生成完成"""
        self.is_generating = False
        self._enable_generate_buttons()
        if success:
            self.update_status("当前图片生成成功")
            self._update_list()
            self.display_current_diagram()
            messagebox.showinfo("成功", "图片生成成功")
        else:
            self.update_status("当前图片生成失败")
            messagebox.showerror("失败", "图片生成失败，请检查代码")
    
    def _generation_complete(self, success: int, total: int):
        """全部生成完成"""
        self.is_generating = False
        self._enable_generate_buttons()
        self.progress_bar.set(0)
        self.update_status(f"完成：成功 {success}/{total}")
        self._update_list()
        if success > 0:
            self.current_index = 0
            self.display_current_diagram()
        messagebox.showinfo("完成", f"成功生成 {success}/{total} 张图片")
    
    def _update_progress(self, progress: float, current: int, total: int, success: int):
        """更新进度"""
        self.progress_bar.set(progress)
        self.update_status(f"正在生成 {current}/{total} (成功 {success})")
    
    def _disable_generate_buttons(self):
        """禁用生成按钮"""
        self.generate_current_btn.configure(state="disabled")
        self.generate_all_btn.configure(state="disabled")
    
    def _enable_generate_buttons(self):
        """启用生成按钮"""
        self.generate_current_btn.configure(state="normal")
        self.generate_all_btn.configure(state="normal")
    
    # ==================== 图片保存功能 ====================
    
    def save_current_image(self):
        """保存当前图片"""
        if not self.diagrams or self.current_index >= len(self.diagrams):
            messagebox.showwarning("警告", "没有可保存的图片")
            return
        diagram = self.diagrams[self.current_index]
        if not diagram.image:
            messagebox.showwarning("警告", "请先生成图片")
            return
        images_dir = self.project_manager.get_images_dir()
        if diagram.source == "剪贴板":
            default_name = f"diagram_{self.current_index + 1}.png"
        else:
            default_name = Path(diagram.source).stem + ".png"
        initial_file = str(images_dir / default_name) if images_dir else default_name
        filepath = filedialog.asksaveasfilename(
            title="保存图片", initialfile=initial_file,
            defaultextension=".png", filetypes=[("PNG 图片", "*.png"), ("JPEG 图片", "*.jpg")]
        )
        if filepath and diagram.save_image(filepath):
            self.update_status(f"图片已保存: {filepath}")
            messagebox.showinfo("成功", "图片保存成功")
    
    def save_all_images(self):
        """批量保存图片"""
        if not self.diagrams:
            messagebox.showwarning("警告", "没有可保存的图片")
            return
        images_dir = self.project_manager.get_images_dir()
        initial_dir = str(images_dir) if images_dir else None
        folder = filedialog.askdirectory(title="选择保存文件夹", initialdir=initial_dir)
        if not folder:
            return
        folder_path = Path(folder)
        success_count = 0
        for i, diagram in enumerate(self.diagrams):
            if not diagram.image:
                continue
            if diagram.source == "剪贴板":
                filename = f"diagram_{i+1}.png"
            else:
                filename = Path(diagram.source).stem + ".png"
            filepath = folder_path / filename
            if diagram.save_image(str(filepath)):
                success_count += 1
        self.update_status(f"已保存 {success_count} 张图片")
        messagebox.showinfo("完成", f"成功保存 {success_count} 张图片")

    # ==================== 显示和更新功能 ====================
    
    def display_current_diagram(self):
        """显示当前图表"""
        if not self.diagrams or self.current_index >= len(self.diagrams):
            return
        diagram = self.diagrams[self.current_index]
        self.code_textbox.delete("1.0", "end")
        self.code_textbox.insert("1.0", diagram.code)
        if diagram.image:
            self._display_image(diagram.image)
        else:
            self.image_label.configure(text="图片未生成\n点击'生成当前'按钮", image=None)
    
    def _display_image(self, image):
        """显示图片"""
        width = int(image.width * self.zoom_level)
        height = int(image.height * self.zoom_level)
        if self.zoom_level != 1.0:
            resized = image.resize((width, height), Image.Resampling.LANCZOS)
        else:
            resized = image
        photo = ctk.CTkImage(light_image=resized, dark_image=resized, size=(width, height))
        self.image_label.configure(image=photo, text="")
        self.image_label.image = photo
    
    def select_diagram(self, index: int):
        """选择图表"""
        self.current_index = index
        self.display_current_diagram()
        self._update_list_selection()
    
    def _update_list_selection(self):
        """更新列表选中状态"""
        # 检查列表项数量是否匹配
        if len(self.list_items) != len(self.diagrams):
            return

        for i, btn in enumerate(self.list_items):
            if i == self.current_index:
                # 选中状态
                btn.configure(
                    fg_color=("#E5E7EB", "#374151"), 
                    text_color=("#1F2937", "#F9FAFB"),
                    font=("Segoe UI", 12, "bold")
                )
            else:
                # 普通状态
                btn.configure(
                    fg_color="transparent", 
                    text_color=("#4B5563", "#9CA3AF"),
                    font=("Segoe UI", 12)
                )

    def _update_list(self):
        """更新列表"""
        for item in self.list_items:
            item.destroy()
        self.list_items.clear()
        for i, diagram in enumerate(self.diagrams):
            self._add_list_item(i, diagram)
        self.count_label.configure(text=f"({len(self.diagrams)})")
        
        # 更新完列表后，应用一次选中态
        self._update_list_selection()
    
    def _add_list_item(self, index: int, diagram: PlantUMLDiagram):
        """添加列表项"""
        if diagram.source == "剪贴板":
            display_name = "剪贴板"
        else:
            display_name = Path(diagram.source).name
            
        # 状态指示
        status = "✓" if diagram.image else "●"
        status_color = "#10B981" if diagram.image else "#9CA3AF" # 绿色或灰色
        
        # 按钮文本，这里由于 CTkButton 不支持多色文本，我们还是用纯文本
        # 但可以通过前缀区分
        btn_text = f"  {display_name}"
        
        # 创建按钮
        item_btn = ctk.CTkButton(
            self.list_frame, 
            text=btn_text,
            command=lambda idx=index: self.select_diagram(idx),
            anchor="w", 
            height=36, 
            corner_radius=8, 
            font=("Segoe UI", 12),
            fg_color="transparent",
            hover_color=("#F3F4F6", "#1F2937"),
            text_color=("#4B5563", "#9CA3AF")
        )
        item_btn.pack(fill="x", padx=0, pady=1)
        
        # 添加一个小圆点或图标作为状态指示（可选，这里用 Label 叠加可能比较复杂，先简单化）
        # 我们利用 Button 的 image 属性来显示状态图标会更好，但为了不引入额外的图标资源，
        # 我们还是通过文字颜色或前缀来区分。
        # 这里我们在按钮左侧添加一个小色块 Frame 来指示状态
        
        # 状态指示条
        status_indicator = ctk.CTkFrame(
            item_btn, 
            width=4, 
            height=16, 
            corner_radius=2,
            fg_color=status_color
        )
        status_indicator.place(relx=0.02, rely=0.5, anchor="w")
        
        # 稍微调整文字 Padding 以避开指示条
        # CTkButton 没有 padding 参数调整文字位置，只能通过空格
        
        # 绑定右键菜单
        item_btn.bind("<Button-3>", lambda e, idx=index: self.show_context_menu(e, idx))
        self.list_items.append(item_btn)
    
    def update_status(self, message: str):
        """更新状态"""
        self.status_label.configure(text=message)
    
    # ==================== 编辑功能 ====================
    
    def edit_current_code(self):
        """编辑当前代码"""
        if not self.diagrams or self.current_index >= len(self.diagrams):
            return
        diagram = self.diagrams[self.current_index]
        
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("编辑代码")
        dialog.geometry("700x600")
        
        # 设置为模态窗口
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 居中显示
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'{width}x{height}+{x}+{y}')
        
        # 文本框
        text_widget = ctk.CTkTextbox(
            dialog, wrap="word", font=("Consolas", 12),
            fg_color=("#FFFFFF", "#1E1E1E"),
            text_color=("#000000", "#FFFFFF")
        )
        text_widget.pack(fill="both", expand=True, padx=20, pady=20)
        text_widget.insert("1.0", diagram.code)
        
        def save_changes():
            new_code = text_widget.get("1.0", "end").strip()
            diagram.code = new_code
            diagram.image = None
            self.display_current_diagram()
            self._update_list()
            dialog.destroy()
            self.update_status("代码已更新")
        
        # 按钮框
        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        ctk.CTkButton(
            btn_frame, text="保存", command=save_changes,
            width=100, height=35, corner_radius=8,
            font=("Microsoft YaHei UI", 13)
        ).pack(side="right", padx=5)
        
        ctk.CTkButton(
            btn_frame, text="取消", command=dialog.destroy,
            width=100, height=35, corner_radius=8,
            font=("Microsoft YaHei UI", 13),
            fg_color="#6c757d", hover_color="#5a6268"
        ).pack(side="right")
    
    def delete_current(self):
        """删除当前"""
        if not self.diagrams or self.current_index >= len(self.diagrams):
            return
        self.diagrams.pop(self.current_index)
        self._update_list()
        if self.diagrams and self.current_index >= len(self.diagrams):
            self.current_index = len(self.diagrams) - 1
        if self.diagrams:
            self.display_current_diagram()
        else:
            self.code_textbox.delete("1.0", "end")
            self.image_label.configure(text="", image=None)
    
    def clear_all(self):
        """清空所有"""
        if self.diagrams and not messagebox.askyesno("确认", "确定清空所有数据吗？"):
            return
        self.diagrams.clear()
        self._update_list()
        self.code_textbox.delete("1.0", "end")
        self.image_label.configure(text="", image=None)
        self.current_index = 0
        self.update_status("已清空")
    
    # ==================== 查看功能 ====================
    
    def zoom_in(self):
        """放大"""
        self.zoom_level *= 1.2
        self._apply_zoom()
    
    def zoom_out(self):
        """缩小"""
        self.zoom_level /= 1.2
        self._apply_zoom()
    
    def zoom_reset(self):
        """重置缩放"""
        self.zoom_level = 1.0
        self._apply_zoom()
    
    def _apply_zoom(self):
        """应用缩放"""
        if not self.diagrams or self.current_index >= len(self.diagrams):
            return
        diagram = self.diagrams[self.current_index]
        if diagram.image:
            self._display_image(diagram.image)
            self.update_status(f"缩放: {int(self.zoom_level * 100)}%")
    
    def prev_diagram(self):
        """上一个"""
        if not self.diagrams:
            return
        self.current_index = (self.current_index - 1) % len(self.diagrams)
        self.display_current_diagram()
    
    def next_diagram(self):
        """下一个"""
        if not self.diagrams:
            return
        self.current_index = (self.current_index + 1) % len(self.diagrams)
        self.display_current_diagram()
    
    # ==================== 搜索功能 ====================
    
    def search_diagrams(self):
        """搜索"""
        keyword = self.search_entry.get().strip()
        if not keyword:
            return
        results = []
        for i, diagram in enumerate(self.diagrams):
            if keyword.lower() in diagram.code.lower() or keyword.lower() in diagram.source.lower():
                results.append(i)
        if results:
            self.current_index = results[0]
            self.display_current_diagram()
            messagebox.showinfo("搜索结果", f"找到 {len(results)} 个匹配项")
        else:
            messagebox.showinfo("搜索结果", "未找到匹配项")
    
    # ==================== 项目管理 ====================
    
    def close_window(self):
        """关闭窗口"""
        self.root.destroy()

    # ==================== 主题切换功能 ====================
    
    def toggle_theme(self):
        """切换主题"""
        if self.current_theme == "light":
            ctk.set_appearance_mode("dark")
            self.current_theme = "dark"
            self.theme_btn.configure(text="🌙 暗色模式")
            self.update_status("已切换到暗色模式")
            # 更新菜单栏样式为暗色
            self._update_menu_theme("dark")
        else:
            ctk.set_appearance_mode("light")
            self.current_theme = "light"
            self.theme_btn.configure(text="☀️ 浅色模式")
            self.update_status("已切换到浅色模式")
            # 更新菜单栏样式为浅色
            self._update_menu_theme("light")
    
    def _update_menu_theme(self, theme):
        """更新菜单栏主题"""
        if theme == "light":
            menu_bg = "#F8F9FA"
            menu_fg = "#212529"
            submenu_bg = "#FFFFFF"
        else:
            menu_bg = "#2B2B2B"
            menu_fg = "#FFFFFF"
            submenu_bg = "#3B3B3B"
        
        # 注意：Tkinter Menu 的样式在创建后很难动态修改
        # 这里只是尝试，实际效果可能有限
        try:
            menubar = self.root.cget("menu")
            if menubar:
                self.root.nametowidget(menubar).configure(bg=menu_bg, fg=menu_fg)
        except:
            pass
    
    def open_project_folder(self):
        """打开项目文件夹"""
        project_path = self.project_manager.get_project_path()
        if project_path:
            import subprocess
            import sys
            try:
                if sys.platform == 'win32':
                    subprocess.run(['explorer', str(project_path)])
                elif sys.platform == 'darwin':
                    subprocess.run(['open', str(project_path)])
                else:
                    subprocess.run(['xdg-open', str(project_path)])
            except Exception as e:
                messagebox.showerror("错误", f"打开失败: {e}")

    # ==================== 右键菜单 ====================
    
    def _create_context_menu(self):
        """创建右键菜单"""
        self.context_menu = Menu(
            self.root, tearoff=0,
            bg="#FFFFFF", fg="#212529",
            activebackground="#007BFF", activeforeground="#FFFFFF",
            font=("Microsoft YaHei UI", 10)
        )
        self.context_menu.add_command(label="重命名", command=self.rename_diagram)
        self.context_menu.add_command(label="编辑代码", command=self.edit_current_code)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="复制代码", command=self.copy_code)
        self.context_menu.add_command(label="复制名称", command=self.copy_name)
        self.context_menu.add_command(label="复制路径", command=self.copy_path)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="在文件管理器中显示", command=self.show_in_explorer)
        self.context_menu.add_command(label="用编辑器打开", command=self.open_in_editor)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="重新生成", command=self.generate_current_image)
        self.context_menu.add_command(label="导出图片", command=self.save_current_image)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="删除", command=self.delete_current)
    
    def show_context_menu(self, event, index):
        """显示右键菜单"""
        self.current_index = index
        self.display_current_diagram()
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
    
    # ==================== 文件管理功能 ====================
    
    def copy_code(self):
        """复制代码"""
        if not self.diagrams or self.current_index >= len(self.diagrams):
            return
        diagram = self.diagrams[self.current_index]
        try:
            pyperclip.copy(diagram.code)
            self.update_status("代码已复制到剪贴板")
        except Exception as e:
            messagebox.showerror("错误", f"复制失败: {e}")
    
    def copy_name(self):
        """复制名称"""
        if not self.diagrams or self.current_index >= len(self.diagrams):
            return
        diagram = self.diagrams[self.current_index]
        name = Path(diagram.source).name if diagram.source != "剪贴板" else "剪贴板"
        try:
            pyperclip.copy(name)
            self.update_status(f"已复制名称: {name}")
        except Exception as e:
            messagebox.showerror("错误", f"复制失败: {e}")
    
    def copy_path(self):
        """复制路径"""
        if not self.diagrams or self.current_index >= len(self.diagrams):
            return
        diagram = self.diagrams[self.current_index]
        if diagram.source == "剪贴板":
            messagebox.showinfo("提示", "剪贴板项没有路径")
            return
        try:
            pyperclip.copy(diagram.source)
            self.update_status(f"已复制路径: {diagram.source}")
        except Exception as e:
            messagebox.showerror("错误", f"复制失败: {e}")
    
    def show_in_explorer(self):
        """在文件管理器中显示"""
        if not self.diagrams or self.current_index >= len(self.diagrams):
            return
        diagram = self.diagrams[self.current_index]
        if diagram.source == "剪贴板":
            messagebox.showinfo("提示", "剪贴板项没有文件路径")
            return
        filepath = Path(diagram.source)
        if not filepath.exists():
            messagebox.showwarning("警告", "文件不存在")
            return
        try:
            import subprocess
            import sys
            if sys.platform == 'win32':
                subprocess.run(['explorer', '/select,', str(filepath)])
            elif sys.platform == 'darwin':
                subprocess.run(['open', '-R', str(filepath)])
            else:
                subprocess.run(['xdg-open', str(filepath.parent)])
            self.update_status("已在文件管理器中显示")
        except Exception as e:
            messagebox.showerror("错误", f"打开失败: {e}")
    
    def open_in_editor(self):
        """用编辑器打开"""
        if not self.diagrams or self.current_index >= len(self.diagrams):
            return
        diagram = self.diagrams[self.current_index]
        if diagram.source == "剪贴板":
            messagebox.showinfo("提示", "剪贴板项没有文件路径")
            return
        filepath = Path(diagram.source)
        if not filepath.exists():
            messagebox.showwarning("警告", "文件不存在")
            return
        try:
            import subprocess
            import sys
            import os
            if sys.platform == 'win32':
                os.startfile(str(filepath))
            elif sys.platform == 'darwin':
                subprocess.run(['open', str(filepath)])
            else:
                subprocess.run(['xdg-open', str(filepath)])
            self.update_status("已用编辑器打开")
        except Exception as e:
            messagebox.showerror("错误", f"打开失败: {e}")
    
    def rename_diagram(self):
        """重命名"""
        if not self.diagrams or self.current_index >= len(self.diagrams):
            return
        diagram = self.diagrams[self.current_index]
        current_name = Path(diagram.source).stem if diagram.source != "剪贴板" else "剪贴板"
        
        dialog = ctk.CTkInputDialog(text="请输入新名称:", title="重命名")
        new_name = dialog.get_input()
        if not new_name:
            return
        
        if diagram.source != "剪贴板" and Path(diagram.source).exists():
            try:
                old_path = Path(diagram.source)
                new_path = old_path.parent / f"{new_name}{old_path.suffix}"
                old_path.rename(new_path)
                diagram.source = str(new_path)
                self.update_status(f"已重命名: {new_name}")
            except Exception as e:
                messagebox.showerror("错误", f"重命名失败: {e}")
                return
        else:
            diagram.source = new_name
        self._update_list()
    
    def export_code(self):
        """导出代码"""
        if not self.diagrams or self.current_index >= len(self.diagrams):
            return
        diagram = self.diagrams[self.current_index]
        filepath = filedialog.asksaveasfilename(
            title="导出代码",
            defaultextension=".puml",
            filetypes=[("PlantUML 文件", "*.puml"), ("文本文件", "*.txt")]
        )
        if filepath:
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(diagram.code)
                self.update_status(f"代码已导出: {filepath}")
            except Exception as e:
                messagebox.showerror("错误", f"导出失败: {e}")
    
    def export_all_codes(self):
        """导出所有代码"""
        if not self.diagrams:
            return
        folder = filedialog.askdirectory(title="选择导出文件夹")
        if not folder:
            return
        folder_path = Path(folder)
        for i, diagram in enumerate(self.diagrams):
            if diagram.source == "剪贴板":
                filename = f"diagram_{i+1}.puml"
            else:
                filename = Path(diagram.source).stem + ".puml"
            filepath = folder_path / filename
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(diagram.code)
            except Exception as e:
                print(f"导出失败 {filename}: {e}")
        self.update_status(f"已导出 {len(self.diagrams)} 个代码文件")
        messagebox.showinfo("完成", f"成功导出 {len(self.diagrams)} 个文件")
    
    def regenerate_failed(self):
        """重新生成失败项"""
        failed = [d for d in self.diagrams if not d.image]
        if not failed:
            messagebox.showinfo("提示", "没有失败的图表")
            return
        messagebox.showinfo("提示", f"找到 {len(failed)} 个未生成的图表，开始重新生成")
        self.generate_all_images()
    
    def show_statistics(self):
        """显示统计信息"""
        total = len(self.diagrams)
        generated = sum(1 for d in self.diagrams if d.image)
        total_lines = sum(len(d.code.split('\n')) for d in self.diagrams)
        
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("统计信息")
        dialog.geometry("400x380")
        dialog.resizable(False, False)
        
        # 统一背景色
        dialog.configure(fg_color=("#F3F4F6", "#111827"))
        
        # 设置为模态窗口
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 居中显示
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'{width}x{height}+{x}+{y}')
        
        # 主容器
        main_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # 标题
        ctk.CTkLabel(
            main_frame,
            text="项目统计",
            font=("Segoe UI", 20, "bold"),
            text_color=("#111827", "#F9FAFB")
        ).pack(pady=(10, 20))
        
        # 统计卡片
        stats_frame = ctk.CTkFrame(
            main_frame, 
            fg_color=("#FFFFFF", "#1F2937"), 
            corner_radius=15,
            border_width=1,
            border_color=("#E5E7EB", "#374151")
        )
        stats_frame.pack(fill="both", expand=True, pady=10)
        
        stats_data = [
            ("总图表数", total, "#3B82F6"),
            ("已生成", generated, "#10B981"),
            ("未生成", total - generated, "#EF4444"),
            ("总代码行数", total_lines, "#8B5CF6"),
            ("平均行数", total_lines // total if total > 0 else 0, "#F59E0B")
        ]
        
        for label, value, color in stats_data:
            row = ctk.CTkFrame(stats_frame, fg_color="transparent")
            row.pack(fill="x", padx=25, pady=10)
            
            ctk.CTkLabel(
                row,
                text=label,
                font=("Segoe UI", 13),
                text_color=("#4B5563", "#D1D5DB"),
                anchor="w"
            ).pack(side="left")
            
            ctk.CTkLabel(
                row,
                text=str(value),
                font=("Segoe UI", 14, "bold"),
                text_color=color,
                anchor="e"
            ).pack(side="right")
        
        # 确定按钮
        ctk.CTkButton(
            main_frame,
            text="确定",
            command=dialog.destroy,
            width=120,
            height=35,
            corner_radius=8,
            font=("Segoe UI", 13),
            fg_color="#3B82F6",
            hover_color="#2563EB"
        ).pack(pady=(20, 10))
        
        dialog.wait_window()
    
    def show_shortcuts(self):
        """显示快捷键"""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("快捷键列表")
        dialog.geometry("500x600")
        dialog.resizable(False, False)
        
        # 统一背景色
        dialog.configure(fg_color=("#F3F4F6", "#111827"))
        
        # 设置为模态窗口
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 居中显示
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'{width}x{height}+{x}+{y}')
        
        # 主容器
        main_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # 标题
        ctk.CTkLabel(
            main_frame,
            text="快捷键列表",
            font=("Segoe UI", 20, "bold"),
            text_color=("#111827", "#F9FAFB")
        ).pack(pady=(10, 20))
        
        # 滚动框
        scroll_frame = ctk.CTkScrollableFrame(
            main_frame,
            fg_color=("#FFFFFF", "#1F2937"),
            corner_radius=15,
            border_width=1,
            border_color=("#E5E7EB", "#374151")
        )
        scroll_frame.pack(fill="both", expand=True, pady=10)
        
        shortcuts_data = [
            ("文件操作", [
                ("Ctrl+O", "打开文件"),
                ("Ctrl+S", "保存当前图片"),
            ]),
            ("编辑操作", [
                ("F2", "编辑代码"),
                ("Ctrl+C", "复制代码"),
                ("Ctrl+F", "搜索"),
                ("Delete", "删除当前"),
            ]),
            ("生成操作", [
                ("F5", "生成当前"),
                ("Ctrl+F5", "生成全部"),
            ]),
            ("查看操作", [
                ("Ctrl+Up", "上一个"),
                ("Ctrl+Down", "下一个"),
                ("Ctrl++", "放大"),
                ("Ctrl+-", "缩小"),
                ("Ctrl+0", "重置缩放"),
                ("Ctrl+T", "切换主题"),
            ])
        ]
        
        for category, shortcuts in shortcuts_data:
            # 分类标题
            ctk.CTkLabel(
                scroll_frame,
                text=category,
                font=("Segoe UI", 14, "bold"),
                text_color=("#3B82F6", "#60A5FA"),
                anchor="w"
            ).pack(anchor="w", padx=20, pady=(15, 5))
            
            # 快捷键列表
            for key, desc in shortcuts:
                row = ctk.CTkFrame(scroll_frame, fg_color="transparent")
                row.pack(fill="x", padx=25, pady=2)
                
                key_label = ctk.CTkLabel(
                    row,
                    text=key,
                    font=("Consolas", 12, "bold"),
                    text_color=("#111827", "#F9FAFB"),
                    fg_color=("#E5E7EB", "#374151"),
                    corner_radius=4,
                    width=100
                )
                key_label.pack(side="left")
                
                ctk.CTkLabel(
                    row,
                    text=desc,
                    font=("Segoe UI", 12),
                    text_color=("#4B5563", "#9CA3AF"),
                    anchor="w"
                ).pack(side="left", padx=15)
        
        # 确定按钮
        ctk.CTkButton(
            main_frame,
            text="确定",
            command=dialog.destroy,
            width=120,
            height=35,
            corner_radius=8,
            font=("Segoe UI", 13),
            fg_color="#3B82F6",
            hover_color="#2563EB"
        ).pack(pady=(20, 10))
        
        dialog.wait_window()
    
    def _bind_shortcuts(self):
        """绑定快捷键"""
        self.root.bind('<Control-o>', lambda e: self.load_from_file())
        self.root.bind('<Control-s>', lambda e: self.save_current_image())
        self.root.bind('<Control-c>', lambda e: self.copy_code())
        self.root.bind('<Control-f>', lambda e: self.search_diagrams())
        self.root.bind('<Control-t>', lambda e: self.toggle_theme())
        self.root.bind('<F2>', lambda e: self.edit_current_code())
        self.root.bind('<F5>', lambda e: self.generate_current_image())
        self.root.bind('<Control-F5>', lambda e: self.generate_all_images())
        self.root.bind('<Delete>', lambda e: self.delete_current())
        self.root.bind('<Control-Up>', lambda e: self.prev_diagram())
        self.root.bind('<Control-Down>', lambda e: self.next_diagram())
