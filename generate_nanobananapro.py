#!/usr/bin/env python3
"""
Nano Banana Pro (Gemini 3 Pro Image) parallel generator with adaptive rate limiting.
Generates all 171 panels for Everpeak Citadel comic.
"""

import os
import sys
import json
import asyncio
import logging
import time as time_module
from pathlib import Path
from google import genai
from google.genai import types
from dotenv import load_dotenv
from PIL import Image

# Load environment
load_dotenv()

# Configuration
PAGES_JSON_DIR = Path("pages")
OUTPUT_DIR = Path("output")
PANELS_DIR = OUTPUT_DIR / "nanobananapro_panels"

# Rate limiting settings - adaptive
MIN_CONCURRENT = 2
MAX_CONCURRENT = int(os.getenv('MAX_CONCURRENT', 15))  # Start conservative
INITIAL_CONCURRENT = 8

# Model configuration
PRO_MODEL_ID = "gemini-3-pro-image-preview"

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


class AdaptiveSemaphore:
    """Semaphore with adaptive concurrency based on rate limit responses."""

    def __init__(self, initial_value, min_value=2, max_value=20):
        self.value = initial_value
        self.min_value = min_value
        self.max_value = max_value
        self._semaphore = asyncio.Semaphore(initial_value)
        self._lock = asyncio.Lock()
        self._current_permits = initial_value

    async def acquire(self):
        """Acquire a permit."""
        await self._semaphore.acquire()

    def release(self):
        """Release a permit."""
        self._semaphore.release()

    async def increase_concurrency(self):
        """Increase concurrency when things are going well."""
        async with self._lock:
            if self._current_permits < self.max_value:
                old = self._current_permits
                self._current_permits = min(self._current_permits + 1, self.max_value)
                # Add a new permit
                self._semaphore.release()
                logger.info(f"⬆️  Increased concurrency: {old} → {self._current_permits}")

    async def decrease_concurrency(self):
        """Decrease concurrency when hitting rate limits."""
        async with self._lock:
            if self._current_permits > self.min_value:
                old = self._current_permits
                self._current_permits = max(self._current_permits - 2, self.min_value)
                # Remove permits by acquiring without releasing
                try:
                    for _ in range(2):
                        if self._current_permits < old:
                            self._semaphore.acquire_nowait()
                except:
                    pass
                logger.warning(f"⬇️  Decreased concurrency: {old} → {self._current_permits}")

    def get_current(self):
        """Get current concurrency level."""
        return self._current_permits


class RPMLimiter:
    """Token bucket rate limiter for requests per minute."""

    def __init__(self, max_per_minute=50):
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
adaptive_semaphore = AdaptiveSemaphore(INITIAL_CONCURRENT, MIN_CONCURRENT, MAX_CONCURRENT)
rpm_limiter = RPMLimiter(max_per_minute=50)

# Stats tracking
stats = {
    'total': 0,
    'successful': 0,
    'skipped': 0,
    'failed': 0,
    'rate_limited': 0,
    'start_time': None
}


def setup_directories():
    """Create output directory structure."""
    PANELS_DIR.mkdir(parents=True, exist_ok=True)
    logger.info("✓ Created output directories")


def load_page_data(page_num):
    """Load page data from JSON file."""
    page_file = PAGES_JSON_DIR / f"page-{page_num:03d}.json"
    if not page_file.exists():
        raise FileNotFoundError(f"Page file not found: {page_file}")

    with open(page_file, 'r', encoding='utf-8') as f:
        return json.load(f)


async def generate_panel_async(panel, page_num, client):
    """Generate a single panel with Nano Banana Pro (with retry logic)."""

    panel_num = panel['panel_num']
    output_path = PANELS_DIR / f"page-{page_num:03d}-panel-{panel_num}.png"

    # Skip if already exists
    if output_path.exists():
        logger.info(f"⏭️  Skipped page {page_num} panel {panel_num} (already exists)")
        stats['skipped'] += 1
        return True

    prompt = panel.get('prompt', '')
    if not prompt:
        logger.error(f"✗ No prompt for page {page_num} panel {panel_num}")
        stats['failed'] += 1
        return False

    # Retry logic with exponential backoff
    max_retries = 5
    base_delay = 2

    for attempt in range(max_retries):
        try:
            # Acquire rate limiting tokens
            await adaptive_semaphore.acquire()
            await rpm_limiter.acquire()

            try:
                # Run sync API call in thread pool
                success = await asyncio.to_thread(
                    generate_panel_sync,
                    prompt,
                    output_path,
                    page_num,
                    panel_num
                )

                if success:
                    stats['successful'] += 1

                    # Occasionally increase concurrency when things go well
                    if stats['successful'] % 10 == 0:
                        await adaptive_semaphore.increase_concurrency()

                    return True
                else:
                    stats['failed'] += 1
                    return False

            finally:
                adaptive_semaphore.release()

        except Exception as e:
            error_str = str(e)

            # Handle rate limiting
            if '429' in error_str or 'rate limit' in error_str.lower():
                stats['rate_limited'] += 1
                await adaptive_semaphore.decrease_concurrency()
                delay = base_delay * (2 ** attempt)
                logger.warning(f"⚠️  Rate limited page {page_num} panel {panel_num}, retry {attempt+1}/{max_retries} in {delay}s")
                await asyncio.sleep(delay)
                continue

            # Handle 503 (service overload)
            elif '503' in error_str:
                delay = base_delay * (2 ** attempt)
                logger.warning(f"⚠️  Service overloaded page {page_num} panel {panel_num}, retry {attempt+1}/{max_retries} in {delay}s")
                await asyncio.sleep(delay)
                continue

            # Other errors
            else:
                logger.error(f"✗ Error page {page_num} panel {panel_num}: {e}")
                stats['failed'] += 1
                return False

    # Max retries exhausted
    logger.error(f"✗ Failed page {page_num} panel {panel_num} after {max_retries} attempts")
    stats['failed'] += 1
    return False


