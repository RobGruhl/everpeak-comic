#!/usr/bin/env python3
"""
Page assembly and CBZ creation for Everpeak Citadel comic.
Assembles selected panel images into full pages and packages as CBZ.
"""

import sys
import json
import zipfile
import argparse
from pathlib import Path
from PIL import Image

# Configuration
PAGES_JSON_DIR = Path("pages")
OUTPUT_DIR = Path("output")
PANELS_DIR = OUTPUT_DIR / "panels"
PAGES_DIR = OUTPUT_DIR / "pages"
CBZ_FILE = OUTPUT_DIR / "everpeak-citadel.cbz"

# Layout settings
PAGE_WIDTH = 1600
PAGE_HEIGHT = 2400
GUTTER = 20
BORDER = 3


def setup_directories():
    """Create output directory structure."""
    PAGES_DIR.mkdir(parents=True, exist_ok=True)
    print(f"✓ Created output directories")


def load_page_data(page_num):
    """Load page data from JSON file."""
    page_file = PAGES_JSON_DIR / f"page-{page_num:03d}.json"

    if not page_file.exists():
        raise FileNotFoundError(f"Page file not found: {page_file}")

    with open(page_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def list_available_pages():
    """List all available page JSON files."""
    if not PAGES_JSON_DIR.exists():
        return []

    page_files = sorted(PAGES_JSON_DIR.glob("page-*.json"))
    pages = []

    for page_file in page_files:
        with open(page_file, 'r', encoding='utf-8') as f:
            page_data = json.load(f)
            pages.append(page_data)

    return pages


def assemble_page(page_data):
    """Assemble panels into a page."""

    page_num = page_data['page_num']
    panels = page_data['panels']
    num_panels = len(panels)

    print(f"\n→ Assembling page {page_num} ({num_panels} panels)...")

    # Check if all panels have been selected
    missing_panels = []
    for panel in panels:
        panel_file = PANELS_DIR / f"page-{page_num:03d}-panel-{panel['panel_num']}.png"
        if not panel_file.exists():
            missing_panels.append(panel['panel_num'])

    if missing_panels:
        print(f"  ✗ Error: Missing selected panels: {missing_panels}")
        print(f"  Run review.py to select variants first")
        return None

    # Create blank page
    page_img = Image.new('RGB', (PAGE_WIDTH, PAGE_HEIGHT), 'white')

    # Simple layout logic
    if num_panels <= 3:
        # Vertical stack
        panel_height = (PAGE_HEIGHT - (num_panels + 1) * GUTTER) // num_panels

        for i, panel in enumerate(panels):
            panel_file = PANELS_DIR / f"page-{page_num:03d}-panel-{panel['panel_num']}.png"
            if panel_file.exists():
                img = Image.open(panel_file)
                # Resize to fit
                img = img.resize((PAGE_WIDTH - 2 * GUTTER, panel_height), Image.Resampling.LANCZOS)

                y = GUTTER + i * (panel_height + GUTTER)
                page_img.paste(img, (GUTTER, y))

    elif num_panels <= 6:
        # 2x3 grid
        cols = 2
        rows = (num_panels + 1) // 2
        panel_width = (PAGE_WIDTH - (cols + 1) * GUTTER) // cols
        panel_height = (PAGE_HEIGHT - (rows + 1) * GUTTER) // rows

        for i, panel in enumerate(panels):
            panel_file = PANELS_DIR / f"page-{page_num:03d}-panel-{panel['panel_num']}.png"
            if panel_file.exists():
                img = Image.open(panel_file)
                img = img.resize((panel_width, panel_height), Image.Resampling.LANCZOS)

                col = i % cols
                row = i // cols
                x = GUTTER + col * (panel_width + GUTTER)
                y = GUTTER + row * (panel_height + GUTTER)
                page_img.paste(img, (x, y))

    else:
        # 3-column grid
        cols = 3
        rows = (num_panels + 2) // 3
        panel_width = (PAGE_WIDTH - (cols + 1) * GUTTER) // cols
        panel_height = (PAGE_HEIGHT - (rows + 1) * GUTTER) // rows

        for i, panel in enumerate(panels):
            panel_file = PANELS_DIR / f"page-{page_num:03d}-panel-{panel['panel_num']}.png"
            if panel_file.exists():
                img = Image.open(panel_file)
                img = img.resize((panel_width, panel_height), Image.Resampling.LANCZOS)

                col = i % cols
                row = i // cols
                x = GUTTER + col * (panel_width + GUTTER)
                y = GUTTER + row * (panel_height + GUTTER)
                page_img.paste(img, (x, y))

    # Save page
    output_file = PAGES_DIR / f"page-{page_num:03d}.png"
    page_img.save(output_file)
    print(f"✓ Saved {output_file.name}")

    return output_file


def create_cbz(pages_data, output_file=None):
    """Create CBZ file from assembled pages."""

    if output_file is None:
        output_file = CBZ_FILE

    print("\n→ Creating CBZ archive...")

    # ComicInfo.xml metadata
    comic_info = """<?xml version="1.0"?>
<ComicInfo xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
  <Title>Everpeak Citadel: Echoes of the Dawn's Crown</Title>
  <Series>Everpeak Citadel</Series>
  <Number>1</Number>
  <Summary>A D&D adventure in the frozen peaks of Everpeak Citadel.</Summary>
  <Publisher>AI-Generated</Publisher>
  <Genre>Fantasy</Genre>
  <PageCount>{}</PageCount>
  <LanguageISO>en</LanguageISO>
</ComicInfo>""".format(len(pages_data))

    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as cbz:
        # Add ComicInfo.xml
        cbz.writestr('ComicInfo.xml', comic_info)

        # Add pages in order
        for page in sorted(pages_data, key=lambda p: p['page_num']):
            page_file = PAGES_DIR / f"page-{page['page_num']:03d}.png"
            if page_file.exists():
                # CBZ readers expect sequential numbering
                cbz.write(page_file, f"{page['page_num']:03d}.png")

    print(f"✓ Created {output_file}")
    print(f"\n🎉 Comic complete! Open {output_file} in any CBZ reader.")


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
        description='Assemble comic pages and create CBZ archive',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python assemble.py 1          # Assemble page 1 only
  python assemble.py 1-5        # Assemble pages 1-5
  python assemble.py            # Assemble all available pages
  python assemble.py 1 --no-cbz # Assemble page without creating CBZ
        """
    )

    parser.add_argument(
        'pages',
        type=str,
        nargs='?',
        help='Page number(s) to assemble (e.g., 1, 1-5, 1,3,5). Omit to assemble all.'
    )

    parser.add_argument(
        '--no-cbz',
        action='store_true',
        help='Skip CBZ creation (only assemble pages)'
    )

    parser.add_argument(
        '--output',
        type=str,
        help='Custom CBZ output filename'
    )

    args = parser.parse_args()

    print("=" * 60)
    print("EVERPEAK CITADEL PAGE ASSEMBLY")
    print("=" * 60)

    setup_directories()

    # Determine which pages to assemble
    if args.pages:
        try:
            page_nums = parse_page_range(args.pages)
        except ValueError:
            print(f"✗ Invalid page argument: {args.pages}")
            print(f"  Use format like: 1, 1-5, or 1,3,5")
            sys.exit(1)

        pages_data = []
        for page_num in page_nums:
            try:
                page_data = load_page_data(page_num)
                pages_data.append(page_data)
            except FileNotFoundError as e:
                print(f"✗ Error: {e}")
                sys.exit(1)
    else:
        # Assemble all available pages
        pages_data = list_available_pages()
        if not pages_data:
            print("✗ No page JSON files found")
            print("  Run parse_script.py first to generate page JSON files")
            sys.exit(1)

        page_nums = [p['page_num'] for p in pages_data]

    print(f"\n→ Assembling {len(pages_data)} page(s): {page_nums}")

    # Assemble pages
    print("\n" + "=" * 60)
    print("ASSEMBLING PAGES")
    print("=" * 60)

    assembled_pages = []
    for page_data in pages_data:
        result = assemble_page(page_data)
        if result:
            assembled_pages.append(page_data)

    if not assembled_pages:
        print("\n✗ No pages were assembled successfully")
        sys.exit(1)

    # Create CBZ
    if not args.no_cbz:
        print("\n" + "=" * 60)
        print("PACKAGING CBZ")
        print("=" * 60)

        output_file = Path(args.output) if args.output else CBZ_FILE
        create_cbz(assembled_pages, output_file)
    else:
        print(f"\n✓ Assembled {len(assembled_pages)} page(s) successfully")
        print("  Skipped CBZ creation (--no-cbz flag)")


if __name__ == "__main__":
    main()
