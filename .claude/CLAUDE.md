# Everpeak Citadel Comic Production

This file contains project context and instructions for Claude Code when working on the Everpeak comic book project.

## Project Overview

**Everpeak Citadel: Echoes of the Dawn's Crown** is a 40-page D&D-inspired comic book being produced using AI-assisted artwork generation with human-in-the-loop review.

- **Format**: CBZ (Comic Book ZIP archive)
- **Distribution**: GitHub repository with CBZ downloads and web preview
- **Production Method**: AI-generated panels with human selection and assembly

## Your Role

You are the **main orchestrator** of the comic production workflow. You handle everything EXCEPT parallel image generation (which is delegated to comic-artist sub-agents).

## Core Responsibilities

### 1. Script Parsing & Planning
- Parse `Comic Book Script - Everpeak.md`
- Extract panel descriptions, dialogue, and visual elements
- Determine appropriate aspect ratios for each panel
- Generate panel-manifest.json with specifications

### 2. Generation Orchestration
- Launch multiple comic-artist sub-agents in parallel
- Each sub-agent generates 3-5 variations of one panel
- Track progress across all parallel generations
- Consolidate results

### 3. Review Interface Generation
- Create review.html from generated panel variations
- Generate selection interface for human review
- Handle user selections from selections.json

### 4. Page Assembly
- Read selected panel variations
- Use image manipulation tools to assemble panels into pages
- Apply borders, gutters, and proper spacing
- Output final page images

### 5. Build Management
- Run CBZ build scripts
- Generate ComicInfo.xml metadata
- Create preview images for GitHub Pages

## Folder Structure

```
everpeak-comic/
├── source/
│   ├── characters/           # Character reference art
│   ├── panels/              # Panel variations (generated)
│   │   └── chapter-XX/
│   │       └── page-XXX/
│   │           └── panel-XX/
│   │               ├── variation-1.png
│   │               ├── variation-2.png
│   │               ├── variation-3.png
│   │               └── metadata.json
│   ├── selected/            # Selected panel versions
│   │   └── selections.json
│   └── pages/               # Assembled full pages
│       └── chapter-XX/
│           └── page-XXX.png
├── releases/                # Final CBZ files
├── review/                  # Review interface
│   └── review.html
└── scripts/                 # Build automation
```

## Panel Specifications

Standard aspect ratios and dimensions:

| Type | Aspect Ratio | Size (px) | Use Case |
|------|--------------|-----------|----------|
| Standard | 3:4 | 768x1024 | Regular panel |
| Wide | 16:9 | 1536x864 | Establishing shots |
| Tall | 9:16 | 864x1536 | Vertical emphasis |
| Square | 1:1 | 1024x1024 | Close-ups |
| Splash | 3:4 | 1536x2048 | Full page |

## Sub-Agent Usage

### comic-artist Sub-Agent

**When to use**: Generating panel variations

**How to use**:
1. Launch multiple instances in parallel (one per panel)
2. Each instance generates 3-5 variations
3. Specify output directory, aspect ratio, and prompt

**Example invocation**:
```
Launch 5 comic-artist sub-agents in parallel to generate Chapter 1, Page 1:

Panel 1 (ch01-pg01-p01):
- Prompt: "Professional comic book panel: Wide establishing shot of Val..."
- Size: 1536x864 (16:9)
- Variations: 3
- Output: source/panels/chapter-01/page-001/panel-01/

Panel 2 (ch01-pg01-p02):
- Prompt: "Professional comic book panel: Prismor on balcony..."
- Size: 864x1536 (9:16)
- Variations: 3
- Output: source/panels/chapter-01/page-001/panel-02/

[etc for remaining panels]
```

**What sub-agents DO**: Generate images only
**What sub-agents DON'T DO**: Assembly, selection, layout, building

## Production Workflow

### Phase 1: Script to Panel Specs

Read the comic script and extract panel information:

```javascript
// Parse script to extract:
{
  "chapter": 1,
  "page": 1,
  "panels": [
    {
      "id": "ch01-pg01-p01",
      "description": "Val walking through crowds...",
      "dialogue": "The Dawn's Crown alignment approaches...",
      "aspectRatio": "16:9",
      "size": "1536x864",
      "characters": ["Val"],
      "setting": "Festival marketplace"
    }
  ]
}
```

### Phase 2: Parallel Generation

Launch comic-artist sub-agents in parallel:
- One sub-agent per panel
- Each generates 3-5 variations
- All run simultaneously for speed

### Phase 3: Review Interface

Generate `review/review.html`:
- Display all panel variations in a grid
- Allow selection of best version
- Save selections to `source/selected/selections.json`

### Phase 4: Human Review

**PAUSE HERE** - Wait for human to:
1. Open review.html in browser
2. Review all panel variations
3. Select best version of each panel
4. Save selections

User will tell you when selections are complete.

### Phase 5: Page Assembly

After selections are saved:
1. Read `source/selected/selections.json`
2. Copy selected panels to `source/selected/chapter-XX/page-XXX/`
3. Use image manipulation to assemble panels:
   - Standard page size: 1536x2048 (3:4 ratio)
   - Add 3px black borders around panels
   - Add 12px white gutters between panels
   - Composite according to layout

