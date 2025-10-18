# Image Continuity System for Comic Production

## The Continuity Challenge

AI-generated images are **not deterministic**. The same prompt can yield wildly different results. For a comic book, we need multiple types of visual continuity:

### Types of Continuity

1. **Style Continuity**: Overall art style, line work, coloring technique must be consistent
2. **Character Continuity**: Val must look like Val in every panel
3. **Scene Continuity**: Sequential panels in the same location maintain consistent backgrounds, lighting
4. **Temporal Continuity**: Movement and action flow naturally from panel to panel

### Why This is Hard

- Text-to-image models generate independently
- Character features drift across generations
- Same description yields different interpretations
- No built-in "memory" of previous panels

## Solution Analysis

### Option 1: Text-Only Prompting (Baseline)
**How it works**: Use extremely detailed, consistent text descriptions

**Pros**:
- Simple, no additional complexity
- Works with any image generation API

**Cons**:
- ❌ Inconsistent results
- ❌ Character appearance drifts significantly
- ❌ Hard to maintain exact visual elements
- ❌ Relies entirely on AI interpretation

**Verdict**: Not sufficient for professional comics

---

### Option 2: Style Reference Only
**How it works**: Include one master style reference with all generations

**Pros**:
- ✅ Maintains overall art style consistency
- ✅ Easy to implement

**Cons**:
- ❌ Doesn't guarantee character consistency
- ❌ Limited control over specific elements
- ❌ Single reference may not cover all scenarios

**Verdict**: Helps but incomplete

---

### Option 3: Character Reference Library
**How it works**: Generate and curate character references, include relevant ones in prompts

**Pros**:
- ✅ Better character consistency
- ✅ Can show different angles/expressions
- ✅ Reusable across entire comic

**Cons**:
- ⚠️ Requires upfront work to build library
- ⚠️ Need to describe references effectively
- ⚠️ Still some variation possible

**Verdict**: Good approach, but needs more

---

### Option 4: Sequential Panel References
**How it works**: Use previous panel(s) as reference when generating next panel

**Pros**:
- ✅ Strong sequential continuity
- ✅ Natural flow between panels
- ✅ Maintains scene context

**Cons**:
- ⚠️ May propagate errors
- ⚠️ Tight coupling between panels
- ⚠️ Limits creative flexibility

**Verdict**: Useful for sequences, not standalone

---

### Option 5: Hierarchical Multi-Reference System ⭐ **RECOMMENDED**

**How it works**: Combine multiple reference types in a hierarchical system

**Reference Hierarchy**:
```
1. Style Master (primary) - Defines overall art style
2. Character Cards (secondary) - Defines character appearance
3. Sequential Context (tertiary) - Provides scene continuity
4. Environmental References (optional) - Location consistency
```

**Pros**:
- ✅ ✅ ✅ Addresses all continuity types
- ✅ Flexible and extensible
- ✅ Leverages Claude's image analysis
- ✅ Scalable reference library
- ✅ Maintains consistency without rigidity

**Cons**:
- ⚠️ More complex implementation
- ⚠️ Requires reference library setup
- ⚠️ More tokens per generation (image analysis)

**Verdict**: Best balance of consistency, quality, and flexibility

## Recommended Solution: Hierarchical Multi-Reference System

### Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│  GENERATION REQUEST                                  │
│  "Generate panel ch01-pg01-p03 with Val and Prismor"│
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│  REFERENCE SELECTOR                                  │
│  1. Style Master → master-style-01.png               │
│  2. Character Refs → val/front.png, prismor/side.png│
│  3. Sequential → panel-02-selected.png               │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│  IMAGE ANALYZER (Claude Read Tool)                   │
│  - Extract colors, lines, proportions                │
│  - Describe style elements                           │
│  - Note key character features                       │
│  - Identify compositional elements                   │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│  ENHANCED PROMPT BUILDER                             │
│  Combines: Reference descriptions + Scene description│
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│  COMIC-ARTIST SUB-AGENT                              │
│  Generates 3-5 variations with continuity            │
└─────────────────────────────────────────────────────┘
```

### Reference Library Structure

```
references/
├── style/
│   ├── master-style-01.png           # Primary art style reference
│   ├── master-style-02.png           # Alternate/backup
│   └── style-guide.json              # Extracted style data
│
├── characters/
│   ├── val/
│   │   ├── turnaround/               # Character from different angles
│   │   │   ├── front.png
│   │   │   ├── side-left.png
│   │   │   ├── side-right.png
│   │   │   ├── back.png
│   │   │   └── three-quarter.png
│   │   ├── expressions/              # Emotional range
│   │   │   ├── neutral.png
│   │   │   ├── happy.png
│   │   │   ├── angry.png
│   │   │   ├── surprised.png
│   │   │   ├── sad.png
│   │   │   └── determined.png
│   │   ├── poses/                    # Common actions
│   │   │   ├── standing.png
│   │   │   ├── walking.png
│   │   │   ├── running.png
│   │   │   ├── fighting-stance.png
│   │   │   └── meditation.png
│   │   ├── details/                  # Close-ups for consistency
│   │   │   ├── face-closeup.png
│   │   │   ├── hands.png
│   │   │   └── equipment.png
│   │   └── character-guide.json      # Character-specific style data
│   │
│   ├── prismor/
│   │   └── [same structure]
│   ├── pocky/
│   ├── lunara/
│   └── malrik/
│
├── environments/
│   ├── everpeak-exterior.png
│   ├── courier-tunnels.png
│   ├── grand-library.png
│   ├── balcony-garden.png
│   └── elven-sanctum.png
│
└── sequential/                       # Selected panels for context
    └── chapter-01/
        └── page-001/
            ├── panel-01-selected.png
            ├── panel-02-selected.png
            └── ...
