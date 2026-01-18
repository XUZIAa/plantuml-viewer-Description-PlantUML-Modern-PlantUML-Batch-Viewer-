"""
PlantUML 快速预览工具 - 主入口
"""

import customtkinter as ctk
from pathlib import Path
import json
from startup import ModernStartupWindow
from ui import ModernPlantUMLViewer


def show_first_launch_welcome():
    """显示首次启动欢迎窗口"""
    welcome = ctk.CTkToplevel()
    welcome.title("致用户的一封信")
    welcome.geometry("600x450")
    welcome.resizable(False, False)
    
    # 居中显示
    welcome.update_idletasks()
    width = welcome.winfo_width()
    height = welcome.winfo_height()
    x = (welcome.winfo_screenwidth() // 2) - (width // 2)
    y = (welcome.winfo_screenheight() // 2) - (height // 2)
    welcome.geometry(f'{width}x{height}+{x}+{y}')
    
    # 设置背景色
    welcome.configure(fg_color=("#F3F4F6", "#111827"))
    
    # 主容器
    main_frame = ctk.CTkFrame(welcome, fg_color="transparent")
    main_frame.pack(fill="both", expand=True, padx=30, pady=30)
    
    # 标题区
    title_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    title_frame.pack(pady=(0, 20))
    
    ctk.CTkLabel(
        title_frame,
        text="PlantUML Viewer",
        font=("Segoe UI", 24, "bold"),
        text_color=("#3B82F6", "#60A5FA")
    ).pack()
    
    # 内容卡片
    content_card = ctk.CTkFrame(
        main_frame, 
        fg_color=("#FFFFFF", "#1F2937"),
        corner_radius=15,
        border_width=1,
        border_color=("#E5E7EB", "#374151")
    )
    content_card.pack(fill="both", expand=True, pady=10)
    
    # 欢迎文本内容
    text_content = (
        "本系统是我在日常写代码的过程中，\n"
        "发现一次一次的预览或者复制到网页进行生成图片十分繁琐，\n"
        "故编写了这个工具，提升了效率。\n\n"
        "希望能帮到需要的你。\n\n"
        "本工具完全免费，严禁用于商业，严禁用于非法场景。"
    )
    
    ctk.CTkLabel(
        content_card,
        text=text_content,
        font=("Segoe UI", 15),
        text_color=("#1F2937", "#F9FAFB"),
        justify="center",
        wraplength=450,
        height=150
    ).pack(fill="both", expand=True, padx=20, pady=20)
    
    # 底部区域
    bottom_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    bottom_frame.pack(fill="x", pady=(20, 0))
    
    # 确定按钮
    confirm_btn = ctk.CTkButton(
        bottom_frame,
        text="请阅读 (5s)",
        command=welcome.destroy,
        width=200,
        height=45,
        corner_radius=8,
        font=("Segoe UI", 14, "bold"),
        fg_color="#9CA3AF",  # 初始灰色
        state="disabled",    # 初始禁用
        hover_color="#2563EB"
    )
    confirm_btn.pack(side="bottom")
    
    # 倒计时逻辑
    def update_timer(seconds):
        if seconds > 0:
            confirm_btn.configure(text=f"请阅读 ({seconds}s)")
            welcome.after(1000, update_timer, seconds - 1)
        else:
            confirm_btn.configure(
                text="我已阅读并同意", 
                state="normal",
                fg_color="#3B82F6"  # 激活变蓝
            )
            
    # 开始倒计时
    update_timer(5)
    
    welcome.transient()
    welcome.grab_set()
    welcome.wait_window()


def check_first_launch():
    """检查是否首次启动"""
    config_file = Path.home() / ".plantuml_viewer_config.json"
    
    if not config_file.exists():
        # 首次启动，显示欢迎窗口
        # 先创建一个临时窗口用于显示欢迎对话框
        temp_root = ctk.CTk()
        temp_root.withdraw()  # 隐藏主窗口
        
        show_first_launch_welcome()
        
        temp_root.destroy()
        
        # 保存配置，标记已启动过
        config = {
            "first_launch": False,
            "launch_count": 1
        }
        config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        return True
    else:
        # 更新启动次数
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            config["launch_count"] = config.get("launch_count", 0) + 1
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except:
            pass
        return False


def main():
    # 检查首次启动
    check_first_launch()
    
    while True:
        # 显示启动窗口
        startup = ModernStartupWindow()
        project_path, project_manager = startup.show()
        
        # 如果用户没有选择项目，退出程序
        if not project_path:
            break
        
        # 打开主窗口
        root = ctk.CTk()
        app = ModernPlantUMLViewer(root, project_manager)
        root.mainloop()


if __name__ == "__main__":
    main()

