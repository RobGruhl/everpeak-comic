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
SPREAD_WIDTH = 3200  # Two-page spread width
GUTTER = 20
BORDER = 3

# Layout strategies for different panel counts
LAYOUT_STRATEGIES = {
    1: "full_page",      # Single splash panel
    2: "vertical_half",  # Two panels stacked vertically
    3: "vertical_third", # Three panels stacked vertically
    4: "2x2_grid",       # Perfect 2x2 grid
    5: "2_over_3",       # 2 wider panels top, 3 smaller bottom (best for 5)
    6: "2x3_grid",       # Standard 2x3 grid
    7: "3_over_4",       # 3 panels top row, 4 panels bottom row
    8: "2x4_grid",       # 2 columns, 4 rows
    9: "3x3_grid",       # Perfect 3x3 grid
}


def setup_directories():
    """Create output directory structure."""
    PAGES_DIR.mkdir(parents=True, exist_ok=True)
    print(f"✓ Created output directories")


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


def apply_layout_2_over_3(page_img, panels, page_num, page_width, page_height):
    """Apply 2-over-3 layout: 2 wider panels on top, 3 smaller panels on bottom."""
    # Top row: 2 panels
    top_panel_width = (page_width - 3 * GUTTER) // 2
    top_panel_height = (page_height - 3 * GUTTER) // 2

    # Bottom row: 3 panels
    bottom_panel_width = (page_width - 4 * GUTTER) // 3
    bottom_panel_height = (page_height - 3 * GUTTER) // 2

    # Place first 2 panels in top row
    for i in range(min(2, len(panels))):
        panel_file = PANELS_DIR / f"page-{page_num:03d}-panel-{panels[i]['panel_num']}.png"
        if panel_file.exists():
            img = Image.open(panel_file)
            img = img.resize((top_panel_width, top_panel_height), Image.Resampling.LANCZOS)
            x = GUTTER + i * (top_panel_width + GUTTER)
            y = GUTTER
            page_img.paste(img, (x, y))

    # Place remaining 3 panels in bottom row
    for i in range(2, min(5, len(panels))):
        panel_file = PANELS_DIR / f"page-{page_num:03d}-panel-{panels[i]['panel_num']}.png"
        if panel_file.exists():
            img = Image.open(panel_file)
            img = img.resize((bottom_panel_width, bottom_panel_height), Image.Resampling.LANCZOS)
            col = i - 2
            x = GUTTER + col * (bottom_panel_width + GUTTER)
            y = GUTTER + top_panel_height + GUTTER
            page_img.paste(img, (x, y))


def apply_layout_3_over_4(page_img, panels, page_num, page_width, page_height):
    """Apply 3-over-4 layout: 3 panels on top row, 4 panels on bottom row."""
    # Top row: 3 panels
    top_panel_width = (page_width - 4 * GUTTER) // 3
    top_panel_height = (page_height - 3 * GUTTER) // 2

    # Bottom row: 4 panels
    bottom_panel_width = (page_width - 5 * GUTTER) // 4
    bottom_panel_height = (page_height - 3 * GUTTER) // 2

    # Place first 3 panels in top row
    for i in range(min(3, len(panels))):
        panel_file = PANELS_DIR / f"page-{page_num:03d}-panel-{panels[i]['panel_num']}.png"
        if panel_file.exists():
            img = Image.open(panel_file)
            img = img.resize((top_panel_width, top_panel_height), Image.Resampling.LANCZOS)
            x = GUTTER + i * (top_panel_width + GUTTER)
            y = GUTTER
            page_img.paste(img, (x, y))

    # Place remaining 4 panels in bottom row
    for i in range(3, min(7, len(panels))):
        panel_file = PANELS_DIR / f"page-{page_num:03d}-panel-{panels[i]['panel_num']}.png"
        if panel_file.exists():
            img = Image.open(panel_file)
            img = img.resize((bottom_panel_width, bottom_panel_height), Image.Resampling.LANCZOS)
            col = i - 3
            x = GUTTER + col * (bottom_panel_width + GUTTER)
            y = GUTTER + top_panel_height + GUTTER
            page_img.paste(img, (x, y))


def apply_standard_grid(page_img, panels, page_num, page_width, page_height, cols, rows):
    """Apply standard grid layout."""
    panel_width = (page_width - (cols + 1) * GUTTER) // cols
    panel_height = (page_height - (rows + 1) * GUTTER) // rows

    for i, panel in enumerate(panels):
        if i >= cols * rows:  # Safety check
            break

        panel_file = PANELS_DIR / f"page-{page_num:03d}-panel-{panel['panel_num']}.png"
        if panel_file.exists():
            img = Image.open(panel_file)
            img = img.resize((panel_width, panel_height), Image.Resampling.LANCZOS)

            col = i % cols
            row = i // cols
            x = GUTTER + col * (panel_width + GUTTER)
            y = GUTTER + row * (panel_height + GUTTER)
            page_img.paste(img, (x, y))


