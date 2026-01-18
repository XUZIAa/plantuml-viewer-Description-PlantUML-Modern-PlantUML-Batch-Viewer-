<div align="center">
<h1>PlantUML Viewer</h1>
<p>
<strong>PlantUML 批量预览与项目管理工具</strong><br>
A Modern Batch Viewer and Manager for PlantUML Diagrams
</p>
<p>
<img src="https://img.shields.io/badge/Version-1.0.0-007ACC?style=for-the-badge&logo=appveyor" alt="Version">
<img src="https://img.shields.io/badge/Platform-Windows-4EAA25?style=for-the-badge&logo=windows" alt="Platform">
<img src="https://img.shields.io/badge/License-MIT-critical?style=for-the-badge" alt="License">
<img src="https://img.shields.io/badge/Python-3.7+-yellow?style=for-the-badge&logo=python" alt="Python">
</p>
<br>
<p>
<a href="#关于项目">关于项目</a> •
<a href="#核心特性">核心特性</a> •
<a href="#示例演示">示例演示</a> •
<a href="#下载与使用">下载与使用</a>
</p>
</div>
<hr>
<h2 id="关于项目"> 关于本项目</h2>
<blockquote>
<p><strong>你好，我是一名在读大学生。</strong></p>
<p>在日常的学习和开发中，我用 PlantUML 来绘制流程图和架构图。我发现传统的生成方式效率很低：需要一步步复制粘贴代码，生成图片后再手动保存，而且随着文件增多，很难进行分类和项目化管理。</p>
<p>为了解决这个痛点，提升生产力，我利用课余时间构造了这个项目。</p>
<p>由于本人还是学生，水平有限，软件中可能存在不足之处，希望大家多多包涵。如果这个项目真的帮助到了你，并且有更多人需要，我将在后续版本中继续优化，计划加入<strong>本地部署模式</strong>（无需联网即可使用）以及加入画图功能等。</p>
</blockquote>
<br>
<h2 id="核心特性"> 核心特性</h2>
<table>
<tr>
<td width="50%" valign="top">
<h3> 高效生产</h3>
<ul>
<li><strong>批量生成</strong>：支持 10 线程并发，速度飞快。</li>
<li><strong>自动化</strong>：一键将代码转换为图片，无需重复操作。</li>
<li><strong>智能搜索</strong>：支持模糊匹配，快速定位代码文件。</li>
</ul>
</td>
<td width="50%" valign="top">
<h3> 项目管理</h3>
<ul>
<li><strong>IDE 式体验</strong>：左侧目录，右侧预览，逻辑清晰。</li>
<li><strong>自动归档</strong>：代码与生成的图片自动分类存储。</li>
<li><strong>状态保存</strong>：自动记忆上次打开的项目和进度。</li>
</ul>
</td>
</tr>
<tr>
<td colspan="2">
<h3> 现代化界面</h3>
<p>基于 CustomTkinter 开发，支持 <strong>浅色/暗色</strong> 主题一键切换，界面整洁，无广告，无多余元素。</p>
</td>
</tr>
</table>
<br>
<h2 id="示例演示"> 示例演示 (Example)</h2>
<p>我在仓库中提供了一个完整的示例项目，位于 <code>example</code> 目录下。你可以下载后直接用本软件打开，体验批量生成的流程。</p>
<p>这是一个典型的项目结构：</p>
<pre>
example/
├── codes/                  # [输入] 这里存放你编写的 puml 代码
│   ├── usecase.puml
│   └── architecture.puml
├── images/                 # [输出] 软件会自动将生成的图片保存在这里
│   ├── usecase.png
│   └── architecture.png
└── .plantuml_project.json  # [配置] 项目配置文件，自动生成
</pre>
<p><em>打开软件后，选择 example 文件夹，点击“生成全部”，即可看到效果。</em></p>
<br>
<h2 id="下载与使用"> 下载与使用</h2>
<p>目前仅支持 Windows 10/11 系统。</p>
<ul>
<li><strong>步骤 1</strong>: 在 Releases 页面下载 <code>PlantUML-Viewer.exe</code> (单文件绿色版)。</li>
<li><strong>步骤 2</strong>: 双击运行，点击“创建新项目”或“打开文件夹”。</li>
<li><strong>步骤 3</strong>: 导入你的 PlantUML 代码，按 <code>F5</code> 生成预览。</li>
</ul>
<br>
<h2 id="声明">⚠️ 重要声明</h2>
<details>
<summary><strong>点击查看免责与使用协议</strong></summary>
<br>
<ul>
<li>本软件<strong>完全免费</strong>，仅供学习交流和个人使用。</li>
<li>支持免费分享，但<strong>严禁用于任何商业用途</strong>。</li>
<li><strong>严禁用于任何违法场景</strong>。</li>
<li>软件内所有生成请求均发送至 PlantUML 官方服务器，请勿上传涉密数据（未来版本将支持离线模式）。</li>
</ul>
</details>
<br>
<hr>
<div align="center">
<br>
<h3>如果这个项目对你有帮助</h3>
<p>请点击右上角的 Star 小星星，这是对我最大的鼓励！<br>
If you like this project, please give it a Star.</p>
<p style="font-size: 12px; color: gray;">
作者：许 | 联系邮箱：pursue_everything@163.com
</p>
<br>
</div>
<hr>

<hr>

<hr>

<div align="center">

<h3>🥤 请作者喝杯奶茶</h3>

<p>
    如果你觉得这个项目对你有帮助，可以请作者喝杯饮料表示鼓励 🍹<br>
    <span style="font-size: 12px; color: gray;">(赞赏完全自愿，代码开源且免费)</span>
</p>

<img src="./nothing/noting.jpg" width="180" alt="微信赞赏码" style="border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">

<br><br>


</div>
