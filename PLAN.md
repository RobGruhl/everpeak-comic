# Everpeak Comic Production Plan

## Overview

This document outlines the complete workflow for producing the Everpeak Citadel comic book, from script to final CBZ format, with a human-in-the-loop review process for AI-generated artwork.

## Core Philosophy

**AI-generated images are not deterministic enough for single-shot production.** We need:
1. Multiple variations per panel (3-5 options)
2. Human review and selection of the best version
3. Organized storage of all variations for future reference
4. Clear tracking of which variations were selected
5. Automated assembly after selection

## Visual Continuity System

**Critical requirement**: Maintain consistent character appearance, art style, and sequential flow across all panels.

See [CONTINUITY.md](CONTINUITY.md) for the complete continuity system documentation.

**Key Strategy**: Hierarchical Multi-Reference System
- **Style Masters**: Define overall art style (line work, colors, technique)
- **Character Library**: Comprehensive references (angles, expressions, poses) for each character
- **Sequential Context**: Use previous panels to maintain scene continuity
- **Enhanced Prompts**: Incorporate reference analysis into generation prompts

This system ensures Val looks like Val in every panel, maintains consistent art style, and creates natural sequential flow.

## Production Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 1: SCRIPT PARSING                                          │
│ - Extract panel descriptions from script                         │
│ - Identify panel specifications (size, layout, etc.)             │
│ - Create panel manifest JSON                                     │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 2: IMAGE GENERATION (Parallel Sub-Agents)                  │
│ - Launch multiple comic-artist sub-agents in parallel            │
│ - Each generates 3-5 variations per panel                        │
│ - Save to organized folder structure                             │
│ - Log generation metadata                                        │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 3: HUMAN REVIEW (Interactive HTML Interface)               │
│ - Generate review.html showing all variations                    │
│ - User clicks to select best version of each panel               │
│ - Selections saved to selections.json                            │
│ - Optional: Add notes/feedback for refinement                    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 4: PAGE ASSEMBLY (Main Claude)                             │
│ - Read selections.json                                           │
│ - Copy/symlink selected panels to working directory              │
│ - Assemble panels into full pages using layout specs             │
│ - Apply consistent styling (borders, gutters, etc.)              │
│ - Export final page images                                       │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 5: CBZ BUILD (Automated Script)                            │
│ - Collect finalized page images                                  │
│ - Generate ComicInfo.xml metadata                                │
│ - Package into CBZ archive                                       │
│ - Generate preview images for web                                │
└─────────────────────────────────────────────────────────────────┘
```

## Folder Structure

```
everpeak-comic/
├── source/
│   ├── characters/                    # Character reference art
│   │   ├── val/
│   │   │   ├── val-variation-1.png
│   │   │   ├── val-variation-2.png
│   │   │   └── reference.json         # Metadata about variations
│   │   ├── prismor/
│   │   ├── pocky/
│   │   ├── lunara/
│   │   └── malrik/
│   │
│   ├── panels/                        # Individual panel variations
│   │   ├── chapter-01/
│   │   │   ├── page-001/
│   │   │   │   ├── panel-01/
│   │   │   │   │   ├── variation-1.png
│   │   │   │   │   ├── variation-2.png
│   │   │   │   │   ├── variation-3.png
│   │   │   │   │   ├── variation-4.png
│   │   │   │   │   ├── variation-5.png
│   │   │   │   │   └── metadata.json   # Generation metadata
│   │   │   │   ├── panel-02/
│   │   │   │   └── ...
│   │   │   ├── page-002/
│   │   │   └── ...
│   │   ├── chapter-02/
│   │   └── ...
│   │
│   ├── selected/                      # Selected panel versions
│   │   ├── chapter-01/
│   │   │   ├── page-001/
│   │   │   │   ├── panel-01.png      # Copy or symlink
│   │   │   │   ├── panel-02.png
│   │   │   │   └── ...
│   │   │   └── ...
│   │   └── selections.json            # Which variations were chosen
│   │
│   └── pages/                         # Assembled full pages
│       ├── chapter-01/
│       │   ├── page-001.png
│       │   ├── page-002.png
│       │   └── ...
│       └── chapter-02/
│
├── releases/                          # Final CBZ files
│   ├── everpeak-citadel-complete.cbz
│   ├── everpeak-citadel-chapter-01.cbz
│   └── ...
│
├── review/                            # Review interface
│   ├── review.html                    # Main review page
│   ├── review.css
│   ├── review.js
│   └── selections.json                # User selections
│
├── scripts/                           # Build automation
│   ├── parse-script.js                # Extract panel specs from script
│   ├── generate-review.js             # Create review HTML
│   ├── assemble-pages.js              # Compose panels into pages
│   ├── create-cbz.sh                  # Package CBZ
│   └── utils/
│
├── docs/                              # GitHub Pages
│   ├── index.html
│   ├── preview/
│   └── downloads/
│
└── Comic Book Script - Everpeak.md   # Source script
```

## Panel Specification Format

Panels should be specified in a `panel-manifest.json` that gets generated from the script:

```json
{
  "chapter": 1,
  "page": 1,
  "panels": [
    {
      "id": "ch01-pg01-p01",
      "number": 1,
      "aspectRatio": "16:9",
      "size": "large",
      "description": "Val walking through crowds, delivering messages...",
      "characters": ["Val", "background crowd"],
      "setting": "Festival marketplace",
      "dialogue": "Val (thought bubble): The Dawn's Crown alignment approaches...",
      "notes": "Wide establishing shot, lots of activity",
      "imagePrompt": "Professional comic book panel: Wide establishing shot of Val, a brass dragonborn monk, walking through crowded festival marketplace..."
    },
    {
      "id": "ch01-pg01-p02",
      "number": 2,
      "aspectRatio": "3:4",
      "size": "medium",
      "description": "Prismor on balcony overlooking preparations...",
      "characters": ["Prismor"],
      "setting": "Citadel balcony",
      "dialogue": "Prismor (thought): Decades I've protected this place...",
      "notes": "Vertical panel, emphasize height and perspective",
      "imagePrompt": "Professional comic book panel: Prismor, blue crystal dragonborn paladin..."
    }
  ]
}
```

### Panel Aspect Ratios & Sizes

Standard panel dimensions for comic pages:

| Type | Aspect Ratio | Typical Use | Dimensions (px) |
|------|--------------|-------------|-----------------|
| Standard | 3:4 | Regular panel | 768x1024 |
| Wide | 16:9 | Establishing shots, action | 1536x864 |
| Tall | 9:16 | Vertical emphasis | 864x1536 |
| Square | 1:1 | Close-ups, portraits | 1024x1024 |
| Splash | Full page | Major moments | 1536x2048 |

## Sub-Agent Responsibilities

### comic-artist Sub-Agent

**ONLY responsible for image generation.** Does NOT handle:
- Page layout
- Panel assembly
- File organization beyond saving variations
- Selection or review

**DOES handle:**
- Receiving panel specification
- Generating N variations (default: 3)
- Saving variations to correct folder
- Logging generation metadata
- Accepting style/character consistency guidance

**Input:**
```json
{
  "panelId": "ch01-pg01-p01",
  "prompt": "Professional comic book panel: Val walking through...",
  "aspectRatio": "16:9",
  "variations": 3,
  "outputDir": "source/panels/chapter-01/page-001/panel-01/",
  "styleReference": "source/characters/val/val-variation-1.png"
}
```

**Output:**
- N image files saved to outputDir
- metadata.json with generation details

### Updated comic-artist.md

The sub-agent definition needs to be updated to:
1. Accept output directory parameter
2. Generate multiple variations in one call
3. Use consistent naming (variation-1.png, variation-2.png, etc.)
4. Save metadata about generation parameters
5. Support aspect ratio specifications

## Main Claude Responsibilities

**Claude orchestrates everything EXCEPT parallel image generation:**

1. **Script Parsing**
   - Read Comic Book Script - Everpeak.md
   - Extract panel descriptions, dialogue, visual elements
   - Generate panel-manifest.json with specifications
   - Determine aspect ratios based on panel descriptions

2. **Generation Orchestration**
   - Launch multiple comic-artist sub-agents in parallel
   - Each sub-agent generates variations for specific panels
   - Track progress and handle errors
   - Consolidate when all complete

3. **Review Interface Generation**
   - Create review.html from panel variations
   - Generate thumbnail grid for easy comparison
   - Set up selection interaction

4. **Page Assembly**
   - Read selections.json after human review
   - Use image manipulation (ImageMagick, Pillow, etc.) to:
     - Load selected panels
     - Apply panel borders (black, 2-3px)
     - Add gutters between panels (white, 8-10px)
     - Arrange panels according to page layout
     - Composite into final page image
   - Save to source/pages/

5. **Build Management**
   - Run CBZ build script
   - Generate preview images for GitHub Pages
   - Update metadata

## Review Interface Design

### review.html Structure

```html
<!DOCTYPE html>
<html>
<head>
    <title>Everpeak Comic Review - Chapter 1, Page 1</title>
    <link rel="stylesheet" href="review.css">