```

### Reference Metadata Format

Each reference includes analysis metadata:

```json
{
  "path": "references/characters/val/turnaround/front.png",
  "type": "character",
  "character": "val",
  "category": "turnaround",
  "angle": "front",
  "generated": "2025-10-18T19:00:00Z",
  "analysis": {
    "colors": {
      "primary": "#CD853F",
      "secondary": "#8B4513",
      "accent": "#FF6347",
      "description": "Warm brass and copper tones with ember-orange accents"
    },
    "style": {
      "lineWork": "Bold black ink outlines, 3-4px weight",
      "shading": "Cel-shaded with hard shadows",
      "detail": "Medium detail with simplified forms",
      "technique": "Digital comic book style"
    },
    "features": {
      "height": "Just under 7 feet, lean athletic build",
      "scales": "Brass/copper metallic sheen, textured but not overly detailed",
      "eyes": "Ember-glow orange, expressive and bright",
      "clothing": "Simple brown monastery robes with visible chalk marks",
      "distinctive": "Prayer beads on wrist, bare clawed feet"
    }
  },
  "prompt_snippet": "Match character appearance: brass dragonborn monk with warm brass/copper scales showing metallic sheen, ember-orange eyes bright and expressive, lean athletic build just under 7 feet tall, simple brown monastery robes with chalk dust, bare clawed feet, prayer beads on wrist"
}
```

## Integration with Workflow

### Phase 0: Reference Library Creation (ONE-TIME SETUP)

#### Step 1: Generate Style Masters

```
Goal: Create 2-3 "perfect" panels that define the art style

Process:
1. Generate 10+ variations of a test panel
2. Human selects best 2-3 that capture desired style
3. Analyze selected panels to extract style elements
4. Save as style-guide.json

What to look for:
- Line art quality (bold, clean, consistent thickness)
- Color palette (limited, cohesive colors)
- Shading technique (flat, cel-shaded, gradient, etc.)
- Detail level (highly detailed vs. simplified)
- Overall "feel" (gritty, whimsical, dramatic, etc.)
```

#### Step 2: Generate Character Reference Library

For EACH main character:

```
1. Turnarounds (5 images):
   - Front view, neutral expression, standing pose
   - Side view (left and right)
   - Back view
   - Three-quarter view

2. Expressions (6 images):
   - Front view, different expressions
   - Neutral, happy, sad, angry, surprised, determined

3. Common Poses (5 images):
   - Standing/idle
   - Walking
   - Running/action
   - Character-specific (Val: meditation, Prismor: sword ready, etc.)

4. Detail Shots (3 images):
   - Face close-up
   - Hands/equipment
   - Full costume details

For each image:
- Generate 3-5 variations
- Human selects best one
- Analyze and save metadata
- Store in organized folder
```

#### Step 3: Analyze All References

```python
# Pseudo-code for analysis process

for reference_image in reference_library:
    # Use Claude's Read tool to analyze
    analysis = claude_read(reference_image)

    # Extract structured data
    metadata = {
        "colors": extract_color_palette(analysis),
        "style": extract_style_elements(analysis),
        "features": extract_character_features(analysis),
        "prompt_snippet": generate_prompt_text(analysis)
    }

    # Save alongside image
    save_json(metadata, reference_image.replace('.png', '.json'))
