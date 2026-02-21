---
name: icon-generator
description: 图标生成和转换工具。用于创建、转换、优化 SVG/PNG/ICO 图标，支持小程序 tabbar 图标、UI 图标、favicon 等场景。当用户需要：(1) 创建新图标 (2) 转换图标格式 (3) 生成多尺寸图标 (4) 批量处理图标 (5) 优化 SVG/PNG/ICO 图标
---

# 图标生成器

用于创建、转换、优化 SVG/PNG/ICO 图标。

## 支持的格式

| 格式 | 说明 | 用途 |
|-----|-----|-----|
| SVG | 矢量图 | 小程序、网页 |
| PNG | 位图 | 通用图片 |
| ICO | Windows图标 | favicon |
| Base64 | 数据URI | 内联使用 |

---

## 格式转换

### 1. SVG → PNG

```javascript
// 使用 canvas 将 SVG 转为 PNG
const svgToPng = async (svgPath, pngPath, width, height) => {
  const fs = uni.getFileSystemManager();
  const svgData = await fs.readFile({ filePath: svgPath, encoding: 'utf-8' });
  
  const canvas = uni.createCanvasContext('canvas');
  const image = canvas.createImage();
  image.src = 'data:image/svg+xml;base64,' + uni.base64Encode(svgData);
  
  image.onload = () => {
    canvas.drawImage(image, 0, 0, width, height);
    canvas.exportToTempFilePath({
      success: (res) => {
        console.log('PNG saved:', res.tempFilePath);
      }
    });
  };
};
```

### 2. PNG → SVG（简单转换）

```python
# Python 脚本转换
from PIL import Image

def png_to_svg(png_path, svg_path, bg_color="#F5F5F5", icon_color="#7A7E83"):
    img = Image.open(png_path)
    width, height = img.size
    
    # 简化的 SVG 转换
    svg = f'''<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
  <rect width="{width}" height="{height}" fill="{bg_color}"/>
  <image href="{png_path}" width="{width}" height="{height}"/>
</svg>'''
    
    with open(svg_path, 'w') as f:
        f.write(svg)
```

### 3. 单图生成多尺寸

```javascript
// 生成多个尺寸的图标
const sizes = [16, 32, 48, 64, 128, 256];

sizes.forEach(size => {
  // 生成不同尺寸的 PNG
});
```

---

## 小程序 Tabbar 图标

### 配置示例

```json
{
  "tabBar": {
    "color": "#7A7E83",
    "selectedColor": "#3cc51f",
    "list": [
      {
        "pagePath": "pages/index/index",
        "iconPath": "static/tabbar/home.svg",
        "selectedIconPath": "static/tabbar/home-active.svg",
        "text": "首页"
      }
    ]
  }
}
```

### 尺寸要求

- 建议尺寸：81x81 像素
- 最大尺寸：144x144 像素
- 推荐格式：PNG 或 SVG

---

## Favicon 图标

### 常用尺寸

| 尺寸 | 用途 |
|-----|-----|
| 16x16 | 浏览器标签 |
| 32x32 | 浏览器标签/任务栏 |
| 48x48 | Android |
| 96x96 | 桌面快捷方式 |
| 192x192 | PWA |
| 512x512 | PWA/应用商店 |

### 生成脚本

```javascript
// 生成 favicon 所需的所有尺寸
const faviconSizes = [16, 32, 48, 96, 192, 512];

faviconSizes.forEach(size => {
  // 1. 生成 PNG
  // 2. 生成 ICO (16, 32, 48)
  // 3. 生成 SVG
});
```

---

## 常用图标模板

### Tabbar 图标（81x81）

```svg
<!-- 首页 - 未选中 -->
<svg width="81" height="81" viewBox="0 0 81 81" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="81" height="81" rx="12" fill="#F5F5F5"/>
  <path d="M40.5 22L22 37V60H31V44H50V60H59V37L40.5 22Z" fill="#7A7E83"/>
</svg>

<!-- 首页 - 选中 -->
<svg width="81" height="81" viewBox="0 0 81 81" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="81" height="81" rx="12" fill="#3CC51F"/>
  <path d="M40.5 22L22 37V60H31V44H50V60H59V37L40.5 22Z" fill="#FFFFFF"/>
</svg>
```

---

## 使用流程

### 创建小程序图标

1. 选择图标类型
2. 生成 SVG 文件
3. 更新 pages.json 配置
4. 编译测试

### 批量转换

1. 准备源图片
2. 选择目标格式
3. 执行批量转换
4. 验证输出

---

## 注意事项

1. 小程序 tabbar 不支持 GIF
2. 图标文件不超过 40KB
3. 建议使用 PNG 或 SVG
4. 选中/未选中图标尺寸必须一致
