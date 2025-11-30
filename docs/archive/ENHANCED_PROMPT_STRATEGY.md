# Enhanced Prompt Strategy & Layout Guide

## Overview

This document outlines the comprehensive prompt enhancement strategy applied to pages 0, 2, 4, 5, and 7. This approach fixes the critical issues identified:
1. **Missing location descriptions** leading to generic settings
2. **Minimal character descriptions** causing inconsistent appearances
3. **Missing fantasy context** resulting in modern clothing instead of medieval fantasy
4. **Inadequate layouts** for panel annotations (Large, Wide)

## Prompt Structure Template

All enhanced prompts follow this structure (~1500-2500 characters):

```
Professional comic book panel illustration.

Location: [Detailed setting description - architecture, environment, atmosphere, time of day, weather, specific features]

Characters:
- [Name] ([position/role in panel]): [Full description: race, age, height, build, scales/skin/hair color, eyes, facial features, expression, clothing details, equipment, body language, current action]

NPCs/Crowd:
- [Type/Role]: [Full description with emphasis on medieval fantasy attire, races, activities]

Creatures (if applicable):
- [Name/Type]: [Full description: size, form, appearance, materials, magical effects, behavior]

Scene: [Detailed composition description - what's happening, positioning, background elements, foreground/midground/background, lighting, atmosphere, camera angle, dramatic elements, story moment]

Dialogue: [Character name (emotion/delivery)]: "[Dialogue text]"

Sound Effects: [If applicable]

Include speech bubbles with dialogue text clearly readable.

Style: Bold ink line art, vibrant colors, dynamic composition, sequential art style, graphic novel quality. [Additional style notes for specific panel]
```

## Key Improvements

### 1. Location Descriptions

**Before (260 chars):**
```
Scene: Verdant essence taking visible form - angry nature elemental Crowd gasping
```

**After (includes in 2000+ char prompt):**
```
Location: Grand Courtyard of Everpeak Citadel during Yule Tree ceremony. Winter festival setting.

Scene: Dramatic reveal as the corrupted Verdant Essence suddenly takes visible physical form, erupting from the ground near the tree. The Verdant Mephit materializes in explosion of green energy, thorny vines, and nature debris. Crowd visible in background and sides, all gasping and recoiling in shock and fear...
```

### 2. Character Descriptions

**Before:**
```
Characters:
- Malrik: Height: 5'6" Build: Slim, agile Skin: Dark gray-blue drow
```

**After:**
```
Characters:
- Malrik (whispering conspiratorially): Drow rogue, 5'6", slim agile acrobat's build, dark gray-blue drow skin, white short hair, pale lavender eyes gleaming with mischief and scheming, sharp cheekbones, roguish conspiratorial smile, dark leather armor, colorful street performer's vest, leaning UP toward Prismor's head (height difference), one hand cupped near mouth whispering, other hand gesturing persuasively, body language of someone pitching a scheme
```

### 3. Fantasy Crowd Context

**Critical Addition:**
```
Crowd/NPCs: Medieval fantasy crowd recoiling in shock and fear - high elves in elegant robes gasping, stout dwarves in heavy furs and chainmail backing away, humans in colorful medieval festival clothing with winter cloaks showing frightened expressions, halflings in practical traveling clothes pointing in alarm, dragonborn in ceremonial fantasy garb with shocked faces. All medieval fantasy attire, NO modern business clothing.
```

The explicit "NO modern business clothing" prevents the modern suit problem.

### 4. Creature Descriptions

**Example - Verdant Mephit:**
```
Creatures:
- Verdant Mephit (center, dramatic reveal): Small angry nature elemental, 2-3 feet tall, body composed of living vines and thorny brambles twisted into vaguely humanoid shape, glowing green pinpoint eyes filled with rage, twisted roots and thorns forming limbs, leaf-like wings rustling aggressively, wild garden scent aura, trail of thorny vines and moss, garden debris (leaves, petals, thorns) swirling around it in angry vortex, corrupted nature essence manifestation, wrong and unnatural
```

## Panel Annotation to Aspect Ratio Mapping

### Updated Sizing Strategy

