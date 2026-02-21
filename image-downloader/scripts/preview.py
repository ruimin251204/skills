import os
from PIL import Image


def preview(image_path: str) -> dict:
    """
    Get image preview information.

    Args:
        image_path: Path to the image file

    Returns:
        dict with width, height, format, size, etc.
    """
    try:
        if not os.path.exists(image_path):
            return {
                "success": False,
                "error": f"File not found: {image_path}"
            }

        with Image.open(image_path) as img:
            info = {
                "success": True,
                "path": image_path,
                "filename": os.path.basename(image_path),
                "width": img.width,
                "height": img.height,
                "format": img.format,
                "mode": img.mode,
                "size_bytes": os.path.getsize(image_path)
            }

            info["size_formatted"] = format_size(info["size_bytes"])
            info["aspect_ratio"] = round(info["width"] / info["height"], 2) if info["height"] > 0 else 0

            return info

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def format_size(size_bytes: int) -> str:
    """Format bytes to human readable size."""
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} TB"


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python preview.py <image_path>")
        sys.exit(1)

    result = preview(sys.argv[1])
    print(result)
