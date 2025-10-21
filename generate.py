#!/usr/bin/env python3
"""
Simple comic generator for Everpeak Citadel.
Reads script, generates panels, assembles pages, creates CBZ.
"""

import os
import re
import json
import zipfile
from pathlib import Path
from openai import OpenAI
from PIL import Image, ImageDraw
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration
SCRIPT_FILE = "Comic Book Script - Everpeak.md"
OUTPUT_DIR = Path("output")
PANELS_DIR = OUTPUT_DIR / "panels"
PAGES_DIR = OUTPUT_DIR / "pages"
CBZ_FILE = OUTPUT_DIR / "everpeak-citadel.cbz"

# Layout settings
PAGE_WIDTH = 1600
PAGE_HEIGHT = 2400
GUTTER = 20
BORDER = 3

# Image generation settings
PANEL_WIDTH = 1024
PANEL_HEIGHT = 1024


def setup_directories():
    """Create output directory structure."""
    PANELS_DIR.mkdir(parents=True, exist_ok=True)
    PAGES_DIR.mkdir(parents=True, exist_ok=True)
    print(f"✓ Created output directories")


def parse_script():
    """
    Parse the comic script and extract panels.
    Returns: list of pages, each containing panels with descriptions and dialogue.
    """
    with open(SCRIPT_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract character descriptions (for prompting)
    char_section = re.search(
        r'## CHARACTER VISUAL DESCRIPTIONS(.*?)^## ',
        content,
        re.MULTILINE | re.DOTALL
    )
    character_descriptions = char_section.group(1) if char_section else ""

    # Find the narrative section
    narrative = re.search(
        r'## COMIC BOOK NARRATIVE.*',
        content,
        re.DOTALL
    )

    if not narrative:
        raise ValueError("Could not find narrative section in script")

    narrative_text = narrative.group(0)

    # Extract pages
    pages = []
    page_pattern = r'### Page (\d+):(.*?)(?=### Page \d+:|### Chapter|\Z)'

    for page_match in re.finditer(page_pattern, narrative_text, re.DOTALL):
        page_num = int(page_match.group(1))
        page_content = page_match.group(2)

        # Extract panels
        panels = []
        panel_pattern = r'\*\*Panel (\d+):\*\*(.*?)(?=\*\*Panel \d+:|\*\*Page notes:|\Z)'

        for panel_match in re.finditer(panel_pattern, page_content, re.DOTALL):
            panel_num = int(panel_match.group(1))
            panel_content = panel_match.group(2).strip()

            # Extract visual description and dialogue
            lines = panel_content.split('\n')
            visual = []
            dialogue = []

            in_dialogue = False
            for line in lines:
                line = line.strip()
                if line.startswith('- **Dialogue:**') or in_dialogue:
                    in_dialogue = True
                    if line and not line.startswith('- **'):
                        dialogue.append(line.lstrip('- '))
                elif line.startswith('-') and not in_dialogue:
                    visual.append(line.lstrip('- ').strip())

            panels.append({
                'panel_num': panel_num,
                'visual': ' '.join(visual),
                'dialogue': ' '.join(dialogue),
                'full_text': panel_content
            })

        if panels:
            pages.append({
                'page_num': page_num,
                'panels': panels
            })

    print(f"✓ Parsed script: {len(pages)} pages, {sum(len(p['panels']) for p in pages)} panels")
    return pages, character_descriptions


def create_panel_prompt(panel, character_descriptions):
    """Create an image generation prompt for a panel."""

    # Build prompt
    prompt = f"""Professional comic book panel illustration.

{panel['visual']}

Style: Bold ink line art, vibrant colors, dynamic composition, sequential art style, graphic novel quality, clean white background between panels."""

    # Limit to reasonable length for API
    if len(prompt) > 4000:
        prompt = prompt[:4000]

    return prompt


def generate_panel_image(panel, page_num, character_descriptions, client):
    """Generate a single panel image using OpenAI."""

    filename = PANELS_DIR / f"page-{page_num:03d}-panel-{panel['panel_num']}.png"

    # Skip if already exists
    if filename.exists():
        print(f"  ↪ Panel {panel['panel_num']} already exists, skipping")
        return filename

    prompt = create_panel_prompt(panel, character_descriptions)

    print(f"  → Generating panel {panel['panel_num']}...")
    print(f"     Prompt: {prompt[:100]}...")

    try:
        response = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024",
            quality="high",
            n=1,
            response_format="b64_json"
        )

        # Decode base64 image data
        import base64
        image_data = base64.b64decode(response.data[0].b64_json)

        # Save image
        with open(filename, 'wb') as f:
            f.write(image_data)

        print(f"  ✓ Saved {filename.name}")
        time.sleep(1)  # Rate limiting

        return filename

    except Exception as e:
        print(f"  ✗ Error generating panel: {e}")
        # Create placeholder
        img = Image.new('RGB', (PANEL_WIDTH, PANEL_HEIGHT), 'lightgray')
        draw = ImageDraw.Draw(img)
        draw.text((50, 50), f"Error: {str(e)[:100]}", fill='black')
        img.save(filename)
        return filename


