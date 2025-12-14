#!/usr/bin/env python3
"""Check all page JSONs for panels missing character/NPC references."""

import json
from pathlib import Path
import re

PAGES_DIR = Path("pages")

# Character name patterns to detect in visual/dialogue
CHARACTER_PATTERNS = {
    'Val': r'\bVal\b',
    'Prismor': r'\bPrismor\b',
    'Apocalypse Winter': r'\b(Apocalypse Winter|Pocky)\b',
    'Lunara': r'\bLunara\b',
    'Malrik': r'\bMalrik\b',
    'Marge': r'\bMarge\b',
    'Alric': r'\b(Alric|Lord Alric)\b',
    'Sorrel': r'\bSorrel\b',
    'Sorrel - Dragon Form': r'\b(Sorrel.*dragon|dragon.*Sorrel|dragon form)\b',
    'Sorrel (halfling disguise)': r'\b(Sorrel.*halfling|halfling.*Sorrel)\b',
    'Marivielle': r'\bMarivielle\b',
    'Barth': r'\bBarth\b',
    'Captain Thorne': r'\bThorne\b',
    'Elara': r'\bElara\b',
}

# NPCs (not main party)
NPC_NAMES = {
    'Marge', 'Alric', 'Sorrel', 'Sorrel - Dragon Form', 'Sorrel (halfling disguise)',
    'Marivielle', 'Barth', 'Captain Thorne', 'Elara'
}

def detect_characters(text):
    """Detect character names in text."""
    found = []
    text_lower = text.lower()

    for char_name, pattern in CHARACTER_PATTERNS.items():
        if re.search(pattern, text, re.IGNORECASE):
            found.append(char_name)

    return found

def check_page(page_num):
    """Check a single page for missing character data."""
    if page_num == 0:
        page_file = PAGES_DIR / "page-000.json"
        if not page_file.exists():
            page_file = PAGES_DIR / "cover.json"
    else:
        page_file = PAGES_DIR / f"page-{page_num:03d}.json"

    if not page_file.exists():
        return None

    with open(page_file, 'r') as f:
        data = json.load(f)

    issues = []

    for panel in data['panels']:
        panel_num = panel['panel_num']
        visual = panel.get('visual', '')
        dialogue = panel.get('dialogue', '')
        characters = panel.get('characters', [])
        npcs = panel.get('npcs', [])

        # Detect mentioned characters
        combined_text = visual + ' ' + dialogue
        detected = detect_characters(combined_text)

        # Check if panel has empty characters AND npcs but mentions characters
        if not characters and not npcs and detected:
            issues.append({
                'panel': panel_num,
                'detected': detected,
                'visual': visual[:80] + '...' if len(visual) > 80 else visual,
                'dialogue': dialogue[:80] + '...' if len(dialogue) > 80 else dialogue
            })

    return issues

def main():
    """Check all pages."""
    print("=" * 80)
    print("CHECKING ALL PAGES FOR MISSING CHARACTER DATA")
    print("=" * 80)

    total_issues = 0
    problem_pages = []

    # Check pages 0-45
    for page_num in range(0, 46):
        issues = check_page(page_num)
        if issues is None:
            continue

        if issues:
            problem_pages.append((page_num, issues))
            total_issues += len(issues)

    # Report
    print(f"\nFound {total_issues} panels with missing character data across {len(problem_pages)} pages\n")

    for page_num, issues in problem_pages:
        print(f"Page {page_num}: {len(issues)} panel(s) missing data")
        for issue in issues:
            print(f"  Panel {issue['panel']}:")
            print(f"    Detected: {', '.join(issue['detected'])}")
            print(f"    Visual: {issue['visual']}")
            if issue['dialogue']:
                print(f"    Dialogue: {issue['dialogue']}")
            print()

    # Summary by page range
    range_0_20 = sum(len(issues) for p, issues in problem_pages if 0 <= p <= 20)
    range_21_45 = sum(len(issues) for p, issues in problem_pages if 21 <= p <= 45)

    print("=" * 80)
    print(f"Pages 0-20: {range_0_20} panels missing data")
    print(f"Pages 21-45: {range_21_45} panels missing data")
    print("=" * 80)

if __name__ == '__main__':
    main()
