# Simplified Comic Layout System

## Overview

The Everpeak Citadel comic now uses a radically simplified layout system with only **2 layouts** and a **single image format**.

**Design Principles:**
- ✅ **Consistency:** All panels are 1024x1536 (portrait, 2:3 aspect ratio)
- ✅ **Simplicity:** Only 2 layouts (splash or 2x2 grid)
- ✅ **Predictability:** Every page follows the same rules
- ✅ **E-reader Friendly:** Fixed 1600x2400 pages work everywhere
- ✅ **Easy to Maintain:** ~186 lines of layout code (vs 550+ before)

## The Two Layouts

### 1. Splash Page (1 Panel)
**Use for:** Impact moments, full-page reveals, dramatic scenes

**Layout:**
- Single panel centered on page
- Maintains 2:3 aspect ratio
- Scaled to fit 1600x2400 page
- Textured background fills empty space

```
┌───────────────────────┐
│                       │
│   ┌─────────────┐     │
│   │             │     │
│   │             │     │
│   │   Panel 1   │     │
│   │  (Splash)   │     │
│   │             │     │
│   │             │     │
│   └─────────────┘     │
│                       │
└───────────────────────┘
```

### 2. Standard Page (2x2 Grid, up to 4 Panels)
**Use for:** Normal storytelling, dialogue, action sequences

**Layout:**
- 4 panels in 2 columns × 2 rows
- Each panel maintains 2:3 aspect ratio
- 20px gutters between panels
- 3px black borders
- Drop shadows for depth

```
┌───────────────────────┐
│  ┌────────┬────────┐  │
│  │ Panel1 │ Panel2 │  │
│  │        │        │  │
│  ├────────┼────────┤  │
│  │ Panel3 │ Panel4 │  │
│  │        │        │  │
│  └────────┴────────┘  │
└───────────────────────┘
```

**If fewer than 4 panels:** Empty slots remain as background

## Image Specifications

**All Panels:**
- **Size:** 1024 × 1536 pixels
- **Aspect Ratio:** 2:3 (portrait)
- **Format:** PNG
- **Quality:** High (OpenAI gpt-image-1)

**Pages:**
- **Size:** 1600 × 2400 pixels
- **Background:** Warm cream (RGB 245, 240, 235) with subtle texture
- **Format:** PNG

## Comic Structure

**Current:** 45 pages, 171 panels total

**Breakdown:**
- Splash pages (1 panel): 3 pages (pages 43-45, final panels)
- Standard pages (4 panels): 42 pages (pages 1-42)

**Sequential Packing:**
- All panels packed sequentially (not preserving original page boundaries)
- Strict rule: Only 1 or 4 panels per page
- 42 pages × 4 panels + 3 pages × 1 panel = 171 panels total

**From Original:**
- Was: 26 pages (various layouts, mixed panel counts)
- First restructure: 56 pages (simplified but allowed 2-3 panels)
- Now: 45 pages (sequential packing, strictly 1 or 4 panels)

## Workflow

### 1. Generation
```bash
# Generate all panels at 1024x1536
python generate.py <page_num> --concurrent 20

# Each panel gets 3 variants for review
# All variants are 1024x1536 portrait
```

### 2. Review & Select
```bash
# Review variants and select favorites
python review.py <page_num>

# UI shows 3 variants per panel
# Click to select, "Preview Final Page" to see assembled layout
```

### 3. Assembly
```bash
# Assemble selected panels into final pages
python assemble.py <page_nums>

# Creates 1600x2400 PNG pages
# Uses splash or 2x2 grid layout automatically
```

### 4. CBZ Creation
```bash
# Package all pages into CBZ comic archive
python assemble.py  # Assembles all and creates CBZ
```

## Code Architecture

**layout_engine.py** (186 lines)
- `layout_splash()` - Single panel layout
- `layout_2x2_grid()` - 4-panel grid layout
- `create_textured_background()` - Cream background with noise
- `draw_panel_with_shadow()` - Panel rendering with shadows

