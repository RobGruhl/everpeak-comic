#!/usr/bin/env python3
"""
Interactive review interface for selecting comic panel variants.
Displays panel descriptions, dialogue, and variant images for selection.
"""

import os
import json
import sys
import shutil
import subprocess
from pathlib import Path
from flask import Flask, render_template_string, request, jsonify, redirect, url_for, send_file
from PIL import Image
import io

# Configuration
PAGES_JSON_DIR = Path("pages")
OUTPUT_DIR = Path("output")
PANELS_DIR = OUTPUT_DIR / "panels"
PAGES_DIR = OUTPUT_DIR / "pages"
SELECTIONS_FILE = OUTPUT_DIR / "selections.json"
VARIANTS_PER_PANEL = 3

# Layout settings (from assemble.py)
PAGE_WIDTH = 1600
PAGE_HEIGHT = 2400
GUTTER = 20

app = Flask(__name__)

# Store current page in global state
current_page_data = None
current_page_num = None


def load_page_data(page_num):
    """Load page data from JSON file."""
    page_file = PAGES_JSON_DIR / f"page-{page_num:03d}.json"

    if not page_file.exists():
        raise FileNotFoundError(f"Page file not found: {page_file}")

    with open(page_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_selections():
    """Load previous selections."""
    if SELECTIONS_FILE.exists():
        with open(SELECTIONS_FILE, 'r') as f:
            return json.load(f)
    return {}


def save_selections(selections):
    """Save selections to JSON file."""
    SELECTIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(SELECTIONS_FILE, 'w') as f:
        json.dump(selections, f, indent=2)


def get_panel_variants(page_num, panel_num):
    """Get all available variants for a panel."""
    variants = []
    variant_num = 1

    while True:
        variant_path = PANELS_DIR / f"page-{page_num:03d}-panel-{panel_num}-v{variant_num}.png"
        if not variant_path.exists():
            break
        variants.append({
            'num': variant_num,
            'path': variant_path,
            'url': f"/image/page-{page_num:03d}-panel-{panel_num}-v{variant_num}.png"
        })
        variant_num += 1

    return variants


def get_panel_selection(page_num, panel_num):
    """Check if a panel has been selected."""
    final_path = PANELS_DIR / f"page-{page_num:03d}-panel-{panel_num}.png"
    return final_path.exists()


@app.route('/image/<path:filename>')
def serve_image(filename):
    """Serve panel images."""
    from flask import send_file
    image_path = PANELS_DIR / filename
    if image_path.exists():
        return send_file(image_path, mimetype='image/png')
    return "Image not found", 404


@app.route('/')
def index():
    """Redirect to page review."""
    if current_page_num:
        return redirect(url_for('review_page', page_num=current_page_num))
    return "No page specified. Run with: python review.py <page_num>", 400


@app.route('/page/<int:page_num>')
def review_page(page_num):
    """Main review interface for a page."""
    try:
        page_data = load_page_data(page_num)
    except FileNotFoundError as e:
        return f"Error: {e}", 404

    selections = load_selections()

    # Prepare panel data with variants
    panels_with_variants = []
    for panel in page_data['panels']:
        panel_num = panel['panel_num']
        variants = get_panel_variants(page_num, panel_num)
        is_selected = get_panel_selection(page_num, panel_num)

        selected_variant = selections.get(f"{page_num}-{panel_num}")

        panels_with_variants.append({
            'panel': panel,
            'variants': variants,
            'is_selected': is_selected,
            'selected_variant': selected_variant,
            'total_variants': len(variants)
        })

    # HTML template
    template = """
<!DOCTYPE html>
<html>
<head>
    <title>Comic Panel Review - Page {{ page_num }}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #1a1a1a;
            color: #e0e0e0;
            padding: 20px;
            line-height: 1.6;
        }

        .header {
            background: #2a2a2a;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
            border-left: 4px solid #4a9eff;
        }

        .header h1 {
            font-size: 28px;
            margin-bottom: 8px;
            color: #fff;
        }

        .header .subtitle {
            color: #999;
            font-size: 14px;
        }

        .progress {
            background: #333;
            height: 8px;
            border-radius: 4px;
            overflow: hidden;
            margin-top: 12px;
        }

        .progress-bar {
            background: #4a9eff;
            height: 100%;
            transition: width 0.3s ease;
        }

        .panel-section {
            background: #2a2a2a;
            padding: 30px;
            border-radius: 8px;
            margin-bottom: 40px;
            border: 2px solid #333;
        }

        .panel-section.selected {
            border-color: #4a9eff;
            background: #2d3540;
        }

        .panel-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 1px solid #444;
        }

        .panel-title {
            font-size: 20px;
            font-weight: bold;
            color: #4a9eff;
        }

        .selected-badge {
            background: #4a9eff;
            color: white;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: bold;
        }

        .panel-info {
            background: #1f1f1f;
            padding: 15px;
            border-radius: 6px;
            margin-bottom: 20px;
            border-left: 3px solid #666;
        }

        .panel-info h3 {
            font-size: 14px;
            text-transform: uppercase;
            color: #999;
            margin-bottom: 8px;
            font-weight: 600;
        }

        .panel-info p {
            color: #ddd;
            font-size: 14px;
            line-height: 1.8;
        }

        .variants-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }

        .variant-card {
            background: #1f1f1f;
            border-radius: 8px;
            overflow: hidden;
            transition: transform 0.2s, box-shadow 0.2s;
            cursor: pointer;
            border: 2px solid #333;
        }

        .variant-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 24px rgba(74, 158, 255, 0.3);
            border-color: #4a9eff;
        }

        .variant-image {
            width: 100%;
            height: auto;
            display: block;
            background: #000;
        }

        .variant-footer {
            padding: 15px;
            text-align: center;
        }

        .variant-number {
            font-size: 12px;
            color: #999;
            margin-bottom: 8px;
        }

        .select-btn {
            background: #4a9eff;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.2s;
            width: 100%;
        }

        .select-btn:hover {
            background: #3a8ee5;
        }

        .select-btn:active {
            transform: scale(0.98);
        }

        .actions {
            display: flex;
            gap: 10px;
            justify-content: center;
            margin-top: 15px;
        }

        .generate-more-btn {
            background: #666;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.2s;
        }

        .generate-more-btn:hover {
            background: #777;
        }

        .preview-btn {
            background: #4a9eff;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.2s;
            margin-left: 10px;
        }

        .preview-btn:hover {
            background: #3a8ee5;
        }

        .preview-btn:disabled {
            background: #555;
            cursor: not-allowed;
        }

        .message {
            position: fixed;
            top: 20px;
            right: 20px;
            background: #4a9eff;
            color: white;
            padding: 15px 25px;
            border-radius: 6px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            z-index: 1000;
            animation: slideIn 0.3s ease;
        }

        @keyframes slideIn {
            from {
                transform: translateX(400px);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }

        .loading {
            text-align: center;
            padding: 40px;
            color: #999;
        }

        .spinner {
            border: 3px solid #333;
            border-top: 3px solid #4a9eff;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .loading-placeholder {
            background: #1f1f1f;
            border-radius: 8px;
            overflow: hidden;
            border: 2px solid #333;
            position: relative;
            aspect-ratio: 1;
        }

        .loading-placeholder::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            border: 3px solid #333;
            border-top: 3px solid #4a9eff;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
        }

        .loading-placeholder::after {
            content: 'Generating...';
            position: absolute;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            color: #999;
            font-size: 12px;
        }

        .preview-modal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.95);
            z-index: 2000;
            display: none;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .preview-modal.active {
            display: flex;
        }

        .preview-content {
            max-width: 90%;
            max-height: 90%;
            background: #2a2a2a;
            border-radius: 8px;
            padding: 20px;
            position: relative;
        }

        .preview-content img {
            max-width: 100%;
            max-height: calc(90vh - 100px);
            display: block;
            margin: 0 auto;
            border-radius: 4px;
        }

        .close-preview {
            position: absolute;
            top: 10px;
            right: 10px;
            background: #666;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            font-weight: 600;
            z-index: 10;
        }

        .close-preview:hover {
            background: #777;
        }

        .preview-actions {
            display: flex;
            gap: 10px;
            justify-content: center;
            flex-wrap: wrap;
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid #444;
        }

        .panel-regen-btn {
            background: #666;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }

        .panel-regen-btn:hover {
            background: #4a9eff;
            transform: translateY(-2px);
        }

        .panel-regen-btn:active {
            transform: translateY(0);
        }

        .back-to-review-btn {
            background: #4a9eff;
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.2s;
            margin-top: 10px;
        }

        .back-to-review-btn:hover {
            background: #3a8ee5;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Page {{ page_num }}: {{ page_data.title }}</h1>
        <div class="subtitle">{{ page_data.panel_count }} panels | Select your favorite variant for each panel</div>
        <div class="progress">
            <div class="progress-bar" style="width: {{ (selected_count / page_data.panel_count * 100) }}%"></div>
        </div>
        <div class="subtitle" style="margin-top: 8px;">
            Progress: {{ selected_count }}/{{ page_data.panel_count }} panels selected
            {% if selected_count >= page_data.panel_count %}
            <button class="preview-btn" onclick="previewPage({{ page_num }})">
                Preview Final Page
            </button>
            {% else %}
            <button class="preview-btn" disabled title="Select all panels to enable preview">
                Preview Final Page ({{ page_data.panel_count - selected_count }} remaining)
            </button>
            {% endif %}
        </div>
    </div>

    <div class="preview-modal" id="preview-modal">
        <div class="preview-content">
            <button class="close-preview" onclick="closePreview()">Close</button>
            <div id="preview-image-container">
                <div class="loading">
                    <div class="spinner"></div>
                    <p>Assembling page preview...</p>
                </div>
            </div>
            <div class="preview-actions" id="preview-actions" style="display: none;">
                {% for item in panels_with_variants %}
                <button class="panel-regen-btn" onclick="regeneratePanel({{ page_num }}, {{ item.panel.panel_num }})">
                    Regenerate Panel {{ item.panel.panel_num }}
                </button>
                {% endfor %}
                <div style="width: 100%; margin-top: 10px; text-align: center;">
                    <button class="back-to-review-btn" onclick="closePreview()">
                        Back to Panel Selection
                    </button>
                </div>
            </div>
        </div>
    </div>

    {% for item in panels_with_variants %}
    <div class="panel-section {% if item.is_selected %}selected{% endif %}" id="panel-{{ item.panel.panel_num }}">
        <div class="panel-header">
            <div class="panel-title">Panel {{ item.panel.panel_num }}</div>
            {% if item.is_selected %}
            <div class="selected-badge">✓ SELECTED (Variant {{ item.selected_variant }})</div>
            {% endif %}
        </div>

        <div class="panel-info">
            <h3>Scene Description</h3>
            <p>{{ item.panel.visual }}</p>
        </div>

        {% if item.panel.dialogue %}
        <div class="panel-info">
            <h3>Dialogue</h3>
            <p>{{ item.panel.dialogue }}</p>
        </div>
        {% endif %}

        {% if item.is_selected %}
        <div class="variants-grid">
            <div class="variant-card" style="border: 3px solid #4a9eff;">
                <img src="/image/page-{{ '%03d' % page_num }}-panel-{{ item.panel.panel_num }}.png" class="variant-image" alt="Selected">
                <div class="variant-footer">
                    <div class="variant-number">✓ Selected (Variant {{ item.selected_variant }})</div>
                </div>
            </div>
        </div>

        <div class="actions">
            <button class="generate-more-btn" onclick="generateMore({{ page_num }}, {{ item.panel.panel_num }})">
                Generate 3 More Variants to Re-select
            </button>
        </div>
        {% elif item.variants %}
        <div class="variants-grid">
            {% for variant in item.variants %}
            <div class="variant-card" onclick="selectVariant({{ page_num }}, {{ item.panel.panel_num }}, {{ variant.num }})">
                <img src="{{ variant.url }}" class="variant-image" alt="Variant {{ variant.num }}">
                <div class="variant-footer">
                    <div class="variant-number">Variant {{ variant.num }}</div>
                    <button class="select-btn">Select This</button>
                </div>
            </div>
            {% endfor %}
        </div>

        <div class="actions">
            <button class="generate-more-btn" onclick="generateMore({{ page_num }}, {{ item.panel.panel_num }})">
                Generate 3 More Variants
            </button>
        </div>
        {% else %}
        <div class="loading">
            <div class="spinner"></div>
            <p>No variants generated yet. Run: python generate.py {{ page_num }}</p>
        </div>
        {% endif %}
    </div>
    {% endfor %}

    <script>
        function selectVariant(pageNum, panelNum, variantNum) {
            fetch('/select/' + pageNum + '/' + panelNum + '/' + variantNum, {
                method: 'POST'
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showMessage('Panel ' + panelNum + ' - Variant ' + variantNum + ' selected!');
                    setTimeout(() => {
                        location.reload();
                    }, 800);
                } else {
                    alert('Error: ' + data.error);
                }
            })
            .catch(error => {
                alert('Error selecting variant: ' + error);
            });
        }

        function generateMore(pageNum, panelNum, skipConfirm = false) {
            if (!skipConfirm && !confirm('Generate 3 more variants for panel ' + panelNum + '? This will call the OpenAI API (~50 seconds per variant).')) {
                return;
            }

            // Add loading placeholders to the grid
            const panelSection = document.getElementById('panel-' + panelNum);
            const grid = panelSection.querySelector('.variants-grid');

            // Add 3 loading placeholders
            for (let i = 0; i < 3; i++) {
                const placeholder = document.createElement('div');
                placeholder.className = 'loading-placeholder';
                grid.appendChild(placeholder);
            }

            showMessage('Generating 3 more variants for panel ' + panelNum + '...');

            fetch('/more/' + pageNum + '/' + panelNum, {
                method: 'POST'
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showMessage('Generated ' + data.new_variants + ' new variants!');
                    setTimeout(() => {
                        location.reload();
                    }, 1500);
                } else {
                    alert('Error: ' + data.error);
                }
            })
            .catch(error => {
                alert('Error generating variants: ' + error);
                location.reload(); // Reload to remove placeholders
            });
        }

        function previewPage(pageNum) {
            const modal = document.getElementById('preview-modal');
            const container = document.getElementById('preview-image-container');
            const actions = document.getElementById('preview-actions');

            modal.classList.add('active');
            container.innerHTML = '<div class="loading"><div class="spinner"></div><p>Assembling page preview...</p></div>';
            actions.style.display = 'none';

            fetch('/preview/' + pageNum)
                .then(response => response.blob())
                .then(blob => {
                    const url = URL.createObjectURL(blob);
                    container.innerHTML = '<img src="' + url + '" alt="Page Preview">';
                    actions.style.display = 'flex';
                })
                .catch(error => {
                    container.innerHTML = '<p style="color: #ff6b6b;">Error generating preview: ' + error + '</p>';
                });
        }

        function regeneratePanel(pageNum, panelNum) {
            if (!confirm('Generate 3 more variants for Panel ' + panelNum + '?\\n\\n~50 seconds per variant (~2.5 minutes total)\\n\\nThis will close the preview and scroll to that panel.')) {
                return;
            }

            closePreview();

            // Scroll to the panel section
            setTimeout(() => {
                const panelSection = document.getElementById('panel-' + panelNum);
                if (panelSection) {
                    panelSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }, 300);

            // Trigger generation (skip the second confirm since we already confirmed)
            generateMore(pageNum, panelNum, true);
        }

        function closePreview() {
            const modal = document.getElementById('preview-modal');
            modal.classList.remove('active');
        }

        function showMessage(text) {
            const existing = document.querySelector('.message');
            if (existing) existing.remove();

            const msg = document.createElement('div');
            msg.className = 'message';
            msg.textContent = text;
            document.body.appendChild(msg);

            setTimeout(() => {
                msg.style.opacity = '0';
                msg.style.transform = 'translateX(400px)';
                setTimeout(() => msg.remove(), 300);
            }, 3000);
        }
    </script>
</body>
</html>
    """

    selected_count = sum(1 for item in panels_with_variants if item['is_selected'])

    return render_template_string(
        template,
        page_num=page_num,
        page_data=page_data,
        panels_with_variants=panels_with_variants,
        selected_count=selected_count
    )


@app.route('/select/<int:page_num>/<int:panel_num>/<int:variant_num>', methods=['POST'])
def select_variant(page_num, panel_num, variant_num):
    """Select a variant and make it the final version."""
    try:
        # Load selections
        selections = load_selections()

        # Source and destination paths
        source = PANELS_DIR / f"page-{page_num:03d}-panel-{panel_num}-v{variant_num}.png"
        dest = PANELS_DIR / f"page-{page_num:03d}-panel-{panel_num}.png"

        if not source.exists():
            return jsonify({'success': False, 'error': 'Variant file not found'}), 404

        # Copy selected variant to final filename
        shutil.copy(source, dest)

        # Delete unchosen variants (clean as you go)
        variant_num_check = 1
        while True:
            variant_path = PANELS_DIR / f"page-{page_num:03d}-panel-{panel_num}-v{variant_num_check}.png"
            if not variant_path.exists():
                break
            if variant_num_check != variant_num:
                variant_path.unlink()
            variant_num_check += 1

        # Save selection
        selections[f"{page_num}-{panel_num}"] = variant_num
        save_selections(selections)

        return jsonify({'success': True})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/preview/<int:page_num>')
def preview_page(page_num):
    """Generate a preview of the assembled page."""
    try:
        # Load page data
        page_data = load_page_data(page_num)
        panels = page_data['panels']
        num_panels = len(panels)

        # Check if all panels have been selected
        missing_panels = []
        for panel in panels:
            panel_file = PANELS_DIR / f"page-{page_num:03d}-panel-{panel['panel_num']}.png"
            if not panel_file.exists():
                missing_panels.append(panel['panel_num'])

        if missing_panels:
            return f"Error: Missing selected panels: {missing_panels}", 400

        # Create blank page
        page_img = Image.new('RGB', (PAGE_WIDTH, PAGE_HEIGHT), 'white')

        # Simple layout logic (from assemble.py)
        if num_panels <= 3:
            # Vertical stack
            panel_height = (PAGE_HEIGHT - (num_panels + 1) * GUTTER) // num_panels

            for i, panel in enumerate(panels):
                panel_file = PANELS_DIR / f"page-{page_num:03d}-panel-{panel['panel_num']}.png"
                if panel_file.exists():
                    img = Image.open(panel_file)
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

        # Return image as response
        img_io = io.BytesIO()
        page_img.save(img_io, 'PNG')
        img_io.seek(0)

        return send_file(img_io, mimetype='image/png')

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/more/<int:page_num>/<int:panel_num>', methods=['POST'])
def generate_more(page_num, panel_num):
    """Generate 3 more variants for a panel."""
    try:
        # Load page data to get panel info
        page_data = load_page_data(page_num)
        panel_data = next((p for p in page_data['panels'] if p['panel_num'] == panel_num), None)

        if not panel_data:
            return jsonify({'success': False, 'error': 'Panel not found'}), 404

        # Delete the final selection if it exists (so user can re-select from new variants)
        final_file = PANELS_DIR / f"page-{page_num:03d}-panel-{panel_num}.png"
        if final_file.exists():
            final_file.unlink()

        # Find the next available variant number
        next_variant_num = 1
        while (PANELS_DIR / f"page-{page_num:03d}-panel-{panel_num}-v{next_variant_num}.png").exists():
            next_variant_num += 1

        # Call generate.py to create more variants
        # This is a simplified approach - you could also import and call the async function directly
        # For now, we'll generate 3 more by manually running the generation
        import asyncio
        from openai import AsyncOpenAI
        import base64
        import aiofiles

        async def generate_additional_variants():
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("OPENAI_API_KEY not set")

            client = AsyncOpenAI(api_key=api_key)
            prompt = panel_data.get('prompt', '')
            size = panel_data.get('size', '1024x1024')

            new_variants = []
            for i in range(3):
                variant_num = next_variant_num + i
                filename = PANELS_DIR / f"page-{page_num:03d}-panel-{panel_num}-v{variant_num}.png"

                response = await client.images.generate(
                    model="gpt-image-1",
                    prompt=prompt,
                    size=size,
                    quality="high",
                    n=1
                )

                image_bytes = base64.b64decode(response.data[0].b64_json)
                async with aiofiles.open(filename, 'wb') as f:
                    await f.write(image_bytes)

                new_variants.append(variant_num)

            await client.close()
            return new_variants

        # Run the async generation
        new_variants = asyncio.run(generate_additional_variants())

        return jsonify({'success': True, 'new_variants': len(new_variants)})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python review.py <page_num>")
        print("Example: python review.py 1")
        sys.exit(1)

    try:
        page_num = int(sys.argv[1])
    except ValueError:
        print("Error: Page number must be an integer")
        sys.exit(1)

    global current_page_num
    current_page_num = page_num

    # Check if page exists
    try:
        load_page_data(page_num)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Run parse_script.py first to generate page JSON files")
        sys.exit(1)

    # Determine port
    port = int(os.getenv('FLASK_PORT', 5001))

    print(f"\n{'='*60}")
    print(f"COMIC PANEL REVIEW - PAGE {page_num}")
    print(f"{'='*60}")
    print(f"\nOpening review interface at http://127.0.0.1:{port}")
    print("Press Ctrl+C to stop the server\n")

    # Open browser
    import webbrowser
    import threading
    def open_browser():
        import time
        time.sleep(1)
        webbrowser.open(f'http://127.0.0.1:{port}/page/{page_num}')

    threading.Thread(target=open_browser, daemon=True).start()

    # Run Flask app
    app.run(debug=False, port=port, host='127.0.0.1')


if __name__ == "__main__":
    main()
