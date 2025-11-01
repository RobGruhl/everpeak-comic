#!/usr/bin/env python3
"""
Sequential panel packing for simplified layout system.

Collects all panels from all pages and packs them sequentially into:
- Splash pages: 1 panel (for dramatic moments)
- Standard pages: 4 panels in 2x2 grid

All panels converted to 1024x1536 (portrait, 2:3 aspect ratio).
"""

import json
import shutil
from pathlib import Path


PAGES_DIR = Path("pages")
BACKUP_DIR = Path("pages_backup_sequential")
OUTPUT_DIR = Path("pages_sequential")


def backup_current_pages():
    """Backup existing pages before restructuring."""
    if BACKUP_DIR.exists():
        shutil.rmtree(BACKUP_DIR)
    shutil.copytree(PAGES_DIR, BACKUP_DIR)
    print(f"✓ Backed up {len(list(PAGES_DIR.glob('page-*.json')))} pages to {BACKUP_DIR}")


def load_all_panels():
    """Load all panels from all pages in sequence."""
    page_files = sorted(PAGES_DIR.glob("page-*.json"))
    all_panels = []

    for page_file in page_files:
        with open(page_file, 'r', encoding='utf-8') as f:
            page_data = json.load(f)

        for panel in page_data['panels']:
            # Keep track of original page for context
            panel_copy = panel.copy()
            panel_copy['original_page'] = page_data['page_num']
            panel_copy['original_title'] = page_data.get('title', '')
            all_panels.append(panel_copy)

    return all_panels


def update_panel_format(panel):
    """Update panel to new format (all portrait 1024x1536)."""
    panel['aspect_ratio'] = 'tall'
    panel['size'] = '1024x1536'
    # Remove annotation since we only have 2 layouts now
    if 'annotation' in panel:
        del panel['annotation']
    # Remove tracking fields
    if 'original_page' in panel:
        del panel['original_page']
    if 'original_title' in panel:
        del panel['original_title']
    return panel


def is_splash_worthy(panel):
    """Determine if a panel should be a splash page."""
    visual = panel.get('visual', '').lower()

    # Keywords that suggest impact/dramatic moments
    splash_keywords = [
        'full reveal',
        'wide shot of',
        'panoramic',
        'dramatic reveal',
        'impact moment',
        'splash',
        'establishing shot',
    ]

    return any(keyword in visual for keyword in splash_keywords)


def pack_panels_sequentially(all_panels):
    """Pack panels into pages of 1 or 4 panels."""
    pages = []
    i = 0
    panels_remaining = len(all_panels)

    while i < len(all_panels):
        panels_left = len(all_panels) - i

        # If we have fewer than 4 panels left, make them splash pages
        if panels_left < 4:
            for panel in all_panels[i:]:
                panel_copy = update_panel_format(panel.copy())
                panel_copy['panel_num'] = 1

                page = {
                    'page_num': len(pages) + 1,
                    'title': panel.get('original_title', f'Page {len(pages) + 1}'),
                    'panel_count': 1,
                    'is_spread': False,
                    'panels': [panel_copy]
                }
                pages.append(page)
            break

        panel = all_panels[i]

        # Check if this should be a splash page
        if is_splash_worthy(panel):
            # Create splash page
            panel_copy = update_panel_format(panel.copy())
            panel_copy['panel_num'] = 1

            page = {
                'page_num': len(pages) + 1,
                'title': panel.get('original_title', f'Page {len(pages) + 1}'),
                'panel_count': 1,
                'is_spread': False,
                'panels': [panel_copy]
            }
            pages.append(page)
            i += 1
        else:
            # Create 4-panel page
            batch = all_panels[i:i+4]
            updated_panels = []

            for j, p in enumerate(batch, 1):
                panel_copy = update_panel_format(p.copy())
                panel_copy['panel_num'] = j
                updated_panels.append(panel_copy)

            # Use title from first panel's original page
            title = batch[0].get('original_title', f'Page {len(pages) + 1}')

            page = {
                'page_num': len(pages) + 1,
                'title': title,
                'panel_count': 4,
                'is_spread': False,
                'panels': updated_panels
            }
            pages.append(page)
            i += 4

    return pages


def save_pages(pages):
    """Save all restructured pages."""
    OUTPUT_DIR.mkdir(exist_ok=True)

    for page in pages:
        output_file = OUTPUT_DIR / f"page-{page['page_num']:03d}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(page, f, indent=2, ensure_ascii=False)


def main():
    """Main entry point."""
    print("=" * 60)
    print("SEQUENTIAL PANEL PACKING")
    print("=" * 60)
    print()
    print("This will pack all panels sequentially into:")
    print("  - Splash pages: 1 panel (dramatic moments)")
    print("  - Standard pages: 4 panels (2x2 grid)")
    print("  - All panels: 1024x1536 (portrait)")
    print()

    response = input("Proceed with sequential packing? (yes/no): ")

    if response.lower() != 'yes':
        print("Cancelled.")
        return

    print()
    backup_current_pages()

    print("\n→ Loading all panels...")
    all_panels = load_all_panels()
    print(f"✓ Loaded {len(all_panels)} panels from {len(list(PAGES_DIR.glob('page-*.json')))} pages")

    print("\n→ Packing panels sequentially...")
    new_pages = pack_panels_sequentially(all_panels)

    # Count splash vs standard pages
    splash_count = sum(1 for p in new_pages if p['panel_count'] == 1)
    standard_count = len(new_pages) - splash_count
    partial_count = sum(1 for p in new_pages if 1 < p['panel_count'] < 4)

    print(f"✓ Created {len(new_pages)} pages:")
    print(f"  - {splash_count} splash pages (1 panel)")
    print(f"  - {standard_count - partial_count} standard pages (4 panels)")
    if partial_count > 0:
        print(f"  - {partial_count} partial pages (2-3 panels)")

    print("\n→ Saving restructured pages...")
    save_pages(new_pages)
    print(f"✓ Saved to {OUTPUT_DIR}")

    print(f"\n{'='*60}")
    print("SEQUENTIAL PACKING COMPLETE")
    print(f"{'='*60}\n")
    print(f"Original: {len(list(PAGES_DIR.glob('page-*.json')))} pages, {len(all_panels)} panels")
    print(f"New:      {len(new_pages)} pages")
    print(f"\nRestructured pages saved to: {OUTPUT_DIR}")
    print(f"Original pages backed up to: {BACKUP_DIR}")

    print("\nNext steps:")
    print("1. Review restructured pages in pages_sequential/")
    print("2. If satisfied, replace pages/ directory:")
    print("   rm -rf pages/")
    print("   mv pages_sequential/ pages/")
    print("3. Delete old panel images:")
    print("   rm -rf output/panels/*")
    print("4. Run generate.py to create new 1024x1536 panels")


if __name__ == "__main__":
    main()
