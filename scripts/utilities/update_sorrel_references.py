#!/usr/bin/env python3
"""Update Sorrel character references to use correct form (halfling vs dragon)."""

import json
import os

# Pages where Sorrel appears in halfling form
HALFLING_PAGES = [4, 9]

# Pages where Sorrel appears in dragon form
DRAGON_PAGES = [23, 25, 35, 38, 41, 42, 45]

def update_page(page_num, form):
    """Update a single page to use correct Sorrel form."""
    filepath = f'pages/page-{page_num:03d}.json'

    if not os.path.exists(filepath):
        print(f"⚠️  {filepath} not found, skipping")
        return

    with open(filepath, 'r') as f:
        data = json.load(f)

    modified = False
    for panel in data.get('panels', []):
        chars = panel.get('characters', [])
        npcs = panel.get('npcs', [])

        # Update characters list
        if 'Sorrel' in chars:
            chars[chars.index('Sorrel')] = form
            modified = True

        # Update NPCs list (for halfling form)
        if 'Sorrel' in npcs:
            if form == 'Sorrel (halfling disguise)':
                npcs[npcs.index('Sorrel')] = form
                modified = True
            else:
                # Move from NPCs to characters if dragon form
                npcs.remove('Sorrel')
                if form not in chars:
                    chars.append(form)
                modified = True

    if modified:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"✓ Updated {filepath} → {form}")
    else:
        print(f"  {filepath} → no changes needed")

def main():
    """Update all Sorrel references."""
    print("Updating Sorrel character references...\n")

    print("Halfling form (early pages):")
    for page_num in HALFLING_PAGES:
        update_page(page_num, 'Sorrel (halfling disguise)')

    print("\nDragon form (after transformation):")
    for page_num in DRAGON_PAGES:
        update_page(page_num, 'Sorrel - Dragon Form')

    print("\n✓ All Sorrel references updated")

if __name__ == '__main__':
    main()