| Annotation | Aspect Ratio | Size | Use Case |
|---|---|---|---|
| None | square | 1024x1024 | Standard panels |
| Large | tall | 1024x1536 | Establishing shots, dramatic reveals |
| Wide | wide | 1536x1024 | Landscape views, action sequences |
| Splash | tall | 1024x1536 | Full page art |

**Critical Fix:** "Large" panels changed from 1024x1024 (square) to 1024x1536 (portrait) to give them appropriate visual weight.

## Layout Strategies by Panel Count

Based on assemble.py:

| Panel Count | Layout Strategy | Description |
|---|---|---|
| 1 | full_page | Single panel fills page |
| 2 | vertical_half | Two panels stacked vertically |
| 3 | vertical_third | Three panels stacked vertically |
| 4 | 2x2_grid | Perfect 2x2 grid |
| 5 | 2_over_3 | 2 wider panels top, 3 smaller bottom |
| 6 | 2x3_grid | Standard 2x3 grid |
| 7 | 3_over_4 | 3 panels top row, 4 panels bottom row |
| 8 | 2x4_grid | 2 columns, 4 rows |
| 9 | 3x3_grid | Perfect 3x3 grid |

**Note on Mixed Aspect Ratios:** Current 2x3 grid doesn't accommodate mixed aspect ratios well (e.g., panel 6 being wide while others are square). Future improvement: implement flexible layouts that respect panel annotations.

## Character Description Components

Each character description should include:

1. **Race & Class:** "Brass dragonborn monk"
2. **Age Appearance:** "early 20s appearance"
3. **Height & Build:** "Just under 7 feet tall, lean athletic build with wiry monk strength"
4. **Skin/Scales/Fur:** "Warm brass/copper-bronze scales with metallic sheen"
5. **Eyes:** "Ember-glow orange eyes, bright and expressive"
6. **Hair (if applicable):** "White hair kept short and practical"
7. **Facial Features:** "Reptilian face with kind open expression, shorter snout"
8. **Expression & Emotion:** "kind reptilian expression now serious"
9. **Clothing:** "Simple monastery robes in earth tones (browns, tans) with chalk dust marks"
10. **Equipment:** "Bare clawed feet. Prayer beads around wrist"
11. **Body Language:** "gesturing as he speaks about courier runes"
12. **Current Action:** "standing near his sled, turning as halfling approaches"

## Location Description Components

Each location description should include:

1. **Primary Location Name:** "Everpeak Citadel sled race starting area"
2. **Physical Environment:** "High on mountain slope with dramatic view DOWN the mountain"
3. **Architecture:** "Starting line area with multiple wooden sleds lined up"
4. **Atmosphere:** "Winter festival setting with decorative flags and banners"
5. **Background Elements:** "Snow-covered mountain landscape. White stone citadel visible in background/above"
6. **Time & Weather:** "Clear winter day with dramatic mountain vistas"
7. **Genre Context:** "Medieval fantasy winter sports setting"

## Examples by Page Type

### Cover (Page 0)
- **Type:** Single panel, portrait (1024x1536)
- **Purpose:** Epic group shot of all 5 heroes
- **Prompt Length:** ~2300 characters
- **Key Elements:** All characters with full descriptions, dramatic citadel background, heroic composition, title treatment

### Establishing Page (Page 2 Panel 1)
- **Annotation:** "Large"
- **Size:** 1024x1536 (portrait)
- **Purpose:** Set scene for ceremony
- **Prompt Length:** ~2400 characters
- **Key Elements:** All 5 heroes visible in crowd, Lunara as focal point, fantasy crowd, location established

### Action Panel (Page 5 Panel 5)
- **Type:** Standard square (1024x1024)
- **Purpose:** Prismor forging with magical resistance
- **Prompt Length:** ~2200 characters
- **Key Elements:** Dynamic action, magical effects (sparks flying wrong), creature manifestations, physical strain

### Character Interaction (Page 7 Panel 5)
- **Type:** Standard square (1024x1024)
- **Purpose:** Malrik and Prismor conversation
- **Prompt Length:** ~2000 characters
- **Key Elements:** Height difference comedy, contrasting personalities, body language, character dynamics

