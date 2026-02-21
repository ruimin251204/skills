import os
from PIL import Image


SUPPORTED_FORMATS = ["jpg", "jpeg", "png", "webp", "gif", "bmp", "tiff"]


def convert_image_format(input_path: str, output_format: str, output_path: str = None) -> dict:
    """
    Convert image to different format.

    Args:
        input_path: Path to input image
        output_format: Target format (jpg, png, webp, gif, bmp)
        output_path: Optional output path

    Returns:
        dict with success and output_path
    """
    try:
        if output_format.lower() not in SUPPORTED_FORMATS:
            return {
                "success": False,
                "error": f"Unsupported format: {output_format}. Supported: {SUPPORTED_FORMATS}"
            }

        with Image.open(input_path) as img:
            if output_path is None:
                name, _ = os.path.splitext(input_path)
                output_path = f"{name}.{output_format.lower()}"

            os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

            if output_format.lower() in ["jpg", "jpeg"]:
                if img.mode in ("RGBA", "LA", "P"):
                    background = Image.new("RGB", img.size, (255, 255, 255))
                    if img.mode == "P":
                        img = img.convert("RGBA")
                    background.paste(img, mask=img.split()[-1] if img.mode in ("RGBA", "LA") else None)
                    background.save(output_path, "JPEG", quality=95)
                else:
                    img.convert("RGB").save(output_path, "JPEG", quality=95)
            else:
                img.save(output_path)

        return {
            "success": True,
            "output_path": output_path,
            "format": output_format.upper()
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print(f"Usage: python convert_format.py <input_path> <output_format> [output_path]")
        print(f"Supported formats: {SUPPORTED_FORMATS}")
        sys.exit(1)

    input_path = sys.argv[1]
    output_format = sys.argv[2]
    output_path = sys.argv[3] if len(sys.argv) > 3 else None

    result = convert_image_format(input_path, output_format, output_path)
    print(result)
