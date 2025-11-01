#!/usr/bin/env python3
"""
Async parallel comic generator for Everpeak Citadel.
Generates multiple variants per panel with intelligent rate limiting.
"""

import os
import sys
import json
import base64
import asyncio
import argparse
import logging
from pathlib import Path
from openai import AsyncOpenAI
from PIL import Image, ImageDraw
from dotenv import load_dotenv
import aiofiles
from tenacity import (
    retry,
    wait_exponential,
    stop_after_attempt,
    retry_if_exception_type
)
from openai import RateLimitError, APIError
import time as time_module

# Load environment variables
load_dotenv()

# Configuration
PAGES_JSON_DIR = Path("pages")
OUTPUT_DIR = Path("output")
PANELS_DIR = OUTPUT_DIR / "panels"
PAGES_DIR = OUTPUT_DIR / "pages"

# Rate limiting settings (can be overridden via env vars or CLI)
MAX_CONCURRENT = int(os.getenv('MAX_CONCURRENT', 20))  # Maximum concurrent API requests (default: 20)
MAX_RPM = int(os.getenv('MAX_RPM', 50))                # Maximum requests per minute
VARIANTS_PER_PANEL = 3  # Number of variants to generate per panel

# Image generation settings
PANEL_WIDTH = 1024
PANEL_HEIGHT = 1024

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


class RPMLimiter:
    """Token bucket rate limiter for requests per minute."""

    def __init__(self, max_per_minute):
        self.max_per_minute = max_per_minute
        self.capacity = float(max_per_minute)
        self.last_update = time_module.time()
        self.lock = asyncio.Lock()

    async def acquire(self):
        """Acquire permission to make a request."""
        async with self.lock:
            now = time_module.time()
            elapsed = now - self.last_update

            # Refill capacity based on time elapsed
            self.capacity = min(
                self.capacity + (self.max_per_minute * elapsed / 60.0),
                self.max_per_minute
            )
            self.last_update = now

            # Wait if no capacity
            while self.capacity < 1.0:
                await asyncio.sleep(0.1)
                now = time_module.time()
                elapsed = now - self.last_update
                self.capacity = min(
                    self.capacity + (self.max_per_minute * elapsed / 60.0),
                    self.max_per_minute
                )
                self.last_update = now

            # Consume one token
            self.capacity -= 1.0


# Global rate limiters
semaphore = asyncio.Semaphore(MAX_CONCURRENT)
rpm_limiter = RPMLimiter(MAX_RPM)


def setup_directories():
    """Create output directory structure."""
    PANELS_DIR.mkdir(parents=True, exist_ok=True)
    PAGES_DIR.mkdir(parents=True, exist_ok=True)
    logger.info("✓ Created output directories")


def load_page_data(page_num):
    """Load page data from JSON file."""
    # Handle cover page (page 0)
    if page_num == 0:
        page_file = PAGES_JSON_DIR / "cover.json"
    else:
        page_file = PAGES_JSON_DIR / f"page-{page_num:03d}.json"

    if not page_file.exists():
        raise FileNotFoundError(f"Page file not found: {page_file}")

    with open(page_file, 'r', encoding='utf-8') as f:
        return json.load(f)


