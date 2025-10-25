# Everpeak Citadel Comic

A simple AI-generated comic book based on a D&D campaign.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set your OpenAI API key
cp .env.example .env
# Edit .env and add your API key

# Generate the comic
python generate.py

# Output will be in output/everpeak-citadel.cbz
```

## What This Does

1. Reads `Comic Book Script - Everpeak.md`
2. Generates one panel image per panel description
3. Assembles panels into comic book pages
4. Packages everything into a CBZ file (standard comic format)

## Requirements

- Python 3.8+
- OpenAI API key (get at https://platform.openai.com/api-keys)
- API credits for full comic (144 panels with gpt-image-1)

## Output

- `output/panels/` - Individual panel images
- `output/pages/` - Assembled page images
- `output/everpeak-citadel.cbz` - Final comic (open with any CBZ reader)

## Format

12 pages, 144 panels total. CBZ format is a standard ZIP archive containing images and metadata.
