# Dynamic Character Description System

## Current Problem

Currently, character descriptions are duplicated in every panel's JSON:

```json
{
  "characters": {
    "Prismor": "Height: 7 feet tall, imposing presence Build: Muscular..."
  }
}
```

**Issues:**
- Massive duplication across 171 panels
- Inconsistencies when descriptions need updates
- Hard to maintain a single source of truth
- Difficult to fix character consistency issues globally

## Proposed Solution: Reference-Based System

### 1. Character Definition File

Create `characters.json` with canonical descriptions:

```json
{
  "Prismor": {
    "name": "Prismor",
    "race": "Blue crystal dragonborn",
    "class": "Paladin (Oath of the Ancients)",
    "age_appearance": "Middle-aged (40s-50s in dragonborn years)",
    "description": {
      "head_face": "Dragonborn reptilian head with noble, dignified features. Deep sapphire blue eyes that show wisdom and contemplation - EYES MUST BE VISIBLE. Defined snout and jaw with dragonborn anatomy. Capable of visible facial expressions. Head covered in crystalline blue scales that have gem-like translucent quality. Scales catch and refract light with internal prismatic effects. Maintains clear dragonborn facial structure - this is a person, not a crystal statue.",
      "body_build": "7 feet tall, imposing presence. Muscular, powerful warrior's physique.",
      "scales_skin": "Crystalline blue scales with hints of forest green throughout body. Gem-like quality to scales but clearly organic dragonborn anatomy. Scales have subtle light refraction but body maintains dragonborn form.",
      "armor_clothing": "Silver/dull steel plate mail base - realistic medieval fantasy metal armor. Heavy plate armor covering chest, shoulders, arms. Forest green vines, leaves, and Oath of the Ancients nature motifs appear to be GROWING ON the silver armor but are PART OF the armor itself. Vines have three-dimensional sculptural quality integrated into the metal. Silver/steel base metal visible between green vine ornamentation. Crystalline accents on armor. Professional craftsmanship.",
      "accessories": "Forest green cape or cloak (can vary by scene).",
      "personality_bearing": "Noble paladin bearing, protective stance, warrior presence."
    },
    "reference_image": "output/references/prismor-reference.png"
  },

  "Val": {
    "name": "Val (Valthirion Emberstride)",
    "race": "Brass dragonborn",
    "class": "Monk",
    "age_appearance": "Early 20s",
    "description": {
      "head_face": "Kind, open reptilian face with shorter snout. Ember-glow orange eyes, bright and expressive.",
      "body_build": "Just under 7 feet tall, lean athletic build with wiry monk strength.",
      "scales_skin": "Warm brass/copper-bronze scales with metallic sheen.",
      "armor_clothing": "Simple monastery robes in earth tones (browns, tans) with chalk dust marks. Bare clawed feet.",
      "accessories": "Prayer beads around wrist.",
      "personality_bearing": "Always in motion, expressive hand gestures, energetic courier demeanor."
    }
  }

  // ... all other characters
}
```

### 2. Location Definition File

Create `locations.json`:

```json
{
  "Festival Marketplace": {
    "name": "Festival Marketplace",
    "parent": "Everpeak Citadel",
    "description": "Bustling marketplace with wooden stalls and festival decorations. Winter setting with snow. Colorful ribbons and banners. Crowds of various fantasy races. Medieval fantasy architecture. Warm lighting from lanterns and magical lights.",
    "atmosphere": "Festive, busy, warm despite winter cold",
    "time_of_day": "varies"
  },

  "The Elven Sanctum": {
    "name": "The Elven Sanctum",
    "parent": "Deep beneath Everpeak Citadel",
    "description": "Hidden cavern deep beneath citadel. Massive central chamber with the Orrery at center - enormous magical device with rotating crystal spheres, suspended lenses, glowing runes, intricate clicking gears and metallic arms. Ancient high elven architecture with carved stone pillars, vaulted ceiling covered in constellation maps and celestial charts. Five alcoves housing the True Lenses for elemental essences. Magical energy crackling through air - emerald (nature), silver-blue (mechanistic), lavender (celestial), golden (harmony), shifting prisms (displacement). Sense of ancient power and sacrifice. Ruins and scars from century-old battle visible on walls and floor. Cathedral-like scale with reverent atmosphere. Medieval high fantasy sanctum with high elven precision engineering.",
    "atmosphere": "Ancient, powerful, sacred, mysterious",
    "lighting": "Magical glow from Orrery and essences"
  }

  // ... all other locations
}
```

### 3. Updated Page JSON Format

Panels reference characters and locations by name:

```json
{
  "page_num": 25,
  "panels": [
    {
      "panel_num": 3,
      "visual": "Prismor's sword striking barrier",
      "dialogue": "Prismor: \"It's deflecting everything!\"",
      "characters": ["Prismor"],
      "npcs": [],
      "creatures": [],
      "location": "The Elven Sanctum",
      "aspect_ratio": "tall",
      "size": "1024x1536"
    }
  ]
}
```

