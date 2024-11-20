import streamlit as st
import json
import os
from io import StringIO, BytesIO

def markdown_to_ipynb(md_content):
    """
    将 Markdown 内容转换为 Jupyter Notebook 格式。
    
    参数:
    - md_content: Markdown 文件内容（字符串）。
    
    返回:
    - ipynb_content: 转换后的 Notebook 文件内容（字节对象）。
    """
    lines = md_content.splitlines()
    
    # 初始化 Notebook 结构
    notebook = {
        "cells": [],
        "metadata": {},
        "nbformat": 4,
        "nbformat_minor": 4
    }

    current_cell = []

    for line in lines:
        # 检测一级标题，标志新的 Markdown 单元格
        if line.startswith("# "):  
            if current_cell:
                notebook['cells'].append({
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": current_cell
                })
                current_cell = []
        current_cell.append(line)

    # 处理文件末尾的剩余内容
    if current_cell:
        notebook['cells'].append({
            "cell_type": "markdown",
            "metadata": {},
            "source": current_cell
        })

    # 转换为 JSON 字节
    ipynb_content = BytesIO()
    json.dump(notebook, ipynb_content, indent=2, ensure_ascii=False)
    ipynb_content.seek(0)
    return ipynb_content

# Streamlit App 主体
st.title("Markdown to Jupyter Notebook Converter")

st.write("上传一个 Markdown 文件，转换为 Jupyter Notebook 文件，并提供下载。")

# 上传 Markdown 文件
uploaded_file = st.file_uploader("选择 Markdown 文件", type=["md"])

if uploaded_file is not None:
    # 读取 Markdown 文件内容
    md_content = uploaded_file.read().decode("utf-8")
    
    # 转换为 Notebook
    ipynb_content = markdown_to_ipynb(md_content)
    
    # 生成下载链接
    st.success("转换成功！点击下方按钮下载文件。")
    st.download_button(
        label="下载 Notebook 文件",
        data=ipynb_content,
        file_name="converted_notebook.ipynb",
        mime="application/json"
    )
