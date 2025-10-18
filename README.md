# Everpeak Citadel: Comic Book Project

A comic book generation project using Claude Code sub-agents to create professional comic art with human-in-the-loop quality control.

## Project Overview

**Everpeak Citadel: Echoes of the Dawn's Crown** is a 40-page D&D-inspired comic book about five heroes who must save a magical citadel from corruption during a rare celestial alignment.

### The Story

Five diverse heroes investigate mysterious magical sabotage during the Winter Festival at Everpeak Citadel. When a noble threatens to corrupt an ancient elven artifact for power, our heroes must work together to restore balance to the citadel's magical essences.

**Read the complete script**: [Comic Book Script - Everpeak.md](Comic%20Book%20Script%20-%20Everpeak.md)

### Characters

- **Val (Valthirion Emberstride)** - Brass Dragonborn Monk and courier
- **Prismor** - Blue Crystal Dragonborn Paladin (Oath of the Ancients)
- **Apocalypse Winter (Pocky)** - Human Wizard with scholarly strength
- **Lunara** - High Elf Druid (Circle of the Moon) with nature magic
- **Malrik** - Drow Rogue and street performer

## Production Workflow

This project demonstrates an innovative approach to comic creation that combines AI-generated artwork with human quality control:

```
📝 Script → 🤖 AI Generation → 👁️ Human Review → 🎨 Assembly → 📦 CBZ
```

### 1. Script Parsing
Claude Code parses the script to extract panel descriptions, determine aspect ratios, and create generation specifications.

### 2. Parallel Generation
Multiple comic-artist sub-agents run in parallel, each generating 3-5 variations of individual panels using OpenAI's gpt-image-1 model.

### 3. Human Review
An HTML interface displays all variations. You select the best version of each panel, ensuring quality and consistency.

### 4. Page Assembly
Selected panels are assembled into complete pages with proper borders, gutters, and layout.

### 5. CBZ Build
Final pages are packaged into standard CBZ (Comic Book ZIP) format for reading in any comic reader.

## Why This Approach?

**AI image generation is not deterministic enough for single-shot production.** By generating multiple variations and using human selection, we get:

- **Quality Control**: Choose the best composition, expression, and details
- **Visual Consistency**: Ensure characters look the same across panels
- **Creative Direction**: Maintain artistic vision throughout the comic
- **Reliability**: AI handles the heavy lifting, humans ensure quality

## File Structure

```
everpeak-comic/
├── source/
│   ├── characters/          # Character reference art
│   ├── panels/             # AI-generated panel variations
│   │   └── chapter-01/
│   │       └── page-001/
│   │           └── panel-01/
│   │               ├── variation-1.png
│   │               ├── variation-2.png
│   │               ├── variation-3.png
│   │               └── metadata.json
│   ├── selected/           # Selected versions
│   │   └── selections.json
│   └── pages/              # Assembled full pages
├── releases/               # Final CBZ files
│   └── everpeak-citadel-chapter-01.cbz
├── review/                 # Review interface
│   └── review.html
├── scripts/                # Build automation
└── Comic Book Script - Everpeak.md
```

## Sub-Agent Architecture

### comic-artist Sub-Agent

The comic-artist sub-agent is responsible for **image generation only**:
- Generates 3-5 variations per panel
- Supports multiple aspect ratios (16:9, 3:4, 9:16, 1:1)
- Saves to organized directories
- Creates generation metadata
- Runs in parallel for efficiency

See [.claude/agents/comic-artist.md](.claude/agents/comic-artist.md) for details.

### Main Claude Workflow

Claude Code orchestrates everything except parallel image generation:
- Script parsing and planning
- Sub-agent coordination
- Review interface generation
- Page assembly
- CBZ building

See [.claude/CLAUDE.md](.claude/CLAUDE.md) for implementation details.

## Distribution Format: CBZ

We use **CBZ (Comic Book ZIP)** as the primary format because:

- ✅ Industry standard format
- ✅ Works with all major comic readers (YACReader, MComix, Sumatra PDF)
- ✅ Cross-platform (Windows, macOS, Linux, iOS, Android)
- ✅ Simple structure (just a ZIP of images)
- ✅ Includes metadata (ComicInfo.xml)
- ✅ Single portable file

