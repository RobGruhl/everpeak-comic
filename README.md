# Everpeak Citadel: Echoes of the Dawn's Crown

An AI-generated comic book based on a D&D campaign. Uses OpenAI's gpt-image-1 for panel artwork and optional Google Gemini 2.5 Flash Image for refinement.

## Project Status

**In Development**: Structured JSON workflow with enhanced prompts

- ✅ Complete 40-page script with full character, NPC, and location descriptions
- ✅ Script parser creates structured JSON files (one per page)
- ✅ Pages 1-2: Fully enhanced with complete descriptions (11 panels)
- ⏳ Pages 4-40: Need enhancement (24 pages, 161 panels remaining)
- ✅ Generation pipeline with OpenAI + optional Gemini refinement
- ✅ Page assembly and CBZ packaging

## Quick Start

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Configure API keys
cat > .env << EOF
OPENAI_API_KEY=your_openai_key_here
GOOGLE_API_KEY=your_google_key_here  # Optional, for Gemini refinement
EOF

# Step 1: Parse script into structured JSON
python parse_script.py

# Step 2: Generate comic (currently TEST MODE - page 1 only)
python generate.py

# Output: output/everpeak-citadel.cbz
```

## What This Does

### Phase 0: Script Parsing (`parse_script.py`)
1. Reads `Comic Book Script - Everpeak.md`
2. Extracts all character, NPC, and creature descriptions
3. Detects characters per panel using nickname mapping
4. Creates structured JSON files in `pages/` directory
5. Generates complete prompts with locations, characters, NPCs, and style

**Current Progress**:
- ✅ Script parsed into 26 page files (171 total panels)
- ✅ Pages 1-2 manually enhanced with complete descriptions
- ⏳ Pages 4-40 have basic descriptions, need full enhancement

### Phase 1: Image Generation (`generate.py`)
1. Loads page data from JSON
2. Generates panels using OpenAI gpt-image-1
3. Optionally refines first 5 panels with Google Gemini
4. Saves OpenAI, Gemini, and final versions

### Phase 2: Page Assembly
1. Loads generated panel images
2. Applies grid layout based on panel count
3. Composites onto 1600x2400 canvas

### Phase 3: CBZ Packaging
1. Creates ZIP archive with .cbz extension
2. Adds ComicInfo.xml metadata
3. Packages assembled pages

## Requirements

- Python 3.8+
- OpenAI API key (get at https://platform.openai.com/api-keys)
- Google API key (optional, for Gemini refinement)
- API credits: ~$5-6 for full comic (171 panels)

## Project Structure

```
everpeak-comic/
├── Comic Book Script - Everpeak.md   # Complete 40-page script
├── parse_script.py                   # Script → JSON parser
├── generate.py                       # Main generation pipeline
├── requirements.txt                  # Python dependencies
├── .env                              # API keys (not committed)
├── pages/                            # Structured JSON (one per page)
│   ├── page-001.json                 # ✅ Enhanced
│   ├── page-002.json                 # ✅ Enhanced
│   ├── page-004.json                 # ⏳ Needs enhancement
│   └── ...
└── output/                           # Generated content
    ├── panels/                       # Individual panel images
    │   ├── *-openai.png              # OpenAI versions
    │   ├── *-gemini.png              # Gemini refined (optional)
    │   └── *.png                     # Final versions
    ├── pages/                        # Assembled full pages
    └── everpeak-citadel.cbz          # Final comic archive
