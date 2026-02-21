import os
import shutil


def rename_image(old_path: str, new_name: str, output_dir: str = None) -> dict:
    """
    Rename an image file.

    Args:
        old_path: Path to the original image
        new_name: New name (without extension)
        output_dir: Optional output directory

    Returns:
        dict with success and new_path
    """
    try:
        if not os.path.exists(old_path):
            return {
                "success": False,
                "error": f"File not found: {old_path}"
            }

        ext = os.path.splitext(old_path)[1]
        if not ext:
            ext = ".jpg"

        if output_dir is None:
            output_dir = os.path.dirname(old_path) or "."

        os.makedirs(output_dir, exist_ok=True)

        new_path = os.path.join(output_dir, f"{new_name}{ext}")

        if os.path.exists(new_path):
            new_path = os.path.join(output_dir, f"{new_name}_{os.getpid()}{ext}")

        shutil.copy2(old_path, new_path)

        return {
            "success": True,
            "old_path": old_path,
            "new_path": new_path
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python rename_image.py <old_path> <new_name> [output_dir]")
        sys.exit(1)

    old_path = sys.argv[1]
    new_name = sys.argv[2]
    output_dir = sys.argv[3] if len(sys.argv) > 3 else None

    result = rename_image(old_path, new_name, output_dir)
    print(result)
