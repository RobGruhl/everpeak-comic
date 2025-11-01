# Professional Comic Book Layout System

## Overview

The Everpeak Citadel comic now uses a professional template-based layout engine that respects panel aspect ratios and creates visually appealing pages optimized for e-readers. The system automatically detects layout patterns and applies appropriate templates.

## Key Features

- **Proportional Scaling:** Wide panels (~1.5x wider), tall panels (~1.5x taller), square panels maintain original aspect ratios
- **Textured Backgrounds:** Subtle paper/canvas texture with warm cream color instead of stark white
- **Drop Shadows:** Panels have soft shadows for depth and professional appearance
- **Template-Based:** Automatic pattern detection with pre-designed layouts for common patterns
- **Custom Layouts:** Support for page-specific custom layout overrides via JSON
- **Consistent Preview:** Review UI preview matches final assembly exactly

## Architecture

### Core Files

**layout_engine.py** - Professional layout system
- `detect_layout_pattern()` - Analyzes panel aspect ratios
- Layout template classes (AllSquareGridLayout, WideTopLayout, etc.)
- `assemble_page_with_layout()` - Main assembly function
- Background texture and shadow rendering

**assemble.py** - Page assembly (updated to use layout_engine)
- Loads panel images
- Calls layout engine
- Supports `custom_layout` field from page JSON

**review.py** - Interactive review UI (updated to use layout_engine)
- Preview function uses same layout engine
- What you see in preview = what you get in final assembly

## Layout Patterns

The system automatically detects these patterns based on panel aspect ratios:

### Pattern 1: All Square (35% of pages)
**Detected when:** All panels are `aspect_ratio: "square"`

**Layout:** Standard grids
- 2 panels: vertical stack (1x2)
- 3 panels: vertical stack (1x3)
- 4 panels: 2x2 grid
- 5 panels: 2-over-3 layout (2 wider top, 3 smaller bottom)
- 6 panels: 2x3 grid
- 7 panels: 3-over-4 layout (3 top, 4 bottom)
- 8 panels: 2x4 grid
- 9 panels: 3x3 grid

**Example Pages:** 1, 4, 7, 10, 13, 16, 19, 38, 39

```
┌─────────────────────────────┐
│ [Textured Background]       │
│  ┌─────┬─────┬─────┐        │
│  │  1  │  2  │  3  │        │
│  ├─────┼─────┼─────┤        │
│  │  4  │  5  │  6  │        │
│  ├─────┼─────┼─────┤        │
│  │  7  │  8  │  9  │        │
│  └─────┴─────┴─────┘        │
└─────────────────────────────┘
```

### Pattern 2: Wide Top (12% of pages)
**Detected when:** First panel is wide, rest are square

**Layout:** Full-width panel at top, grid below
- Top panel spans full width at 1.5:1 aspect ratio
- Remaining panels in balanced grid (1 or 2 columns depending on count)

**Example Pages:** 5, 8, 17

```
┌─────────────────────────────┐
│ [Textured Background]       │
│  ┌─────────────────────┐    │
│  │    1 (wide top)     │    │
│  └─────────────────────┘    │
│  ┌─────┬─────┐              │
│  │  2  │  3  │              │
│  ├─────┼─────┤              │
│  │  4  │  5  │              │
│  └─────┴─────┘              │
└─────────────────────────────┘
```

### Pattern 3: Wide Bottom (31% of pages)
**Detected when:** Last panel is wide, rest are square

**Layout:** Grid on top, full-width panel at bottom
- Top panels in balanced grid
- Bottom panel spans full width for dramatic conclusion

**Example Pages:** 20, 40

```
┌─────────────────────────────┐
│ [Textured Background]       │
│  ┌─────┬─────┐              │
│  │  1  │  2  │              │
│  ├─────┼─────┤              │
│  │  3  │  4  │              │
│  └─────┴─────┘              │
│  ┌─────────────────────┐    │
│  │   5 (wide bottom)   │    │
│  └─────────────────────┘    │
└─────────────────────────────┘
```

### Pattern 4: Bookend Wide (dual wide panels)
**Detected when:** First and last panels are wide, middle are square

