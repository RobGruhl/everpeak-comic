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
from io import BytesIO

# Try to import Gemini (optional for refinement)
try:
    from google import genai
    from google.genai import types
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

# Load environment variables from .env file
load_dotenv()

# Configuration
PAGES_JSON_DIR = Path("pages")  # Structured page JSON files
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


def load_page_data(page_num):
    """Load page data from JSON file."""
    page_file = PAGES_JSON_DIR / f"page-{page_num:03d}.json"

    if not page_file.exists():
        raise FileNotFoundError(f"Page file not found: {page_file}")

    with open(page_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def list_available_pages():
    """List all available page JSON files."""
    if not PAGES_JSON_DIR.exists():
        return []

    page_files = sorted(PAGES_JSON_DIR.glob("page-*.json"))
    pages = []

    for page_file in page_files:
        with open(page_file, 'r', encoding='utf-8') as f:
            page_data = json.load(f)
            pages.append(page_data)

    return pages


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
    # Match both single pages (Page 1:) and page ranges (Page 2-3:)
    page_pattern = r'### Page (\d+)(?:-\d+)?:(.*?)(?=### Page \d+(?:-\d+)?:|### Chapter|\Z)'

    for page_match in re.finditer(page_pattern, narrative_text, re.DOTALL):
        page_num = int(page_match.group(1))  # Use first page number in range
        page_content = page_match.group(2)

        # Extract panels (handle optional annotations like "(Wide)", "(Large)", etc.)
        panels = []
        panel_pattern = r'\*\*Panel (\d+)(?:\s*\([^)]+\))?:\*\*(.*?)(?=\*\*Panel \d+(?:\s*\([^)]+\))?:|\*\*Page notes:|\Z)'

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

    # Extract condensed character info (just main party for brevity)
    # Note: Full character_descriptions is ~11K chars, too long for prompt
    # This extracts just key visual identifiers for main characters
    condensed_chars = """
Characters reference:
- Val: Brass dragonborn monk, 7ft tall, brass/copper scales, orange eyes, monastery robes
- Prismor: Blue crystal dragonborn paladin, crystalline blue scales, plate armor, greatsword
- Pocky: Human wizard, dark hair, blue robes with silver trim, carries books and scrolls
- Lunara: High elf druid, long silver-blonde hair, earth-tone robes, nature-themed
- Malrik: Drow rogue, dark skin, white hair, performer's outfit with cards and coins
"""

    # Build prompt
    prompt = f"""Professional comic book panel illustration.

{condensed_chars}

Panel: {panel['visual']}"""

    # Add dialogue if present
    if panel['dialogue']:
        prompt += f"\n\nDialogue: {panel['dialogue']}"
        prompt += "\n\nInclude speech bubbles with the dialogue text clearly readable."

    prompt += "\n\nStyle: Bold ink line art, vibrant colors, dynamic composition, sequential art style, graphic novel quality."

    # Limit to reasonable length for API
    if len(prompt) > 4000:
        prompt = prompt[:4000]

    return prompt


def generate_panel_image(panel, page_num, client):
    """Generate a single panel image using OpenAI, optionally refine with Gemini."""

    # OpenAI filename
    openai_filename = PANELS_DIR / f"page-{page_num:03d}-panel-{panel['panel_num']}-openai.png"
    # Final filename (will be symlinked or copied)
    final_filename = PANELS_DIR / f"page-{page_num:03d}-panel-{panel['panel_num']}.png"

    # Get prompt from panel data (pre-built in JSON)
    prompt = panel.get('prompt', '')

    if not prompt:
        print(f"  ✗ Error: No prompt found for panel {panel['panel_num']}")
        return None

    # Skip if already exists
    if openai_filename.exists():
        print(f"  ↪ Panel {panel['panel_num']} (OpenAI) already exists, skipping generation")

        # Refine with Gemini for panels 1-5
        if panel['panel_num'] <= 5 and GEMINI_AVAILABLE:
            gemini_file = refine_panel_with_gemini(openai_filename, prompt, panel['panel_num'])

        return final_filename

    print(f"  → Generating panel {panel['panel_num']} with OpenAI...")
    print(f"     Prompt: {prompt[:100]}...")

    try:
        response = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024",
            quality="high",
            n=1
        )

        # Decode base64 image data
        import base64
        image_base64 = response.data[0].b64_json
        image_bytes = base64.b64decode(image_base64)

        # Save OpenAI image
        with open(openai_filename, 'wb') as f:
            f.write(image_bytes)

        print(f"  ✓ Saved OpenAI version: {openai_filename.name}")

        # Copy to final filename (for assembly to use)
        with open(final_filename, 'wb') as f:
            f.write(image_bytes)

        time.sleep(1)  # Rate limiting

        # Refine with Gemini for panels 1-5
        if panel['panel_num'] <= 5 and GEMINI_AVAILABLE:
            gemini_file = refine_panel_with_gemini(openai_filename, prompt, panel['panel_num'])
            if gemini_file:
                # Copy Gemini version to final filename for assembly
                import shutil
                shutil.copy(gemini_file, final_filename)
                print(f"  → Using Gemini version for final assembly")

        return final_filename

    except Exception as e:
        print(f"  ✗ Error generating panel: {e}")
        # Create placeholder
        img = Image.new('RGB', (PANEL_WIDTH, PANEL_HEIGHT), 'lightgray')
        draw = ImageDraw.Draw(img)
        draw.text((50, 50), f"Error: {str(e)[:100]}", fill='black')
        img.save(openai_filename)
        img.save(final_filename)
        return final_filename