### Recommended Readers

- **YACReader** (Windows, macOS, Linux) - Full-featured with library management
- **MComix** (Windows, Linux) - Lightweight and fast
- **Sumatra PDF** (Windows) - Multi-format minimalist reader

## GitHub Pages

The repository includes a GitHub Pages site for:
- Project showcase and documentation
- Character art gallery
- Sample pages preview
- CBZ download links

Visit: [https://robgruhl.github.io/everpeak-comic](https://robgruhl.github.io/everpeak-comic)

## Technology Stack

- **Claude Code** - Workflow orchestration and scripting
- **OpenAI gpt-image-1** - High-quality comic art generation
- **Sub-agents** - Parallel, specialized task handling
- **Python + Pillow** - Image manipulation and assembly
- **Bash scripts** - Build automation
- **HTML/CSS/JS** - Review interface

## Documentation

- **[PLAN.md](PLAN.md)** - Complete production workflow and implementation plan
- **[.claude/CLAUDE.md](.claude/CLAUDE.md)** - Project instructions for Claude Code
- **[sub-agents.md](sub-agents.md)** - Sub-agent overview
- **[SUBAGENT_USAGE.md](SUBAGENT_USAGE.md)** - Usage documentation

## Panel Specifications

Standard panel dimensions for digital comics:

| Type | Aspect Ratio | Size (px) | Use Case |
|------|--------------|-----------|----------|
| Standard | 3:4 | 768x1024 | Regular panel |
| Wide | 16:9 | 1536x864 | Establishing shots, action sequences |
| Tall | 9:16 | 864x1536 | Vertical emphasis, falling/climbing |
| Square | 1:1 | 1024x1024 | Close-ups, portraits |
| Splash | 3:4 | 1536x2048 | Full page dramatic moments |

## Getting Started

### Prerequisites

- Claude Code installed
- OpenAI API key with gpt-image-1 access
- Python 3.8+ with Pillow (for page assembly)
- Comic reader software (recommended: YACReader)

### Environment Setup

1. Clone the repository
2. Add your OpenAI API key to `.env`:
   ```
   OPENAI_API_KEY=sk-your-key-here
   ```

### Generate Your First Page

Ask Claude Code:
```
Generate Chapter 1, Page 1 panels
```

Claude will:
1. Parse the script for panel specifications
2. Launch parallel sub-agents to generate variations
3. Create the review interface
4. Wait for you to select your preferred versions
5. Assemble the final page

### Review Selections

Open `review/review.html` in your browser to review and select panel variations.

### Build CBZ

After pages are assembled:
```bash
./scripts/create-cbz.sh 1  # Chapter number
```

Find your CBZ in `releases/everpeak-citadel-chapter-01.cbz`

## Development Status

This project is in active development. Current focus:

- [x] Complete 40-page script with detailed character descriptions
- [x] Sub-agent architecture and workflow design
- [x] Folder structure and organization
- [x] Panel specification format
- [ ] Review interface implementation
- [ ] Page assembly scripts
- [ ] CBZ build automation
- [ ] Character reference art generation
- [ ] Chapter 1 production

## Future Enhancements

- **Style transfer** - Apply consistent art style across panels
- **Character consistency** - Face detection and matching
- **Automated lettering** - Add dialogue and captions programmatically
- **Color grading** - Unified color palette per chapter
- **PDF export** - Alternative format for digital reading
- **Web viewer** - Interactive HTML5 comic reader

## Contributing

This is a demonstration project exploring AI-assisted comic creation. The workflow and tools are designed to be extensible for other comic projects.

## License

MIT License - see [LICENSE](LICENSE) for details.

## About

This project demonstrates how AI-assisted workflows can augment creative processes. By combining:
- Traditional comic book storytelling
- AI-generated artwork with multiple variations
- Human quality control and selection
- Automated assembly and packaging

We create a production pipeline that leverages AI's speed while maintaining human creative direction.

**Created with Claude Code** - [Learn more about sub-agents](https://docs.claude.com/en/docs/claude-code)

---

**Repository**: https://github.com/RobGruhl/everpeak-comic