**No Complex Logic:**
- No aspect ratio detection
- No pattern matching
- No spread pages
- No custom layouts
- No mixed aspect ratios

**Simple Decision:**
```python
if num_panels == 1:
    layout_splash(page_img, panel_images)
else:
    layout_2x2_grid(page_img, panel_images)
```

## Page JSON Format

```json
{
  "page_num": 3,
  "title": "The Ceremony Begins (Part 1)",
  "panel_count": 4,
  "is_spread": false,
  "panels": [
    {
      "panel_num": 1,
      "visual": "Scene description",
      "dialogue": "Character dialogue",
      "characters": {...},
      "npcs": {...},
      "aspect_ratio": "tall",
      "size": "1024x1536",
      "prompt": "Complete prompt for image generation"
    },
    // ... 3 more panels
  ]
}
```

**Key Fields:**
- `aspect_ratio`: Always "tall"
- `size`: Always "1024x1536"
- `is_spread`: Always false
- `panel_count`: 1 or 2-4 (never more than 4)

## Benefits of Simplified System

| Aspect | Before | After |
|--------|--------|-------|
| **Layouts** | 7 complex templates | 2 simple layouts |
| **Aspect Ratios** | 3 (square, wide, tall) | 1 (portrait) |
| **Page Dimensions** | Variable (spreads) | Fixed (1600x2400) |
| **Code** | 550+ lines | 186 lines |
| **Mental Model** | Complex pattern detection | Simple: 1 or 4 panels |
| **Predictability** | Varies by content | Always consistent |
| **Maintenance** | Difficult | Easy |

## Migration from Old System

**Backups Created:**
- `pages_backup/` - Original 26 pages with mixed aspects
- `pages_backup_sequential/` - Previous 56 pages (allowed 2-3 panels)
- Git commit `4bc5753` - Complex layout system (26 pages)
- Git commit `c362629` - First simplification (56 pages, 2-4 panels allowed)
- Git commit `884adcc` - Sequential packing (45 pages, strictly 1 or 4 panels)

**Restructuring Scripts:**
- `restructure_pages.py` - First simplification (tried to preserve pages)
- `sequential_pack.py` - Sequential packing (ignores page boundaries)

**Sequential Packing Process:**
1. Loads all 171 panels from all pages in order
2. Packs into groups of 4 panels (standard 2x2 grid pages)
3. If fewer than 4 panels remain, creates splash pages (1 panel each)
4. Result: 42 standard pages + 3 splash pages = 45 pages total

**To Revert (if needed):**
```bash
git revert 884adcc  # Undo sequential packing → back to 56 pages
git revert c362629  # Undo first simplification → back to 26 pages
# Or restore from pages_backup/ or pages_backup_sequential/
```

## Limitations & Trade-offs

**What We Gave Up:**
- Variable panel sizes (wide establishing shots, tall dramatic reveals)
- Spread pages (two-page panoramic scenes)
- Custom layouts for special pages
- Exact panel counts from original script

**What We Gained:**
- Predictable, consistent output
- Much simpler code
- Easier to maintain and debug
- Works great on all e-readers
- Faster to generate (no complex layouts)
- Easier to review (all same aspect)

## Next Steps

1. **Delete old panels:** `rm -rf output/panels/*`
2. **Generate new panels:** All at 1024x1536
3. **Review and select:** Using simplified review UI
4. **Assemble:** Pages will use splash or 2x2 grid
5. **Package:** Create final CBZ

## Questions?

- **Why 2:3 aspect ratio?** Portrait works better for reading flow and fits more detail
- **Why max 4 panels?** 2x2 grid is balanced and readable on all devices
- **What about wide scenes?** Use splash page or sequence across 2 pages
- **Can we add layouts?** Yes, but defeats the simplification goal

## File Reference

- `layout_engine.py` - Simplified layout system
- `restructure_pages.py` - Page restructuring tool
- `assemble.py` - Uses simplified layouts
- `review.py` - Preview uses simplified layouts
- `generate.py` - Generates 1024x1536 panels
- `pages/` - 56 restructured page JSONs
- `pages_backup/` - Original 26 pages
