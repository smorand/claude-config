# Video Creation Guide

## Creating Videos from Images

### Single Image to Video Clip

Convert static images to video clips with proper aspect ratio and padding:

```bash
# Landscape (16:9) - 1920x1080
ffmpeg -loop 1 -i image.jpg -t 7 \
  -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=30" \
  -c:v libx264 -preset fast -crf 23 -pix_fmt yuv420p output.mp4

# Portrait (9:16) - 1080x1920 for social media
ffmpeg -loop 1 -i image.png -t 5 \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,fps=30" \
  -c:v libx264 -preset fast -crf 23 -pix_fmt yuv420p output.mp4

# Square (1:1) - 1080x1080 for Instagram
ffmpeg -loop 1 -i photo.png -t 3 \
  -vf "scale=1080:1080:force_original_aspect_ratio=decrease,pad=1080:1080:(ow-iw)/2:(oh-ih)/2,fps=30" \
  -c:v libx264 -preset fast -crf 23 -pix_fmt yuv420p output.mp4
```

**Key parameters:**
- `-loop 1`: Loop the input image
- `-t DURATION`: Duration in seconds
- `scale=W:H:force_original_aspect_ratio=decrease`: Scale down to fit
- `pad=W:H:(ow-iw)/2:(oh-ih)/2`: Center with padding
- `fps=30`: Set frame rate
- `-pix_fmt yuv420p`: Ensure compatibility

### Slideshow from Multiple Images

```bash
# Simple slideshow (3 seconds per image)
ffmpeg -framerate 1/3 -pattern_type glob -i '*.jpg' \
  -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" \
  -c:v libx264 -crf 23 -pix_fmt yuv420p slideshow.mp4

# Slideshow with zoom/pan effect
ffmpeg -framerate 1/5 -pattern_type glob -i 'img*.jpg' \
  -vf "zoompan=d=125:fps=25,scale=1920:1080,fade=in:0:25:fade=out:100:25" \
  -c:v libx264 -crf 23 slideshow.mp4
```

## Video Transitions

### Two-Video Transition

Basic crossfade between two videos:

```bash
# Simple fade (1-second transition at 5-second mark)
ffmpeg -i video1.mp4 -i video2.mp4 -filter_complex \
  "[0:v][1:v]xfade=transition=fade:duration=1:offset=5[v]" \
  -map "[v]" output.mp4

# Dissolve transition
ffmpeg -i video1.mp4 -i video2.mp4 -filter_complex \
  "[0:v][1:v]xfade=transition=dissolve:duration=2:offset=8[v]" \
  -map "[v]" output.mp4
```

### Multi-Video Transition Chain

**CRITICAL: Offset Calculation**

Each xfade transition **overlaps** videos, making the output duration shorter than the sum of inputs. Always calculate the next offset from the **output duration** of the previous transition.

**Formula:**
```
offset = previous_output_duration - transition_duration
new_output_duration = previous_offset + next_video_duration
```

**Example: 3 videos with 2-second transitions**

Video durations:
- v0.mp4: 30 seconds
- v1.mp4: 12 seconds
- v2.mp4: 18 seconds

Offset calculations:
```
Transition 1 (v0 → v1):
  offset = 30 - 2 = 28s
  output_duration = 28 + 12 = 40s (NOT 42s!)

Transition 2 (output1 → v2):
  offset = 40 - 2 = 38s (NOT 40s!)
  output_duration = 38 + 18 = 56s

Final duration: 56 seconds (not 60s!)
```

**Correct FFmpeg command:**
```bash
ffmpeg -i v0.mp4 -i v1.mp4 -i v2.mp4 -filter_complex "\
  [0:v]setpts=PTS-STARTPTS[v0]; \
  [1:v]setpts=PTS-STARTPTS[v1]; \
  [2:v]setpts=PTS-STARTPTS[v2]; \
  [v0][v1]xfade=transition=dissolve:duration=2:offset=28[vout1]; \
  [vout1][v2]xfade=transition=dissolve:duration=2:offset=38[vout]" \
  -map "[vout]" output.mp4
```

**Common Mistakes:**

❌ **WRONG:** Using cumulative input durations
```
offset1 = 30 - 2 = 28 ✓
offset2 = 30 + 12 - 2 = 40 ✗ (Incorrect!)
```

✅ **CORRECT:** Using output duration after previous xfade
```
offset1 = 30 - 2 = 28 ✓
output1 = 28 + 12 = 40 ✓
offset2 = 40 - 2 = 38 ✓ (Correct!)
```

### Available Transition Types

- `fade`: Crossfade
- `fadeblack`: Fade to black
- `fadewhite`: Fade to white
- `dissolve`: Dissolve effect
- `wipeleft`, `wiperight`, `wipeup`, `wipedown`: Wipe transitions
- `slideleft`, `slideright`, `slideup`, `slidedown`: Slide transitions
- `circlecrop`: Circular crop transition
- `rectcrop`: Rectangular crop transition
- `distance`: Distance-based transition

