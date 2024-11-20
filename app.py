import streamlit as st
import json
from io import BytesIO

def markdown_to_ipynb(md_content):
    """
    将 Markdown 内容按照一级标题拆分为 Markdown 单元格并转换为 Jupyter Notebook 格式。

    参数:
    - md_content: Markdown 文件内容（字符串）。

    返回:
    - BytesIO 对象，包含 Jupyter Notebook JSON 数据。
    """
    lines = md_content.splitlines(keepends=True)  # 保留换行符
    notebook = {
        "cells": [],
        "metadata": {},
        "nbformat": 4,
        "nbformat_minor": 4
    }

    current_cell = []  # 当前 Markdown 单元格内容

    for line in lines:
        if line.startswith("# "):  # 检测一级标题
            if current_cell:  # 如果已有内容，保存当前单元格
                notebook["cells"].append({
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": current_cell
                })
                current_cell = []  # 开启新的单元格
        current_cell.append(line)  # 添加当前行到单元格

    # 添加最后一个单元格
    if current_cell:
        notebook["cells"].append({
            "cell_type": "markdown",
            "metadata": {},
            "source": current_cell
        })

    # 将 Notebook 数据转换为 JSON 字节流
    ipynb_content = BytesIO(json.dumps(notebook, indent=2, ensure_ascii=False).encode("utf-8"))
    return ipynb_content

# Streamlit 应用部分
st.title("Markdown to Jupyter Notebook Converter")

st.write("上传一个 Markdown 文件，按一级标题拆分为 Markdown Cell 并转换为 Jupyter Notebook 文件。")

# 上传 Markdown 文件
uploaded_file = st.file_uploader("选择 Markdown 文件", type=["md"])

if uploaded_file is not None:
    try:
        # 获取上传文件名并移除扩展名
        md_filename = uploaded_file.name.rsplit(".", 1)[0]

        # 解码上传文件内容
        md_content = uploaded_file.read().decode("utf-8")

        # 转换 Markdown 为 Jupyter Notebook
        ipynb_content = markdown_to_ipynb(md_content)

        # 下载按钮，文件名与 Markdown 文件名一致
        ipynb_filename = f"{md_filename}.ipynb"

        st.success(f"转换成功！点击下方按钮下载文件：{ipynb_filename}")
        st.download_button(
            label="下载 Notebook 文件",
            data=ipynb_content,
            file_name=ipynb_filename,
            mime="application/json"
        )
    except Exception as e:
        st.error(f"转换失败：{e}")
