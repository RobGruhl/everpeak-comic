#!/usr/bin/env python3
"""
Optimize comic pages for web delivery.
Generates WebP versions at reduced resolution with quality optimization.
"""

import subprocess
from pathlib import Path
from PIL import Image
import json
import sys

# Configuration
SOURCE_DIR = Path("output/pages")
TARGET_DIR = Path("site/images/pages")
THUMB_DIR = Path("site/images/thumbnails")

# Optimization settings
PAGE_WIDTH = 1200
PAGE_HEIGHT = 1800
THUMB_WIDTH = 200
THUMB_HEIGHT = 300
WEBP_QUALITY = 88
THUMB_QUALITY = 80


def check_imagemagick():
    """Check if ImageMagick is available."""
    try:
        result = subprocess.run(
            ["magick", "--version"],
            capture_output=True,
            text=True,
            check=False
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


def optimize_page_imagemagick(source_path, target_path, width, height, quality):
    """Use ImageMagick to optimize image to WebP."""
    cmd = [
        "magick", str(source_path),
        "-resize", f"{width}x{height}",
        "-quality", str(quality),
        "-define", "webp:method=6",  # Best compression
        str(target_path)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ImageMagick failed: {result.stderr}")


def optimize_page_pillow(source_path, target_path, width, height, quality):
    """Use Pillow to optimize image to WebP (fallback)."""
    img = Image.open(source_path)
    # Resize maintaining aspect ratio
    img.thumbnail((width, height), Image.Resampling.LANCZOS)
    img.save(target_path, "WEBP", quality=quality, method=6)


def generate_thumbnail(source_path, target_path):
    """Generate thumbnail using Pillow for precise control."""
    img = Image.open(source_path)
    img.thumbnail((THUMB_WIDTH, THUMB_HEIGHT), Image.Resampling.LANCZOS)
    img.save(target_path, "WEBP", quality=THUMB_QUALITY)


def format_size(bytes_size):
    """Format bytes to human-readable size."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} TB"


def main():
    """Main optimization process."""
    # Check prerequisites
    use_imagemagick = check_imagemagick()
    if use_imagemagick:
        print("✓ Using ImageMagick for optimization")
    else:
        print("⚠ ImageMagick not found, using Pillow (slower, less optimal)")

    # Create output directories
    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    THUMB_DIR.mkdir(parents=True, exist_ok=True)

    # Find all page images
    page_files = sorted(SOURCE_DIR.glob("page-*.png"))

    if not page_files:
        print(f"✗ No page files found in {SOURCE_DIR}")
        print(f"  Make sure comic pages have been generated first.")
        sys.exit(1)

    print(f"\nFound {len(page_files)} pages to optimize")
    print(f"Target: {PAGE_WIDTH}x{PAGE_HEIGHT}px WebP @ quality {WEBP_QUALITY}")
    print(f"Thumbnails: {THUMB_WIDTH}x{THUMB_HEIGHT}px WebP @ quality {THUMB_QUALITY}\n")

    total_original_size = 0
    total_optimized_size = 0
    total_thumb_size = 0

    # Process each page
    for i, page_file in enumerate(page_files, 1):
        page_num = page_file.stem  # e.g., "page-001"
        target_path = TARGET_DIR / f"{page_num}.webp"
        thumb_path = THUMB_DIR / f"{page_num}.webp"

        original_size = page_file.stat().st_size
        total_original_size += original_size

        print(f"[{i}/{len(page_files)}] Processing {page_num}...")

        try:
            # Generate optimized page
            if use_imagemagick:
                optimize_page_imagemagick(
                    page_file, target_path,
                    PAGE_WIDTH, PAGE_HEIGHT, WEBP_QUALITY
                )
            else:
                optimize_page_pillow(
                    page_file, target_path,
                    PAGE_WIDTH, PAGE_HEIGHT, WEBP_QUALITY
                )

            optimized_size = target_path.stat().st_size
            total_optimized_size += optimized_size

            # Generate thumbnail
            generate_thumbnail(page_file, thumb_path)
            thumb_size = thumb_path.stat().st_size
            total_thumb_size += thumb_size

            # Calculate savings
            reduction = (1 - optimized_size / original_size) * 100

            print(f"  Original: {format_size(original_size)}")
            print(f"  Optimized: {format_size(optimized_size)} (-{reduction:.1f}%)")
            print(f"  Thumbnail: {format_size(thumb_size)}")

        except Exception as e:
            print(f"  ✗ Error: {e}")
            continue

    # Summary
    print("\n" + "="*60)
    print("OPTIMIZATION SUMMARY")
    print("="*60)
    print(f"Pages processed: {len(page_files)}")
    print(f"\nOriginal total:   {format_size(total_original_size)}")
    print(f"Optimized total:  {format_size(total_optimized_size)}")
    print(f"Thumbnails total: {format_size(total_thumb_size)}")
    print(f"Combined web size: {format_size(total_optimized_size + total_thumb_size)}")

    total_reduction = (1 - (total_optimized_size + total_thumb_size) / total_original_size) * 100
    print(f"\nTotal size reduction: {total_reduction:.1f}%")
    print(f"Space saved: {format_size(total_original_size - total_optimized_size - total_thumb_size)}")

    print(f"\n✓ Optimized images saved to: {TARGET_DIR}")
    print(f"✓ Thumbnails saved to: {THUMB_DIR}")

    # Average sizes
    avg_page_size = total_optimized_size / len(page_files) if page_files else 0
    avg_thumb_size = total_thumb_size / len(page_files) if page_files else 0
    print(f"\nAverage page size: {format_size(avg_page_size)}")
    print(f"Average thumbnail size: {format_size(avg_thumb_size)}")


if __name__ == "__main__":
    main()