def generate_panel_sync(prompt, output_path, page_num, panel_num):
    """Synchronous generation (called from thread pool)."""
    try:
        client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

        config = types.GenerateContentConfig(
            response_modalities=['Image'],
            image_config=types.ImageConfig(aspect_ratio='2:3')
        )

        response = client.models.generate_content(
            model=PRO_MODEL_ID,
            contents=prompt,
            config=config
        )

        # Save image
        for part in response.parts:
            if image := part.as_image():
                image.save(str(output_path))
                # Re-open with PIL to get size
                pil_img = Image.open(str(output_path))
                size = pil_img.size
                logger.info(f"✓ Generated page {page_num:03d} panel {panel_num} ({size[0]}x{size[1]})")
                return True

        logger.error(f"✗ No image in response for page {page_num} panel {panel_num}")
        return False

    except Exception as e:
        # Re-raise to be handled by retry logic
        raise


async def generate_page(page_num, client):
    """Generate all panels for a page."""
    try:
        page_data = load_page_data(page_num)
        panels = page_data.get('panels', [])

        if not panels:
            logger.warning(f"⚠️  No panels found for page {page_num}")
            return []

        logger.info(f"📄 Page {page_num}: {len(panels)} panels")

        # Generate all panels for this page in parallel
        tasks = [generate_panel_async(panel, page_num, client) for panel in panels]
        results = await asyncio.gather(*tasks)

        return results

    except FileNotFoundError:
        logger.warning(f"⚠️  Page {page_num} JSON not found, skipping")
        return []
    except Exception as e:
        logger.error(f"✗ Error processing page {page_num}: {e}")
        return []


async def main():
    """Main generation pipeline."""
    import argparse

    parser = argparse.ArgumentParser(description='Generate comic panels with Nano Banana Pro')
    parser.add_argument('pages', nargs='?', default='1-45',
                       help='Page range (e.g., "1-45", "1,3,5", "10")')
    parser.add_argument('--concurrent', type=int, default=INITIAL_CONCURRENT,
                       help=f'Initial concurrent requests (default: {INITIAL_CONCURRENT})')
    args = parser.parse_args()

    # Update initial concurrency
    global adaptive_semaphore
    adaptive_semaphore = AdaptiveSemaphore(args.concurrent, MIN_CONCURRENT, MAX_CONCURRENT)

    # Parse page range
    pages = []
    if '-' in args.pages:
        start, end = map(int, args.pages.split('-'))
        pages = list(range(start, end + 1))
    elif ',' in args.pages:
        pages = [int(p.strip()) for p in args.pages.split(',')]
    else:
        pages = [int(args.pages)]

    setup_directories()

    # Calculate total panels
    total_panels = 0
    for page_num in pages:
        try:
            page_data = load_page_data(page_num)
            total_panels += len(page_data.get('panels', []))
        except:
            pass

    logger.info("=" * 70)
    logger.info("NANO BANANA PRO COMIC GENERATION")
    logger.info("=" * 70)
    logger.info(f"Model: {PRO_MODEL_ID}")
    logger.info(f"Pages: {args.pages} ({len(pages)} pages)")
    logger.info(f"Total panels: {total_panels}")
    logger.info(f"Initial concurrency: {args.concurrent}")
    logger.info(f"Adaptive range: {MIN_CONCURRENT}-{MAX_CONCURRENT}")
    logger.info(f"Estimated cost: ${total_panels * 0.134:.2f}")
    logger.info(f"Output: {PANELS_DIR}/")
    logger.info("=" * 70)

    stats['total'] = total_panels
    stats['start_time'] = time_module.time()

    client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

    # Process all pages
    logger.info(f"\n🚀 Starting generation...")

    for page_num in pages:
        await generate_page(page_num, client)

        # Progress update
        completed = stats['successful'] + stats['skipped']
        logger.info(f"📊 Progress: {completed}/{total_panels} panels "
                   f"({stats['successful']} generated, {stats['skipped']} skipped, "
                   f"{stats['failed']} failed, {stats['rate_limited']} rate limited) "
                   f"[Concurrency: {adaptive_semaphore.get_current()}]")

    # Final stats
    elapsed = time_module.time() - stats['start_time']
    completed = stats['successful'] + stats['skipped']

    logger.info("\n" + "=" * 70)
    logger.info("✓ GENERATION COMPLETE")
    logger.info("=" * 70)
    logger.info(f"Time: {elapsed/60:.1f} minutes ({elapsed:.0f}s)")
    logger.info(f"Total: {completed}/{total_panels} panels")
    logger.info(f"  Generated: {stats['successful']}")
    logger.info(f"  Skipped: {stats['skipped']}")
    logger.info(f"  Failed: {stats['failed']}")
    logger.info(f"  Rate limited: {stats['rate_limited']}")
    logger.info(f"Actual cost: ${stats['successful'] * 0.134:.2f}")
    logger.info(f"Output: {PANELS_DIR}/")
    logger.info("=" * 70)

    if stats['failed'] > 0:
        logger.warning(f"\n⚠️  {stats['failed']} panels failed - you can re-run to retry")


if __name__ == "__main__":
    asyncio.run(main())
