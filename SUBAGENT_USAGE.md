# Comic Artist Sub-Agent Usage Guide

This guide explains how to use the Comic Artist sub-agent for generating consistent, stylized artwork using OpenAI's gpt-image-1 model.

## What is a Sub-Agent?

A sub-agent is a specialized AI agent within Claude Code that has specific tools and expertise. The Comic Artist sub-agent is designed to:
- Generate images using OpenAI's gpt-image-1 model
- Analyze reference images for style and aesthetic
- Maintain consistent visual style across multiple generations
- Create comic panels, character designs, and illustrations

## Setup

### 1. Prerequisites

Ensure you have:
- Node.js 14+ installed
- OpenAI API key with gpt-image-1 access
- This project built: `npm run build`

### 2. Configure API Key

Create or update the `.env` file in the project root:

```bash
OPENAI_API_KEY=your-openai-api-key-here
```

The sub-agent will automatically load this environment variable.

### 3. Optional: Custom Output Directory

By default, images are saved to `~/Pictures/gpt-image-1/gpt-images/`. To customize:

```bash
# In .env file
GPT_IMAGE_OUTPUT_DIR=/path/to/your/custom/directory
```

## Using the Sub-Agent

### Invoke the Sub-Agent

In Claude Code, you can invoke the Comic Artist sub-agent in parallel with other agents. Claude Code will automatically delegate image generation tasks to this agent when appropriate, or you can explicitly invoke it.

### Example Workflows

#### 1. Generate Image with Style Reference

```
User: I have a reference image here [uploads style-ref.png]. Create a comic panel
showing a hero standing on a cliff at sunset in this same style.

Sub-Agent will:
1. Use Read tool to analyze style-ref.png
2. Extract style elements (colors, line work, composition)
3. Generate detailed prompt incorporating the style
4. Call the CLI to generate the image
5. Return the generated image path
```

#### 2. Create Multiple Consistent Images

```
User: Using the style from my reference, create 3 different character poses:
1. Standing confidently
2. Running
3. Looking surprised

Sub-Agent will:
1. Analyze the reference style
2. Document the style parameters
3. Generate each image with consistent prompt patterns
4. Ensure visual consistency across all three
```

#### 3. Edit Existing Image

```
User: Take this image [uploads hero.png] and add a cape flowing in the wind

Sub-Agent will:
1. Note the source image path
2. Craft edit prompt
3. Use CLI edit command to modify the image
4. Return the edited result
```

## Manual CLI Usage

You can also use the CLI directly for testing or scripting:

### Generate Image

```bash
node ./build/cli.js generate \
  --prompt "Comic panel, hero on cliff at sunset, dramatic sky, vibrant colors" \
  --size 1024x1024 \
  --quality high \
  --format png
```

### Edit Image

```bash
node ./build/cli.js edit \
  --image /path/to/hero.png \
  --prompt "Add a flowing red cape" \
  --quality high
```

### CLI Options

**Generate Command**:
- `-p, --prompt <text>`: Description of image to generate (required)
- `-s, --size <size>`: 1024x1024, 1536x1024, or 1024x1536 (default: 1024x1024)
- `-q, --quality <quality>`: high, medium, or low (default: high)
- `-n, --number <n>`: Number of images 1-10 (default: 1)
- `-f, --format <format>`: png, jpeg, or webp (default: png)
- `-b, --background <style>`: transparent, opaque, or auto (default: auto)

**Edit Command**:
- `-i, --image <path>`: Path to source image (required)
- `-p, --prompt <text>`: Edit description (required)
- `-m, --mask <path>`: Path to mask image (optional)
- `-s, --size <size>`: Image dimensions (default: 1024x1024)
- `-q, --quality <quality>`: Output quality (default: high)
- `-n, --number <n>`: Number of variations (default: 1)

## Tips for Best Results

### 1. Style Analysis

When providing reference images:
- Upload clear, high-quality examples
- Provide 2-3 references if possible for consistent style
- Mention any specific elements you want to preserve

### 2. Prompt Engineering