**Layout:** Wide top, grid middle, wide bottom
- Top panel: full-width establishing shot
- Middle panels: balanced grid
- Bottom panel: full-width conclusion

**Example Pages:** 5, 17, 24, 34

```
┌─────────────────────────────┐
│ [Textured Background]       │
│  ┌─────────────────────┐    │
│  │    1 (wide top)     │    │
│  └─────────────────────┘    │
│  ┌─────┬─────┐              │
│  │  2  │  3  │              │
│  ├─────┼─────┤              │
│  │  4  │  5  │              │
│  └─────┴─────┘              │
│  ┌─────────────────────┐    │
│  │  6 (wide bottom)    │    │
│  └─────────────────────┘    │
└─────────────────────────────┘
```

### Pattern 5: Tall Left (8% of pages)
**Detected when:** First panel is tall, rest are square

**Layout:** Tall panel on left side, grid on right
- Left panel: full-height tall panel (1:1.5 aspect)
- Right panels: grid layout in remaining space

**Example Pages:** 2, 11

```
┌─────────────────────────────┐
│ [Textured Background]       │
│  ┌────┬─────┬─────┐         │
│  │    │  2  │  3  │         │
│  │ 1  ├─────┼─────┤         │
│  │tall│  4  │  5  │         │
│  │    ├─────┼─────┤         │
│  │    │  6  │  7  │         │
│  └────┴─────┴─────┘         │
└─────────────────────────────┘
```

### Pattern 6: Splash (full-page)
**Detected when:** Single panel (any aspect ratio)

**Layout:** Panel fills entire page with gutters
- Perfect for cover pages, full-page reveals, dramatic moments

**Example Pages:** 0 (cover), 23

```
┌─────────────────────────────┐
│ [Textured Background]       │
│  ┌─────────────────────┐    │
│  │                     │    │
│  │                     │    │
│  │     1 (splash)      │    │
│  │                     │    │
│  │                     │    │
│  └─────────────────────┘    │
└─────────────────────────────┘
```

### Pattern 7: Mixed (complex patterns)
**Detected when:** Aspect ratios don't match common patterns

**Layout:** Fallback to square grid with slight distortion
- **Recommendation:** Add `custom_layout` field to JSON for these pages

**Requires Custom Layout:** Pages with mid-page wide/tall panels

## Custom Layout Overrides

For complex pages that don't fit standard patterns, add a `custom_layout` field to the page JSON:

```json
{
  "page_num": 24,
  "panel_count": 9,
  "custom_layout": "bookend_wide",
  "panels": [...]
}
```

Available custom layout values:
- `"all_square"` - Force square grid
- `"wide_top"` - Force wide top layout
- `"wide_bottom"` - Force wide bottom layout
- `"bookend_wide"` - Force dual wide layout
- `"tall_left"` - Force tall left layout
- `"splash"` - Force full-page splash

## Design Specifications

### Page Dimensions
- **Standard Page:** 1600x2400 pixels
- **Spread Page:** 3200x2400 pixels (double-wide)

### Visual Elements
- **Background Color:** RGB(245, 240, 235) - Warm cream/off-white
- **Texture Intensity:** 15% random variation for subtle paper texture
- **Gutter:** 20px between panels and page edges
- **Panel Border:** 3px black border around each panel
- **Drop Shadow:** 4px offset, 6px blur, 40% opacity

### Aspect Ratio Proportions
- **Square:** 1:1 (1024x1024)
- **Wide:** 1.5:1 (1536x1024)
- **Tall:** 1:1.5 (1024x1536)

Panels maintain these relative proportions in layouts. Wide panels get ~1.5x the width of square panels. Tall panels get ~1.5x the height.

## Spread Pages

Pages with `"is_spread": true` and `"page_end": X` are two-page spreads:

- **Width:** 3200px (double standard width)
- **Layout:** Same templates apply but with more horizontal space
- **Examples:** Pages 2-3, 5-6, 11-12, 14-15, etc.

Spread pages often have more panels (6-9) and benefit from the wider canvas for dramatic layouts.

## Usage

### Assembling Pages

