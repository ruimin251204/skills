import os
import requests
from PIL import Image
from io import BytesIO


def download_image(url: str, save_path: str, preview: bool = False) -> dict:
    """
    Download a single image from URL.

    Args:
        url: Image URL
        save_path: Local path to save the image
        preview: Whether to show preview info

    Returns:
        dict with success, file_path, and error info
    """
    try:
        os.makedirs(os.path.dirname(save_path) or ".", exist_ok=True)

        response = requests.get(url, timeout=30)
        response.raise_for_status()

        with open(save_path, "wb") as f:
            f.write(response.content)

        result = {
            "success": True,
            "file_path": save_path,
            "size": len(response.content)
        }

        if preview:
            result["preview"] = get_image_info(save_path)

        return result

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def get_image_info(image_path: str) -> dict:
    """Get image metadata."""
    try:
        with Image.open(image_path) as img:
            return {
                "width": img.width,
                "height": img.height,
                "format": img.format,
                "mode": img.mode,
                "size_bytes": os.path.getsize(image_path)
            }
    except Exception:
        return {}


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python download_image.py <url> <save_path>")
        sys.exit(1)

    result = download_image(sys.argv[1], sys.argv[2])
    print(result)
