#!/usr/bin/env python3
"""
图标格式转换工具
支持: SVG ↔ PNG ↔ ICO ↔ Base64
"""

import os
import sys
import base64
import json
from pathlib import Path

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


def load_svg_as_image(svg_path):
    """加载 SVG 并转换为 PIL Image"""
    if not HAS_PIL:
        print("需要安装 Pillow: pip install pillow")
        return None
    
    from PIL import Image, ImageDraw
    
    with open(svg_path, 'r', encoding='utf-8') as f:
        svg_content = f.read()
    
    width, height = 81, 81
    
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    return img


def svg_to_png(svg_path, png_path, size=(81, 81)):
    """SVG 转 PNG"""
    if not HAS_PIL:
        print("需要安装 Pillow: pip install pillow")
        return False
    
    try:
        from cairosvg import svg2png
        svg2png(url=svg_path, write_to=png_path, output_width=size[0], output_height=size[1])
        print(f"✓ SVG → PNG: {png_path}")
        return True
    except ImportError:
        print("需要安装 cairosvg: pip install cairosvg")
        return False
    except Exception as e:
        print(f"✗ 转换失败: {e}")
        return False


def png_to_svg(png_path, svg_path, bg_color="#F5F5F5"):
    """PNG 转 SVG (嵌入图片)"""
    try:
        import mimetypes
        mime_type, _ = mimetypes.guess_type(png_path)
        
        with open(png_path, 'rb') as f:
            img_data = base64.b64encode(f.read()).decode('utf-8')
        
        img = Image.open(png_path)
        width, height = img.size
        
        svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
  <rect width="{width}" height="{height}" fill="{bg_color}"/>
  <image href="data:{mime_type};base64,{img_data}" x="0" y="0" width="{width}" height="{height}"/>
</svg>'''
        
        with open(svg_path, 'w', encoding='utf-8') as f:
            f.write(svg)
        
        print(f"✓ PNG → SVG: {svg_path}")
        return True
    except Exception as e:
        print(f"✗ 转换失败: {e}")
        return False


def create_ico(png_paths, ico_path):
    """创建 ICO 文件 (多尺寸)"""
    if not HAS_PIL:
        print("需要安装 Pillow: pip install pillow")
        return False
    
    try:
        images = []
        for png_path in png_paths:
            img = Image.open(png_path)
            images.append(img)
        
        images[0].save(
            ico_path,
            format='ICO',
            sizes=[(img.width, img.height) for img in images],
            append_images=images[1:]
        )
        
        print(f"✓ 创建 ICO: {ico_path}")
        return True
    except Exception as e:
        print(f"✗ 创建失败: {e}")
        return False


def png_to_base64(png_path):
    """PNG 转 Base64"""
    try:
        with open(png_path, 'rb') as f:
            data = base64.b64encode(f.read()).decode('utf-8')
        
        mime_type, _ = mimetypes.guess_type(png_path)
        data_uri = f"data:{mime_type};base64,{data}"
        
        print(f"✓ Base64 编码完成 (长度: {len(data)})")
        return data_uri
    except Exception as e:
        print(f"✗ 编码失败: {e}")
        return None


def base64_to_png(base64_str, png_path):
    """Base64 转 PNG"""
    try:
        if base64_str.startswith('data:'):
            base64_str = base64_str.split(',')[1]
        
        img_data = base64.b64decode(base64_str)
        
        with open(png_path, 'wb') as f:
            f.write(img_data)
        
        print(f"✓ Base64 → PNG: {png_path}")
        return True
    except Exception as e:
        print(f"✗ 解码失败: {e}")
        return False


def resize_image(input_path, output_path, size):
    """调整图片尺寸"""
    if not HAS_PIL:
        print("需要安装 Pillow: pip install pillow")
        return False
    
    try:
        img = Image.open(input_path)
        
        if img.mode == 'RGBA':
            img = img.resize(size, Image.LANCZOS)
        else:
            img = img.convert('RGBA')
            img = img.resize(size, Image.LANCZOS)
        
        img.save(output_path)
        print(f"✓ 调整尺寸: {input_path} → {output_path} ({size[0]}x{size[1]})")
        return True
    except Exception as e:
        print(f"✗ 调整失败: {e}")
        return False


def batch_convert(input_dir, output_dir, output_format='png', size=(81, 81)):
    """批量转换"""
    os.makedirs(output_dir, exist_ok=True)
    
    input_path = Path(input_dir)
    count = 0
    
    for file in input_path.glob('*'):
        if file.suffix.lower() in ['.png', '.jpg', '.jpeg', '.svg']:
            output_file = Path(output_dir) / f"{file.stem}.{output_format}"
            
            if file.suffix.lower() == '.svg' and output_format == 'png':
                svg_to_png(str(file), str(output_file), size)
                count += 1
            elif file.suffix.lower() in ['.png', '.jpg'] and output_format == 'png':
                resize_image(str(file), str(output_file), size)
                count += 1
    
    print(f"✓ 批量转换完成: {count} 个文件")


def print_menu():
    print("""
=== 图标格式转换工具 ===
1. SVG → PNG
2. PNG → SVG
3. PNG → ICO (多尺寸)
4. PNG → Base64
5. Base64 → PNG
6. 调整图片尺寸
7. 批量转换
8. 创建 Tabbar 图标对
0. 退出
""")


def create_tabbar_icon(name, output_dir, icon_color="#7A7E83", active_color="#3CC51F"):
    """创建 Tabbar 图标对"""
    os.makedirs(output_dir, exist_ok=True)
    
    icons = {
        'home': {
            'path': 'M40.5 22L22 37V60H31V44H50V60H59V37L40.5 22Z',
        },
        'category': {
            'path': '<rect x="24" y="22" width="33" height="33" rx="4" stroke="{c}" stroke-width="3"/><line x1="24" y1="34" x2="57" y2="34" stroke="{c}" stroke-width="3"/><line x1="34" y1="22" x2="34" y2="55" stroke="{c}" stroke-width="3"/><line x1="47" y1="22" x2="47" y2="55" stroke="{c}" stroke-width="3"/>',
        },
        'cart': {
            'path': '<path d="M28 60H54L48 46H32L28 60Z" fill="{c}"/><circle cx="36" cy="52" r="4" stroke="{c}" stroke-width="2"/><circle cx="48" cy="52" r="4" stroke="{c}" stroke-width="2"/>',
        },
        'user': {
            'path': '<circle cx="40.5" cy="32" r="12" stroke="{c}" stroke-width="3"/><path d="M24 62C24 52 32 44 40.5 44C49 44 57 52 57 62" stroke="{c}" stroke-width="3" stroke-linecap="round"/>',
        },
        'admin': {
            'path': '<rect x="24" y="22" width="33" height="37" rx="4" stroke="{c}" stroke-width="3"/><line x1="32" y1="32" x2="48" y2="32" stroke="{c}" stroke-width="3" stroke-linecap="round"/><line x1="32" y1="40" x2="48" y2="40" stroke="{c}" stroke-width="3" stroke-linecap="round"/><line x1="32" y1="48" x2="40" y2="48" stroke="{c}" stroke-width="3" stroke-linecap="round"/>',
        },
        'search': {
            'path': '<circle cx="38" cy="38" r="10" stroke="{c}" stroke-width="3"/><line x1="45" y1="45" x2="55" y2="55" stroke="{c}" stroke-width="3" stroke-linecap="round"/>',
        },
        'order': {
            'path': '<rect x="22" y="24" width="37" height="33" rx="4" stroke="{c}" stroke-width="3"/><line x1="30" y1="32" x2="51" y2="32" stroke="{c}" stroke-width="3" stroke-linecap="round"/><line x1="30" y1="40" x2="51" y2="40" stroke="{c}" stroke-width="3" stroke-linecap="round"/><line x1="30" y1="48" x2="43" y2="48" stroke="{c}" stroke-width="3" stroke-linecap="round"/>',
        },
        'favorite': {
            'path': 'M40.5 26L35 36L24 38L32 46L34 58L40.5 52L47 58L49 46L57 38L46 36L40.5 26Z',
        },
    }
    
    if name not in icons:
        print(f"✗ 未知的图标: {name}")
        print(f"可用图标: {', '.join(icons.keys())}")
        return
    
    path_template = icons[name]['path']
    
    inactive = f'''<svg width="81" height="81" viewBox="0 0 81 81" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="81" height="81" rx="12" fill="#F5F5F5"/>
  {path_template.format(c=icon_color)}
