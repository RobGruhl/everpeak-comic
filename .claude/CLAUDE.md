# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Everpeak Citadel: Echoes of the Dawn's Crown** is an AI-generated comic book based on a D&D campaign. The project uses:
- **OpenAI gpt-image-1** for panel artwork generation
- **Google Gemini 2.5 Flash Image** for optional image refinement
- **Structured JSON workflow** for consistent, accurate prompts
- **Python + Pillow** for page assembly and CBZ packaging

**Key Files:**
- `Comic Book Script - Everpeak.md` - Complete 40-page script with full character, NPC, location, and creature descriptions
- `parse_script.py` - Parses script into structured JSON files (one per page)
- `generate.py` - Main generation pipeline (load JSON → generate → optionally refine with Gemini → assemble → package)
- `pages/page-NNN.json` - Structured page data with complete prompts
- `requirements.txt` - Python dependencies (openai, Pillow, python-dotenv, google-genai)
- `.env` - API keys (not committed)

## Development Commands

### Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt

# Configure API keys
# Create .env file with:
OPENAI_API_KEY=your_openai_key_here
GOOGLE_API_KEY=your_google_key_here  # Optional, for Gemini refinement
```

### Running

```bash
# Step 1: Parse script into structured JSON (run after script changes)
python parse_script.py

# Output: pages/page-001.json through page-040.json (26 pages, 171 panels total)

# Step 2: Generate comic panels and pages
python generate.py

# Currently in TEST MODE - generates only page 1
# Output:
# - output/panels/page-001-panel-1-openai.png (OpenAI versions)
# - output/panels/page-001-panel-1-gemini.png (Gemini refined, panels 1-5 only)
# - output/panels/page-001-panel-1.png (final version used for assembly)
# - output/pages/page-001.png (assembled full page)
# - output/everpeak-citadel.cbz (final comic archive)
```

### Testing Changes
```bash
# Test script parsing without API calls
python parse_script.py

# Test single panel generation
# Modify TEST MODE filter in generate.py (line ~438)

