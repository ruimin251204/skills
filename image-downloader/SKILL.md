---
name: image-downloader
description: 图片下载工具，支持从URL批量下载图片、格式转换、重命名和预览功能。使用场景：(1) 从指定URL下载单张或多张图片 (2) 批量下载多个图片链接 (3) 图片格式转换 (4) 图片重命名 (5) 下载前预览图片
---

# Image Downloader

从URL下载图片的工具，支持批量下载、格式转换、重命名和预览功能。

## 使用方式

### 1. 下载单张图片

```python
from scripts.download_image import download_image

# 下载单张图片
result = download_image(
    url="https://example.com/image.jpg",
    save_path="images/photo.jpg",
    preview=True  # 显示预览
)
```

### 2. 批量下载

```python
from scripts.batch_download import batch_download

# 从URL列表批量下载
results = batch_download(
    urls=[
        "https://example.com/img1.jpg",
        "https://example.com/img2.png",
        "https://example.com/img3.webp"
    ],
    output_dir="images/",
    prefix="photo_"  # 可选前缀
)
```

### 3. 格式转换

```python
from scripts.convert_format import convert_image_format

# 转换图片格式
convert_image_format(
    input_path="images/photo.jpg",
    output_format="png",  # 支持: jpg, png, webp, gif, bmp
    output_path="images/photo.png"
)
```

### 4. 重命名

```python
from scripts.rename_image import rename_image

# 重命名图片
rename_image(
    old_path="images/photo.jpg",
    new_name="vacation_2024",
    output_dir="images/"
)
```

## 脚本说明

### scripts/download_image.py
- 功能：下载单张图片，支持预览
- 参数：url (str), save_path (str), preview (bool)
- 返回：dict，包含success、file_path、error信息

### scripts/batch_download.py  
- 功能：批量下载多个URL的图片
- 参数：urls (list), output_dir (str), prefix (str)
- 返回：list[dict]，每个元素包含各图片的下载结果

### scripts/convert_format.py
- 功能：转换图片格式
- 参数：input_path (str), output_format (str), output_path (str)
- 返回：dict，包含success、output_path信息

### scripts/rename_image.py
- 功能：重命名图片文件
- 参数：old_path (str), new_name (str), output_dir (str)
- 返回：dict，包含success、new_path信息

### scripts/preview.py
- 功能：显示图片预览信息
- 参数：image_path (str)
- 返回：dict，包含width、height、format、size等信息