### Wide Cinematic (Page 5 Panel 7)
- **Annotation:** "Wide"
- **Size:** 1536x1024 (landscape)
- **Purpose:** Party gathering, ominous realization
- **Prompt Length:** ~2400 characters
- **Key Elements:** All 5 party members, unstable javelin focal point, dramatic lighting, mood

## NPCs vs Characters

**Characters:** Main party members (Val, Prismor, Apocalypse Winter, Lunara, Malrik) go in `characters` field

**NPCs:** Everyone else goes in `npcs` field:
- Named NPCs: Barth, Marge, Sorrel, etc.
- Generic NPCs: "Well-dressed gambler", "Halfling courier"
- Crowds: "Fantasy Crowd", "Race contestants"

**Creatures:** Monsters and elementals go in `creatures` field:
- Verdant Mephit
- Gear Mephit manifestations
- Blink Mephits (future)

## Fantasy Setting Enforcement

### Critical Instructions to Include

For any panel with crowds or background characters:

```
All medieval fantasy attire. NO modern clothing, NO business suits, NO ties.
```

### Fantasy Race Diversity

When describing crowds:
```
Medieval fantasy crowd - high elves in elegant robes, stout dwarves in heavy furs and chainmail, humans in colorful medieval festival clothing, halflings in practical traveling clothes, dragonborn in ceremonial fantasy garb
```

## Spread Pages

**Identification:** `"is_spread": true` and `"page_end": X` in JSON

**Examples:**
- Page 2-3: 6 panels
- Page 5-6: 7 panels

**Assembly Width:** 3200px (double normal 1600px)

**Panel Annotation Strategy:** First and last panels often Wide (1536x1024) to anchor the spread

## Generation Performance

With enhanced prompts and 20 concurrent requests:
- **Pages 0, 2, 4, 5, 7:** 24 panels × 3 variants = 72 images
- **Time:** 390.4 seconds (~6.5 minutes)
- **Average:** ~5.4 seconds per image
- **Parallelism:** Full panel-level - all panels start simultaneously

## Future Pages Enhancement Workflow

To enhance remaining pages (1, 3, 6, 8-40):

1. **Read original script** - extract panel annotations, dialogue, scene descriptions
2. **Read character descriptions** - match characters appearing in each panel
3. **Identify locations** - match scenes to major location descriptions
4. **Check for creatures** - identify any mephits or monsters
5. **Build comprehensive prompt** following template above
6. **Update JSON** with full character descriptions, npcs, creatures
7. **Verify aspect ratios** match annotations (Large → tall, Wide → wide)
8. **Test generate** one page to verify quality
9. **Batch generate** remaining pages with --concurrent 20

## Common Pitfalls to Avoid

1. **Empty character descriptions** - Always pull full details from script
2. **Modern clothing in crowds** - Always specify medieval fantasy attire explicitly
3. **Missing location context** - Generic "marketplace" vs "Everpeak Citadel festival marketplace with white stone architecture..."
4. **Wrong aspect ratios** - "Large" must be tall (1024x1536), not square
5. **Characters in wrong field** - NPCs like Marge, Barth, Sorrel go in `npcs`, not `characters`
6. **Minimal scene descriptions** - Need composition, lighting, mood, camera angle details
7. **Missing body language** - Character descriptions should include current action and emotion

## Results Achieved

**Pages Enhanced:** 0, 2, 4, 5, 7
**Panels Enhanced:** 24 panels
**Prompt Size:** 1500-2500 characters (vs original 260 characters)
**Key Fixes:**
- ✅ Fantasy crowds with explicit medieval attire
- ✅ Full character descriptions for consistency
- ✅ Complete location descriptions for setting
- ✅ Creature descriptions for mephits
- ✅ Correct aspect ratios for annotations
- ✅ Comprehensive scene composition details

**Remaining:** 20 pages, ~147 panels need same enhancement treatment

## Next Steps for User

When you wake up, you can:
1. Review the generated variants: `python review.py 0` (or 2, 4, 5, 7)
2. Select favorite variants for each panel
3. Assemble pages: `python assemble.py 0,2,4,5,7`
4. Review assembled pages
5. If satisfied with quality, apply same enhancement to remaining pages
6. Use this document as template for future page enhancements