# View generated CBZ
# Use any CBZ reader app (YACReader, Calibre, CDisplayEx, etc.)
```

## Architecture

### Workflow Pipeline

The generation process follows a structured data approach:

**Phase 0: Script Parsing (`parse_script.py`)**
- Reads `Comic Book Script - Everpeak.md`
- Extracts ALL character descriptions (5 main party + 9 NPCs/supporting characters)
- Extracts NPC descriptions separately
- Extracts creature/monster descriptions (mephits, Sorrel's dragon form, etc.)
- Identifies major locations with descriptions
- Parses COMIC BOOK NARRATIVE into structured pages
- **Character detection**: Uses nickname mapping (e.g., "Pocky" → "Apocalypse Winter")
- Creates one JSON file per page in `pages/` directory
- Each panel includes:
  - `panel_num`, `annotation` (e.g., "Wide", "Large"), `visual`, `dialogue`
  - `characters`: Dict of main party characters in this panel with full descriptions
  - `npcs`: Dict of NPCs in this panel with full descriptions
  - `creatures`: Dict of creatures/monsters in this panel with full descriptions (if applicable)
  - `aspect_ratio`, `size`: Determined from annotation
  - `prompt`: Complete ready-to-use prompt with location, characters, scene, dialogue, and style

**Current Status: Pages 1-2 have been manually enhanced with:**
- Complete character descriptions (all physical details, equipment, distinctive traits)
- Proper NPC categorization (e.g., Marge moved from characters to npcs)
- Location descriptions (marketplace, balcony, library, courtyard, mountain path)
- Creature descriptions (Verdant Mephit with full visual details)
- Enhanced prompts incorporating all the above

**Remaining: Pages 4-40 (24 pages, ~161 panels) need the same enhancement treatment.**

**Phase 1: Image Generation (`generate_panel_image()`)**
- Loads page data from JSON (e.g., `pages/page-001.json`)
- For each panel, uses the pre-built `prompt` field (no prompt construction needed)
- Calls OpenAI Images API with gpt-image-1 model:
  - Parameters: size from panel data (1024x1024, 1536x1024, etc.), high quality
  - Response: base64 JSON (decoded and saved)
  - Saves as `page-XXX-panel-X-openai.png`
- Rate limiting: 1s sleep between calls
- **Optional Gemini Refinement** (panels 1-5 only if `GEMINI_AVAILABLE`):
  - Sends OpenAI image + original prompt to Gemini 2.5 Flash Image
  - Asks Gemini to refine: character accuracy, text clarity, composition, art consistency
  - Saves as `page-XXX-panel-X-gemini.png`
  - Uses Gemini version as final if available
- Saves final version as `page-XXX-panel-X.png` (for assembly)
- Resume capability: Skips if OpenAI version already exists
- Error handling: Creates gray placeholder on failure

**Phase 2: Page Assembly (`assemble_page()`)**
- Loads generated panel images for a page
- Applies simple layout logic based on panel count:
  - ≤3 panels: Vertical stack
  - 4-6 panels: 2-column grid
  - 7+ panels: 3-column grid
- Resizes panels to fit layout (LANCZOS resampling)
- Composites onto 1600x2400 white canvas with 20px gutters, 3px borders
- Saves assembled page to `output/pages/`

**Phase 3: CBZ Packaging (`create_cbz()`)**
- Creates ZIP archive with .cbz extension
- Adds ComicInfo.xml metadata (title, series, genre, page count)
- Includes assembled page images in sequential order
- CBZ format is standard - readable by all comic reader apps

### JSON Structure Example

```json
{
  "page_num": 1,
  "title": "Character Introductions",
  "panel_count": 5,
  "panels": [
    {
      "panel_num": 1,
      "annotation": null,
      "visual": "Val walking through crowds, delivering messages...",
      "dialogue": "Val (thought bubble): \"The Dawn's Crown alignment...\"",
      "characters": {
        "Val": "Brass dragonborn monk. Just under 7 feet tall, lean athletic build... [COMPLETE DESCRIPTION]"
      },
      "npcs": {},
      "aspect_ratio": "square",
      "size": "1024x1024",
      "prompt": "Professional comic book panel illustration.\n\nLocation: Everpeak Citadel festival marketplace...\n\nCharacters:\n- Val: [COMPLETE DETAILS]...\n\nScene: [FULL SCENE DESCRIPTION]...\n\nDialogue: [DIALOGUE]...\n\nStyle: Bold ink line art, vibrant colors..."
    }
  ]
}
```

### Character Nickname Mapping

The parser handles character nicknames used in the script:

```python
nickname_map = {
    'pocky': 'Apocalypse Winter',
    'val': 'Val',
    'valthirion': 'Val',
    'prismor': 'Prismor',
    'lunara': 'Lunara',
    'malrik': 'Malrik',
    'marge': 'Marge',
    'alric': 'Alric',
    'sorrel': 'Sorrel'
}
```

This ensures characters are correctly detected even when referred to by nickname (e.g., "Pocky" in script → "Apocalypse Winter" in character descriptions).

### Enhanced Prompt Structure

Enhanced prompts (pages 1-2 completed, others need work) include:

1. **Location Description**: Detailed environment context from script location descriptions
2. **Characters**: Full descriptions including:
   - Race, class, age appearance
   - Height, build, physical features
   - Eyes, hair, skin color, distinctive traits
   - Clothing and equipment with specific details
   - Personality-driven body language
3. **NPCs**: Same level of detail as characters, properly categorized
4. **Creatures**: Monster/elemental descriptions when applicable
5. **Scene**: Detailed action and composition
6. **Dialogue**: Speech with clear instructions for thought bubbles vs. speech bubbles
7. **Style**: Consistent comic book art direction

### Error Handling & Resume Capability

Key design pattern: **graceful degradation**

- Panel generation checks if `-openai.png` exists before calling API (skip if present)
- Allows resuming after failures without regenerating everything
- API errors create gray placeholder images instead of crashing
- Page assembly continues even if some panels are placeholders
- CBZ creation skips missing pages rather than failing
- Gemini refinement is optional - system works without it

### Current Limitations (TEST MODE)

Line ~438 in `generate.py`:
```python
# TEST MODE: Only generate page 1
page_num = 1
```

This limits generation to page 1 during development to:
- Reduce API costs during testing
- Enable faster iteration on layout/assembly logic
- Test full pipeline end-to-end without waiting for all 171 panels

**To generate full comic**: Change `page_num` to desired page number or modify to loop through all pages.

## Character & Entity Reference

### Main Party (5 characters)
- **Val** (Valthirion Emberstride): Brass dragonborn monk, courier
- **Prismor**: Blue crystal dragonborn paladin, Oath of the Ancients
- **Apocalypse Winter** (Pocky): Human wizard, scholar
- **Lunara**: High elf druid, Circle of the Moon
- **Malrik**: Drow rogue, street performer

### Key NPCs
- **Marge**: Head Librarian (human woman, 40s-50s)
- **Marivielle Greenbough**: Café owner (half-elf)
- **Barth**: Blacksmith (drow)
- **Lord Alric**: Antagonist (human noble, 40s)
- **Sorrel**: Gold dragon wyrmling in halfling disguise

### Creatures/Monsters
- **Verdant Mephit**: Nature Essence corrupted (vines, thorns, 2-3 ft)
- **Blink Mephit**: Displacement Essence corrupted (nearly invisible, flickers)
- **Gear Mephit**: Mechanistic Essence corrupted (clockwork, brass, iron)
- **Starlight Mephit**: Celestial Essence corrupted (star-fields, cosmic dust)
- **Melody Mephit**: Harmony Essence corrupted (pastel sound waves)

### Major Locations
- **Everpeak Citadel Exterior**: Massive mountain fortress, white stone, crystalline towers
- **Festival Marketplace**: Bustling stalls, decorations, winter setting
- **Grand Courtyard**: Open space for Yule Tree ceremony
- **The Grand Library**: Soaring ceilings, endless shelves, magical lights
- **The Observatory**: Small domed chamber with glass ceiling
- **Courier Tunnels**: Rough stone, chalk runes, displacement magic
- **Balcony Garden Café**: Impossible sunny terrace, lush greenery
- **The Elven Sanctum**: Hidden cavern, the Orrery at center

## Cost Considerations

- **OpenAI gpt-image-1**: ~$0.02-0.04 per 1024x1024 image, more for larger sizes
- Full comic estimate: 171 panels × ~$0.03 avg = ~$5-6
- TEST MODE (page 1): 5 panels × ~$0.03 = ~$0.15
- **Google Gemini 2.5 Flash Image**: First 50 refinements per day are free, then low cost
- Gemini refinement (panels 1-5): 5 panels = free tier

## Making Changes

### Enhancing Page JSON Files

Pages 1-2 are complete. Pages 4-40 need enhancement. For each page:

1. Read the page JSON file
2. Read the comic script to find character, NPC, location, creature descriptions
3. For each panel, enhance:
   - `characters`: Add complete descriptions from script
   - `npcs`: Move non-main-party characters here, add complete descriptions
   - `creatures`: Add creature descriptions if present
   - `prompt`: Rewrite to include:
     - Location description (from script's MAJOR LOCATIONS)
     - Complete character descriptions
     - Complete NPC descriptions
     - Complete creature descriptions if applicable
     - Enhanced scene description
     - Clear dialogue/thought bubble instructions
     - Style directive
4. Save enhanced JSON

**Recommended approach**: Create a script to automate this for remaining 24 pages.

### Modifying Layouts

Edit `assemble_page()` layout logic in `generate.py`:
- Adjust `PAGE_WIDTH`, `PAGE_HEIGHT` constants for different page sizes
- Change `GUTTER` spacing between panels
- Modify conditional branches to alter grid patterns
- Consider panel count and content when designing layouts

### Changing Image Quality

Edit generation parameters in `generate_panel_image()`:
- `size`: Read from panel JSON (1024x1024, 1536x1024, 1024x1536, 1536x2048)
- `quality`: "high" (current setting)
- Aspect ratios determined by panel annotations in script

### Improving Character Consistency

Current approach: Detailed text descriptions in every prompt

Future improvements:
- Generate character reference sheets first
- Use reference images as input to gpt-image-1 (if supported)
- Create style master reference for consistent art style
- Implement visual continuity system (see CONTINUITY.md for detailed plan)

### Adding Dialogue Rendering

Current system generates pure artwork. Speech bubbles are requested in prompts but may need manual lettering.

To add programmatic lettering:
- Use Pillow's `ImageDraw.text()` after assembly
- Parse dialogue from panel JSON (already available)
- Implement bubble shapes, tail pointing, word wrapping
- Use comic lettering fonts (Comic Sans, Anime Ace, Blambot fonts)

## Output Structure

```
pages/
├── page-001.json
├── page-002.json
├── ...
└── page-040.json