Example using Python + Pillow:
```python
from PIL import Image, ImageDraw

def assemble_page(page_num, selections):
    page = Image.new('RGB', (1536, 2048), 'white')

    # Load selected panels
    # Apply layout
    # Add borders and gutters
    # Composite

    page.save(f'source/pages/chapter-01/page-{page_num:03d}.png')
```

### Phase 6: CBZ Build

Run build script:
```bash
./scripts/create-cbz.sh 1  # Chapter number
```

This will:
1. Collect pages from `source/pages/chapter-01/`
2. Rename to sequential numbers (001.png, 002.png, etc.)
3. Create ComicInfo.xml
4. Package into CBZ

## Character Descriptions

Keep these handy for consistent prompts:

### Val (Valthirion Emberstride)
Brass dragonborn monk, just under 7 feet tall, lean athletic build, warm brass/copper-bronze scales with metallic sheen, ember-glow orange eyes, kind open expression, short snout, simple monastery robes in browns and tans with chalk dust, bare clawed feet, prayer beads on wrist, expressive hand gestures

### Prismor
Blue crystal dragonborn paladin, 7 feet tall, muscular powerful build, crystalline blue scales with green hints gem-like quality, deep sapphire blue eyes, noble bearing, plate armor with crystalline accents, Oath of the Ancients symbols (leaves vines), greatsword, forest green cape, perfect military posture

### Apocalypse Winter (Pocky)
Human wizard, early 20s, 5'10", strong but scholarly build, dark unkempt hair, keen blue eyes, pale skin, determined jawline, practical wizard robes in deep blue with silver trim, leather satchel with scrolls, component pouch, quarterstaff, ink-stained fingers, reading glasses

### Lunara
High elf druid, appears in her 20s, 5'8", graceful lithe build, long flowing chestnut brown hair with woven flowers, vibrant green eyes, fair skin with slight tan, pointed ears, serene expression, practical druid robes in earthy greens and browns, living vines and flowers in clothing, wooden staff with natural patterns, leaf-shaped pendant

### Malrik
Drow rogue, young adult, 5'6", slim agile build, dark gray-blue drow skin, short white hair, pale lavender eyes, sharp cheekbones, mischievous warm smile, dark leather armor with colorful vest underneath, playing cards, mysterious pendant, quick fluid movements

## Prompt Engineering for Panels

Always structure panel prompts as:

```
Professional comic book panel illustration: [Description]

Characters: [Full character descriptions]
Setting: [Environment details]
Action: [What's happening]
Mood: [Emotional tone]
Camera: [Angle/framing]

Style: Bold ink line art, vibrant colors, dynamic composition, sequential art style, graphic novel quality, white background
```

## Best Practices

1. **Parallel Processing**: Always launch multiple sub-agents in parallel for efficiency
2. **Panel Numbering**: Use consistent zero-padded IDs (ch01-pg01-p01)
3. **Directory Structure**: Always create directories before generating
4. **Error Handling**: Check for failed generations and report clearly
5. **Selections**: Never proceed with assembly without selections.json
6. **Consistency**: Use character reference images when available

## Common Commands

### Generate Character References
```bash
# Generate variations of a character for reference
```

### Generate Page Panels
```bash
# Launch parallel sub-agents for all panels on a page
```

### Create Review Interface
```bash
# Generate review.html from panel variations
```

### Assemble Page
```bash
# After selections, assemble panels into final page
```

### Build CBZ
```bash
./scripts/create-cbz.sh [chapter-number]
```

## File Locations

- **Script**: `Comic Book Script - Everpeak.md`
- **Sub-agent**: `.claude/agents/comic-artist.md`
- **Plan**: `PLAN.md`
- **Character refs**: `source/characters/`
- **Generated panels**: `source/panels/`
- **Selections**: `source/selected/selections.json`
- **Final pages**: `source/pages/`
- **CBZ output**: `releases/`

## User Workflow

When user says "Generate Chapter 1, Page 1":
1. Parse script for Page 1 panels
2. Launch parallel sub-agents
3. Generate review.html
4. Tell user: "Review interface ready at review/review.html - please select your preferred variations"
5. **WAIT** for user to complete review
6. User says "selections complete"
7. Read selections.json
8. Assemble page
9. Show preview of assembled page

## Important Notes

- **Never skip the review phase** - Human selection is critical
- **Sub-agents run in parallel** - Don't wait for one to finish before starting another
- **Maintain consistency** - Use the same character descriptions across all panels
- **Track progress** - Use TodoWrite to track multi-step processes
- **Report clearly** - Show what was generated, where it's saved, and next steps

## Success Metrics

- Panels generated with correct aspect ratios
- All variations saved to proper directories
- Review interface displays correctly
- Selections persist accurately
- Assembled pages have proper borders and spacing
- CBZ files open correctly in comic readers
- Visual consistency maintained across panels

See `PLAN.md` for the complete implementation plan and detailed specifications.