```

### Phase 1: Panel Generation with Multi-Reference

#### Enhanced Panel Specification

```json
{
  "panelId": "ch01-pg01-p03",
  "chapter": 1,
  "page": 1,
  "panel": 3,
  "description": "Val and Prismor talking in marketplace",
  "aspectRatio": "16:9",
  "characters": [
    {
      "name": "val",
      "role": "primary",
      "angle": "three-quarter",
      "expression": "friendly",
      "pose": "standing",
      "references": [
        "references/characters/val/turnaround/three-quarter.png",
        "references/characters/val/expressions/happy.png"
      ]
    },
    {
      "name": "prismor",
      "role": "secondary",
      "angle": "side",
      "expression": "neutral",
      "pose": "standing",
      "references": [
        "references/characters/prismor/turnaround/side-left.png"
      ]
    }
  ],
  "environment": {
    "location": "festival-marketplace",
    "reference": "references/environments/marketplace.png"
  },
  "sequential": {
    "previousPanel": "ch01-pg01-p02",
    "reference": "source/panels/chapter-01/page-001/panel-02/variation-3.png",
    "continuity": "Val is moving from left to right, Prismor enters from right"
  },
  "style": {
    "reference": "references/style/master-style-01.png"
  }
}
```

#### Reference Analysis Process

```python
def analyze_references_for_panel(panel_spec):
    """
    Analyze all reference images and build enhanced descriptions
    """

    references = {
        "style": {},
        "characters": {},
        "environment": {},
        "sequential": {}
    }

    # 1. Analyze style reference
    style_img = panel_spec['style']['reference']
    style_json = load_json(style_img.replace('.png', '.json'))
    references['style'] = style_json['analysis']

    # 2. Analyze character references
    for char in panel_spec['characters']:
        char_analyses = []
        for ref_path in char['references']:
            char_json = load_json(ref_path.replace('.png', '.json'))
            char_analyses.append(char_json['analysis'])

        # Merge character reference analyses
        references['characters'][char['name']] = merge_analyses(char_analyses)

    # 3. Analyze sequential reference (if applicable)
    if panel_spec.get('sequential'):
        seq_img = panel_spec['sequential']['reference']
        # Analyze the actual selected panel (may not have pre-saved JSON)
        seq_analysis = claude_read(seq_img)
        references['sequential'] = {
            "previous_composition": extract_composition(seq_analysis),
            "lighting": extract_lighting(seq_analysis),
            "camera_angle": extract_camera(seq_analysis)
        }

    return references
```

#### Enhanced Prompt Construction

```python
def build_continuity_prompt(panel_spec, reference_analyses):
    """
    Build a prompt that incorporates all reference analyses
    """

    prompt = ["Professional comic book panel illustration:\n"]

    # STYLE SECTION
    style = reference_analyses['style']
    prompt.append("STYLE CONTINUITY:")
    prompt.append(f"Art style: {style['style']['lineWork']}, {style['style']['shading']}")
    prompt.append(f"Color approach: {style['colors']['description']}")
    prompt.append(f"Detail level: {style['style']['detail']}")
    prompt.append(f"Technique: {style['style']['technique']}")
    prompt.append("")

    # CHARACTER SECTION(S)
    for char_name, char_data in reference_analyses['characters'].items():
        prompt.append(f"CHARACTER CONTINUITY - {char_name.upper()}:")
        prompt.append(f"Appearance: {char_data['features']['description']}")
        prompt.append(f"Current angle: {panel_spec['characters'][char_name]['angle']}")
        prompt.append(f"Current expression: {panel_spec['characters'][char_name]['expression']}")
        prompt.append(f"Colors: {char_data['colors']['description']}")
        prompt.append(f"Match exact appearance from reference images.")
        prompt.append("")

    # SEQUENTIAL SECTION
    if 'sequential' in reference_analyses:
        seq = reference_analyses['sequential']
        prompt.append("SEQUENTIAL CONTINUITY:")
        prompt.append(f"Previous panel composition: {seq['previous_composition']}")
        prompt.append(f"Maintained lighting: {seq['lighting']}")
        prompt.append(f"Camera perspective: {seq['camera_angle']}")
        prompt.append(f"Narrative flow: {panel_spec['sequential']['continuity']}")
        prompt.append("")

    # ENVIRONMENT SECTION
    if panel_spec.get('environment'):
        env = reference_analyses.get('environment', {})
        prompt.append("ENVIRONMENT:")
        prompt.append(f"Location: {panel_spec['environment']['location']}")
        if env:
            prompt.append(f"Setting details: {env.get('description', '')}")
        prompt.append("")

    # SCENE DESCRIPTION
    prompt.append("SCENE:")
    prompt.append(f"{panel_spec['description']}")
    prompt.append(f"Composition: {panel_spec['aspectRatio']} panel")
    prompt.append("")

    # TECHNICAL REQUIREMENTS
    prompt.append("REQUIREMENTS:")
    prompt.append("- Match EXACT character appearance from character references")
    prompt.append("- Match art style from style reference")
    prompt.append("- Maintain sequential continuity with previous panel")
    prompt.append("- Keep consistent lighting and perspective within the scene")

    return "\n".join(prompt)