def refine_panel_with_gemini(openai_filename, original_prompt, panel_num):
    """Refine an OpenAI-generated panel using Gemini."""

    if not GEMINI_AVAILABLE:
        print(f"  ⚠ Gemini not available, skipping refinement")
        return None

    # Determine aspect ratio description
    img = Image.open(openai_filename)
    width, height = img.size

    if width > height * 1.2:
        aspect = "wide horizontal"
    elif height > width * 1.2:
        aspect = "tall vertical"
    else:
        aspect = "square"

    gemini_filename = str(openai_filename).replace('.png', '-gemini.png')

    # Skip if already exists
    if Path(gemini_filename).exists():
        print(f"  ↪ Gemini refinement already exists, skipping")
        return gemini_filename

    print(f"  → Refining panel {panel_num} with Gemini...")

    try:
        client = genai.Client()

        # Load image data
        with open(openai_filename, 'rb') as f:
            image_data = f.read()

        # Create refinement prompt
        # Extract dialogue from prompt
        dialogue_section = ""
        if "Dialogue:" in original_prompt:
            dialogue_start = original_prompt.find("Dialogue:")
            dialogue_end = original_prompt.find("\n\n", dialogue_start)
            if dialogue_end == -1:
                dialogue_end = original_prompt.find("\nInclude", dialogue_start)
            if dialogue_end == -1:
                dialogue_end = len(original_prompt)
            dialogue_section = original_prompt[dialogue_start:dialogue_end].strip()

        refine_prompt = f"""The attached image is a comic book panel. The panel should depict: {original_prompt}

This should be a {aspect} image in comic book style.

CRITICAL: This panel MUST include speech bubbles with the following dialogue:
{dialogue_section}

Please refine this image to better match the description, ensuring:
- ALL dialogue text is preserved in clear, readable speech bubbles
- Speech bubbles are positioned near the speaking character
- Characters match their descriptions accurately
- Composition follows the scene description
- Art style is consistent (bold ink line art, vibrant colors)

DO NOT remove or alter any dialogue text. The speech bubbles are essential to the comic."""

        # Send to Gemini
        response = client.models.generate_content(
            model="gemini-2.5-flash-image",
            contents=[
                types.Part(inline_data=types.Blob(data=image_data, mime_type="image/png")),
                types.Part(text=refine_prompt)
            ],
        )

        # Save refined image
        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                refined_image = Image.open(BytesIO(part.inline_data.data))
                refined_image.save(gemini_filename)
                print(f"  ✓ Saved Gemini refinement: {Path(gemini_filename).name}")
                return gemini_filename

        print(f"  ✗ No image data in Gemini response")
        return None

    except Exception as e:
        print(f"  ✗ Error refining with Gemini: {e}")
        return None


def assemble_page(page_data):
    """Assemble panels into a page."""

    page_num = page_data['page_num']
    panels = page_data['panels']
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

    # Load page data from JSON
    print("\n→ Loading page data from JSON files...")
    page_num = 1  # TEST MODE: Only generate page 1

    try:
        page_data = load_page_data(page_num)
        print(f"✓ Loaded page {page_num}: '{page_data['title']}' ({page_data['panel_count']} panels)")
    except FileNotFoundError as e:
        print(f"\n✗ Error: {e}")
        print(f"\n  Run parse_script.py first to generate page JSON files:")
        print(f"  python parse_script.py")
        return

    print(f"\n⚠️  TEST MODE: Only generating page {page_num}")

    # Generate panels for each page
    print("\n" + "=" * 60)
    print("GENERATING PANELS")
    print("=" * 60)

    print(f"\n📄 Page {page_data['page_num']} ({page_data['panel_count']} panels)")

    for panel in page_data['panels']:
        generate_panel_image(panel, page_data['page_num'], client)

    # Assemble pages
    print("\n" + "=" * 60)
    print("ASSEMBLING PAGES")
    print("=" * 60)

    assemble_page(page_data)

    # Create CBZ
    print("\n" + "=" * 60)
    print("PACKAGING CBZ")
    print("=" * 60)

    create_cbz([page_data])


if __name__ == "__main__":
    main()
