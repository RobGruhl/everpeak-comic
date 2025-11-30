# Everpeak Comic Project Cleanup Plan

## Summary
**Current Status:** 620+ MB of output data, 20 Python scripts, 9 markdown docs
**Goal:** Organize into clean directory structure, archive old work, keep only active files

---

## 1. OUTPUT DIRECTORY CLEANUP (620+ MB → ~50 MB)

### ✅ KEEP - Active/Current
```
output/
├── panels/           437 MB - CURRENT panels with variants (page-XXX-panel-X-vN.png)
├── pages/             45 MB - Assembled pages
├── references/       3.3 MB - Character references (Prismor)
└── everpeak-nanobananapro.cbz  352 MB - LATEST complete CBZ
```

### 🗑️ DELETE - Old/Obsolete (545 MB freed)
```
output/
├── nanobananapro_panels/   183 MB - OLD panels (superseded by output/panels/)
├── nanobananapro/          8.5 MB - OLD assembled pages
├── everpeak-citadel.cbz    6.3 MB - OLD CBZ (superseded by nanobananapro)
├── test_nanobananapro.png  216 KB - Test image
├── quota_test.png          996 KB - Test image
├── selections.json         4 KB   - Old selection data
└── images/                 empty  - Empty directory
```

---

## 2. PYTHON SCRIPTS ORGANIZATION

### ✅ KEEP - Core Active Scripts (move to scripts/)
```
scripts/
├── generate.py              # Main generator
├── parse_script.py          # Script parser
├── review.py                # Review tool
├── assemble.py              # Page assembler
├── build_databases.py       # DB builder
├── convert_pages.py         # Page converter
└── generate_reference.py    # Reference generator
```

### 🗑️ DELETE - One-off/Obsolete Scripts
```
fix_orrery_battle_pages.py     # One-off fix (already done)
fix_split_party_pages.py       # One-off fix (already done)
fix_tunnels_script.py          # One-off fix (already done)
comprehensive_json_fixer.py    # One-off fix (already done)
restructure_pages.py           # One-off migration (already done)
generate_nanobananapro.py      # Old generator (superseded)
test_google_quota.py           # Test script
check_all_pages.py             # Utility (can recreate if needed)
check_panels.py                # Utility (can recreate if needed)
```

### 🔄 KEEP - Utility Scripts (move to scripts/)
```
scripts/
├── layout_engine.py           # Layout utilities
├── analyze_layouts.py         # Analysis tool
├── sequential_pack.py         # CBZ packer
└── create_cbz_from_panels.py  # CBZ creator
```

---

## 3. MARKDOWN DOCUMENTATION

### ✅ KEEP - Active Documentation
```
docs/
├── Comic Book Script - Everpeak.md    # Source script
├── everpeak-complete-module.md        # Complete D&D module
├── DYNAMIC_DESCRIPTIONS.md            # System design
├── README.md                          # Project readme
└── CLAUDE.md (in .claude/)            # Project instructions
```

### 🔄 ARCHIVE - Reference Documentation (move to docs/archive/)
```
docs/archive/
├── ENHANCED_PROMPT_STRATEGY.md    # Old strategy (superseded by DYNAMIC)
├── LAYOUT_GUIDE.md                # Old layout guide
├── SIMPLE_LAYOUT.md               # Simplified guide
├── everpeak-transcript.md         # Review transcript
└── plan.md                        # Old planning doc
```

---

## 4. BACKUP DIRECTORIES

### 🔄 ARCHIVE - Old Page Backups (move to archive/)
```
archive/
├── pages_backup/                  804 KB - Backup before conversion
└── pages_backup_sequential/       388 KB - Sequential backup
```

---

## 5. LOG FILES

### 🗑️ DELETE - Old Logs
```
generation_pages_20-39_v2.log
generation_pages_20-39.log
generation_log.txt
```

---

## PROPOSED DIRECTORY STRUCTURE