```

### Prompt Template Example

Here's what a fully enhanced prompt looks like:

```
Professional comic book panel illustration:

STYLE CONTINUITY:
Art style: Bold black ink outlines (3-4px weight), cel-shaded with hard shadows
Color approach: Limited palette with warm brass/copper tones, cool blues, vibrant accent colors
Detail level: Medium detail with simplified forms for readability
Technique: Digital comic book style, clean and professional

CHARACTER CONTINUITY - VAL:
Appearance: Brass dragonborn monk, just under 7 feet tall with lean athletic build
Physical features: Warm brass/copper scales with metallic sheen, ember-orange eyes bright and expressive, shorter snout with kind open expression
Costume: Simple brown monastery robes with visible chalk dust marks, bare clawed feet, prayer beads on left wrist
Current angle: Three-quarter view
Current expression: Friendly, smiling
Match exact appearance from reference images.

CHARACTER CONTINUITY - PRISMOR:
Appearance: Blue crystal dragonborn paladin, 7 feet tall with muscular powerful build
Physical features: Crystalline blue scales with green hints and gem-like quality, deep sapphire blue eyes, noble bearing, dignified reptilian features
Costume: Plate armor with crystalline accents, Oath of Ancients symbols (leaves and vines), greatsword strapped to back, forest green cape
Current angle: Side view (left side visible)
Current expression: Neutral, calm
Match exact appearance from reference images.

SEQUENTIAL CONTINUITY:
Previous panel composition: Wide shot of marketplace with Val walking left to right, festival stalls in background
Maintained lighting: Morning sunlight from upper left, warm golden hour lighting, long shadows
Camera perspective: Mid-level eye line, slight Dutch angle for dynamic feel
Narrative flow: Val continues moving right, Prismor enters from right side of frame, they meet in center

ENVIRONMENT:
Location: Festival marketplace in Everpeak Citadel courtyard
Setting details: Crowded festival stalls with colorful banners, stone architecture of citadel visible in background, morning mist in air, vendors and citizens in background

SCENE:
Val and Prismor meet in the crowded festival marketplace. Val is gesturing animatedly while talking, Prismor listens attentively. Background crowd bustling with activity. Both characters are the focus, positioned in center-right of frame.
Composition: 16:9 wide panel for environmental context

REQUIREMENTS:
- Match EXACT character appearance from character references (Val's brass scales, Prismor's blue crystal scales and armor)
- Match art style from style reference (bold ink lines, cel-shading, limited color palette)
- Maintain sequential continuity with previous panel (same lighting, same location, character positions flow naturally)
- Keep consistent lighting and perspective within the scene
- Background characters should be less detailed to maintain focus on Val and Prismor
```

## Implementation Steps

### Phase 1: Initial Setup (Do First)

```bash
# 1. Create reference library structure
mkdir -p references/{style,characters,environments,sequential}
mkdir -p references/characters/{val,prismor,pocky,lunara,malrik}/{turnaround,expressions,poses,details}

# 2. Generate style masters
# Ask Claude: "Generate 10 variations of a test panel to establish art style"
# Human selects best 2-3
# Save to references/style/

# 3. Analyze style masters
# Ask Claude: "Analyze these style references and extract style guide data"
# Save to references/style/style-guide.json
```

### Phase 2: Character Reference Generation

```bash
# For each character:
# 1. Generate turnarounds (5 angles × 3 variations = 15 images)
# 2. Generate expressions (6 emotions × 3 variations = 18 images)
# 3. Generate poses (5 poses × 3 variations = 15 images)
# 4. Human reviews and selects best of each

# Total per character: ~15-20 reference images
# Total for 5 characters: ~75-100 reference images

# This is a one-time investment that pays dividends throughout production
```

### Phase 3: Integration with Panel Generation

```python
# Updated panel generation workflow