```bash
# Assemble single page
python assemble.py 2

# Assemble multiple pages
python assemble.py 1,2,3

# Assemble range
python assemble.py 1-5

# Assemble all pages
python assemble.py

# Skip CBZ creation
python assemble.py 2 --no-cbz

# Cleanup variants after assembly
python assemble.py 2 --cleanup-variants
```

### Previewing in Review UI

```bash
# Launch review UI for a page
python review.py 2
```

Click "Preview Final Page" button to see assembled layout before final export.

## How It Works

### Assembly Pipeline

1. **Load page JSON** - Read panel metadata including aspect ratios
2. **Check panel selection** - Ensure all panels have chosen variants
3. **Load panel images** - Open PNG files from output/panels/
4. **Detect pattern** - Analyze aspect ratios to determine layout pattern
5. **Select template** - Choose appropriate layout template class
6. **Calculate layout** - Template computes box positions and sizes
7. **Create background** - Generate textured background image
8. **Draw panels** - Place each panel with shadow and border
9. **Save page** - Write final PNG to output/pages/

### Pattern Detection Logic

```python
aspects = [panel.get('aspect_ratio', 'square') for panel in panels]

if all(a == 'square' for a in aspects):
    return 'all_square'
elif aspects[0] == 'tall' and all(a == 'square' for a in aspects[1:]):
    return 'tall_left'
elif aspects[0] == 'wide' and aspects[-1] == 'wide':
    return 'bookend_wide'
elif aspects[0] == 'wide':
    return 'wide_top'
elif aspects[-1] == 'wide':
    return 'wide_bottom'
else:
    return 'mixed'
```

## Common Layout Issues and Solutions

### Issue: Panels look squished or stretched

**Cause:** Panel aspect ratio in JSON doesn't match actual generated image size

**Solution:** Verify `aspect_ratio` and `size` fields in page JSON match:
- `"aspect_ratio": "square", "size": "1024x1024"`
- `"aspect_ratio": "wide", "size": "1536x1024"`
- `"aspect_ratio": "tall", "size": "1024x1536"`

### Issue: Mid-page wide panel doesn't span full width

**Cause:** Wide panels only span full width if they're first or last

**Solution:** Add custom layout override if you want mid-page full-width spanning

### Issue: Pattern detection chooses wrong template

**Cause:** Complex aspect ratio pattern doesn't match predefined templates

**Solution:** Add `"custom_layout": "pattern_name"` to page JSON to force specific template

### Issue: Preview doesn't match final assembly

**Cause:** Old review.py using different layout logic

**Solution:** Ensure you're running updated review.py that imports layout_engine

## Performance

- **Background generation:** ~50ms per page (one-time, includes texture)
- **Panel placement:** ~10ms per panel (resize, shadow, border)
- **Total assembly:** ~200-400ms per page depending on panel count
- **Preview generation:** Same as assembly (uses identical code)

## Future Enhancements

Potential improvements to the layout system:

1. **Advanced Templates:**
   - L-shaped layouts (tall panel left + grid right with wide bottom)
   - T-shaped layouts (wide top + vertical columns below)
   - Diagonal/dynamic panel arrangements

2. **Smart Spacing:**
   - Variable gutter sizes based on panel importance
   - Tighter spacing for sequential action panels
   - Wider spacing for scene changes

3. **Background Variations:**
   - Multiple texture styles (paper, canvas, parchment)
   - Per-page background customization
   - Color themes (warm, cool, monochrome)

4. **Panel Effects:**
   - Borderless panels for immersive moments
   - Bleeding panels (extend to page edge)
   - Overlapping panels for dynamic action

5. **AI-Assisted Layout:**
   - Analyze panel content to suggest optimal layouts
   - Detect character positions for better flow
   - Recommend panel sizes based on story beats

## References

- **Comic Book Layout Principles:** Panel flow, reader eye movement, visual hierarchy
- **E-Reader Optimization:** High-resolution panels, touch-friendly spacing, zoom compatibility
- **Professional Comics:** Analysis of major publisher layout strategies

## Questions or Issues?

For layout questions or to report issues:
- Check this guide first
- Review generated pages in output/pages/
- Compare with panel JSON in pages/
- Verify aspect_ratio fields match generated image sizes
- Try custom_layout override for complex pages
