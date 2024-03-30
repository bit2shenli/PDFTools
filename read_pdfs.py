# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  IDE         : PyCharm
  File Name   : read_pdfs
  Description : 根据 pdf 文件，获取某个学校调剂的院校信息
  Summary     : 1、
                2、
                3、
  Author      : chenyushencc@gmail.com
  date        : 2024/3/31 0:10
-------------------------------------------------
"""
import io
import os
import asyncio
import aiofiles
from PyPDF2 import PdfReader


def get_files():

    # 定义当前文件夹路径
    current_folder_path = os.getcwd()

    # 列出当前文件夹下的所有文件和文件夹
    items = os.listdir(current_folder_path)

    # 选择特定的文件夹
    target_folder_name = '211_2023'
    target_folder_path = os.path.join(current_folder_path, target_folder_name)

    # 获取文件夹中的所有文件
    files = os.listdir(target_folder_path)

    # 筛选出 PDF 文件
    pdf_files = [os.path.join(target_folder_path, f) for f in files if f.endswith('.pdf')]

    return pdf_files


async def read_pdf(pdf_path, code):
    # 使用os.path.basename()函数获取文件名
    file_name = os.path.basename(pdf_path)

    async with aiofiles.open(pdf_path, 'rb') as f:

        file_content = await f.read()
        # 创建PdfReader对象
        reader = PdfReader(io.BytesIO(file_content))

        # 获取PDF文件的页数
        num_pages = len(reader.pages)
        print(f"{file_name} total number of pages:", num_pages)

        for i in range(num_pages):
            first_page = reader.pages[i]
            text = first_page.extract_text()
            count = text.count(code)
            # print(f"Text on {i} page:", count)

            if count:
                print(f"{code} {file_name}")
                break


async def read_multiple_pdfs(code):
    file_paths = get_files()
    tasks = [read_pdf(file_path, code) for file_path in file_paths]
    await asyncio.gather(*tasks)
    print("~end~")


if __name__ == "__main__":
    code = "91002"      # 监控调剂学校代码
    asyncio.run(read_multiple_pdfs(code))