def generate_panel_with_continuity(panel_spec):
    """
    Generate a panel using multi-reference continuity system
    """

    # 1. Gather all relevant references
    references = select_references(panel_spec)

    # 2. Analyze references (use cached analyses when available)
    analyses = analyze_references(references)

    # 3. Build enhanced prompt
    enhanced_prompt = build_continuity_prompt(panel_spec, analyses)

    # 4. Launch comic-artist sub-agent with enhanced prompt
    result = launch_comic_artist_agent(
        panel_id=panel_spec['panelId'],
        prompt=enhanced_prompt,
        size=panel_spec['size'],
        variations=3,
        output_dir=f"source/panels/chapter-{panel_spec['chapter']:02d}/page-{panel_spec['page']:03d}/panel-{panel_spec['panel']:02d}/"
    )

    # 5. Save reference metadata with generated panels
    save_generation_metadata(result, references, analyses)

    return result
```

## Best Practices

### Style References
- ✅ Generate multiple style masters early in the process
- ✅ Use the same style reference for entire chapters or the whole comic
- ✅ Re-analyze if style evolves or improves
- ⚠️ Don't change style references mid-chapter

### Character References
- ✅ Create comprehensive library before starting main production
- ✅ Include multiple angles and expressions
- ✅ Update library if character changes (costume, injuries, etc.)
- ✅ Use reference closest to desired panel (right angle, right expression)
- ⚠️ Don't mix references from different generation batches

### Sequential References
- ✅ Use for adjacent panels in same scene
- ✅ Maintain lighting and perspective consistency
- ⚠️ Don't chain too many (error propagation risk)
- ⚠️ Reset for scene changes (different location/time)

### Prompt Engineering
- ✅ Be specific about what to match from each reference
- ✅ Use consistent terminology across all prompts
- ✅ Include technical details (colors, line weights, proportions)
- ✅ Prioritize: Style > Character > Sequential > Environment
- ⚠️ Don't make prompts too long (diminishing returns)

## Reference Image Viewer

### Purpose

With 80+ reference images organized across multiple folders, we need an efficient way to:
- Browse the reference library
- View references when crafting panel prompts
- Compare references side-by-side
- Review metadata and analysis
- Select appropriate references for specific panels

### Viewer Interface Design

**Location**: `references/viewer.html`

**Features**:
1. **Library Browser**: Hierarchical view of all references
2. **Filter System**: Filter by character, type (turnaround/expression/pose), style
3. **Thumbnail Grid**: Visual overview with metadata overlays
4. **Lightbox View**: Full-size image viewing with analysis data
5. **Comparison Mode**: View multiple references side-by-side
6. **Selection Tool**: Mark references for use in upcoming panel generation

### HTML Structure

```html
<!DOCTYPE html>
<html>
<head>
    <title>Everpeak Reference Library</title>
    <link rel="stylesheet" href="viewer.css">
