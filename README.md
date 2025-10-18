# Everpeak Citadel: Comic Book Project

A comic book generation project using Claude Code sub-agents to create professional comic art and illustrations.

## Project Overview

**Everpeak Citadel: Echoes of the Dawn's Crown** is a D&D-inspired comic book about five heroes who must save a magical citadel from corruption during a rare celestial alignment.

This repository contains:
- Complete comic book script with character descriptions and panel breakdowns
- Sub-agent definitions for automated comic art generation
- Documentation on the sub-agent approach for creative projects

## The Comic

The story follows five diverse heroes as they investigate mysterious magical sabotage during the Winter Festival at Everpeak Citadel. When a noble threatens to corrupt an ancient elven artifact for power, our heroes must work together to restore balance to the citadel's magical essences.

See [Comic Book Script - Everpeak.md](Comic%20Book%20Script%20-%20Everpeak.md) for the complete script.

## Characters

### The Party
- **Val (Valthirion Emberstride)** - Brass Dragonborn Monk and courier
- **Prismor** - Blue Crystal Dragonborn Paladin (Oath of the Ancients)
- **Apocalypse Winter (Pocky)** - Human Wizard with scholarly strength
- **Lunara** - High Elf Druid (Circle of the Moon) with nature magic
- **Malrik** - Drow Rogue and street performer seeking redemption

### Key NPCs
- **Sorrel** - Mysterious halfling child (secretly a gold dragon wyrmling)
- **Lord Alric** - The antagonist seeking forbidden power
- Plus various supporting characters in the citadel

## Sub-Agent Approach

This project uses Claude Code's sub-agent system to generate comic book artwork. The `comic-artist` sub-agent leverages OpenAI's gpt-image-1 model to create consistent character illustrations and comic panels.

### How It Works

1. **Agent Definition**: The `.claude/agents/comic-artist.md` file defines the specialized agent
2. **Character Descriptions**: Detailed visual descriptions ensure consistency
3. **Parallel Generation**: Multiple agents can run simultaneously for faster results
4. **Style Consistency**: Professional comic book style maintained across all images

See [sub-agents.md](sub-agents.md) and [SUBAGENT_USAGE.md](SUBAGENT_USAGE.md) for detailed documentation.

## Generated Artwork

Character illustrations are generated using the sub-agent system and saved to your Pictures folder. Each character has been designed with specific visual traits to ensure consistency throughout the comic.

## Technology Stack

- **Claude Code**: For orchestrating the creative workflow
- **OpenAI gpt-image-1**: For generating high-quality comic art
- **Sub-agents**: For specialized, autonomous task handling

## Project Structure

```
everpeak-comic/
├── .claude/
│   └── agents/
│       └── comic-artist.md      # Sub-agent definition
├── Comic Book Script - Everpeak.md  # Complete comic script
├── sub-agents.md                # Sub-agent overview
├── SUBAGENT_USAGE.md           # Usage documentation
└── README.md                    # This file
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## About

This project demonstrates an innovative approach to comic book creation by combining:
- Traditional storytelling and script writing
- AI-assisted artwork generation
- Agent-based workflow automation

The goal is to explore new creative possibilities at the intersection of traditional comic book artistry and modern AI tools.
