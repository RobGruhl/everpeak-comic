#!/usr/bin/env python3
"""
Restructure comic pages for simplified layout system.

Converts existing pages (with variable panel counts) into new structure:
- Splash pages: 1 panel
- Standard pages: 4 panels in 2x2 grid

All panels converted to 1024x1536 (portrait, 2:3 aspect ratio).
"""

import json
import shutil
from pathlib import Path


PAGES_DIR = Path("pages")
BACKUP_DIR = Path("pages_backup")
OUTPUT_DIR = Path("pages_restructured")


def backup_current_pages():
    """Backup existing pages before restructuring."""
    if BACKUP_DIR.exists():
        shutil.rmtree(BACKUP_DIR)
    shutil.copytree(PAGES_DIR, BACKUP_DIR)
    print(f"✓ Backed up {len(list(PAGES_DIR.glob('page-*.json')))} pages to {BACKUP_DIR}")


def load_page(page_file):
    """Load a page JSON file."""
    with open(page_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_page(page_data, page_num):
    """Save a restructured page JSON."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    output_file = OUTPUT_DIR / f"page-{page_num:03d}.json"

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(page_data, f, indent=2, ensure_ascii=False)


def update_panel_format(panel):
    """Update panel to new format (all portrait 1024x1536)."""
    panel['aspect_ratio'] = 'tall'
    panel['size'] = '1024x1536'
    # Remove annotation since we only have 2 layouts now
    if 'annotation' in panel:
        del panel['annotation']
    return panel


def restructure_single_page(old_page, start_panel_num=1):
    """
    Restructure a single page into new format.

    Returns list of new pages (may split into multiple pages).
    """
    panels = old_page['panels']
    num_panels = len(panels)

    new_pages = []

    if num_panels == 1:
        # Splash page - keep as is
        new_page = {
            'page_num': None,  # Will be assigned later
            'title': old_page.get('title', ''),
            'panel_count': 1,
            'is_spread': False,
            'panels': [update_panel_format(panels[0].copy())]
        }
        new_pages.append(new_page)

    elif num_panels <= 4:
        # Single 2x2 grid page
        updated_panels = [update_panel_format(p.copy()) for p in panels]

        # Renumber panels 1-4
        for i, panel in enumerate(updated_panels, 1):
            panel['panel_num'] = i

        new_page = {
            'page_num': None,  # Will be assigned later
            'title': old_page.get('title', ''),
            'panel_count': len(updated_panels),
            'is_spread': False,
            'panels': updated_panels
        }
        new_pages.append(new_page)

    else:
        # Multiple pages needed
        # Strategy: Split into groups of 4, last group can be 1-4 panels

        for i in range(0, num_panels, 4):
            batch = panels[i:i+4]
            updated_batch = [update_panel_format(p.copy()) for p in batch]

            # Renumber panels 1-4 within this page
            for j, panel in enumerate(updated_batch, 1):
                panel['panel_num'] = j

            new_page = {
                'page_num': None,  # Will be assigned later
                'title': f"{old_page.get('title', '')} (Part {len(new_pages) + 1})",
                'panel_count': len(updated_batch),
                'is_spread': False,
                'panels': updated_batch
            }
            new_pages.append(new_page)

    return new_pages


def restructure_all_pages():
    """Restructure all pages in the pages directory."""
    page_files = sorted(PAGES_DIR.glob("page-*.json"))

    print(f"\n{'='*60}")
    print("RESTRUCTURING PAGES")
    print(f"{'='*60}\n")

    all_new_pages = []
    stats = {
        'original_pages': len(page_files),
        'original_panels': 0,
        'new_pages': 0,
        'splits': 0,  # Pages that were split
    }

    for page_file in page_files:
        old_page = load_page(page_file)
        old_num = old_page['page_num']
        old_count = len(old_page['panels'])

        stats['original_panels'] += old_count

        new_pages = restructure_single_page(old_page)

        if len(new_pages) > 1:
            stats['splits'] += 1
            print(f"  Page {old_num:2d} ({old_count} panels) → Split into {len(new_pages)} pages")
        else:
            print(f"  Page {old_num:2d} ({old_count} panels) → {new_pages[0]['panel_count']} panel(s)")

        all_new_pages.extend(new_pages)

    # Assign new page numbers
    for i, page in enumerate(all_new_pages, 1):
        page['page_num'] = i
        save_page(page, i)

    stats['new_pages'] = len(all_new_pages)

    print(f"\n{'='*60}")
    print("RESTRUCTURING COMPLETE")
    print(f"{'='*60}\n")
    print(f"Original: {stats['original_pages']} pages, {stats['original_panels']} panels")
    print(f"New:      {stats['new_pages']} pages ({stats['splits']} splits)")
    print(f"\nRestructured pages saved to: {OUTPUT_DIR}")
    print(f"Original pages backed up to: {BACKUP_DIR}")

    return stats


def main():
    """Main entry point."""
    print("=" * 60)
    print("COMIC PAGE RESTRUCTURING")
    print("=" * 60)
    print()
    print("This will restructure all pages to the simplified system:")
    print("  - Splash pages: 1 panel (full page)")
    print("  - Standard pages: 4 panels (2x2 grid)")
    print("  - All panels: 1024x1536 (portrait)")
    print()

    response = input("Proceed with restructuring? (yes/no): ")

    if response.lower() != 'yes':
        print("Cancelled.")
        return

    print()
    backup_current_pages()
    stats = restructure_all_pages()

    print("\nNext steps:")
    print("1. Review restructured pages in pages_restructured/")
    print("2. If satisfied, replace pages/ directory:")
    print("   rm -rf pages/")
    print("   mv pages_restructured/ pages/")
    print("3. Delete old panel images (different aspect ratios)")
    print("4. Run generate.py to create new 1024x1536 panels")


if __name__ == "__main__":
    main()
