#!/bin/bash

echo "=========================================="
echo "Everpeak Comic Project Cleanup"
echo "=========================================="
echo ""

# Safety check
read -p "This will reorganize and delete files. Continue? (yes/no) " -n 3 -r
echo
if [[ ! $REPLY =~ ^yes$ ]]
then
    echo "Cleanup cancelled."
    exit 1
fi

echo "Starting cleanup..."
echo ""

# Create new directories
echo "→ Creating new directory structure..."
mkdir -p scripts/core
mkdir -p scripts/utilities
mkdir -p docs/archive
mkdir -p archive

# Move core scripts
echo "→ Moving core scripts to scripts/core/..."
mv generate.py scripts/core/ 2>/dev/null
mv parse_script.py scripts/core/ 2>/dev/null
mv assemble.py scripts/core/ 2>/dev/null
mv review.py scripts/core/ 2>/dev/null

# Move utility scripts
echo "→ Moving utility scripts to scripts/utilities/..."
mv build_databases.py scripts/utilities/ 2>/dev/null
mv convert_pages.py scripts/utilities/ 2>/dev/null
mv generate_reference.py scripts/utilities/ 2>/dev/null
mv layout_engine.py scripts/utilities/ 2>/dev/null
mv analyze_layouts.py scripts/utilities/ 2>/dev/null
mv sequential_pack.py scripts/utilities/ 2>/dev/null
mv create_cbz_from_panels.py scripts/utilities/ 2>/dev/null

# Move docs to archive
echo "→ Archiving old documentation..."
mv ENHANCED_PROMPT_STRATEGY.md docs/archive/ 2>/dev/null
mv LAYOUT_GUIDE.md docs/archive/ 2>/dev/null
mv SIMPLE_LAYOUT.md docs/archive/ 2>/dev/null
mv everpeak-transcript.md docs/archive/ 2>/dev/null
mv plan.md docs/archive/ 2>/dev/null

# Move main docs to docs/
echo "→ Organizing documentation..."
mv "Comic Book Script - Everpeak.md" docs/ 2>/dev/null
mv everpeak-complete-module.md docs/ 2>/dev/null
mv DYNAMIC_DESCRIPTIONS.md docs/ 2>/dev/null
# README.md and LICENSE stay in root

# Move page backups to archive
echo "→ Archiving page backups..."
mv pages_backup archive/ 2>/dev/null
mv pages_backup_sequential archive/ 2>/dev/null

# Delete old output directories
echo "→ Deleting obsolete output directories..."
rm -rf output/nanobananapro_panels
rm -rf output/nanobananapro
rm -rf output/images

# Delete old CBZ and test files
echo "→ Deleting old CBZ and test files..."
rm -f output/everpeak-citadel.cbz
rm -f output/test_nanobananapro.png
rm -f output/quota_test.png
rm -f output/selections.json

# Delete one-off fix scripts
echo "→ Deleting one-off fix scripts..."
rm -f fix_orrery_battle_pages.py
rm -f fix_split_party_pages.py
rm -f fix_tunnels_script.py
rm -f comprehensive_json_fixer.py
rm -f restructure_pages.py
rm -f generate_nanobananapro.py
rm -f test_google_quota.py
rm -f check_all_pages.py
rm -f check_panels.py

# Delete log files
echo "→ Deleting log files..."
rm -f *.log
rm -f generation_log.txt

echo ""
echo "=========================================="
echo "✓ Cleanup complete!"
echo "=========================================="
echo ""
echo "New directory structure:"
tree -L 2 -d --dirsfirst . 2>/dev/null || find . -maxdepth 2 -type d | sort
echo ""
echo "Space usage:"
du -sh output/ archive/ 2>/dev/null
echo ""
echo "Next steps:"
echo "1. Verify project still works: python scripts/core/generate.py 1"
echo "2. Review changes with: git status"
echo "3. Commit cleanup: git add -A && git commit -m 'Clean up project structure'"