For consistent results:
- Be specific about artistic techniques (e.g., "cel-shaded", "watercolor", "ink line art")
- Include color palette details when known
- Reference composition patterns from your style guide
- Specify mood and lighting

### 3. Batch Generation

For multiple related images:
- Start with one successful generation
- Note the exact prompt that worked
- Use consistent parameters across the batch
- Save successful outputs as reference

### 4. Iterative Refinement

If results aren't perfect:
- Start broad, then refine
- Use the edit command to make small adjustments
- Build a library of effective prompts
- Document what works for your style

## Output Organization

Generated images are saved with timestamps:

```
~/Pictures/gpt-image-1/gpt-images/
  image-2024-01-15T10-30-45-123Z.png
  image-2024-01-15T10-31-22-456Z.png
  ...
```

## Parallel Sub-Agent Execution

Claude Code supports running multiple sub-agents in parallel. For example:

```
User: Generate a hero image AND analyze my codebase for improvements

Claude Code will:
- Launch Comic Artist sub-agent to generate the image
- Launch another sub-agent to analyze code
- Both run simultaneously for faster results
```

## Troubleshooting

### API Key Issues

```
Error: OPENAI_API_KEY environment variable is required.
```

**Solution**: Ensure `.env` file exists with your API key

### Build Issues

```
Error: Cannot find module './build/cli.js'
```

**Solution**: Run `npm run build` to compile TypeScript

### Image Quality Issues

If images don't match your style:
- Provide more detailed style references
- Be more specific in prompts about techniques
- Use the edit command to refine results
- Experiment with quality settings

### File Not Found

```
Error: Image file not found: /path/to/image.png
```

**Solution**: Verify file paths are absolute and files exist

## Examples

### Example 1: Comic Cover Art

```bash
node ./build/cli.js generate \
  --prompt "Comic book cover, superhero team pose, dynamic composition, bold colors, dramatic lighting, professional comic art style" \
  --size 1536x1024 \
  --quality high \
  --format png
```

### Example 2: Character Design Sheet

```bash
# Generate multiple angles
for pose in "front view" "side view" "back view"; do
  node ./build/cli.js generate \
    --prompt "Character design, $pose, clean line art, model sheet style" \
    --size 1024x1024 \
    --quality high
done
```

### Example 3: Edit with Mask

Create a mask image where white areas will be edited:

```bash
node ./build/cli.js edit \
  --image character.png \
  --mask character-mask.png \
  --prompt "Add glowing energy effects" \
  --quality high
```

## Advanced Features

### Using Style References

The sub-agent can analyze uploaded images and extract:
- Color palettes (specific hex values)
- Line work style (thickness, technique)
- Composition patterns
- Lighting approaches
- Texture and detail levels

This analysis is then incorporated into generation prompts for style consistency.

### Maintaining Character Consistency

For comic series:
1. Generate a reference character design
2. Save detailed style notes
3. Use consistent prompt patterns
4. Reference previous successful generations
5. Use edit command to maintain features across panels

## Integration with Claude Code

The Comic Artist sub-agent integrates seamlessly with Claude Code's workflow:

- **Automatic Delegation**: Claude Code recognizes image generation requests
- **Tool Access**: Uses Read, Write, Bash tools for complete workflow
- **Parallel Execution**: Can generate images while other tasks run
- **Context Awareness**: Understands project context and style requirements

## Next Steps

1. Test the sub-agent with a simple generation
2. Upload reference images for your project's style
3. Create a style guide document with effective prompts
4. Build a library of reference images
5. Experiment with different parameters

## Support

For issues or questions:
- Check this guide first
- Verify your setup (API key, build, Node.js version)
- Review the sub-agent configuration in `.claude/agents/comic-artist.md`
- Check OpenAI API status if generation fails

## API Costs

OpenAI's gpt-image-1 model charges per image generated:
- High quality: ~$0.04 per image
- Medium quality: ~$0.02 per image
- Low quality: ~$0.01 per image

Monitor your usage and costs through the OpenAI dashboard.