## Mixing Images and Videos with Transitions

When combining images with videos, **always convert images to video clips first**:

```bash
# Step 1: Convert images to video clips
ffmpeg -loop 1 -i title.png -t 3 \
  -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=30" \
  -c:v libx264 -preset fast -crf 23 temp_title.mp4

ffmpeg -loop 1 -i logo.png -t 5 \
  -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=30" \
  -c:v libx264 -preset fast -crf 23 temp_logo.mp4

# Step 2: Create transitions between clips
# title (3s) → video (30s) → logo (5s)
# With 1-second transitions
ffmpeg -i temp_title.mp4 -i video.mp4 -i temp_logo.mp4 -filter_complex "\
  [0:v]setpts=PTS-STARTPTS[v0]; \
  [1:v]setpts=PTS-STARTPTS[v1]; \
  [2:v]setpts=PTS-STARTPTS[v2]; \
  [v0][v1]xfade=transition=dissolve:duration=1:offset=2[vout1]; \
  [vout1][v2]xfade=transition=dissolve:duration=1:offset=31[vout]" \
  -map "[vout]" output.mp4

# Offset calculations:
# T1: offset = 3 - 1 = 2, output = 2 + 30 = 32
# T2: offset = 32 - 1 = 31, output = 31 + 5 = 36s total
```

## Video Concatenation

### Simple Concatenation (Same Format)

Fast method using concat demuxer (no re-encoding):

```bash
# Create list file (list.txt):
# file 'video1.mp4'
# file 'video2.mp4'
# file 'video3.mp4'

ffmpeg -f concat -safe 0 -i list.txt -c copy output.mp4
```

### Concatenation with Re-encoding (Different Formats)

```bash
# Concatenate videos with different formats/codecs
ffmpeg -i video1.mp4 -i video2.avi -i video3.mov \
  -filter_complex "[0:v][0:a][1:v][1:a][2:v][2:a]concat=n=3:v=1:a=1[v][a]" \
  -map "[v]" -map "[a]" -c:v libx264 -crf 23 -c:a aac output.mp4
```

## Complete Example Workflows

### Workflow 1: Title → Video → Logo

```bash
# Durations: title=3s, video=30s, logo=5s
# Transition: 1s dissolve

# Convert images to clips
ffmpeg -loop 1 -i title.png -t 3 \
  -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=30" \
  -c:v libx264 -preset fast -crf 23 title.mp4

ffmpeg -loop 1 -i logo.png -t 5 \
  -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=30" \
  -c:v libx264 -preset fast -crf 23 logo.mp4

# Create transitions
# T1: offset = 3-1 = 2, output = 2+30 = 32
# T2: offset = 32-1 = 31, output = 31+5 = 36s
ffmpeg -i title.mp4 -i video.mp4 -i logo.mp4 -filter_complex "\
  [0:v]setpts=PTS-STARTPTS[v0]; \
  [1:v]setpts=PTS-STARTPTS[v1]; \
  [2:v]setpts=PTS-STARTPTS[v2]; \
  [v0][v1]xfade=transition=dissolve:duration=1:offset=2[vout1]; \
  [vout1][v2]xfade=transition=dissolve:duration=1:offset=31[vout]" \
  -map "[vout]" -c:v libx264 -crf 23 -pix_fmt yuv420p final.mp4
```

### Workflow 2: Multiple Video Segments with Cuts

```bash
# Four segments: intro (10s), segment1 (20s), segment2 (15s), outro (8s)
# 2-second transitions between each

# Offset calculations:
# T1: offset = 10-2 = 8, output = 8+20 = 28
# T2: offset = 28-2 = 26, output = 26+15 = 41
# T3: offset = 41-2 = 39, output = 39+8 = 47s total

ffmpeg -i intro.mp4 -i seg1.mp4 -i seg2.mp4 -i outro.mp4 -filter_complex "\
  [0:v]setpts=PTS-STARTPTS[v0]; \
  [1:v]setpts=PTS-STARTPTS[v1]; \
  [2:v]setpts=PTS-STARTPTS[v2]; \
  [3:v]setpts=PTS-STARTPTS[v3]; \
  [v0][v1]xfade=transition=fade:duration=2:offset=8[vout1]; \
  [vout1][v2]xfade=transition=fade:duration=2:offset=26[vout2]; \
  [vout2][v3]xfade=transition=fade:duration=2:offset=39[vout]" \
  -map "[vout]" -c:v libx264 -crf 23 final.mp4
```

## Best Practices

1. **Always convert images to video clips first** before using in transitions
2. **Calculate offsets from output durations**, not cumulative input durations
3. **Use consistent resolution and frame rate** across all clips
4. **Use `-pix_fmt yuv420p`** for maximum compatibility
5. **Test with short clips first** before processing full videos
6. **Keep track of durations** in comments for complex chains