</head>
<body>
    <header>
        <h1>Panel Review & Selection</h1>
        <nav>
            <button id="prev-page">← Previous Page</button>
            <span>Chapter 1, Page 1</span>
            <button id="next-page">Next Page →</button>
        </nav>
        <div class="progress">
            <span id="selection-progress">0/5 panels selected</span>
            <button id="save-selections" disabled>Save Selections</button>
        </div>
    </header>

    <main>
        <!-- Panel 1 -->
        <section class="panel-group" data-panel-id="ch01-pg01-p01">
            <div class="panel-info">
                <h2>Panel 1</h2>
                <p class="description">Val walking through crowds...</p>
                <p class="specs">Aspect Ratio: 16:9 (Wide establishing shot)</p>
                <p class="dialogue">"The Dawn's Crown alignment approaches..."</p>
            </div>
            <div class="variations">
                <div class="variation" data-variation="1">
                    <img src="../source/panels/chapter-01/page-001/panel-01/variation-1.png" alt="Variation 1">
                    <button class="select-btn">Select This</button>
                </div>
                <div class="variation" data-variation="2">
                    <img src="../source/panels/chapter-01/page-001/panel-01/variation-2.png" alt="Variation 2">
                    <button class="select-btn">Select This</button>
                </div>
                <div class="variation" data-variation="3">
                    <img src="../source/panels/chapter-01/page-001/panel-01/variation-3.png" alt="Variation 3">
                    <button class="select-btn">Select This</button>
                </div>
            </div>
            <div class="feedback">
                <textarea placeholder="Optional notes or refinement requests..."></textarea>
                <button class="regenerate-btn">Regenerate This Panel</button>
            </div>
        </section>

        <!-- Repeat for each panel -->
    </main>

    <script src="review.js"></script>
