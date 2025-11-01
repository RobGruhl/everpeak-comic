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

**Current:** 56 pages, 171 panels total

**Breakdown:**
- Splash pages (1 panel): ~3 pages
- Standard pages (2-4 panels): ~53 pages

**From Original:**
- Was: 26 pages (various layouts)
- Now: 56 pages (simplified layouts)
- Many pages were split (e.g., 6-panel page → two 4-panel and 2-panel pages)

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
- Git commit `4bc5753` - Complex layout system
- Git commit `c362629` - Simplified system

**Restructuring:**
- Automated by `restructure_pages.py`
- Splits pages with >4 panels
- Updates all aspect ratios to "tall"
- Updates all sizes to "1024x1536"

**To Revert (if needed):**
```bash
git revert c362629  # Undo simplification
# Or restore from pages_backup/
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
