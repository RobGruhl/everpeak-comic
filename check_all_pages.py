#!/usr/bin/env python3
"""
Comprehensive checker for all page JSON files to identify:
- Missing location context
- Modern terms that should be fantasy
- Missing character descriptions
- Inconsistent fantasy setting
"""

import json
from pathlib import Path

# Modern terms to flag
MODERN_TERMS = [
    'coffee', 'laptop', 'phone', 'computer', 'modern',
    'electricity', 'electronic', 'digital', 'internet',
    'car', 'truck', 'bicycle', 'motorcycle',
    'plastic', 'rubber', 'synthetic',
    'contemporary', 'today', 'current'
]

# Check for minimal location descriptions (too generic)
MINIMAL_SCENE_PATTERNS = [
    'Scene: Party',
    'Scene: Mal',
    'Scene: Val',
    'Scene: Pri',
    'Scene: Lun',
    'Scene: Poc',
    '\nScene: \n',
    'Location:\n\nCharacters',  # Missing location entirely
]

def check_page(page_num):
    """Check a single page for issues."""
    page_file = Path(f"pages/page-{page_num:03d}.json")
    if not page_file.exists():
        return None

    with open(page_file, 'r') as f:
        page = json.load(f)

    issues = []

    for panel in page.get('panels', []):
        panel_num = panel.get('panel_num')
        prompt = panel.get('prompt', '')
        visual = panel.get('visual', '')

        # Check for modern terms
        for term in MODERN_TERMS:
            if term.lower() in prompt.lower() or term.lower() in visual.lower():
                issues.append(f"  Panel {panel_num}: Contains modern term '{term}'")

        # Check for missing location
        if 'Location:' not in prompt and 'professional comic book panel' in prompt.lower():
            issues.append(f"  Panel {panel_num}: Missing Location description")

        # Check for minimal scene descriptions
        for pattern in MINIMAL_SCENE_PATTERNS:
            if pattern in prompt:
                issues.append(f"  Panel {panel_num}: Minimal/generic scene description")
                break

        # Check if fantasy style directive is present
        if 'medieval fantasy' not in prompt.lower() and 'fantasy' not in prompt.lower():
            issues.append(f"  Panel {panel_num}: Missing fantasy style directive")

    return issues

def main():
    """Check all pages 15-45."""
    print("="*70)
    print("CHECKING PAGES 15-45 FOR CONSISTENCY ISSUES")
    print("="*70)
    print()

    pages_with_issues = []
    total_issues = 0

    for page_num in range(15, 46):
        issues = check_page(page_num)
        if issues is None:
            continue

        if issues:
            pages_with_issues.append(page_num)
            print(f"Page {page_num}: {len(issues)} issue(s)")
            for issue in issues:
                print(issue)
                total_issues += 1
            print()

    print("="*70)
    print(f"SUMMARY: {len(pages_with_issues)} pages with issues, {total_issues} total issues")

    if pages_with_issues:
        print(f"Pages needing fixes: {', '.join(map(str, pages_with_issues))}")
    else:
        print("✓ All pages 15-45 look good!")
    print("="*70)

if __name__ == "__main__":
    main()