@retry(
    retry=retry_if_exception_type((RateLimitError, APIError)),
    wait=wait_exponential(multiplier=1, min=1, max=60),
    stop=stop_after_attempt(3)
)
async def generate_panel_variant_async(panel, page_num, variant_num, client, is_cover=False):
    """Generate a single variant of a panel with retry logic."""

    # Use cover naming for cover page
    if is_cover or page_num == 0:
        variant_filename = PANELS_DIR / f"cover-panel-{panel['panel_num']}-v{variant_num}.png"
    else:
        variant_filename = PANELS_DIR / f"page-{page_num:03d}-panel-{panel['panel_num']}-v{variant_num}.png"

    # Get prompt from panel data
    prompt = panel.get('prompt', '')
    if not prompt:
        logger.error(f"  ✗ No prompt found for panel {panel['panel_num']}")
        return None

    # Get size from panel data or use default
    size = panel.get('size', '1024x1024')

    # Acquire rate limiting tokens
    async with semaphore:
        await rpm_limiter.acquire()

        try:
            start_time = time_module.time()

            # Generate image with OpenAI
            response = await client.images.generate(
                model="gpt-image-1",
                prompt=prompt,
                size=size,
                quality="high",
                n=1
            )

            duration = time_module.time() - start_time

            # Decode and save image
            image_bytes = base64.b64decode(response.data[0].b64_json)

            async with aiofiles.open(variant_filename, 'wb') as f:
                await f.write(image_bytes)

            logger.info(f"  ✓ Panel {panel['panel_num']} variant {variant_num} generated in {duration:.1f}s")
            return variant_filename

        except Exception as e:
            logger.error(f"  ✗ Error generating panel {panel['panel_num']} variant {variant_num}: {e}")

            # Create placeholder on failure
            img = Image.new('RGB', (PANEL_WIDTH, PANEL_HEIGHT), 'lightgray')
            draw = ImageDraw.Draw(img)
            draw.text((50, 50), f"Error: {str(e)[:100]}", fill='black')
            img.save(variant_filename)

            return variant_filename


async def generate_panel_variants(panel, page_num, client, is_cover=False):
    """Generate all variants for a single panel concurrently."""

    # Determine file naming prefix
    if is_cover or page_num == 0:
        prefix = "cover"
        final_filename = PANELS_DIR / f"cover-panel-{panel['panel_num']}.png"
        variant_pattern = lambda v: PANELS_DIR / f"cover-panel-{panel['panel_num']}-v{v}.png"
    else:
        prefix = f"page-{page_num:03d}"
        final_filename = PANELS_DIR / f"page-{page_num:03d}-panel-{panel['panel_num']}.png"
        variant_pattern = lambda v: PANELS_DIR / f"page-{page_num:03d}-panel-{panel['panel_num']}-v{v}.png"

    # Check if final selection already exists
    if final_filename.exists():
        logger.info(f"  ↪ Panel {panel['panel_num']} already selected, skipping")
        return

    # Check if all variants already exist
    all_exist = all(
        variant_pattern(i).exists()
        for i in range(1, VARIANTS_PER_PANEL + 1)
    )

    if all_exist:
        logger.info(f"  ↪ Panel {panel['panel_num']} variants already generated, skipping")
        return

    logger.info(f"  → Generating {VARIANTS_PER_PANEL} variants for panel {panel['panel_num']}...")

    # Generate all variants concurrently
    tasks = [
        generate_panel_variant_async(panel, page_num, variant_num, client, is_cover)
        for variant_num in range(1, VARIANTS_PER_PANEL + 1)
    ]

    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Count successes
    successes = sum(1 for r in results if r is not None and not isinstance(r, Exception))
    logger.info(f"  ✓ Panel {panel['panel_num']}: {successes}/{VARIANTS_PER_PANEL} variants generated")


async def generate_page_panels(page_data, client):
    """Generate all panels for a page."""

    page_num = page_data['page_num']
    panels = page_data['panels']
    is_spread = page_data.get('is_spread', False)
    is_cover = page_data.get('is_cover', False)
    page_end = page_data.get('page_end')

    # Display page info
    page_label = "Cover" if is_cover else f"Page {page_num}"
    if is_spread and page_end:
        page_label += f"-{page_end} (SPREAD)"

    logger.info(f"\n📄 {page_label} ({len(panels)} panels, {len(panels) * VARIANTS_PER_PANEL} total images)")

    # Process all panels in parallel (each panel generates 3 variants concurrently)
    # The semaphore limits total concurrent API requests across all panels
    tasks = [
        generate_panel_variants(panel, page_num, client, is_cover)
        for panel in panels
    ]
    await asyncio.gather(*tasks)