</svg>'''
    
    active = f'''<svg width="81" height="81" viewBox="0 0 81 81" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="81" height="81" rx="12" fill="{active_color}"/>
  {path_template.format(c='#FFFFFF')}
</svg>'''
    
    with open(os.path.join(output_dir, f'{name}.svg'), 'w', encoding='utf-8') as f:
        f.write(inactive)
    
    with open(os.path.join(output_dir, f'{name}-active.svg'), 'w', encoding='utf-8') as f:
        f.write(active)
    
    print(f"✓ 创建图标: {name}.svg, {name}-active.svg")


def main():
    if not HAS_PIL:
        print("警告: Pillow 未安装，部分功能不可用")
        print("安装: pip install pillow")
    
    while True:
        print_menu()
        choice = input("请选择 (0-8): ").strip()
        
        if choice == '0':
            break
        elif choice == '1':
            svg_path = input("SVG 文件路径: ").strip()
            png_path = input("PNG 输出路径: ").strip()
            size_input = input("尺寸 (默认 81x81): ").strip()
            size = tuple(map(int, size_input.split('x'))) if size_input else (81, 81)
            svg_to_png(svg_path, png_path, size)
        elif choice == '2':
            png_path = input("PNG 文件路径: ").strip()
            svg_path = input("SVG 输出路径: ").strip()
            png_to_svg(png_path, svg_path)
        elif choice == '3':
            png_path = input("PNG 文件路径 (多个用逗号分隔): ").strip()
            ico_path = input("ICO 输出路径: ").strip()
            paths = [p.strip() for p in png_path.split(',')]
            create_ico(paths, ico_path)
        elif choice == '4':
            png_path = input("PNG 文件路径: ").strip()
            png_to_base64(png_path)
        elif choice == '5':
            base64_str = input("Base64 字符串: ").strip()
            png_path = input("PNG 输出路径: ").strip()
            base64_to_png(base64_str, png_path)
        elif choice == '6':
            input_path = input("输入文件: ").strip()
            output_path = input("输出文件: ").strip()
            size_input = input("尺寸 (如 81x81): ").strip()
            size = tuple(map(int, size_input.split('x')))
            resize_image(input_path, output_path, size)
        elif choice == '7':
            input_dir = input("输入目录: ").strip()
            output_dir = input("输出目录: ").strip()
            output_format = input("输出格式 (png/svg): ").strip() or 'png'
            size_input = input("尺寸 (默认 81x81): ").strip()
            size = tuple(map(int, size_input.split('x'))) if size_input else (81, 81)
            batch_convert(input_dir, output_dir, output_format, size)
        elif choice == '8':
            name = input("图标名称: ").strip()
            output_dir = input("输出目录: ").strip() or 'output'
            create_tabbar_icon(name, output_dir)
        else:
            print("无效选择")


if __name__ == '__main__':
    main()
