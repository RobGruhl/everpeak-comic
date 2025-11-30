#!/usr/bin/env python3
"""
Analyze all page layouts and show detected patterns.
Helpful for understanding what layout will be used for each page.
"""

import json
from pathlib import Path
from layout_engine import detect_layout_pattern

PAGES_JSON_DIR = Path("pages")


def analyze_page(page_file):
    """Analyze a single page and return layout info."""
    with open(page_file, 'r', encoding='utf-8') as f:
        page_data = json.load(f)

    page_num = page_data['page_num']
    panels = page_data['panels']
    is_spread = page_data.get('is_spread', False)
    custom_layout = page_data.get('custom_layout', None)

    # Get aspect ratios
    aspects = [p.get('aspect_ratio', 'square') for p in panels]

    # Detect pattern
    pattern = custom_layout if custom_layout else detect_layout_pattern(panels)

    return {
        'page_num': page_num,
        'panel_count': len(panels),
        'is_spread': is_spread,
        'aspects': aspects,
        'pattern': pattern,
        'custom': custom_layout is not None
    }


def main():
    """Analyze all pages and display layout pattern summary."""

    print("=" * 80)
    print("COMIC BOOK LAYOUT ANALYSIS")
    print("=" * 80)
    print()

    # Find all page files
    page_files = sorted(PAGES_JSON_DIR.glob("page-*.json"))

    # Analyze each page
    results = []
    for page_file in page_files:
        try:
            result = analyze_page(page_file)
            results.append(result)
        except Exception as e:
            print(f"Error analyzing {page_file.name}: {e}")

    # Group by pattern
    patterns = {}
    for result in results:
        pattern = result['pattern']
        if pattern not in patterns:
            patterns[pattern] = []
        patterns[pattern].append(result)

    # Display summary
    print(f"Total Pages: {len(results)}")
    print(f"Pattern Distribution:")
    print()

    for pattern, pages in sorted(patterns.items()):
        count = len(pages)
        pct = count / len(results) * 100
        print(f"  {pattern:15s} : {count:2d} pages ({pct:5.1f}%)")

    print()
    print("=" * 80)
    print("DETAILED BREAKDOWN")
    print("=" * 80)
    print()

    for pattern, pages in sorted(patterns.items()):
        print(f"\n{pattern.upper()} ({len(pages)} pages)")
        print("-" * 80)

        for page in sorted(pages, key=lambda p: p['page_num']):
            spread_marker = " [SPREAD]" if page['is_spread'] else ""
            custom_marker = " [CUSTOM]" if page['custom'] else ""
            aspect_summary = ", ".join(page['aspects'])

            print(f"  Page {page['page_num']:2d}: {page['panel_count']} panels - "
                  f"{aspect_summary}{spread_marker}{custom_marker}")

    print()
    print("=" * 80)
    print("RECOMMENDATIONS")
    print("=" * 80)
    print()

    # Find pages that might need custom layouts
    mixed_pages = [p for p in results if p['pattern'] == 'mixed']

    if mixed_pages:
        print("Pages with MIXED patterns may benefit from custom layouts:")
        for page in mixed_pages:
            aspect_summary = ", ".join(page['aspects'])
            print(f"  Page {page['page_num']:2d}: {aspect_summary}")
            print(f"    Consider adding 'custom_layout' field to page-{page['page_num']:03d}.json")
        print()
    else:
        print("✓ All pages have recognized patterns!")
        print()

    # Check for unusual spread pages
    spread_pages = [p for p in results if p['is_spread']]
    print(f"Spread Pages: {len(spread_pages)} pages")
    for page in spread_pages:
        print(f"  Page {page['page_num']:2d}: {page['panel_count']} panels - {page['pattern']}")

    print()


if __name__ == "__main__":
    main()
