import requests
import os
from urllib.parse import urlparse
import hashlib


def fetch_image(url: str, save_dir="Fetched_Images"):
    """
    Fetch an image from a given URL and save it to the specified directory.
    Returns the saved filename if successful, otherwise None.
    """
    try:
        # Ensure save directory exists
        os.makedirs(save_dir, exist_ok=True)

        # Fetch image
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # Extract filename from URL
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)

        if not filename or "." not in filename:
            # Default filename with hash to avoid duplicates
            file_hash = hashlib.md5(url.encode()).hexdigest()[:8]
            filename = f"downloaded_{file_hash}.jpg"

        filepath = os.path.join(save_dir, filename)

        # Avoid duplicate downloads
        if os.path.exists(filepath):
            print(f"↻ Skipped duplicate: {filename}")
            return None

        # Save image in binary mode
        with open(filepath, "wb") as f:
            f.write(response.content)

        print(f"✓ Successfully fetched: {filename}")
        print(f"✓ Image saved to {filepath}")
        return filename

    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error: {e}")
    except Exception as e:
        print(f"✗ An error occurred: {e}")
    return None


def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")

    # Allow multiple URLs
    urls = input("Please enter one or more image URLs (comma separated): ").split(",")

    for url in [u.strip() for u in urls if u.strip()]:
        fetch_image(url)

    print("\nConnection strengthened. Community enriched.")


if __name__ == "__main__":
    main()