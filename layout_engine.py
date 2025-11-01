#!/usr/bin/env python3
"""
Professional comic book layout engine.
Handles mixed aspect ratio panels with proportional scaling and textured backgrounds.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
from typing import List, Dict, Tuple, Optional
import random


# Layout Configuration
PAGE_WIDTH = 1600
PAGE_HEIGHT = 2400  # Default, but can be variable
SPREAD_WIDTH = 3200
GUTTER = 20
PANEL_BORDER = 3
SHADOW_OFFSET = 4
SHADOW_BLUR = 6

# Layout options
USE_VARIABLE_HEIGHT = True  # Set to False for fixed 2400px height
ALLOW_FULL_WIDTH_WIDE = True  # Wide panels span full width when True

# Background Configuration
BACKGROUND_COLOR = (245, 240, 235)  # Warm off-white/cream
TEXTURE_INTENSITY = 0.15  # Subtle texture overlay


class LayoutBox:
    """Represents a positioned panel box with dimensions."""

    def __init__(self, x: int, y: int, width: int, height: int, panel_num: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.panel_num = panel_num

    def __repr__(self):
        return f"Panel {self.panel_num}: ({self.x}, {self.y}) {self.width}x{self.height}"


class LayoutTemplate:
    """Base class for layout templates."""

    def __init__(self, page_width: int, page_height: int):
        self.page_width = page_width
        self.page_height = page_height
        self.gutter = GUTTER

    def calculate_layout(self, panels: List[Dict]) -> List[LayoutBox]:
        """Calculate panel positions and sizes. Override in subclasses."""
        raise NotImplementedError


class AllSquareGridLayout(LayoutTemplate):
    """Standard grid layout for all-square panels."""

    def calculate_layout(self, panels: List[Dict]) -> List[LayoutBox]:
        """Calculate equal-sized grid layout."""
        num_panels = len(panels)

        # Determine grid dimensions
        if num_panels == 1:
            cols, rows = 1, 1
        elif num_panels == 2:
            cols, rows = 1, 2
        elif num_panels == 3:
            cols, rows = 1, 3
        elif num_panels == 4:
            cols, rows = 2, 2
        elif num_panels == 5:
            # Special 2-over-3 layout
            return self._layout_2_over_3(panels)
        elif num_panels == 6:
            cols, rows = 2, 3
        elif num_panels == 7:
            # Special 3-over-4 layout
            return self._layout_3_over_4(panels)
        elif num_panels == 8:
            cols, rows = 2, 4
        elif num_panels == 9:
            cols, rows = 3, 3
        else:
            # Fallback: 3-column grid
            cols = 3
            rows = (num_panels + 2) // 3

        # Calculate panel dimensions
        panel_width = (self.page_width - (cols + 1) * self.gutter) // cols
        panel_height = (self.page_height - (rows + 1) * self.gutter) // rows

        # Create layout boxes
        boxes = []
        for i, panel in enumerate(panels):
            col = i % cols
            row = i // cols
            x = self.gutter + col * (panel_width + self.gutter)
            y = self.gutter + row * (panel_height + self.gutter)
            boxes.append(LayoutBox(x, y, panel_width, panel_height, panel['panel_num']))

        return boxes

    def _layout_2_over_3(self, panels: List[Dict]) -> List[LayoutBox]:
        """2 wider panels on top, 3 smaller below."""
        top_panel_width = (self.page_width - 3 * self.gutter) // 2
        top_panel_height = (self.page_height - 3 * self.gutter) // 2

        bottom_panel_width = (self.page_width - 4 * self.gutter) // 3
        bottom_panel_height = (self.page_height - 3 * self.gutter) // 2

        boxes = []

        # Top 2 panels
        for i in range(min(2, len(panels))):
            x = self.gutter + i * (top_panel_width + self.gutter)
            y = self.gutter
            boxes.append(LayoutBox(x, y, top_panel_width, top_panel_height, panels[i]['panel_num']))

        # Bottom 3 panels
        for i in range(2, min(5, len(panels))):
            col = i - 2
            x = self.gutter + col * (bottom_panel_width + self.gutter)
            y = self.gutter + top_panel_height + self.gutter
            boxes.append(LayoutBox(x, y, bottom_panel_width, bottom_panel_height, panels[i]['panel_num']))

        return boxes

    def _layout_3_over_4(self, panels: List[Dict]) -> List[LayoutBox]:
        """3 panels on top, 4 on bottom."""
        top_panel_width = (self.page_width - 4 * self.gutter) // 3
        top_panel_height = (self.page_height - 3 * self.gutter) // 2

        bottom_panel_width = (self.page_width - 5 * self.gutter) // 4
        bottom_panel_height = (self.page_height - 3 * self.gutter) // 2

        boxes = []

        # Top 3 panels
        for i in range(min(3, len(panels))):
            x = self.gutter + i * (top_panel_width + self.gutter)
            y = self.gutter
            boxes.append(LayoutBox(x, y, top_panel_width, top_panel_height, panels[i]['panel_num']))

        # Bottom 4 panels
        for i in range(3, min(7, len(panels))):
            col = i - 3
            x = self.gutter + col * (bottom_panel_width + self.gutter)
            y = self.gutter + top_panel_height + self.gutter
            boxes.append(LayoutBox(x, y, bottom_panel_width, bottom_panel_height, panels[i]['panel_num']))

        return boxes


class WideTopLayout(LayoutTemplate):
    """Layout with full-width panel at top, grid below."""

    def calculate_layout(self, panels: List[Dict]) -> List[LayoutBox]:
        """Wide panel at top, remaining panels in grid."""
        boxes = []

        # First panel: full-width wide
        wide_height = int((self.page_width - 2 * self.gutter) / 1.5)  # Maintain 1.5:1 aspect
        boxes.append(LayoutBox(
            self.gutter,
            self.gutter,
            self.page_width - 2 * self.gutter,
            wide_height,
            panels[0]['panel_num']
        ))

        # Remaining panels in grid
        remaining_panels = panels[1:]
        remaining_height = self.page_height - wide_height - 3 * self.gutter

        if len(remaining_panels) <= 3:
            # Single column
            panel_height = (remaining_height - len(remaining_panels) * self.gutter) // len(remaining_panels)
            panel_width = self.page_width - 2 * self.gutter

            for i, panel in enumerate(remaining_panels):
                y = self.gutter + wide_height + self.gutter + i * (panel_height + self.gutter)
                boxes.append(LayoutBox(self.gutter, y, panel_width, panel_height, panel['panel_num']))
        else:
            # 2-column grid for remaining
            cols = 2
            rows = (len(remaining_panels) + 1) // 2
            panel_width = (self.page_width - 3 * self.gutter) // 2
            panel_height = (remaining_height - (rows + 1) * self.gutter) // rows

            for i, panel in enumerate(remaining_panels):
                col = i % cols
                row = i // cols
                x = self.gutter + col * (panel_width + self.gutter)
                y = self.gutter + wide_height + self.gutter + row * (panel_height + self.gutter)
                boxes.append(LayoutBox(x, y, panel_width, panel_height, panel['panel_num']))

        return boxes


class WideBottomLayout(LayoutTemplate):
    """Layout with grid on top, full-width panel at bottom."""

    def calculate_layout(self, panels: List[Dict]) -> List[LayoutBox]:
        """Grid panels on top, wide panel at bottom."""
        boxes = []

        # Calculate wide panel height (bottom)
        wide_height = int((self.page_width - 2 * self.gutter) / 1.5)

        # Space for grid panels
        grid_height = self.page_height - wide_height - 3 * self.gutter
        grid_panels = panels[:-1]  # All except last

        # Layout grid panels
        if len(grid_panels) <= 2:
            # Vertical stack
            panel_width = self.page_width - 2 * self.gutter
            panel_height = (grid_height - len(grid_panels) * self.gutter) // len(grid_panels)

            for i, panel in enumerate(grid_panels):
                y = self.gutter + i * (panel_height + self.gutter)
                boxes.append(LayoutBox(self.gutter, y, panel_width, panel_height, panel['panel_num']))
        else:
            # 2-column grid
            cols = 2
            rows = (len(grid_panels) + 1) // 2
            panel_width = (self.page_width - 3 * self.gutter) // 2
            panel_height = (grid_height - (rows + 1) * self.gutter) // rows

            for i, panel in enumerate(grid_panels):
                col = i % cols
                row = i // cols
                x = self.gutter + col * (panel_width + self.gutter)
                y = self.gutter + row * (panel_height + self.gutter)
                boxes.append(LayoutBox(x, y, panel_width, panel_height, panel['panel_num']))

        # Last panel: full-width at bottom
        boxes.append(LayoutBox(
            self.gutter,
            self.page_height - wide_height - self.gutter,
            self.page_width - 2 * self.gutter,
            wide_height,
            panels[-1]['panel_num']
        ))

        return boxes


class BookendWideLayout(LayoutTemplate):
    """Layout with wide panels at top and bottom, grid in middle."""

    def calculate_layout(self, panels: List[Dict]) -> List[LayoutBox]:
        """Wide top, grid middle, wide bottom."""
        boxes = []

        # Top and bottom wide panels
        wide_height = int((self.page_width - 2 * self.gutter) / 1.5)

        # Top wide panel
        boxes.append(LayoutBox(
            self.gutter,
            self.gutter,
            self.page_width - 2 * self.gutter,
            wide_height,
            panels[0]['panel_num']
        ))

        # Middle grid panels
        middle_panels = panels[1:-1]
        middle_height = self.page_height - 2 * wide_height - 4 * self.gutter

        if len(middle_panels) <= 2:
            # Single column
            panel_width = self.page_width - 2 * self.gutter
            panel_height = (middle_height - len(middle_panels) * self.gutter) // len(middle_panels)

            for i, panel in enumerate(middle_panels):
                y = self.gutter + wide_height + self.gutter + i * (panel_height + self.gutter)
                boxes.append(LayoutBox(self.gutter, y, panel_width, panel_height, panel['panel_num']))
        else:
            # 2-column grid
            cols = 2
            rows = (len(middle_panels) + 1) // 2
            panel_width = (self.page_width - 3 * self.gutter) // 2
            panel_height = (middle_height - (rows + 1) * self.gutter) // rows

            for i, panel in enumerate(middle_panels):
                col = i % cols
                row = i // cols
                x = self.gutter + col * (panel_width + self.gutter)
                y = self.gutter + wide_height + self.gutter + row * (panel_height + self.gutter)
                boxes.append(LayoutBox(x, y, panel_width, panel_height, panel['panel_num']))

        # Bottom wide panel
        boxes.append(LayoutBox(
            self.gutter,
            self.page_height - wide_height - self.gutter,
            self.page_width - 2 * self.gutter,
            wide_height,
            panels[-1]['panel_num']
        ))

        return boxes


class TallLeftLayout(LayoutTemplate):
    """Layout with tall panel on left, grid on right."""

    def calculate_layout(self, panels: List[Dict]) -> List[LayoutBox]:
        """Tall panel on left, grid panels on right."""
        boxes = []

        # Tall panel (left side) - proportional 1:1.5 aspect
        tall_width = int((self.page_height - 2 * self.gutter) / 1.5)

        # Left tall panel
        boxes.append(LayoutBox(
            self.gutter,
            self.gutter,
            tall_width,
            self.page_height - 2 * self.gutter,
            panels[0]['panel_num']
        ))

        # Right grid panels
        right_panels = panels[1:]
        right_width = self.page_width - tall_width - 3 * self.gutter

        if len(right_panels) <= 2:
            # Vertical stack on right
            panel_height = (self.page_height - (len(right_panels) + 1) * self.gutter) // len(right_panels)

            for i, panel in enumerate(right_panels):
                y = self.gutter + i * (panel_height + self.gutter)
                boxes.append(LayoutBox(
                    self.gutter + tall_width + self.gutter,
                    y,
                    right_width,
                    panel_height,
                    panel['panel_num']
                ))
        else:
            # 2-column grid on right
            cols = 2
            rows = (len(right_panels) + 1) // 2
            panel_width = (right_width - self.gutter) // 2
            panel_height = (self.page_height - (rows + 1) * self.gutter) // rows

            for i, panel in enumerate(right_panels):
                col = i % cols
                row = i // cols
                x = self.gutter + tall_width + self.gutter + col * (panel_width + self.gutter)
                y = self.gutter + row * (panel_height + self.gutter)
                boxes.append(LayoutBox(x, y, panel_width, panel_height, panel['panel_num']))

        return boxes


class TallLeftWideBottomLayout(LayoutTemplate):
    """Layout with tall panel on left, grid in middle, wide panel at bottom."""

    def calculate_layout(self, panels: List[Dict]) -> List[LayoutBox]:
        """Tall left, square grid middle-right, wide bottom with proper aspect ratios."""
        boxes = []

        # For spread pages, work with the available space more intelligently
        is_spread = self.page_width > self.page_height

        # Calculate available space
        available_height = self.page_height - 3 * self.gutter
        available_width = self.page_width - 2 * self.gutter

        # For wide panel (1.5:1 aspect ratio), determine appropriate size
        # Don't stretch to full width - maintain aspect ratio
        if is_spread:
            # Use ~60% of available width for wide panel
            wide_panel_width = int(available_width * 0.6)
            wide_height = int(wide_panel_width / 1.5)  # Maintain 1.5:1 aspect
        else:
            # Portrait page: use most of width
            wide_panel_width = int(available_width * 0.9)
            wide_height = int(wide_panel_width / 1.5)

        # Top section gets remaining height
        top_section_height = available_height - wide_height - self.gutter

        # Tall panel (1:1.5 aspect ratio)
        tall_height = top_section_height
        tall_width = int(tall_height / 1.5)  # Maintain 1:1.5 aspect

        # Place tall panel on left
        boxes.append(LayoutBox(
            self.gutter,
            self.gutter,
            tall_width,
            tall_height,
            panels[0]['panel_num']
        ))

        # Middle panels (grid on right side of top section)
        middle_panels = panels[1:-1]  # All except first and last
        right_width = available_width - tall_width - self.gutter

        if len(middle_panels) == 1:
            # Single panel on right - make it square
            panel_size = min(right_width, top_section_height)
            boxes.append(LayoutBox(
                self.gutter + tall_width + self.gutter,
                self.gutter,
                panel_size,
                panel_size,
                middle_panels[0]['panel_num']
            ))
        elif len(middle_panels) <= 4:
            # 2x2 grid on right - square panels
            cols = 2
            rows = (len(middle_panels) + 1) // 2
            panel_width = (right_width - self.gutter) // 2
            panel_height = (top_section_height - self.gutter * (rows + 1)) // rows

            # Make panels as square as possible
            panel_size = min(panel_width, panel_height)

            for i, panel in enumerate(middle_panels):
                col = i % cols
                row = i // cols
                x = self.gutter + tall_width + self.gutter + col * (panel_size + self.gutter)
                y = self.gutter + row * (panel_size + self.gutter)
                boxes.append(LayoutBox(x, y, panel_size, panel_size, panel['panel_num']))
        else:
            # 3-column grid for more panels
            cols = 3
            rows = (len(middle_panels) + 2) // 3
            panel_width = (right_width - 2 * self.gutter) // 3
            panel_height = (top_section_height - self.gutter * (rows + 1)) // rows
            panel_size = min(panel_width, panel_height)

            for i, panel in enumerate(middle_panels):
                col = i % cols
                row = i // cols
                x = self.gutter + tall_width + self.gutter + col * (panel_size + self.gutter)
                y = self.gutter + row * (panel_size + self.gutter)
                boxes.append(LayoutBox(x, y, panel_size, panel_size, panel['panel_num']))

        # Last panel: wide panel at bottom, centered (not stretched full width)
        wide_x = (self.page_width - wide_panel_width) // 2  # Center horizontally
        boxes.append(LayoutBox(
            wide_x,
            self.page_height - wide_height - self.gutter,
            wide_panel_width,
            wide_height,
            panels[-1]['panel_num']
        ))

        return boxes


class SplashLayout(LayoutTemplate):
    """Full-page single panel layout."""

    def calculate_layout(self, panels: List[Dict]) -> List[LayoutBox]:
        """Single panel fills entire page with gutters."""
        return [LayoutBox(
            self.gutter,
            self.gutter,
            self.page_width - 2 * self.gutter,
            self.page_height - 2 * self.gutter,
            panels[0]['panel_num']
        )]


def detect_layout_pattern(panels: List[Dict]) -> str:
    """
    Analyze panel aspect ratios and detect optimal layout pattern.

    Returns layout pattern name:
    - 'all_square': All panels are square
    - 'wide_top': First panel is wide, rest are square
    - 'wide_bottom': Last panel is wide, rest are square
    - 'bookend_wide': First and last panels are wide
    - 'tall_left': First panel is tall, rest are square
    - 'tall_left_wide_bottom': First tall, middle square, last wide
    - 'splash': Single panel (any aspect ratio)
    - 'mixed': Complex pattern requiring custom layout
    """
    if len(panels) == 1:
        return 'splash'

    aspects = [p.get('aspect_ratio', 'square') for p in panels]

    # Check for all square
    if all(a == 'square' for a in aspects):
        return 'all_square'

    # Check for tall left + wide bottom pattern
    if aspects[0] == 'tall' and aspects[-1] == 'wide':
        # Check if middle panels are all square
        if all(a == 'square' for a in aspects[1:-1]):
            return 'tall_left_wide_bottom'

    # Check for tall left pattern
    if aspects[0] == 'tall' and all(a == 'square' for a in aspects[1:]):
        return 'tall_left'

    # Check for wide patterns
    if aspects[0] == 'wide' and aspects[-1] == 'wide':
        # Check if middle are all square
        if all(a == 'square' for a in aspects[1:-1]):
            return 'bookend_wide'

    if aspects[0] == 'wide' and all(a == 'square' for a in aspects[1:]):
        return 'wide_top'

    if aspects[-1] == 'wide' and all(a == 'square' for a in aspects[:-1]):
        return 'wide_bottom'

    # Complex mixed pattern
    return 'mixed'


def select_layout_template(pattern: str, page_width: int, page_height: int) -> LayoutTemplate:
    """Select appropriate layout template based on detected pattern."""
    templates = {
        'all_square': AllSquareGridLayout,
        'wide_top': WideTopLayout,
        'wide_bottom': WideBottomLayout,
        'bookend_wide': BookendWideLayout,
        'tall_left': TallLeftLayout,
        'tall_left_wide_bottom': TallLeftWideBottomLayout,
        'splash': SplashLayout,
        'mixed': AllSquareGridLayout,  # Fallback to grid for complex patterns
    }

    template_class = templates.get(pattern, AllSquareGridLayout)
    return template_class(page_width, page_height)


def create_textured_background(width: int, height: int) -> Image.Image:
    """
    Create subtle textured background for professional comic appearance.
    """
    # Create base background
    bg = Image.new('RGB', (width, height), BACKGROUND_COLOR)

    # Generate subtle noise texture
    pixels = bg.load()
    for y in range(height):
        for x in range(width):
            # Add subtle random variation
            variation = int((random.random() - 0.5) * TEXTURE_INTENSITY * 255)
            r, g, b = BACKGROUND_COLOR
            pixels[x, y] = (
                max(0, min(255, r + variation)),
                max(0, min(255, g + variation)),
                max(0, min(255, b + variation))
            )

    # Very slight blur to smooth texture
    bg = bg.filter(ImageFilter.GaussianBlur(0.5))

    return bg


def draw_panel_with_shadow(page_img: Image.Image, panel_img: Image.Image, box: LayoutBox):
    """
    Draw a panel with drop shadow onto the page.
    """
    # Create shadow layer
    shadow = Image.new('RGBA', (box.width + SHADOW_OFFSET * 2, box.height + SHADOW_OFFSET * 2), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rectangle(
        [SHADOW_OFFSET, SHADOW_OFFSET, box.width + SHADOW_OFFSET, box.height + SHADOW_OFFSET],
        fill=(0, 0, 0, 100)
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(SHADOW_BLUR))

    # Paste shadow
    page_img.paste(shadow, (box.x - SHADOW_OFFSET, box.y - SHADOW_OFFSET), shadow)

    # Resize panel to fit box (proportional scaling)
    panel_resized = panel_img.resize((box.width, box.height), Image.Resampling.LANCZOS)

    # Draw border
    bordered_panel = Image.new('RGB', (box.width, box.height), 'black')
    bordered_panel.paste(panel_resized, (PANEL_BORDER, PANEL_BORDER))

    # Paste panel
    page_img.paste(bordered_panel, (box.x, box.y))


def assemble_page_with_layout(panels_data: List[Dict], panel_images: List[Image.Image],
                                page_width: int = PAGE_WIDTH, page_height: int = PAGE_HEIGHT,
                                custom_layout: Optional[str] = None) -> Image.Image:
    """
    Assemble a comic page using professional layout engine.

    Args:
        panels_data: List of panel dictionaries with aspect_ratio info
        panel_images: List of loaded panel images (same order as panels_data)
        page_width: Page width in pixels
        page_height: Page height in pixels
        custom_layout: Optional custom layout override pattern

    Returns:
        Assembled page image
    """
    # Create textured background
    page_img = create_textured_background(page_width, page_height)

    # Detect layout pattern
    pattern = custom_layout if custom_layout else detect_layout_pattern(panels_data)

    # Select and apply layout template
    template = select_layout_template(pattern, page_width, page_height)
    layout_boxes = template.calculate_layout(panels_data)

    # Draw each panel with shadow
    for box, panel_img in zip(layout_boxes, panel_images):
        draw_panel_with_shadow(page_img, panel_img, box)

    return page_img