def cleanup_variants(page_num, panels):
    """Delete variant files for a page after successful assembly."""
    deleted_count = 0

    for panel in panels:
        # Find all variant files (page-XXX-panel-X-v*.png)
        pattern = f"page-{page_num:03d}-panel-{panel['panel_num']}-v*.png"
        variant_files = list(PANELS_DIR.glob(pattern))

        for variant_file in variant_files:
            try:
                variant_file.unlink()
                deleted_count += 1
            except Exception as e:
                print(f"  ⚠ Warning: Could not delete {variant_file.name}: {e}")

    if deleted_count > 0:
        print(f"  ✓ Cleaned up {deleted_count} variant file(s)")

    return deleted_count


def assemble_page(page_data, cleanup=False):
    """Assemble panels into a page using smart layout strategies."""

    page_num = page_data['page_num']
    panels = page_data['panels']
    num_panels = len(panels)
    is_spread = page_data.get('is_spread', False)
    is_cover = page_data.get('is_cover', False)

    # Determine page dimensions
    if is_spread:
        page_width = SPREAD_WIDTH
        page_height = PAGE_HEIGHT
        page_type = "spread"
    else:
        page_width = PAGE_WIDTH
        page_height = PAGE_HEIGHT
        page_type = "cover" if is_cover else "page"

    print(f"\n→ Assembling {page_type} {page_num} ({num_panels} panels){' [TWO-PAGE SPREAD]' if is_spread else ''}...")

    # Check if all panels have been selected (skip for cover since it won't have variants)
    if not is_cover:
        missing_panels = []
        for panel in panels:
            # For cover page, look for cover-panel-1.png instead of page-000-panel-1.png
            if page_num == 0:
                panel_file = PANELS_DIR / f"cover-panel-{panel['panel_num']}.png"
            else:
                panel_file = PANELS_DIR / f"page-{page_num:03d}-panel-{panel['panel_num']}.png"

            if not panel_file.exists():
                missing_panels.append(panel['panel_num'])

        if missing_panels:
            print(f"  ✗ Error: Missing selected panels: {missing_panels}")
            print(f"  Run review.py to select variants first")
            return None

    # Create blank page
    page_img = Image.new('RGB', (page_width, page_height), 'white')

    # Apply layout strategy based on panel count
    layout_strategy = LAYOUT_STRATEGIES.get(num_panels)

    if num_panels == 1 or is_cover:
        # Full page splash
        apply_standard_grid(page_img, panels, page_num, page_width, page_height, 1, 1)

    elif num_panels == 2:
        # Vertical stack (2 rows, 1 column)
        apply_standard_grid(page_img, panels, page_num, page_width, page_height, 1, 2)

    elif num_panels == 3:
        # Vertical stack (3 rows, 1 column)
        apply_standard_grid(page_img, panels, page_num, page_width, page_height, 1, 3)

    elif num_panels == 4:
        # 2x2 grid
        apply_standard_grid(page_img, panels, page_num, page_width, page_height, 2, 2)

    elif num_panels == 5:
        # 2-over-3 layout (optimal for 5 panels)
        apply_layout_2_over_3(page_img, panels, page_num, page_width, page_height)

    elif num_panels == 6:
        # 2x3 grid
        apply_standard_grid(page_img, panels, page_num, page_width, page_height, 2, 3)

    elif num_panels == 7:
        # 3-over-4 layout (optimal for 7 panels)
        apply_layout_3_over_4(page_img, panels, page_num, page_width, page_height)

    elif num_panels == 8:
        # 2x4 grid
        apply_standard_grid(page_img, panels, page_num, page_width, page_height, 2, 4)

    elif num_panels == 9:
        # 3x3 grid
        apply_standard_grid(page_img, panels, page_num, page_width, page_height, 3, 3)

    else:
        # Fallback: use 3-column grid for 10+ panels
        cols = 3
        rows = (num_panels + 2) // 3
        apply_standard_grid(page_img, panels, page_num, page_width, page_height, cols, rows)

    # Save page with appropriate naming
    if page_num == 0:
        output_file = PAGES_DIR / "cover.png"
    else:
        output_file = PAGES_DIR / f"page-{page_num:03d}.png"

    page_img.save(output_file)
    print(f"✓ Saved {output_file.name} ({page_width}x{page_height})")

    # Cleanup variants if requested (skip for cover)
    if cleanup and not is_cover:
        cleanup_variants(page_num, panels)

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
  python assemble.py 1                    # Assemble page 1 only
  python assemble.py 1-5                  # Assemble pages 1-5
  python assemble.py                      # Assemble all available pages
  python assemble.py 1 --no-cbz           # Assemble page without creating CBZ
  python assemble.py 1 --cleanup-variants # Assemble and delete variant files
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

    parser.add_argument(
        '--cleanup-variants',
        action='store_true',
        help='Delete variant files (v1, v2, etc.) after successful assembly'
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
        result = assemble_page(page_data, cleanup=args.cleanup_variants)
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