</body>
</html>
```

### selections.json Format

```json
{
  "chapter": 1,
  "page": 1,
  "timestamp": "2025-10-18T18:45:00Z",
  "selections": {
    "ch01-pg01-p01": {
      "selectedVariation": 2,
      "notes": "Better composition on the crowd",
      "regenerateRequested": false
    },
    "ch01-pg01-p02": {
      "selectedVariation": 1,
      "notes": "",
      "regenerateRequested": false
    }
  },
  "pageStatus": "complete"
}
```

## Page Assembly Process

Using image manipulation tools (recommend ImageMagick or Python Pillow):

### Basic Page Layout Algorithm

```python
def assemble_page(page_number, selections):
    # Standard comic page: 6.625" x 10.25" at 300 DPI = 1988 x 3075 px
    # We'll use 1536 x 2048 for digital (3:4 aspect ratio)

    page = create_blank_image(1536, 2048, color='white')

    # Define gutters and margins
    margin = 40  # pixels
    gutter = 12  # pixels between panels
    border = 3   # pixels for panel borders

    # Read panel layout for this page
    layout = get_panel_layout(page_number)

    for panel_spec in layout:
        # Load selected panel
        panel_path = get_selected_panel_path(panel_spec['id'], selections)
        panel_img = load_image(panel_path)

        # Resize to fit layout slot
        panel_img = resize_to_fit(panel_img, panel_spec['width'], panel_spec['height'])

        # Add border
        panel_img = add_border(panel_img, border, color='black')

        # Composite onto page at correct position
        paste_image(page, panel_img, panel_spec['x'], panel_spec['y'])

    # Save final page
    save_image(page, f'source/pages/chapter-{chapter}/page-{page_number}.png')