async def generate_pages_async(page_nums, force=False, concurrent=None, rpm=None):
    """Generate panels for specified pages."""

    # Check for API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        logger.error("✗ Error: OPENAI_API_KEY environment variable not set")
        logger.error("  Set it in .env file or: export OPENAI_API_KEY='your-key-here'")
        return

    client = AsyncOpenAI(api_key=api_key)

    # Use provided values or defaults
    concurrent = concurrent or MAX_CONCURRENT
    rpm = rpm or MAX_RPM

    logger.info("=" * 60)
    logger.info("EVERPEAK CITADEL COMIC GENERATOR")
    logger.info(f"Concurrent requests: {concurrent} | RPM limit: {rpm}")
    logger.info(f"Variants per panel: {VARIANTS_PER_PANEL}")
    logger.info("=" * 60)

    setup_directories()

    # Load page data
    pages_data = []
    for page_num in page_nums:
        try:
            page_data = load_page_data(page_num)
            pages_data.append(page_data)
            logger.info(f"✓ Loaded page {page_num}: '{page_data.get('title', 'Untitled')}' ({page_data['panel_count']} panels)")
        except FileNotFoundError as e:
            logger.error(f"✗ Error loading page {page_num}: {e}")
            logger.error("  Run parse_script.py first to generate page JSON files")
            return

    if not pages_data:
        logger.error("✗ No valid pages to generate")
        return

    # Generate panels
    logger.info("\n" + "=" * 60)
    logger.info("GENERATING PANEL VARIANTS")
    logger.info("=" * 60)

    start_time = time_module.time()

    for page_data in pages_data:
        await generate_page_panels(page_data, client)

    duration = time_module.time() - start_time
    total_variants = sum(p['panel_count'] * VARIANTS_PER_PANEL for p in pages_data)

    logger.info("\n" + "=" * 60)
    logger.info(f"✓ Generation complete in {duration:.1f}s ({total_variants} images)")
    logger.info(f"  Next step: python review.py {page_nums[0]}")
    logger.info("=" * 60)

    await client.close()


def parse_page_range(page_arg):
    """Parse page argument (e.g., '1', '1-5', '1,3,5')."""
    pages = []

    for part in page_arg.split(','):
        if '-' in part:
            start, end = part.split('-')
            pages.extend(range(int(start), int(end) + 1))
        else:
            pages.append(int(part))

    return sorted(set(pages))


def main():
    """Main entry point."""

    parser = argparse.ArgumentParser(
        description='Generate comic panel variants with OpenAI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate.py 1          # Generate page 1
  python generate.py 1-5        # Generate pages 1-5
  python generate.py 1,3,5      # Generate pages 1, 3, and 5
  python generate.py 1 --force  # Regenerate page 1 even if exists
        """
    )

    parser.add_argument(
        'pages',
        type=str,
        help='Page number(s) to generate (e.g., 1, 1-5, 1,3,5)'
    )

    parser.add_argument(
        '--force',
        action='store_true',
        help='Regenerate panels even if they already exist'
    )

    parser.add_argument(
        '--concurrent',
        type=int,
        default=MAX_CONCURRENT,
        help=f'Maximum concurrent requests (default: {MAX_CONCURRENT})'
    )

    parser.add_argument(
        '--rpm',
        type=int,
        default=MAX_RPM,
        help=f'Maximum requests per minute (default: {MAX_RPM})'
    )

    args = parser.parse_args()

    # Update global rate limiters
    global semaphore, rpm_limiter
    semaphore = asyncio.Semaphore(args.concurrent)
    rpm_limiter = RPMLimiter(args.rpm)

    # Parse page numbers
    try:
        page_nums = parse_page_range(args.pages)
    except ValueError as e:
        logger.error(f"✗ Invalid page argument: {args.pages}")
        logger.error(f"  Use format like: 1, 1-5, or 1,3,5")
        sys.exit(1)

    # Run async generation
    asyncio.run(generate_pages_async(page_nums, args.force, args.concurrent, args.rpm))


if __name__ == "__main__":
    main()
