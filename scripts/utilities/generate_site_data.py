#!/usr/bin/env python3
"""
Generate metadata JSON files for the website.
Creates pages.json with page navigation data and copies database files.
"""

import json
import shutil
from pathlib import Path

# Configuration
PAGES_JSON_DIR = Path("pages")
OUTPUT_DATA_DIR = Path("site/data")
CHARACTERS_SOURCE = Path("characters.json")
LOCATIONS_SOURCE = Path("locations.json")


def get_unique_characters(page_data):
    """Extract unique characters from all panels."""
    characters = set()
    for panel in page_data.get('panels', []):
        # Handle characters field (can be list or dict)
        if 'characters' in panel:
            if isinstance(panel['characters'], list):
                characters.update(panel['characters'])
            elif isinstance(panel['characters'], dict):
                characters.update(panel['characters'].keys())

        # Handle npcs field (can be list or dict)
        if 'npcs' in panel:
            if isinstance(panel['npcs'], list):
                characters.update(panel['npcs'])
            elif isinstance(panel['npcs'], dict):
                characters.update(panel['npcs'].keys())

    return sorted(list(characters))


def get_locations(page_data):
    """Extract unique locations from all panels."""
    locations = set()
    for panel in page_data.get('panels', []):
        if 'location' in panel and panel['location']:
            locations.add(panel['location'])
    return sorted(list(locations))


def generate_pages_metadata():
    """Generate pages.json with navigation metadata."""
    pages = []

    # Check for cover.json first
    cover_file = PAGES_JSON_DIR / "cover.json"
    if cover_file.exists():
        with open(cover_file, 'r', encoding='utf-8') as f:
            page_data = json.load(f)

        pages.append({
            "page": 0,
            "title": page_data.get('title', 'Cover'),
            "panel_count": page_data.get('panel_count', 1),
            "is_spread": page_data.get('is_spread', False),
            "is_cover": True,
            "image": "images/pages/page-000.webp",
            "thumbnail": "images/thumbnails/page-000.webp",
            "characters": get_unique_characters(page_data),
            "locations": get_locations(page_data)
        })

    # Load all numbered page JSON files
    page_files = sorted(PAGES_JSON_DIR.glob("page-*.json"))

    for page_file in page_files:
        with open(page_file, 'r', encoding='utf-8') as f:
            page_data = json.load(f)

        page_num = page_data.get('page_num')
        if page_num is None:
            # Try to extract from filename
            try:
                page_num = int(page_file.stem.split('-')[1])
            except (IndexError, ValueError):
                print(f"Warning: Could not determine page number for {page_file}")
                continue

        is_cover = page_data.get('is_cover', False)

        pages.append({
            "page": page_num,
            "title": page_data.get('title', f'Page {page_num}'),
            "panel_count": page_data.get('panel_count', 0),
            "is_spread": page_data.get('is_spread', False),
            "is_cover": is_cover,
            "image": f"images/pages/page-{page_num:03d}.webp",
            "thumbnail": f"images/thumbnails/page-{page_num:03d}.webp",
            "characters": get_unique_characters(page_data),
            "locations": get_locations(page_data)
        })

    # Sort by page number
    pages.sort(key=lambda p: p['page'])

    return pages


def copy_database_files():
    """Copy character and location databases to site/data."""
    OUTPUT_DATA_DIR.mkdir(parents=True, exist_ok=True)

    files_copied = []

    if CHARACTERS_SOURCE.exists():
        shutil.copy(CHARACTERS_SOURCE, OUTPUT_DATA_DIR / "characters.json")
        files_copied.append("characters.json")
        print(f"✓ Copied {CHARACTERS_SOURCE} → {OUTPUT_DATA_DIR / 'characters.json'}")
    else:
        print(f"⚠ Warning: {CHARACTERS_SOURCE} not found")

    if LOCATIONS_SOURCE.exists():
        shutil.copy(LOCATIONS_SOURCE, OUTPUT_DATA_DIR / "locations.json")
        files_copied.append("locations.json")
        print(f"✓ Copied {LOCATIONS_SOURCE} → {OUTPUT_DATA_DIR / 'locations.json'}")
    else:
        print(f"⚠ Warning: {LOCATIONS_SOURCE} not found")

    return files_copied


def main():
    """Main data generation process."""
    print("Generating site metadata...\n")

    # Generate pages metadata
    pages_data = generate_pages_metadata()

    # Create output directory
    OUTPUT_DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Write pages.json
    output_file = OUTPUT_DATA_DIR / "pages.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(pages_data, f, indent=2)

    print(f"✓ Generated {output_file}")
    print(f"  Pages: {len(pages_data)}")

    # Calculate statistics
    total_panels = sum(p['panel_count'] for p in pages_data)
    unique_characters = set()
    unique_locations = set()

    for page in pages_data:
        unique_characters.update(page['characters'])
        unique_locations.update(page['locations'])

    print(f"  Total panels: {total_panels}")
    print(f"  Unique characters: {len(unique_characters)}")
    print(f"  Unique locations: {len(unique_locations)}")

    # Show page range
    if pages_data:
        first_page = pages_data[0]['page']
        last_page = pages_data[-1]['page']
        print(f"  Page range: {first_page} to {last_page}")

    print()

    # Copy database files
    copied = copy_database_files()

    print(f"\n✓ Site data generation complete!")
    print(f"  Output directory: {OUTPUT_DATA_DIR}")
    print(f"  Files created: pages.json, {', '.join(copied)}")


if __name__ == "__main__":
    main()