```
everpeak-comic/
├── .claude/                    # Claude Code settings
├── .git/                       # Git repository
├── venv/                       # Python virtual environment
│
├── docs/                       # Documentation
│   ├── Comic Book Script - Everpeak.md
│   ├── everpeak-complete-module.md
│   ├── DYNAMIC_DESCRIPTIONS.md
│   ├── README.md
│   └── archive/                # Old/reference docs
│       ├── ENHANCED_PROMPT_STRATEGY.md
│       ├── LAYOUT_GUIDE.md
│       ├── SIMPLE_LAYOUT.md
│       ├── everpeak-transcript.md
│       └── plan.md
│
├── scripts/                    # Python scripts
│   ├── core/                   # Core generation
│   │   ├── generate.py
│   │   ├── parse_script.py
│   │   ├── assemble.py
│   │   └── review.py
│   └── utilities/              # Utility scripts
│       ├── build_databases.py
│       ├── convert_pages.py
│       ├── generate_reference.py
│       ├── layout_engine.py
│       ├── analyze_layouts.py
│       ├── sequential_pack.py
│       └── create_cbz_from_panels.py
│
├── pages/                      # Page JSON files (45 files)
│
├── output/                     # Generated output
│   ├── panels/                 # All panel variants
│   ├── pages/                  # Assembled pages
│   ├── references/             # Character references
│   └── everpeak-nanobananapro.cbz
│
├── archive/                    # Old backups
│   ├── pages_backup/
│   └── pages_backup_sequential/
│
├── characters.json             # Character database
├── locations.json              # Location database
├── style.json                  # Style database
├── requirements.txt            # Python dependencies
├── .gitignore
└── LICENSE
```

---

## CLEANUP SCRIPT

Create `cleanup.sh` to execute the plan:

```bash
#!/bin/bash

echo "Everpeak Comic Project Cleanup"
echo "=============================="

# Create new directories
mkdir -p scripts/core scripts/utilities docs/archive archive

# Move scripts
mv generate.py parse_script.py assemble.py review.py scripts/core/
mv build_databases.py convert_pages.py generate_reference.py scripts/utilities/
mv layout_engine.py analyze_layouts.py sequential_pack.py create_cbz_from_panels.py scripts/utilities/

# Move docs
mv ENHANCED_PROMPT_STRATEGY.md LAYOUT_GUIDE.md SIMPLE_LAYOUT.md everpeak-transcript.md plan.md docs/archive/

# Move page backups
mv pages_backup pages_backup_sequential archive/

# Delete old output
rm -rf output/nanobananapro_panels output/nanobananapro output/images
rm output/everpeak-citadel.cbz output/test_nanobananapro.png output/quota_test.png output/selections.json

# Delete old scripts
rm fix_orrery_battle_pages.py fix_split_party_pages.py fix_tunnels_script.py
rm comprehensive_json_fixer.py restructure_pages.py generate_nanobananapro.py
rm test_google_quota.py check_all_pages.py check_panels.py

# Delete logs
rm *.log generation_log.txt 2>/dev/null

echo "✓ Cleanup complete!"
echo "Freed space:"
du -sh output/ pages_backup* 2>/dev/null
```

---

## SPACE SAVINGS

**Before:** ~620 MB + clutter
**After:** ~50-100 MB organized

**Space freed:** ~545 MB
- output/nanobananapro_panels: 183 MB
- output/everpeak-citadel.cbz: 6.3 MB
- output/nanobananapro: 8.5 MB
- Old CBZ and test files: ~350 MB (if we keep only latest CBZ)
- Scripts: minimal
- Logs: minimal

---

## EXECUTION PLAN

1. **REVIEW** this plan with user
2. **CREATE** backup of entire project (just in case)
3. **EXECUTE** cleanup.sh
4. **VERIFY** project still works
5. **GIT COMMIT** the reorganization

## NOTES

- Keep output/everpeak-nanobananapro.cbz (latest complete CBZ)
- All panels in output/panels/ are current and needed for review tool
- Page backups moved to archive/ (not deleted, just in case)
- All one-off fix scripts can be safely deleted (work already done)
