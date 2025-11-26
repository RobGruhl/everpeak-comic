#!/usr/bin/env python3
"""
Comprehensive JSON fixer for all 45 pages.
Adds location descriptions, fantasy style directives, and enhances scene context.
"""

import json
from pathlib import Path

# Location descriptions from the script
LOCATIONS = {
    "citadel_exterior": """Location: Everpeak Citadel - massive mountain fortress carved from white stone with multiple crystalline towers reaching skyward. Built atop converging ley lines (faint glowing lines visible in mountain). Snow-capped peaks surrounding. Ancient high elven architecture mixed with newer additions. Magical lights and lanterns visible. Grand courtyards, terrace gardens on impossible ledges, winding paths and staircases carved into mountain. Festival decorations - ribbons, lanterns, banners. Smoke from chimneys and forges. Winter setting with snow.""",

    "marketplace": """Location: Everpeak Citadel Festival Marketplace - bustling open plaza with merchant stalls, vendor booths selling spiced pastries and hot cider. Colorful festival ribbons and banners overhead. White stone architecture. Winter setting with snow on ground. Medieval fantasy market atmosphere - no modern items. Mix of fantasy races (elves, dwarves, dragonborn, halflings, humans) shopping and selling. Warm braziers, magical lanterns providing light. Street performers entertaining crowds.""",

    "grand_courtyard": """Location: Grand Courtyard of Everpeak Citadel - massive open plaza carved from white stone, surrounded by towering crystalline spires. Ancient high elven architecture with elegant columns and arches. Winter setting with snow and festival decorations (banners, magical lanterns, ribbons). Snow-capped mountain peaks visible in background. Clear winter sky. Center prepared for ceremonies with circular ritual space. Medieval fantasy architecture.""",

    "forge_fair": """Location: Everpeak Citadel Forge Fair area - large open courtyard/plaza converted into smithing demonstration area. Winter festival setting with decorative banners and festival stalls. Forge setups prominent - working forges with glowing hot coals (orange-red heat), anvils, smithing tools displayed, metalwork samples. Smoke rising from forges. Snow on ground but area warmed by forge heat. White stone citadel architecture visible in background. Medieval fantasy setting.""",

    "sled_race_course": """Location: Everpeak Citadel sled race starting area - high on mountain slope with dramatic view down mountainside showing winding sled race course carved into snowy slopes. Starting line with multiple wooden sleds. Winter festival setting with decorative flags and banners marking course. Snow-covered mountain landscape. White stone citadel visible in background/above. Clear winter day with dramatic mountain vistas. Medieval fantasy winter sports setting.""",

    "balcony_cafe": """Location: Balcony Garden Café - impossible sunny terrace high in snow-covered mountains. Lush greenery everywhere - flowering vines, potted exotic plants, herbs growing. Magical warmth despite winter outside. Wooden tables and chairs with nature carvings. Stone balcony railing overlooks snow-covered citadel below. Sunlight streaming through leaves creating dappled shadows. High fantasy garden oasis. NO modern items. Medieval fantasy aesthetic.""",

    "courier_tunnels": """Location: Courier Tunnels - rough-hewn stone passages carved through mountain rock. Narrow winding maze-like tunnels with cramped passages. Chalk runes and magical symbols covering walls in white and colored chalk (red, blue, green, yellow) showing different magical routes. Some runes glowing faintly with cold blue magical energy, others flickering showing corruption. Smudged and tampered runes visible in places - deliberate sabotage. Dim magical lighting creating mysterious atmosphere. Occasional spatial distortions visible. Medieval fantasy dungeon with corrupted displacement magic.""",

    "grand_library": """Location: The Grand Library - soaring ceilings with endless shelves of ancient tomes and scrolls. Tall arched windows filtering light onto reading tables. Floating magical lights providing illumination. Wooden ladders on rails to reach high shelves. Dust motes in air. Scholar's paradise with books floor to ceiling. Ancient manuscripts, star-charts, arcane diagrams visible. Quiet, reverent atmosphere. High elven architecture - elegant carved wood and stone. Medieval fantasy grand library.""",

    "observatory": """Location: The Observatory - small domed chamber at citadel's peak. Glass ceiling showing night sky and stars. Brass orrery at center with moving spheres representing celestial bodies. Star-charts on walls. Telescopes and astronomical instruments. Cold blue magical light from runes. Ancient elven construction with precision clockwork mechanisms. Sense of cosmic significance. Medieval fantasy astronomical chamber.""",

    "elven_sanctum": """Location: The Elven Sanctum - hidden cavern deep beneath citadel. Massive central chamber with the Orrery at center - enormous magical device with rotating crystal spheres, glowing runes, clicking gears. Ancient high elven architecture - carved pillars, vaulted ceiling with constellation maps. Five alcoves housing True Lenses for elemental essences. Magical energy crackling through air. Sense of ancient power and sacrifice. Ruins of century-old battle visible. Medieval high fantasy sanctum.""",
}