</head>
<body>
    <!-- Sidebar: Navigation & Filters -->
    <aside class="sidebar">
        <h1>Reference Library</h1>

        <section class="filters">
            <h2>Filters</h2>
            <div class="filter-group">
                <label>Type:</label>
                <button class="filter-btn active" data-type="all">All</button>
                <button class="filter-btn" data-type="style">Style</button>
                <button class="filter-btn" data-type="character">Characters</button>
                <button class="filter-btn" data-type="environment">Environments</button>
            </div>

            <div class="filter-group" id="character-filter">
                <label>Character:</label>
                <button class="filter-btn" data-character="val">Val</button>
                <button class="filter-btn" data-character="prismor">Prismor</button>
                <button class="filter-btn" data-character="pocky">Pocky</button>
                <button class="filter-btn" data-character="lunara">Lunara</button>
                <button class="filter-btn" data-character="malrik">Malrik</button>
            </div>

            <div class="filter-group" id="category-filter">
                <label>Category:</label>
                <button class="filter-btn" data-category="turnaround">Turnarounds</button>
                <button class="filter-btn" data-category="expressions">Expressions</button>
                <button class="filter-btn" data-category="poses">Poses</button>
                <button class="filter-btn" data-category="details">Details</button>
            </div>
        </section>

        <section class="tree-view">
            <h2>Library Structure</h2>
            <ul class="tree">
                <li>
                    <span class="folder">📁 style</span>
                    <ul><li class="file">master-style-01.png</li></ul>
                </li>
                <li>
                    <span class="folder">📁 characters</span>
                    <ul>
                        <li>
                            <span class="folder">📁 val</span>
                            <ul>
                                <li><span class="folder">📁 turnaround</span></li>
                                <li><span class="folder">📁 expressions</span></li>
                                <li><span class="folder">📁 poses</span></li>
                                <li><span class="folder">📁 details</span></li>
                            </ul>
                        </li>
                        <!-- Repeat for other characters -->
                    </ul>
                </li>
            </ul>
        </section>

        <section class="selection-panel">
            <h2>Selected References</h2>
            <p class="selection-count">0 selected</p>
            <button id="export-selection">Export Selection</button>
            <button id="clear-selection">Clear All</button>
        </section>
    </aside>

    <!-- Main: Image Grid -->
    <main class="image-grid">
        <div class="toolbar">
            <div class="view-controls">
                <button class="view-btn active" data-view="grid">Grid</button>
                <button class="view-btn" data-view="list">List</button>
                <button class="view-btn" data-view="compare">Compare</button>
            </div>
            <div class="sort-controls">
                <label>Sort:</label>
                <select id="sort-select">
                    <option value="name">Name</option>
                    <option value="date">Date Added</option>
                    <option value="type">Type</option>
                    <option value="character">Character</option>
                </select>
            </div>
            <div class="search">
                <input type="text" id="search-input" placeholder="Search references...">
            </div>
        </div>

        <!-- Reference Cards -->
        <div class="cards-container" id="cards-container">
            <!-- Card Template -->
            <div class="reference-card" data-type="character" data-character="val" data-category="turnaround">
                <div class="card-image">
                    <img src="val/turnaround/front.png" alt="Val - Front View">
                    <div class="card-overlay">
                        <button class="btn-view">👁️ View</button>
                        <button class="btn-select">✓ Select</button>
                    </div>
                </div>
                <div class="card-info">
                    <h3>Val - Front View</h3>
                    <span class="badge badge-character">Character</span>
                    <span class="badge badge-turnaround">Turnaround</span>
                    <p class="card-description">Front-facing reference with neutral expression</p>
                </div>
                <div class="card-meta">
                    <span>📅 2025-10-18</span>
                    <span>🎨 1024x1536</span>
                </div>
            </div>
            <!-- More cards generated dynamically -->
        </div>
    </main>

    <!-- Lightbox: Full Image View -->
    <div class="lightbox" id="lightbox" style="display: none;">
        <div class="lightbox-content">
            <button class="lightbox-close">✕</button>
            <div class="lightbox-image">
                <img id="lightbox-img" src="" alt="">
            </div>
            <div class="lightbox-sidebar">
                <h2 id="lightbox-title">Image Title</h2>

                <section class="metadata-section">
                    <h3>Basic Info</h3>
                    <dl>
                        <dt>Path:</dt>
                        <dd id="meta-path"></dd>
                        <dt>Type:</dt>
                        <dd id="meta-type"></dd>
                        <dt>Character:</dt>
                        <dd id="meta-character"></dd>
                        <dt>Category:</dt>
                        <dd id="meta-category"></dd>
                        <dt>Size:</dt>
                        <dd id="meta-size"></dd>
                        <dt>Generated:</dt>
                        <dd id="meta-date"></dd>
                    </dl>
                </section>

                <section class="analysis-section">
                    <h3>Style Analysis</h3>
                    <div id="analysis-content">
                        <h4>Colors</h4>
                        <p id="analysis-colors"></p>

                        <h4>Line Work</h4>
                        <p id="analysis-linework"></p>

                        <h4>Features</h4>
                        <p id="analysis-features"></p>
                    </div>
                </section>

                <section class="prompt-section">
                    <h3>Prompt Snippet</h3>
                    <textarea id="prompt-snippet" readonly></textarea>
                    <button id="copy-prompt">Copy to Clipboard</button>
                </section>

                <div class="lightbox-actions">
                    <button class="btn-select-lightbox">Add to Selection</button>
                    <button class="btn-analyze">Re-analyze with Claude</button>
                </div>
            </div>
        </div>
    </div>

    <script src="viewer.js"></script>
</body>
</html>
```

### Key Features

#### 1. Hierarchical Navigation
- Tree view showing folder structure
- Click folders to expand/collapse
- Click files to view in lightbox

#### 2. Smart Filtering
- Filter by type (style/character/environment)
- Filter by specific character
- Filter by category (turnaround/expression/pose/details)
- Multiple filters can be active simultaneously

#### 3. Visual Grid Display
- Thumbnail cards with key metadata
- Hover overlay with quick actions
- Badges showing type and category
- Responsive grid layout

#### 4. Lightbox Viewer
- Full-size image display
- Complete metadata panel
- Saved analysis data
- Prompt snippet for reuse
- Copy prompt to clipboard

#### 5. Comparison Mode
- Select multiple references
- View side-by-side
- Compare metadata
- Export selection list

#### 6. Selection System
- Mark references for upcoming panel generation
- Export selection to JSON
- Format: Compatible with panel specification

### Viewer JavaScript (viewer.js)

```javascript
class ReferenceViewer {
    constructor() {
        this.references = [];
        this.filteredReferences = [];
        this.selectedReferences = new Set();
        this.currentFilters = {
            type: 'all',
            character: null,
            category: null,
            search: ''
        };

        this.init();
    }