output/
├── panels/
│   ├── page-001-panel-1-openai.png
│   ├── page-001-panel-1-gemini.png (if Gemini available)
│   ├── page-001-panel-1.png (final)
│   └── ...
├── pages/
│   ├── page-001.png
│   ├── page-002.png
│   └── ...
└── everpeak-citadel.cbz
```

CBZ internal structure:
```
everpeak-citadel.cbz (ZIP archive)
├── ComicInfo.xml
├── 001.png
├── 002.png
└── ...
```

## Known Issues

1. **Character consistency**: AI-generated characters vary between panels
   - Mitigation: Complete detailed descriptions in every prompt
   - Future: Reference image system, style masters (see CONTINUITY.md)

2. **Layout simplicity**: Fixed grid layouts don't adapt to panel content
   - Current: Panel count determines layout
   - Future: Content-aware layouts (action panels get more space)

3. **Dialogue rendering**: Text-to-image models handle speech bubbles inconsistently
   - Mitigation: Clear instructions in prompts
   - Alternative: Programmatic lettering post-generation

4. **JSON enhancement incomplete**: Only pages 1-2 fully enhanced
   - Remaining: 24 pages (161 panels) need complete descriptions added
   - Blocks: Full comic generation until enhanced
   - Solution: Create automation script or continue manual enhancement

5. **Gemini API key loading**: `.env` file may not be loaded by running scripts
   - Workaround: Restart Python session after adding GOOGLE_API_KEY
   - Alternative: Export key in shell before running

## Next Steps

1. **Complete JSON enhancement**: Enhance remaining 24 pages with complete descriptions
2. **Test generation**: Generate page 1 with enhanced prompts, verify quality
3. **Iterate on pages 2-3**: Test Gemini refinement, compare quality
4. **Scale up**: Remove TEST MODE, generate full comic (or chapter at a time)
5. **Review and select**: Human review of variations, select best panels
6. **Assemble final**: Build complete CBZ with selected panels
7. **Publish**: Upload to GitHub releases, create preview images for documentation