# Generic fantasy dungeon for combat scenes
COMBAT_LOCATION = """Location: Everpeak Citadel interior - stone corridors and chambers. Rough stone walls, vaulted ceilings, medieval fantasy architecture. Dim magical lighting (cold blue glow from runes). Battle-scarred from conflict. Medieval fantasy dungeon atmosphere."""

# Style suffix to add to all prompts
FANTASY_STYLE = "medieval fantasy setting, high fantasy atmosphere"

def get_location_for_page(page_num):
    """Determine location based on page number and story flow."""
    if page_num <= 2:
        return "marketplace"  # Character introductions
    elif page_num <= 4:
        return "grand_courtyard"  # Yule Tree ceremony
    elif page_num <= 6:
        return "forge_fair"  # Forge Fair
    elif page_num == 7:
        return "sled_race_course"  # Sled race
    elif page_num <= 8:
        return "sled_race_course"  # Race continues
    elif page_num == 9:
        return "grand_library"  # Library scene
    elif page_num <= 11:
        return "balcony_cafe"  # Balcony Garden
    elif page_num <= 24:
        return "courier_tunnels"  # Tunnel exploration and combat
    elif page_num <= 35:
        return "courier_tunnels"  # Continuing through tunnels
    elif page_num <= 42:
        return "elven_sanctum"  # Final battle location
    else:
        return "citadel_exterior"  # Aftermath

def enhance_prompt(prompt, page_num, panel_num):
    """Enhance a prompt with location and fantasy style."""

    # Skip if already has detailed location
    if "Location:" in prompt and len(prompt) > 500:
        # Just add style if missing
        if FANTASY_STYLE not in prompt.lower():
            prompt = prompt.replace("Style: Bold ink line art",
                                  f"Style: Bold ink line art, {FANTASY_STYLE},")
        return prompt

    # Get appropriate location
    location_key = get_location_for_page(page_num)
    location_desc = LOCATIONS.get(location_key, COMBAT_LOCATION)

    # Check if prompt already starts with "Professional comic book panel"
    if not prompt.startswith("Professional comic book panel"):
        prompt = "Professional comic book panel illustration.\n\n" + prompt

    # Insert location after the opening if not present
    lines = prompt.split('\n')
    new_lines = [lines[0]]  # Keep "Professional comic book panel illustration."

    # Add blank line and location if not already there
    if not any('Location:' in line for line in lines[:5]):
        new_lines.append("")
        new_lines.append(location_desc)
        new_lines.append("")

    # Add rest of original prompt
    new_lines.extend(lines[1:])

    # Rejoin
    prompt = '\n'.join(new_lines)

    # Add fantasy style to Style: line if missing
    if "Style:" in prompt and FANTASY_STYLE not in prompt.lower():
        prompt = prompt.replace(
            "Style: Bold ink line art, vibrant colors, dynamic composition, sequential art style, graphic novel quality.",
            f"Style: Bold ink line art, vibrant colors, dynamic composition, sequential art style, graphic novel quality, {FANTASY_STYLE}."
        )

    return prompt

def fix_page(page_num):
    """Fix a single page's JSON."""
    page_file = Path(f"pages/page-{page_num:03d}.json")
    if not page_file.exists():
        return False

    with open(page_file, 'r', encoding='utf-8') as f:
        page = json.load(f)

    modified = False
    for panel in page.get('panels', []):
        panel_num = panel.get('panel_num')
        old_prompt = panel.get('prompt', '')

        if old_prompt:
            new_prompt = enhance_prompt(old_prompt, page_num, panel_num)
            if new_prompt != old_prompt:
                panel['prompt'] = new_prompt
                modified = True

    if modified:
        with open(page_file, 'w', encoding='utf-8') as f:
            json.dump(page, f, indent=2, ensure_ascii=False)
        return True
    return False

def main():
    """Fix all pages 1-45."""
    print("="*70)
    print("COMPREHENSIVE JSON FIXER")
    print("="*70)
    print()
    print("Enhancing all pages with:")
    print("  - Location descriptions")
    print("  - Fantasy style directives")
    print("  - Scene context")
    print()
    print("="*70)
    print()

    fixed_count = 0
    for page_num in range(1, 46):
        if fix_page(page_num):
            print(f"✓ Fixed page {page_num}")
            fixed_count += 1
        else:
            print(f"  Skipped page {page_num} (already enhanced or not found)")

    print()
    print("="*70)
    print(f"COMPLETE: Fixed {fixed_count} pages")
    print("="*70)

if __name__ == "__main__":
    main()