```

### Standard Page Layouts

Pre-defined templates for common layouts:

- **3-panel vertical**: Full width, stacked
- **6-panel grid**: 2 columns x 3 rows
- **Splash + 2**: Full width splash, two panels below
- **Wide + 4**: Wide establishing, 2x2 grid below
- **Custom**: Define per page in script

## CBZ Build Process

### create-cbz.sh Script

```bash
#!/bin/bash

CHAPTER=$1
OUTPUT_DIR="releases"

# Create temporary directory
TEMP_DIR=$(mktemp -d)

# Copy pages in order
cp source/pages/chapter-${CHAPTER}/page-*.png "$TEMP_DIR/"

# Rename to sequential numbers (001.png, 002.png, etc.)
cd "$TEMP_DIR"
counter=1
for file in page-*.png; do
    new_name=$(printf "%03d.png" $counter)
    mv "$file" "$new_name"
    counter=$((counter + 1))
done

# Create ComicInfo.xml
cat > ComicInfo.xml <<EOF
<?xml version="1.0"?>
<ComicInfo>
    <Title>Everpeak Citadel: Echoes of the Dawn's Crown</Title>
    <Series>Everpeak Citadel</Series>
    <Number>$CHAPTER</Number>
    <Summary>High in the Frostveil Mountains, Everpeak Citadel prepares for the Winter Festival...</Summary>
    <Writer>Claude &amp; Rob Gruhl</Writer>
    <Publisher>Independent</Publisher>
    <Genre>Fantasy</Genre>
    <PageCount>$(ls -1 *.png | wc -l)</PageCount>
    <LanguageISO>en</LanguageISO>
</ComicInfo>
EOF

# Create CBZ (just a renamed ZIP)
zip -r "../${OUTPUT_DIR}/everpeak-citadel-chapter-${CHAPTER}.cbz" .

# Cleanup
cd -
rm -rf "$TEMP_DIR"

