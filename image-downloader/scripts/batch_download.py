import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm


def download_single(url: str, output_dir: str, prefix: str = "") -> dict:
    """Download a single image from URL."""
    try:
        os.makedirs(output_dir, exist_ok=True)

        filename = url.split("/")[-1].split("?")[0]
        if not filename or "." not in filename:
            filename = "image.jpg"

        if prefix:
            name, ext = os.path.splitext(filename)
            filename = f"{prefix}{name}{ext}"

        save_path = os.path.join(output_dir, filename)

        response = requests.get(url, timeout=30)
        response.raise_for_status()

        with open(save_path, "wb") as f:
            f.write(response.content)

        return {
            "success": True,
            "url": url,
            "file_path": save_path,
            "size": len(response.content)
        }

    except Exception as e:
        return {
            "success": False,
            "url": url,
            "error": str(e)
        }


def batch_download(urls: list, output_dir: str = "images/", prefix: str = "", max_workers: int = 5) -> list:
    """
    Batch download multiple images from URLs.

    Args:
        urls: List of image URLs
        output_dir: Output directory
        prefix: Optional prefix for filenames
        max_workers: Maximum concurrent downloads

    Returns:
        List of download results
    """
    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(download_single, url, output_dir, prefix): url for url in urls}

        for future in tqdm(as_completed(futures), total=len(urls), desc="Downloading"):
            results.append(future.result())

    success_count = sum(1 for r in results if r["success"])
    print(f"\nDownload complete: {success_count}/{len(urls)} successful")

    return results


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python batch_download.py <url1> <url2> ...")
        sys.exit(1)

    urls = sys.argv[1:]
    results = batch_download(urls)
    for r in results:
        print(r)
