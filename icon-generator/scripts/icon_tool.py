import os
import sys
from PIL import Image
import io

def resize_icon(input_path, output_path, size=(81, 81)):
    """调整图标尺寸"""
    try:
        img = Image.open(input_path)
        img = img.resize(size, Image.LANCZOS)
        img.save(output_path)
        print(f"✓ {input_path} -> {output_path}")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def convert_png_to_svg_style(png_path, svg_path, bg_color="#F5F5F5", icon_color="#7A7E83"):
    """将PNG转换为SVG样式（需要PNG有透明背景）"""
    try:
        img = Image.open(png_path)
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        width, height = img.size
        pixels = img.load()
        
        svg_parts = []
        svg_parts.append(f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">')
        
        # 添加背景
        svg_parts.append(f'<rect width="{width}" height="{height}" rx="12" fill="{bg_color}"/>')
        
        # 简化：只保留非透明像素作为图标区域
        min_x, min_y = width, height
        max_x, max_y = 0, 0
        
        for y in range(height):
            for x in range(width):
                if pixels[x, y][3] > 128:  # 不透明度 > 50%
                    min_x = min(min_x, x)
                    min_y = min(min_y, y)
                    max_x = max(max_x, x)
                    max_y = max(max_y, y)
        
        if min_x < max_x and min_y < max_y:
            icon_width = max_x - min_x + 1
            icon_height = max_y - min_y + 1
            
            # 创建简化矩形表示图标区域
            svg_parts.append(f'<rect x="{min_x}" y="{min_y}" width="{icon_width}" height="{icon_height}" fill="{icon_color}"/>')
        
        svg_parts.append('</svg>')
        
        with open(svg_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(svg_parts))
        
        print(f"✓ {png_path} -> {svg_path}")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def create_tabbar_icons(base_name, output_dir, icon_color="#7A7E83", active_color="#3CC51F"):
    """创建tabbar图标对（未选中和选中）"""
    os.makedirs(output_dir, exist_ok=True)
    
    # 图标路径定义
    icons = {
        'home': {
            'path': 'M40.5 22L22 37V60H31V44H50V60H59V37L40.5 22Z',
            'desc': '首页'
        },
        'category': {
            'path': '''<rect x="24" y="22" width="33" height="33" rx="4" stroke="{color}" stroke-width="3"/>
  <line x1="24" y1="34" x2="57" y2="34" stroke="{color}" stroke-width="3"/>
  <line x1="34" y1="22" x2="34" y2="55" stroke="{color}" stroke-width="3"/>
  <line x1="47" y1="22" x2="47" y2="55" stroke="{color}" stroke-width="3"/>''',
            'desc': '分类'
        },
        'cart': {
            'path': '''<path d="M28 60H54L48 46H32L28 60Z" fill="{color}"/>
  <circle cx="36" cy="52" r="4" stroke="{color}" stroke-width="2"/>
  <circle cx="48" cy="52" r="4" stroke="{color}" stroke-width="2"/>''',
            'desc': '购物车'
        },
        'user': {
            'path': '''<circle cx="40.5" cy="32" r="12" stroke="{color}" stroke-width="3"/>
  <path d="M24 62C24 52 32 44 40.5 44C49 44 57 52 57 62" stroke="{color}" stroke-width="3" stroke-linecap="round"/>''',
            'desc': '用户'
        },
        'admin': {
            'path': '''<rect x="24" y="22" width="33" height="37" rx="4" stroke="{color}" stroke-width="3"/>
  <line x1="32" y1="32" x2="48" y2="32" stroke="{color}" stroke-width="3" stroke-linecap="round"/>
  <line x1="32" y1="40" x2="48" y2="40" stroke="{color}" stroke-width="3" stroke-linecap="round"/>
  <line x1="32" y1="48" x2="40" y2="48" stroke="{color}" stroke-width="3" stroke-linecap="round"/>''',
            'desc': '管理'
        }
    }
    
    if base_name not in icons:
        print(f"✗ Unknown icon: {base_name}")
        return False
    
    icon_info = icons[base_name]
    
    # 创建未选中图标
    inactive_svg = f'''<svg width="81" height="81" viewBox="0 0 81 81" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="81" height="81" rx="12" fill="#F5F5F5"/>
  {icon_info['path'].format(color=icon_color)}
</svg>'''
    
    # 创建选中图标
    active_svg = f'''<svg width="81" height="81" viewBox="0 0 81 81" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="81" height="81" rx="12" fill="{active_color}"/>
  {icon_info['path'].format(color='#FFFFFF')}
</svg>'''
    
    # 保存文件
    inactive_path = os.path.join(output_dir, f'{base_name}.svg')
    active_path = os.path.join(output_dir, f'{base_name}-active.svg')
    
    with open(inactive_path, 'w', encoding='utf-8') as f:
        f.write(inactive_svg)
    
    with open(active_path, 'w', encoding='utf-8') as f:
        f.write(active_svg)
    
    print(f"✓ Created: {inactive_path}")
    print(f"✓ Created: {active_path}")
    return True

def batch_resize(input_dir, output_dir, size=(81, 81)):
    """批量调整图标尺寸"""
    os.makedirs(output_dir, exist_ok=True)
    
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            resize_icon(input_path, output_path, size)

if __name__ == '__main__':
    print("=== 图标工具 ===")
    print("1. 创建tabbar图标对")
    print("2. 调整图标尺寸")
    print("3. PNG转SVG样式")
    
    choice = input("请选择 (1-3): ").strip()
    
    if choice == '1':
        name = input("图标名称 (home/category/cart/user/admin): ").strip()
        output = input("输出目录 (默认: output): ").strip() or 'output'
        create_tabbar_icons(name, output)
    elif choice == '2':
        input_dir = input("输入目录: ").strip()
        output_dir = input("输出目录: ").strip()
        size = input("尺寸 (默认 81x81): ").strip()
        if size:
            w, h = map(int, size.split('x'))
            batch_resize(input_dir, output_dir, (w, h))
        else:
            batch_resize(input_dir, output_dir)
    elif choice == '3':
        png_path = input("PNG文件路径: ").strip()
        svg_path = input("SVG输出路径: ").strip()
        convert_png_to_svg_style(png_path, svg_path)
    else:
        print("无效选择")