def assemble_page(page, pages_data):
    """Assemble panels into a page."""

    page_num = page['page_num']
    panels = page['panels']
    num_panels = len(panels)

    print(f"\n→ Assembling page {page_num} ({num_panels} panels)...")

    # Create blank page
    page_img = Image.new('RGB', (PAGE_WIDTH, PAGE_HEIGHT), 'white')

    # Simple layout logic
    if num_panels <= 3:
        # Vertical stack
        panel_height = (PAGE_HEIGHT - (num_panels + 1) * GUTTER) // num_panels

        for i, panel in enumerate(panels):
            panel_file = PANELS_DIR / f"page-{page_num:03d}-panel-{panel['panel_num']}.png"
            if panel_file.exists():
                img = Image.open(panel_file)
                # Resize to fit
                img = img.resize((PAGE_WIDTH - 2 * GUTTER, panel_height), Image.Resampling.LANCZOS)

                y = GUTTER + i * (panel_height + GUTTER)
                page_img.paste(img, (GUTTER, y))

    elif num_panels <= 6:
        # 2x3 grid
        cols = 2
        rows = (num_panels + 1) // 2
        panel_width = (PAGE_WIDTH - (cols + 1) * GUTTER) // cols
        panel_height = (PAGE_HEIGHT - (rows + 1) * GUTTER) // rows

        for i, panel in enumerate(panels):
            panel_file = PANELS_DIR / f"page-{page_num:03d}-panel-{panel['panel_num']}.png"
            if panel_file.exists():
                img = Image.open(panel_file)
                img = img.resize((panel_width, panel_height), Image.Resampling.LANCZOS)

                col = i % cols
                row = i // cols
                x = GUTTER + col * (panel_width + GUTTER)
                y = GUTTER + row * (panel_height + GUTTER)
                page_img.paste(img, (x, y))

    else:
        # 3-column grid
        cols = 3
        rows = (num_panels + 2) // 3
        panel_width = (PAGE_WIDTH - (cols + 1) * GUTTER) // cols
        panel_height = (PAGE_HEIGHT - (rows + 1) * GUTTER) // rows

        for i, panel in enumerate(panels):
            panel_file = PANELS_DIR / f"page-{page_num:03d}-panel-{panel['panel_num']}.png"
            if panel_file.exists():
                img = Image.open(panel_file)
                img = img.resize((panel_width, panel_height), Image.Resampling.LANCZOS)

                col = i % cols
                row = i // cols
                x = GUTTER + col * (panel_width + GUTTER)
                y = GUTTER + row * (panel_height + GUTTER)
                page_img.paste(img, (x, y))

    # Save page
    output_file = PAGES_DIR / f"page-{page_num:03d}.png"
    page_img.save(output_file)
    print(f"✓ Saved {output_file.name}")

    return output_file


def create_cbz(pages_data):
    """Create CBZ file from assembled pages."""

    print("\n→ Creating CBZ archive...")

    # ComicInfo.xml metadata
    comic_info = """<?xml version="1.0"?>
<ComicInfo xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
  <Title>Everpeak Citadel: Echoes of the Dawn's Crown</Title>
  <Series>Everpeak Citadel</Series>
  <Number>1</Number>
  <Summary>A D&D adventure in the frozen peaks of Everpeak Citadel.</Summary>
  <Publisher>AI-Generated</Publisher>
  <Genre>Fantasy</Genre>
  <PageCount>{}</PageCount>
  <LanguageISO>en</LanguageISO>
</ComicInfo>""".format(len(pages_data))

    with zipfile.ZipFile(CBZ_FILE, 'w', zipfile.ZIP_DEFLATED) as cbz:
        # Add ComicInfo.xml
        cbz.writestr('ComicInfo.xml', comic_info)

        # Add pages in order
        for page in sorted(pages_data, key=lambda p: p['page_num']):
            page_file = PAGES_DIR / f"page-{page['page_num']:03d}.png"
            if page_file.exists():
                # CBZ readers expect sequential numbering
                cbz.write(page_file, f"{page['page_num']:03d}.png")

    print(f"✓ Created {CBZ_FILE}")
    print(f"\n🎉 Comic complete! Open {CBZ_FILE} in any CBZ reader.")


def main():
    """Main generation workflow."""

    print("=" * 60)
    print("EVERPEAK CITADEL COMIC GENERATOR")
    print("=" * 60)

    # Check for API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("\n✗ Error: OPENAI_API_KEY environment variable not set")
        print("  Set it with: export OPENAI_API_KEY='your-key-here'")
        return

    client = OpenAI(api_key=api_key)

    # Setup
    setup_directories()

    # Parse script
    pages, character_descriptions = parse_script()

    # TEST MODE: Only generate page 1
    pages = [p for p in pages if p['page_num'] == 1]
    print(f"\n⚠️  TEST MODE: Only generating page {pages[0]['page_num']}")

    # Generate panels for each page
    print("\n" + "=" * 60)
    print("GENERATING PANELS")
    print("=" * 60)

    for page in pages:
        print(f"\n📄 Page {page['page_num']} ({len(page['panels'])} panels)")

        for panel in page['panels']:
            generate_panel_image(panel, page['page_num'], character_descriptions, client)

    # Assemble pages
    print("\n" + "=" * 60)
    print("ASSEMBLING PAGES")
    print("=" * 60)

    for page in pages:
        assemble_page(page, pages)

    # Create CBZ
    print("\n" + "=" * 60)
    print("PACKAGING CBZ")
    print("=" * 60)

    create_cbz(pages)


if __name__ == "__main__":
    main()