```

## Characters

### Main Party (5 heroes)
- **Val** (Valthirion Emberstride): Brass dragonborn monk, courier
- **Prismor**: Blue crystal dragonborn paladin, Oath of the Ancients
- **Apocalypse Winter** (Pocky): Human wizard, scholar
- **Lunara**: High elf druid, Circle of the Moon
- **Malrik**: Drow rogue, street performer

### Key NPCs
- **Marge**: Head Librarian
- **Marivielle Greenbough**: Café owner
- **Barth**: Drow blacksmith
- **Lord Alric**: Antagonist (human noble)
- **Sorrel**: Gold dragon wyrmling (disguised as halfling)

### Creatures
- **Verdant Mephit**: Corrupted Nature Essence (vines, thorns)
- **Blink Mephit**: Corrupted Displacement Essence (nearly invisible)
- **Gear Mephit**: Corrupted Mechanistic Essence (clockwork)
- **Starlight Mephit**: Corrupted Celestial Essence (cosmic)
- **Melody Mephit**: Corrupted Harmony Essence (sound waves)

## Story Summary

The winter festival at Everpeak Citadel coincides with the Dawn's Crown celestial alignment - a once-per-century event. When the Yule Tree ceremony goes wrong and magical essences become corrupted, five unlikely heroes must investigate. They discover Lord Alric's conspiracy to corrupt the ancient Elven Orrery for power, leading to an epic battle in the hidden sanctum beneath the citadel.

## Technical Details

### Structured JSON Format

Each page JSON includes complete panel specifications:

```json
{
  "page_num": 1,
  "title": "Character Introductions",
  "panel_count": 5,
  "panels": [
    {
      "panel_num": 1,
      "annotation": null,
      "visual": "Val walking through crowds...",
      "dialogue": "Val (thought bubble): ...",
      "characters": {
        "Val": "Brass dragonborn monk. Just under 7 feet... [COMPLETE]"
      },
      "npcs": {},
      "aspect_ratio": "square",
      "size": "1024x1024",
      "prompt": "Professional comic book panel illustration.\n\nLocation: ...\n\nCharacters:\n- Val: ...\n\nScene: ...\n\nDialogue: ...\n\nStyle: ..."
    }
  ]
}
```

### Image Generation Models

- **OpenAI gpt-image-1**: Latest image model, excellent quality
  - Sizes: 1024x1024 (square), 1536x1024 (wide), 1024x1536 (tall)
  - Quality: High
  - Cost: ~$0.02-0.04 per image

- **Google Gemini 2.5 Flash Image** (optional refinement):
  - Refines OpenAI images for better character accuracy and text clarity
  - First 50 images/day free
  - Currently used for panels 1-5 as test

### Current Limitations

1. **TEST MODE**: Currently generates only page 1 (5 panels)
   - Remove page_num limit in generate.py to generate all pages

2. **JSON Enhancement Incomplete**: Only pages 1-2 fully enhanced
   - Remaining 24 pages need complete character/NPC/location descriptions
   - Blocks full comic generation

3. **Character Consistency**: AI-generated characters vary between panels
   - Mitigation: Extremely detailed descriptions in every prompt
   - Future: Reference image system (see CONTINUITY.md)

## Cost Estimate

- **Full Comic**: 171 panels × ~$0.03 avg = ~$5-6 (OpenAI only)
- **With Gemini Refinement**: +$0 (free tier covers testing)
- **Test Mode (Page 1)**: 5 panels × ~$0.03 = ~$0.15

## Format

- **Pages**: 26 pages (some combined as page ranges in script)
- **Panels**: 171 total panels
- **Format**: CBZ (Comic Book ZIP) - standard format readable by all comic apps
- **Page Size**: 1600x2400 pixels
- **Panel Sizes**: Variable (1024x1024, 1536x1024, 1024x1536, 1536x2048)

## Next Steps

1. ✅ Complete script parsing with character detection
2. ✅ Enhance pages 1-2 with full descriptions
3. ⏳ Enhance remaining 24 pages (automate or continue manually)
4. ⏳ Generate page 1 with enhanced prompts, verify quality
5. ⏳ Test Gemini refinement quality
6. ⏳ Scale up to full comic generation
7. ⏳ Human review and panel selection
8. ⏳ Assemble final CBZ
9. ⏳ Publish to GitHub releases

## Documentation

- **[.claude/CLAUDE.md](.claude/CLAUDE.md)**: Complete technical documentation
- **[CONTINUITY.md](CONTINUITY.md)**: Visual continuity system plan
- **[PLAN.md](PLAN.md)**: Original production workflow plan
- **[Comic Script](Comic%20Book%20Script%20-%20Everpeak.md)**: Full 40-page script

## License

This project is an experimental AI-generated comic. The D&D campaign story is original. Generated artwork uses OpenAI and Google AI models.
