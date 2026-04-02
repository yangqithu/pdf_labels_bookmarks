# 操作方式示例 (无双引号，支持复杂标题): 
# python pdf_labels_overwrite.py "你的文献.pdf" 13 -b 13-引言 // 45-Chapter 1: The Beginning // 80：第二章：总结论

import argparse
import re
from pathlib import Path
from pypdf import PdfReader, PdfWriter
from pypdf.constants import PageLabelStyle

def set_pdf_labels(input_file, body_start_page, bookmarks=None):
    input_path = Path(input_file).resolve()
    temp_path = input_path.with_name(f".{input_path.name}.tmp")

    try:
        with open(input_path, "rb") as f:
            reader = PdfReader(f)
            writer = PdfWriter()
            writer.append_pages_from_reader(reader)
            
            total_pages = len(writer.pages)

            # 只有当传入的大于 0 的正文页码时，才修改页码标签
            if body_start_page > 0:
                intro_count = max(0, body_start_page - 1)
                intro_count = min(intro_count, total_pages)

                if intro_count > 0:
                    writer.set_page_label(
                        page_index_from=0, 
                        page_index_to=intro_count - 1, 
                        style=PageLabelStyle.LOWERCASE_ROMAN,  # type: ignore
                        start=1
                    )
                    
                if intro_count < total_pages:
                    writer.set_page_label(
                        page_index_from=intro_count, 
                        page_index_to=total_pages - 1, 
                        style=PageLabelStyle.DECIMAL,          # type: ignore
                        start=1
                    )
            else:
                print("ℹ️ 未指定正文起始页，跳过页码标签修改。")

            # 第三段：添加书签
            if bookmarks:
                full_bookmark_str = " ".join(bookmarks)
                bookmark_list = full_bookmark_str.split("//")
                
                for bm in bookmark_list:
                    bm = bm.strip()
                    if not bm:
                        continue
                        
                    # 核心改动：使用正则切分。
                    # 匹配第一个出现的 "-" 或 ":" 或 "："。
                    # maxsplit=1 保证绝对只切一刀，标题中后续出现的任何符号都会被安全保留。
                    parts = re.split(r'[-:：]', bm, maxsplit=1)
                    
                    if len(parts) == 2:
                        page_str, title = parts
                    else:
                        print(f"⚠️ 警告: 书签格式错误被跳过 '{bm}'。请使用 '物理页码-章节名' 格式。")
                        continue

                    try:
                        physical_page = int(page_str.strip())
                        target_page_index = physical_page - 1

                        if 0 <= target_page_index < total_pages:
                            writer.add_outline_item(
                                title=title.strip(),
                                page_number=target_page_index
                            )
                            print(f"   + 成功挂载书签: [第{physical_page}页] {title.strip()}")
                        else:
                            print(f"⚠️ 警告: 书签页码 {physical_page} 超出范围 (共 {total_pages} 页)，已跳过。")
                    except ValueError:
                        print(f"⚠️ 警告: 无法解析书签页码 '{page_str}'，已跳过。")

            with open(temp_path, "wb") as out_f:
                writer.write(out_f)

        temp_path.replace(input_path)
        print(f"\n✅ 处理成功！已直接覆写原文件: {input_path}")
        if body_start_page > 0:
            print(f"   - 物理第 1 到 {intro_count} 页设为了罗马数字")
            print(f"   - 物理第 {body_start_page} 页起设为了阿拉伯数字 1")

    except Exception as e:
        print(f"❌ 运行报错: {e}")
        if temp_path.exists():
            temp_path.unlink()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PDF 页码修改与书签添加工具")
    parser.add_argument("input", help="输入 PDF 文件路径")
    
    parser.add_argument(
        "pages", 
        type=int, 
        nargs="?", 
        default=0, 
        help="正文第一页所在的物理页码 (如只需添加书签，可彻底省略此参数，或输入0)"
    )
    
    parser.add_argument(
        "-b", "--bookmarks", 
        nargs="*", 
        help="添加书签。请使用 // 作为多个书签的分割符，且无需加双引号。例如: -b 13-引言 // 45-Chapter 1: Start // 80-结论"
    )
    
    args = parser.parse_args()
    
    if args.pages == 0 and not args.bookmarks:
        print("⚠️ 提示: 你没有输入正文页码，也没有使用 -b 添加书签，文件未做任何修改。")
    else:
        set_pdf_labels(args.input, args.pages, args.bookmarks)