    async init() {
        await this.loadReferences();
        this.setupEventListeners();
        this.render();
    }

    async loadReferences() {
        // Load reference metadata from JSON files
        // In practice, this would scan the references directory
        // and load associated .json metadata files

        try {
            const response = await fetch('references-index.json');
            this.references = await response.json();
            this.filteredReferences = [...this.references];
        } catch (error) {
            console.error('Failed to load references:', error);
            this.generateReferenceIndex();
        }
    }

    generateReferenceIndex() {
        // If no index exists, scan directory structure
        // This would be generated by Claude when analyzing references
    }

    setupEventListeners() {
        // Filter buttons
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.handleFilter(e));
        });

        // Search input
        document.getElementById('search-input').addEventListener('input', (e) => {
            this.currentFilters.search = e.target.value;
            this.applyFilters();
        });

        // View mode buttons
        document.querySelectorAll('.view-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.handleViewChange(e));
        });

        // Sort select
        document.getElementById('sort-select').addEventListener('change', (e) => {
            this.sortReferences(e.target.value);
        });

        // Export selection
        document.getElementById('export-selection').addEventListener('click', () => {
            this.exportSelection();
        });

        // Clear selection
        document.getElementById('clear-selection').addEventListener('click', () => {
            this.clearSelection();
        });

        // Lightbox close
        document.querySelector('.lightbox-close').addEventListener('click', () => {
            this.closeLightbox();
        });
    }

    handleFilter(event) {
        const btn = event.target;
        const filterType = btn.dataset.type || btn.dataset.character || btn.dataset.category;

        // Update filter state
        if (btn.dataset.type) {
            this.currentFilters.type = filterType;
        } else if (btn.dataset.character) {
            this.currentFilters.character = filterType;
        } else if (btn.dataset.category) {
            this.currentFilters.category = filterType;
        }

        // Update button states
        btn.parentElement.querySelectorAll('.filter-btn').forEach(b => {
            b.classList.remove('active');
        });
        btn.classList.add('active');

        this.applyFilters();
    }

    applyFilters() {
        this.filteredReferences = this.references.filter(ref => {
            // Type filter
            if (this.currentFilters.type !== 'all' && ref.type !== this.currentFilters.type) {
                return false;
            }

            // Character filter
            if (this.currentFilters.character && ref.character !== this.currentFilters.character) {
                return false;
            }

            // Category filter
            if (this.currentFilters.category && ref.category !== this.currentFilters.category) {
                return false;
            }

            // Search filter
            if (this.currentFilters.search) {
                const searchLower = this.currentFilters.search.toLowerCase();
                return ref.path.toLowerCase().includes(searchLower) ||
                       (ref.description || '').toLowerCase().includes(searchLower);
            }

            return true;
        });

        this.render();
    }

    render() {
        const container = document.getElementById('cards-container');
        container.innerHTML = '';

        this.filteredReferences.forEach(ref => {
            const card = this.createCard(ref);
            container.appendChild(card);
        });

        this.updateSelectionCount();
    }

    createCard(ref) {
        const card = document.createElement('div');
        card.className = 'reference-card';
        card.dataset.path = ref.path;

        card.innerHTML = `
            <div class="card-image">
                <img src="${ref.path}" alt="${ref.description || ref.path}" loading="lazy">
                <div class="card-overlay">
                    <button class="btn-view" onclick="viewer.openLightbox('${ref.path}')">👁️ View</button>
                    <button class="btn-select" onclick="viewer.toggleSelection('${ref.path}')">
                        ${this.selectedReferences.has(ref.path) ? '✓ Selected' : '+ Select'}
                    </button>
                </div>
            </div>
            <div class="card-info">
                <h3>${this.getDisplayName(ref)}</h3>
                <span class="badge badge-${ref.type}">${ref.type}</span>
                ${ref.category ? `<span class="badge badge-${ref.category}">${ref.category}</span>` : ''}
                <p class="card-description">${ref.description || ''}</p>
            </div>
            <div class="card-meta">
                <span>📅 ${new Date(ref.generated).toLocaleDateString()}</span>
                <span>🎨 ${ref.analysis?.size || 'N/A'}</span>
            </div>
        `;

        return card;
    }

    openLightbox(path) {
        const ref = this.references.find(r => r.path === path);
        if (!ref) return;

        // Update lightbox image
        document.getElementById('lightbox-img').src = ref.path;
        document.getElementById('lightbox-title').textContent = this.getDisplayName(ref);

        // Update metadata
        document.getElementById('meta-path').textContent = ref.path;
        document.getElementById('meta-type').textContent = ref.type;
        document.getElementById('meta-character').textContent = ref.character || 'N/A';
        document.getElementById('meta-category').textContent = ref.category || 'N/A';
        document.getElementById('meta-size').textContent = ref.analysis?.size || 'N/A';
        document.getElementById('meta-date').textContent = new Date(ref.generated).toLocaleString();

        // Update analysis
        if (ref.analysis) {
            document.getElementById('analysis-colors').textContent = ref.analysis.colors?.description || 'No analysis';
            document.getElementById('analysis-linework').textContent = ref.analysis.style?.lineWork || 'No analysis';
            document.getElementById('analysis-features').textContent = ref.analysis.features?.description || 'No analysis';
        }

        // Update prompt snippet
        document.getElementById('prompt-snippet').value = ref.prompt_snippet || 'No prompt snippet available';

        // Show lightbox
        document.getElementById('lightbox').style.display = 'flex';
    }

    closeLightbox() {
        document.getElementById('lightbox').style.display = 'none';
    }

    toggleSelection(path) {
        if (this.selectedReferences.has(path)) {
            this.selectedReferences.delete(path);
        } else {
            this.selectedReferences.add(path);
        }
        this.render();
    }

    clearSelection() {
        this.selectedReferences.clear();
        this.render();
    }

    exportSelection() {
        const selected = Array.from(this.selectedReferences).map(path => {
            return this.references.find(r => r.path === path);
        });

        const exportData = {
            exported: new Date().toISOString(),
            count: selected.length,
            references: selected
        };

        // Download as JSON
        const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `reference-selection-${Date.now()}.json`;
        a.click();
        URL.revokeObjectURL(url);
    }

    updateSelectionCount() {
        const count = this.selectedReferences.size;
        document.querySelector('.selection-count').textContent = `${count} selected`;
    }

    getDisplayName(ref) {
        // Extract meaningful name from path
        const parts = ref.path.split('/');
        return parts[parts.length - 1].replace(/\.[^/.]+$/, "").replace(/-/g, ' ');
    }
}

