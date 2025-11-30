#!/usr/bin/env python3
"""
Convert all page JSON files from embedded descriptions to reference-based format.

OLD FORMAT:
{
  "characters": {
    "Prismor": "Full description here..."
  },
  "prompt": "Complete pre-built prompt..."
}

NEW FORMAT:
{
  "characters": ["Prismor"],
  "location": "The Elven Sanctum"
  // No prompt field - will be assembled dynamically
}
"""

import json
from pathlib import Path
import shutil
from datetime import datetime

PAGES_DIR = Path("pages")
BACKUP_DIR = Path("pages_backup")

def backup_pages():
    """Create backup of all page files before conversion."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUP_DIR / timestamp
    backup_path.mkdir(parents=True, exist_ok=True)

    page_files = list(PAGES_DIR.glob("page-*.json"))
    for page_file in page_files:
        shutil.copy2(page_file, backup_path / page_file.name)

    print(f"✓ Backed up {len(page_files)} page files to {backup_path}")
    return backup_path


def detect_location_from_prompt(prompt):
    """
    Extract location name from prompt text.
    Returns location name or None.
    """
    if not prompt or 'Location:' not in prompt:
        return None

    # Extract the location line
    location_section = prompt.split('Location:')[1].split('\n')[0].strip()

    # Match against known locations
    known_locations = [
        "The Elven Sanctum",
        "Festival Marketplace",
        "The Grand Library",
        "Barth's Forge",
        "Balcony Garden Café",
        "Courier Tunnels",
        "Grand Courtyard",
        "Sled Race Course",
        "The Observatory",
        "Mountain Path",
        "Everpeak Citadel Exterior"
    ]

    for known_loc in known_locations:
        if known_loc.lower() in location_section.lower():
            return known_loc

    # Return the extracted text if no match (will need manual cleanup)
    return location_section if location_section else None


def convert_panel(panel):
    """Convert a single panel from old to new format."""
    new_panel = {
        "panel_num": panel["panel_num"],
        "visual": panel["visual"],
        "dialogue": panel.get("dialogue", ""),
        "aspect_ratio": panel["aspect_ratio"],
        "size": panel["size"]
    }

    # Convert characters dict to list of names
    characters = panel.get("characters", {})
    new_panel["characters"] = [name for name in characters.keys() if characters[name]]

    # Convert NPCs dict to list of names
    npcs = panel.get("npcs", {})
    new_panel["npcs"] = [name for name in npcs.keys() if npcs[name]]

    # Convert creatures dict to list of names (store as npcs for now)
    creatures = panel.get("creatures", {})
    creature_names = [name for name in creatures.keys() if creatures[name]]
    if creature_names:
        # Add to NPCs list (we can separate later if needed)
        new_panel["npcs"].extend(creature_names)

    # Detect location from prompt
    prompt = panel.get("prompt", "")
    location = detect_location_from_prompt(prompt)
    if location:
        new_panel["location"] = location

    # Remove old prompt field - will be generated dynamically
    # (Don't include it in new format)

    return new_panel


def convert_page_file(page_path):
    """Convert a single page file to new format."""
    with open(page_path, 'r') as f:
        page_data = json.load(f)

    # Convert all panels
    new_panels = []
    for panel in page_data.get("panels", []):
        new_panels.append(convert_panel(panel))

    # Build new page structure
    new_page = {
        "page_num": page_data["page_num"],
        "title": page_data.get("title", ""),
        "panel_count": page_data["panel_count"],
        "is_spread": page_data.get("is_spread", False),
        "panels": new_panels
    }

    # Write back to file
    with open(page_path, 'w') as f:
        json.dump(new_page, f, indent=2)

    return len(new_panels)


def main():
    print("=" * 60)
    print("CONVERTING PAGE FILES TO REFERENCE-BASED FORMAT")
    print("=" * 60)

    # Backup existing pages
    backup_path = backup_pages()

    # Convert all pages
    page_files = sorted(PAGES_DIR.glob("page-*.json"))
    total_panels = 0

    print(f"\nConverting {len(page_files)} page files...")
    for page_file in page_files:
        panel_count = convert_page_file(page_file)
        total_panels += panel_count
        print(f"  ✓ {page_file.name}: {panel_count} panels")

    print("\n" + "=" * 60)
    print("CONVERSION COMPLETE")
    print("=" * 60)
    print(f"\n✓ Converted {len(page_files)} pages ({total_panels} panels)")
    print(f"✓ Backup saved to: {backup_path}")
    print("\nNext steps:")
    print("1. Review converted page files")
    print("2. Update generate.py with dynamic prompt assembly")
    print("3. Test generation with page 1")


if __name__ == "__main__":
    main()
