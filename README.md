# PDF Label & Bookmark Overwriter

一个轻量级的 Python 命令行工具，专为解决学术文献和电子书的 **PDF 页码错位**与**书签缺失**问题而设计。

它可以直接覆写 PDF 底层的页码标签（将前言设为罗马数字，正文设为阿拉伯数字），并支持在不加双引号的情况下，通过极简的命令行语法快速挂载多个书签。

## ✨ 核心功能

* **物理页码重置**：自动将指定页面之前的页码设为罗马数字（i, ii, iii...），并将正文起始页重置为阿拉伯数字 1。
* **极简书签挂载**：支持在终端直接追加书签，无需繁琐的双引号包裹。
* **智能正则容错**：自动识别章节名中的特殊符号（支持中英文冒号、横杠），允许章节名包含无限个空格，自动过滤格式错误。
* **无损原地覆写**：处理完成后直接安全替换原文件，不产生冗余的副本文件。

## 🛠️ 依赖安装

本脚本仅依赖 `pypdf` 库。请确保你的 Python 环境已安装该库：

```bash
pip install pypdf
```

## 🚀 使用指南

【提示】把这个脚本的绝对路径和PDF的绝对路径直接喂给AI agent吧！描述要求，然后什么都不用管，你不需要学习繁琐的命令行操作指令，它会自动帮你做好一切的。

以WorkBuddy为例：
<img width="1076" height="195" alt="image" src="https://github.com/user-attachments/assets/407bc5d7-073c-4b14-a3bd-e6de7567f779" />
<img width="1059" height="977" alt="image" src="https://github.com/user-attachments/assets/ce614d08-b767-4a82-9a2a-b22250ea0d9a" />

最终效果：
<img width="562" height="787" alt="image" src="https://github.com/user-attachments/assets/c6d00742-cce4-4a8b-a4a1-5cbbb419e487" />


基本命令格式如下：

```bash
python pdf_labels_overwrite.py <PDF文件路径> [正文起始物理页码] [-b 书签列表...]
```

### 场景 1：全功能模式（修改页码 + 添加书签）
假设你的正文从 PDF 的第 13 页开始，你需要设置页码，并顺手添加几个书签。多个书签之间使用 `//` 分隔。

```bash
python pdf_labels_overwrite.py "你的文献.pdf" 13 -b 13-引言 // 45-Chapter 1: The Beginning // 80：第二章：总结论
```

### 场景 2：仅添加书签（不修改页码）
如果你只想快速打几个书签，可以彻底省略正文页码参数，直接使用 `-b`。

```bash
python pdf_labels_overwrite.py "你的文献.pdf" -b 13-引言 // 45-第一章 // 80-结论
```

### 场景 3：仅修改页码（不添加书签）
如果你只需要重置罗马数字和阿拉伯数字的页码逻辑。

```bash
python pdf_labels_overwrite.py "你的文献.pdf" 13
```

## ⚠️ 注意事项

* 书签参数格式必须为 `物理页码-章节名` 或 `物理页码:章节名`。
* 物理页码指的是 PDF 阅读器顶部显示的绝对页数（从 1 开始）。
* 多个书签之间请务必使用 `//` 作为分隔符。

## 📄 协议

本项目基于 MIT 协议开源。