echo "✓ Created releases/everpeak-citadel-chapter-${CHAPTER}.cbz"
```

## Implementation Steps

### Phase 0: Reference Library Creation (CRITICAL FIRST STEP)

**Before generating any comic panels**, create the reference library for visual continuity.

See [CONTINUITY.md](CONTINUITY.md) for complete details.

0a. **Create reference folder structure**
   ```bash
   mkdir -p references/{style,characters,environments,sequential}
   mkdir -p references/characters/{val,prismor,pocky,lunara,malrik}/{turnaround,expressions,poses,details}
   ```

0b. **Generate and select style masters**
   - Generate 10 variations of a test panel
   - Human selects best 2-3 that define the art style
   - Analyze and save style guide data
   - Estimated time: 1 hour

0c. **Generate character reference library**
   - For each of 5 main characters:
     - Turnarounds: 5 angles × 3 variations = 15 images → select best 5
     - Expressions: 6 emotions × 3 variations = 18 images → select best 6
     - Poses: 5 poses × 3 variations = 15 images → select best 5
   - Total per character: ~16 reference images
   - Total for all 5 characters: ~80 reference images
   - Estimated time: 6-8 hours
   - **This is a one-time investment that ensures consistency across all 40 pages**

0d. **Analyze all references**
   - Use Claude's Read tool to analyze each reference image
   - Extract style elements, color palettes, character features
   - Save analysis metadata alongside each reference
   - Generate prompt snippets for reuse

### Phase 1: Foundation (Do This Second)

1. **Create folder structure**
   ```bash
   mkdir -p source/{characters,panels,selected,pages}
   mkdir -p releases review scripts docs/preview
   ```

2. **Update comic-artist sub-agent**
   - Modify `.claude/agents/comic-artist.md`
   - Add parameters for output directory, variations, aspect ratio
   - Update to save metadata.json

3. **Create `.claude/CLAUDE.md`**
   - Project context and instructions for main Claude
   - Panel specification format
   - Assembly instructions
   - Build process

4. **Update README.md**
   - Document new workflow
   - Explain review process
   - Link to PLAN.md

### Phase 2: Generation Pipeline

5. **Create script parser**
   - Extract panel descriptions from script
   - Generate panel-manifest.json

6. **Test parallel generation**
   - Generate one page worth of panels
   - Verify folder structure
   - Check metadata

### Phase 3: Review Interface

7. **Build review.html**
   - HTML structure
   - CSS styling
   - JavaScript for selection

8. **Test selection workflow**
   - Generate review page
   - Make selections
   - Verify selections.json

### Phase 4: Assembly

9. **Create page assembly script**
   - Python script using Pillow
   - Read selections
   - Composite panels
   - Output final pages

10. **Test full page assembly**
    - Assemble one complete page
    - Verify output quality

### Phase 5: Build & Release

11. **Create CBZ build script**
    - Bash script to package CBZ
    - Generate ComicInfo.xml
    - Test with YACReader

12. **Set up GitHub Pages**
    - Landing page
    - Preview images
    - Download links

## Success Criteria

- [ ] **Reference Library**: Style masters and character references created and analyzed
- [ ] **Visual Continuity**: Characters recognizable across multiple panels
- [ ] **Sub-agent Generation**: Generates 3+ variations per panel with consistent style
- [ ] **Organization**: All variations saved to organized folders with metadata
- [ ] **Review Interface**: Loads and displays all variations correctly
- [ ] **Selections**: Persist to selections.json with proper tracking
- [ ] **Page Assembly**: Reads selections and composites panels correctly
- [ ] **Layout**: Final pages have proper borders, gutters, and composition
- [ ] **CBZ Format**: Opens correctly in YACReader with metadata
- [ ] **GitHub Pages**: Showcases project with previews and downloads

## Next Steps

After creating this plan:
1. Update `.claude/agents/comic-artist.md` with new parameters
2. Create `.claude/CLAUDE.md` with project instructions
3. Update `README.md` with workflow documentation
4. Create initial folder structure
5. Begin implementation of Phase 1

## Future Enhancements

- ✅ **Style consistency** - Addressed via hierarchical multi-reference system (see CONTINUITY.md)
- ✅ **Character consistency** - Addressed via character reference library (see CONTINUITY.md)
- **Automated lettering**: Add dialogue and captions programmatically using text positioning
- **Panel border variations**: Different styles (borderless, rounded, dramatic angles)
- **Color grading**: Automated color adjustment for mood (darker for dramatic scenes, etc.)
- **Advanced face consistency**: Face detection and matching algorithms
- **PDF export**: High-resolution PDF format in addition to CBZ
- **Web viewer**: Interactive HTML5 comic reader with page-turn animations
- **Batch processing**: Generate entire chapters at once with dependency tracking
- **Reference evolution**: ML-based selection of which references produce best results