**Note:** No `prompt` field - it will be assembled dynamically.

### 4. Dynamic Prompt Assembly

Update `generate.py` to assemble prompts at generation time:

```python
def load_character_descriptions():
    """Load canonical character descriptions."""
    with open('characters.json', 'r') as f:
        return json.load(f)

def load_location_descriptions():
    """Load canonical location descriptions."""
    with open('locations.json', 'r') as f:
        return json.load(f)

def build_character_prompt_section(character_name, characters_db, context="default"):
    """
    Build character description for prompt.

    Args:
        character_name: Name of character
        characters_db: Character database loaded from characters.json
        context: Scene context (e.g., "action", "dialogue", "resting")

    Returns:
        Formatted character description string
    """
    char = characters_db.get(character_name)
    if not char:
        return f"- {character_name}: [CHARACTER NOT FOUND IN DATABASE]"

    desc = char['description']

    # Build full description
    parts = [
        f"- {char['name']} ({char['race']} {char['class']}, {char['age_appearance']})",
        f"  HEAD/FACE: {desc['head_face']}",
        f"  BUILD: {desc['body_build']}",
        f"  APPEARANCE: {desc['scales_skin']}",
        f"  CLOTHING/ARMOR: {desc['armor_clothing']}",
    ]

    if desc.get('accessories'):
        parts.append(f"  ACCESSORIES: {desc['accessories']}")

    if desc.get('personality_bearing'):
        parts.append(f"  BEARING: {desc['personality_bearing']}")

    return "\n".join(parts)

def assemble_prompt(panel_data, characters_db, locations_db):
    """
    Dynamically assemble prompt from panel data and reference databases.

    Args:
        panel_data: Panel dict from page JSON
        characters_db: Loaded character descriptions
        locations_db: Loaded location descriptions

    Returns:
        Complete prompt string ready for image generation
    """
    parts = ["Professional comic book panel illustration.\n"]

    # Location
    location_name = panel_data.get('location')
    if location_name and location_name in locations_db:
        loc = locations_db[location_name]
        parts.append(f"Location: {loc['name']}")
        parts.append(f"{loc['description']}\n")

    # Characters
    if panel_data.get('characters'):
        parts.append("Characters:")
        for char_name in panel_data['characters']:
            char_desc = build_character_prompt_section(char_name, characters_db)
            parts.append(char_desc)
        parts.append("")

    # NPCs (similar to characters)
    if panel_data.get('npcs'):
        parts.append("NPCs:")
        for npc_name in panel_data['npcs']:
            npc_desc = build_character_prompt_section(npc_name, characters_db)
            parts.append(npc_desc)
        parts.append("")

    # Scene description
    parts.append(f"Scene: {panel_data['visual']}\n")

    # Dialogue
    if panel_data.get('dialogue'):
        parts.append(f"Dialogue: {panel_data['dialogue']}\n")
        parts.append("Include speech bubbles with dialogue text clearly readable.\n")

    # Style
    parts.append("Style: Bold ink line art, vibrant colors, dynamic composition, sequential art style, graphic novel quality, medieval fantasy setting, high fantasy atmosphere.")

    return "\n".join(parts)
```

### 5. Migration Strategy

**Phase 1: Create Reference Files**
1. Extract all unique character descriptions → `characters.json`
2. Extract all unique location descriptions → `locations.json`
3. Review and consolidate to single canonical version per entity

**Phase 2: Update Page JSONs**
1. Replace character description dicts with character name lists
2. Replace location description strings with location names
3. Remove pre-built `prompt` fields

**Phase 3: Update Generator**
1. Add prompt assembly logic to `generate.py`
2. Load character/location DBs at startup
3. Build prompts dynamically for each panel

**Phase 4: Validate**
1. Regenerate a test page (e.g., page 1)
2. Compare output to original
3. Verify consistency

## Benefits

1. **Single Source of Truth**: Update Prismor once, affects all 50+ panels instantly
2. **Consistency**: Guaranteed identical descriptions across all panels
3. **Maintainability**: Easy to fix character consistency issues
4. **Reference Images**: Can add `reference_image` field per character
5. **Flexibility**: Context-aware descriptions (action vs. resting poses)
6. **Version Control**: Track character evolution over time
7. **Reusability**: Character DB can be used for future comics/chapters

## Example Workflow

1. User: "Prismor's armor should be silver with green vines"
2. Update ONE entry in `characters.json`
3. Run: `python generate.py --regenerate page-25 page-27 page-45`
4. All three panels now use corrected description
5. Done - no manual JSON editing across dozens of files

## Advanced Features (Future)

- **Reference image support**: Pass character reference to image API
- **Contextual variations**: "Prismor (battle-damaged)" vs "Prismor (ceremonial)"
- **Pose libraries**: Common poses/expressions per character
- **Outfit changes**: Track costume changes across story arc
- **Relationship context**: "Prismor talking to Val" gets specific body language
