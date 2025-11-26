#!/usr/bin/env python3
"""Check panel counts for all pages."""

from pathlib import Path
import json

panel_dir = Path("output/nanobananapro_panels")
pages_dir = Path("pages")

print("=" * 70)
print("PANEL COUNT CHECK")
print("=" * 70)
print()

missing = []
incomplete = []
complete = []

for page_num in range(1, 46):
    # Check expected panel count from JSON
    page_file = pages_dir / f"page-{page_num:03d}.json"
    if not page_file.exists():
        continue

    with open(page_file) as f:
        page_data = json.load(f)
    expected = page_data.get('panel_count', 4)

    # Count actual panels
    panels = list(panel_dir.glob(f"page-{page_num:03d}-panel-*.png"))
    actual = len(panels)

    if actual == 0:
        missing.append((page_num, expected))
        print(f"❌ Page {page_num}: 0/{expected} panels (MISSING)")
    elif actual < expected:
        incomplete.append((page_num, actual, expected))
        print(f"⚠️  Page {page_num}: {actual}/{expected} panels (INCOMPLETE)")
    else:
        complete.append((page_num, actual))

print()
print("=" * 70)
print(f"✓ Complete: {len(complete)} pages")
print(f"⚠️  Incomplete: {len(incomplete)} pages")
print(f"❌ Missing: {len(missing)} pages")
print(f"Total panels: {sum(c[1] for c in complete) + sum(i[1] for i in incomplete)}/171")
print("=" * 70)

if incomplete:
    print()
    print("INCOMPLETE PAGES:")
    for page_num, actual, expected in incomplete:
        print(f"  Page {page_num}: {actual}/{expected} panels")

if missing:
    print()
    print("MISSING PAGES:")
    for page_num, expected in missing:
        print(f"  Page {page_num}: needs {expected} panels")
