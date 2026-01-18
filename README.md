# 🎨 PlantUML Viewer | PlantUML 快速预览工具

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue?style=flat-square)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)
![Python](https://img.shields.io/badge/python-3.7+-yellow?style=flat-square)

**现代化的 PlantUML 批量预览和管理工具**

**A Modern Batch Viewer and Manager for PlantUML Diagrams**

[📥 下载 Download](#下载) | [✨ 特性 Features](#特性) | [🚀 快速开始 Quick Start](#快速开始) | [📖 文档 Docs](#文档)

</div>

---

## 🌟 为什么选择 PlantUML Viewer？

<table>
<tr>
<td width="50%">

### ❌ 传统方式的痛点

- 每次只能生成一张图
- 需要手动管理文件
- 界面老旧，体验差
- 没有项目管理功能
- 效率低下，浪费时间

</td>
<td width="50%">

### ✅ 使用 PlantUML Viewer

- **批量生成**，一键搞定
- **自动管理**项目文件
- **现代化界面**，赏心悦目
- **完整的项目管理**系统
- **效率提升 10 倍**！

</td>
</tr>
</table>

---

## ✨ 特性

### 🎨 现代化界面
- 基于 **CustomTkinter** 的精美 UI 设计
- 支持 **浅色/暗色** 主题切换（Ctrl+T）
- **卡片式布局**，圆角设计
- **可拖动分隔条** 自由调整布局

### ⚡ 批量生成
- **10 线程并发**生成，速度飞快
- **实时进度显示**，一目了然
- 支持生成当前或全部图表
- 自动重试失败项

### 📁 项目管理
- 类似 **IDE** 的项目管理方式
- 自动保存项目状态
- **最近项目列表**，快速访问
- 代码和图片分类存储

### 🔍 智能搜索
- 快速查找代码和文件
- 支持模糊匹配
- 实时搜索结果
- 自动跳转到匹配项

### ⌨️ 快捷键支持
- `F5` - 生成当前图片
- `Ctrl+F5` - 生成全部图片
- `Ctrl+S` - 保存图片
- `Ctrl+T` - 切换主题
- 更多快捷键...

### 🎯 其他特性
- 从剪贴板快速导入
- 批量保存图片
- 图片缩放预览
- 右键菜单快捷操作
- 完整的文件管理

---

## 📥 下载

### Windows

| 版本 | 文件 | 大小 | 说明 |
|------|------|------|------|
| v1.0.0 | [PlantUML-Viewer.exe](https://github.com/你的用户名/plantuml-viewer/releases) | ~50MB | 单文件版，无需安装 |

**系统要求：**
- Windows 10/11 (64-bit)
- 网络连接（访问 PlantUML 服务器）
- 4GB+ 内存推荐

---

## 🚀 快速开始

### 1️⃣ 下载并运行

```bash
# 下载 PlantUML-Viewer.exe
# 双击运行（首次运行会显示欢迎窗口）
```

### 2️⃣ 创建项目

- 选择 **"创建新项目"**
- 选择一个文件夹作为项目目录
- 输入项目名称

### 3️⃣ 导入代码

**方式一：从剪贴板**
```
复制 PlantUML 代码 → 点击"剪贴板"按钮 → 输入文件名
```

**方式二：打开文件**
```
点击"打开文件"→ 选择 .puml 文件 → 自动导入
```

**方式三：打开文件夹**
```
点击"打开文件夹"→ 选择包含 .puml 文件的文件夹 → 批量导入
```

### 4️⃣ 生成图片

```
点击"生成全部"→ 等待进度条完成 → 查看生成的图片
```

### 5️⃣ 保存图片

```
点击"批量保存"→ 选择保存位置 → 完成！
```

---

## 📸 界面预览

<div align="center">

### 主界面
*现代化的卡片式布局，清爽简洁*

### 浅色模式
*护眼舒适，适合白天使用*

### 暗色模式
*酷炫优雅，适合夜间使用*

### 批量生成
*10 线程并发，速度飞快*

</div>

---

## 🎯 使用场景

<table>
<tr>
<td width="33%">

### 📊 软件架构设计
绘制系统架构图、组件图、部署图

</td>
<td width="33%">

### 🔄 流程图绘制
业务流程、数据流程、泳道图

</td>
<td width="33%">

### 💾 数据库设计
ER 图、类图、关系图

</td>
</tr>
<tr>
<td width="33%">

### 📝 项目文档
技术文档、设计文档、API 文档

</td>
<td width="33%">

### 🎓 毕业设计
论文配图、系统设计、流程说明

</td>
<td width="33%">

### 💼 技术分享
演示文稿、技术博客、教程配图

</td>
</tr>
</table>

---

## 📖 文档

### 快捷键列表

| 功能 | 快捷键 |
|------|--------|
| 打开文件 | `Ctrl+O` |
| 保存图片 | `Ctrl+S` |
| 生成当前 | `F5` |
| 生成全部 | `Ctrl+F5` |
| 编辑代码 | `F2` |
| 搜索 | `Ctrl+F` |
| 切换主题 | `Ctrl+T` |
| 上一个 | `Ctrl+Up` |
| 下一个 | `Ctrl+Down` |
| 放大 | `Ctrl++` |
| 缩小 | `Ctrl+-` |
| 重置缩放 | `Ctrl+0` |

### 项目结构

```
项目文件夹/
├── codes/              # PlantUML 代码文件
│   ├── diagram1.puml
│   ├── diagram2.puml
│   └── ...
├── images/             # 生成的图片
│   ├── diagram1.png
│   ├── diagram2.png
│   └── ...
└── .plantuml_project.json  # 项目配置
```

### 支持的文件格式

- `.puml` - PlantUML 标准格式
- `.plantuml` - PlantUML 完整格式
- `.pu` - PlantUML 简写格式
- `.txt` - 文本格式

---

## 🛠️ 技术栈

- **Python 3.7+** - 编程语言
- **CustomTkinter** - 现代化 UI 框架
- **Pillow (PIL)** - 图像处理库
- **Requests** - HTTP 请求库
- **PyInstaller** - 打包工具
- **PlantUML Server** - 图表生成服务

---

## 🤝 贡献

欢迎贡献代码、报告问题、提出建议！

### 如何贡献

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 报告问题

发现 Bug？[提交 Issue](https://github.com/你的用户名/plantuml-viewer/issues)

---

## 📝 更新日志

### v1.0.0 (2026-01-18)

#### ✨ 新功能
- 🎨 全新现代化界面设计
- ⚡ 10 线程并发批量生成
- 📁 完整的项目管理系统
- 🔍 智能搜索功能
- 🌓 浅色/暗色主题切换
- ⌨️ 丰富的快捷键支持

#### 🐛 Bug 修复
- 修复编码问题
- 优化性能
- 改进用户体验

---

## ❓ 常见问题

### Q: 图片生成失败怎么办？
**A:** 检查网络连接，确保能访问 PlantUML 服务器。检查代码语法是否正确。

### Q: 可以离线使用吗？
**A:** 需要网络连接访问 PlantUML 服务器。可以自建本地服务器实现离线使用。

### Q: 支持哪些操作系统？
**A:** 目前仅支持 Windows 10/11。未来可能支持 macOS 和 Linux。

### Q: 如何更改 PlantUML 服务器地址？
**A:** 修改 `generator.py` 中的 `server_url` 参数。

### Q: 杀毒软件报毒怎么办？
**A:** 这是误报，可以添加到信任列表。程序完全开源，可以查看源代码。

---

## 🙏 致谢

感谢以下开源项目：

- [PlantUML](https://plantuml.com/) - 强大的 UML 图表工具
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - 现代化的 Tkinter 主题
- [Pillow](https://python-pillow.org/) - Python 图像处理库

---

## 💰 支持项目 | Support

如果这个项目对你有帮助，可以请作者喝杯咖啡 ☕

If this project helps you, you can buy me a coffee ☕

<div align="center">

### 微信赞赏 | WeChat Reward

<table>
<tr>
<td align="center">
<img src="https://via.placeholder.com/200x200?text=WeChat+QR+Code" width="200" height="200" alt="微信赞赏码"/>
<br/>
<b>微信扫码赞赏</b>
</td>
<td align="center">
<img src="https://via.placeholder.com/200x200?text=Alipay+QR+Code" width="200" height="200" alt="支付宝收款码"/>
<br/>
<b>支付宝扫码赞赏</b>
</td>
</tr>
</table>

**说明：**
- 💝 赞赏完全自愿，不影响软件使用
- 🎁 赞赏不代表购买任何服务或承诺
- ☕ 你的支持是我持续更新的动力

</div>

---

## 📧 联系方式

- **作者：** 许
- **邮箱：** pursue_everything@163.com
- **问题反馈：** [GitHub Issues](https://github.com/你的用户名/plantuml-viewer/issues)

---

## ⚠️ 重要声明 | Important Notice

### 免责声明 | Disclaimer

1. 本软件完全免费，仅供学习和个人使用
2. 严禁将本软件用于任何商业用途
3. 严禁将本软件用于任何违法用途
4. 使用本软件产生的任何后果由使用者自行承担
5. 作者不对软件的功能性、安全性、稳定性做任何保证

### 知识产权声明 | Intellectual Property

1. 本软件使用 MIT License 开源协议
2. 本软件使用的第三方库遵循各自的开源协议
3. PlantUML 是独立的开源项目，本软件仅作为客户端工具
4. 本软件不是 PlantUML 官方工具

### 隐私声明 | Privacy

1. 本软件不收集任何用户数据
2. 生成图片需要将代码发送到 PlantUML 服务器
3. 建议敏感数据使用自建服务器

---

## 📄 许可证

本项目采用 [MIT License](LICENSE) 开源协议。

---

<div align="center">

**如果觉得这个项目对你有帮助，请给个 Star ⭐**

**If you find this project helpful, please give it a Star ⭐**

Made with ❤️ by 许

</div>