// Initialize viewer
const viewer = new ReferenceViewer();
```

### Integration with Workflow

**When building panel prompts**:
1. Open reference viewer at `references/viewer.html`
2. Filter to relevant character and pose type
3. Select appropriate references
4. Export selection
5. Selection JSON automatically includes metadata and prompt snippets
6. Use selected references in panel generation

**Automatic indexing**:
- When Claude analyzes references, it generates `references-index.json`
- Viewer loads this index for fast browsing
- No need to scan filesystem on every load

### Benefits

- 📚 **Easy Browsing**: Visual interface for 80+ references
- 🔍 **Smart Search**: Find references quickly by character, type, or keyword
- 📊 **Metadata Access**: View analysis data alongside images
- 🎯 **Quick Selection**: Mark references for panel generation
- 📋 **Copy Prompts**: Reuse analyzed prompt snippets
- 🔄 **Export Selections**: Generate panel specs with proper references

## Success Metrics

A successful continuity system should achieve:

- [ ] **Character Recognition**: Same character recognizable across 20+ panels
- [ ] **Style Consistency**: Art style remains cohesive throughout comic
- [ ] **Sequential Flow**: Adjacent panels feel connected and natural
- [ ] **Variation Control**: Generated variations differ in composition, not core elements
- [ ] **Efficiency**: Reference analysis cached and reused effectively
- [ ] **Scalability**: System works for 40+ pages without drift

## Future Enhancements

1. **Automatic Reference Selection**: ML model to choose best references based on panel requirements
2. **Style Transfer**: Apply reference style more directly (if supported by image generation API)
3. **Face Consistency**: Specialized face-matching to ensure same facial features
4. **Reference Evolution**: Track which references produce best results and prioritize them
5. **Semantic Matching**: Match references based on scene similarity, not just character presence

## Conclusion

The **Hierarchical Multi-Reference System** provides the best balance between consistency and flexibility. By maintaining a structured reference library and using Claude's image analysis capabilities to incorporate references into prompts, we can achieve professional-level visual continuity while still allowing creative variation.

The upfront investment in building a reference library (estimated 75-100 images) pays dividends throughout the entire comic production process, ensuring that Val always looks like Val, the art style stays consistent, and sequential panels flow naturally.
