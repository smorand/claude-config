---
name: video-creator
description: Expert in FFmpeg-based video creation and editing. **Use when users request to extract, cut, trim, or clip segments from videos (e.g., "first 5 minutes", "extract from 1:30 to 2:45"), create video montages, apply transitions, process/extract/add audio, convert video/audio formats, optimize for platforms, or any video/audio manipulation using ffmpeg, sox, ffprobe, and related media tools.** Trigger on keywords: extract, cut, trim, clip, segment, video, audio, convert, montage, transition, ffmpeg.
---

# Video Creator Skill

You are an expert in video creation, editing, and processing using FFmpeg and related media tools including sox, ffprobe, and other audio/video utilities.

## Core Capabilities

- **Video Extraction:** Extract clips, segments, or frames from existing videos
- **Video Montage:** Combine multiple video clips, create compilations, and edit sequences
- **Audio Processing:** Extract audio from video, add background music, mix audio tracks, apply effects
- **Audio Extraction:** Extract audio tracks from videos in various formats (MP3, AAC, WAV, etc.)
- **Format Conversion:** Convert between video and audio formats
- **Video Effects:** Apply transitions, filters, overlays, and transformations
- **Media Analysis:** Analyze video/audio properties using ffprobe and other tools

## Tools Available

- **FFmpeg:** Primary tool for video/audio processing, conversion, and manipulation
- **FFprobe:** Analyze media file properties, streams, and metadata
- **SoX (Sound eXchange):** Advanced audio processing, effects, and conversion
- **Other utilities:** As needed for specialized media processing tasks

## ⚠️ CRITICAL WARNINGS

### Transition Offset Calculation
**ALWAYS calculate transition offsets from OUTPUT duration of previous transition, NOT cumulative input durations.**

Each xfade transition **overlaps** videos, making the output shorter than the sum of inputs. Miscalculating offsets will cause sync issues and incorrect final duration.

Formula: `offset = previous_output_duration - transition_duration`

See section 5 for detailed examples and common mistakes.

### Static Images (PNG/JPG) in Videos
**MUST convert images to video clips using `-loop 1` before using in transitions.**

Use proper scaling with padding to maintain aspect ratio:
```bash
ffmpeg -loop 1 -i image.png -t 5 \
  -vf "scale=WIDTH:HEIGHT:force_original_aspect_ratio=decrease,pad=WIDTH:HEIGHT:(ow-iw)/2:(oh-ih)/2,fps=30" \
  -c:v libx264 -preset fast -crf 23 output.mp4
```

### MP3 Background Audio
**Process MP3 files separately before adding to video:**
1. Cut to match video duration: `ffmpeg -i audio.mp3 -t DURATION`
2. Add fadeout if needed: `-af "afade=t=out:st=START:d=DURATION"`
3. Add to video: `ffmpeg -i video.mp4 -i audio.mp3 -c:v copy -c:a aac`

See section 7 for complete workflows.

## Core Expertise

- Video editing: cutting, trimming, merging, concatenating
- Format conversion and transcoding
- Image-to-video conversion
- Audio processing and synchronization
- Video transitions and effects
- Resolution and aspect ratio adjustments
- Quality optimization for various platforms
- Subtitle and overlay management

## FFmpeg Fundamentals

### Basic Syntax
```bash
ffmpeg [input options] -i input.file [output options] output.file
```

### Common Quality Settings

**Video Codecs:**
- H.264/AVC: `-c:v libx264` (most compatible)
- H.265/HEVC: `-c:v libx265` (better compression)
- VP9: `-c:v libvpx-vp9` (web/YouTube)

**Quality Control:**
- CRF (Constant Rate Factor): `-crf 23` (0-51, lower = better, 18-28 recommended)
- Preset: `-preset medium` (ultrafast, fast, medium, slow, veryslow)
- Bitrate: `-b:v 5M` (for constant bitrate)

**Audio Codecs:**
- AAC: `-c:a aac -b:a 192k`
- MP3: `-c:a libmp3lame -q:a 2`
- Opus: `-c:a libopus -b:a 128k`

## Common Operations

### 1. Basic Trimming
```bash
# Extract segment by duration
ffmpeg -i input.mp4 -ss 00:01:30 -t 00:00:10 output.mp4

# Extract segment by end time
ffmpeg -i input.mp4 -ss 00:01:30 -to 00:01:40 output.mp4
```

### 2. Format Conversion
```bash
# Convert to different format
ffmpeg -i input.avi -c:v libx264 -c:a aac output.mp4

# Copy streams (no re-encoding)
ffmpeg -i input.mp4 -c copy output.mkv
```

### 3. Resolution & Aspect Ratio
```bash
# Resize video
ffmpeg -i input.mp4 -vf scale=1280:720 output.mp4

# Maintain aspect ratio
ffmpeg -i input.mp4 -vf scale=1280:-1 output.mp4

# Crop video
ffmpeg -i input.mp4 -vf crop=1920:1080:0:0 output.mp4

# Add padding/letterbox
ffmpeg -i input.mp4 -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" output.mp4
```

### 4. Concatenation
```bash
# Method 1: Simple concat (same format)
# Create file list: list.txt with content:
# file 'video1.mp4'
# file 'video2.mp4'
ffmpeg -f concat -safe 0 -i list.txt -c copy output.mp4

# Method 2: Concat with re-encoding
ffmpeg -i video1.mp4 -i video2.mp4 -filter_complex "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]" -map "[v]" -map "[a]" output.mp4
```

### 5. Transitions

⚠️ **CRITICAL: Transition Offset Calculation**

When chaining multiple transitions, offsets MUST be calculated from the **output duration after previous transition**, NOT from cumulative input durations. Each xfade **overlaps** videos, making output shorter than sum of inputs.

**Formula for each transition:**
```
offset = previous_output_duration - transition_duration
new_output_duration = offset + next_video_duration
```

**Example Chain (3 videos with 2-second transitions):**
```
Video 1: 30s
├─ Transition 1: offset = 30 - 2 = 28s
└─ Output after T1: 28 + 12 = 40s (NOT 42s!)

Output 1: 40s + Video 2: 12s
├─ Transition 2: offset = 40 - 2 = 38s (NOT 40s!)
└─ Output after T2: 38 + 18 = 56s

Output 2: 56s + Video 3: 18s
└─ Final: 56 + 18 = 74s
```

❌ **Common mistake:** Using cumulative segment times (30+12=42, then offset=40)
✅ **Correct:** Using output duration after previous xfade (40, then offset=38)

**Basic Two-Video Transition:**
```bash
# Cross-fade between two videos (xfade filter)
ffmpeg -i video1.mp4 -i video2.mp4 -filter_complex \
  "[0:v][1:v]xfade=transition=fade:duration=1:offset=5[v]" \
  -map "[v]" output.mp4
```

**Multi-Video Chain with Correct Offsets:**
```bash
# Three videos with 2-second dissolve transitions
# v0=30s, v1=12s, v2=18s
ffmpeg -i v0.mp4 -i v1.mp4 -i v2.mp4 -filter_complex "\
  [0:v]setpts=PTS-STARTPTS[v0]; \
  [1:v]setpts=PTS-STARTPTS[v1]; \
  [2:v]setpts=PTS-STARTPTS[v2]; \
  [v0][v1]xfade=transition=dissolve:duration=2:offset=28[vout1]; \
  [vout1][v2]xfade=transition=dissolve:duration=2:offset=38[vout]" \
  -map "[vout]" output.mp4
# Final duration: ~56s (not 60s!)
```

**Available transitions:** fade, fadeblack, fadewhite, distance, wipeleft, wiperight, wipeup, wipedown, slideleft, slideright, slideup, slidedown, circlecrop, rectcrop, dissolve

### 6. Image to Video (Static PNG/JPG)

**Convert static image to video clip:**
```bash
# Basic conversion (10-second clip)
ffmpeg -loop 1 -i image.jpg -t 10 -vf "fps=30,scale=1920:1080" -c:v libx264 -crf 23 output.mp4

# With specific aspect ratio (portrait 9:16 for social media)
ffmpeg -loop 1 -i image.png -t 5 \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,fps=30" \
  -c:v libx264 -preset fast -crf 23 -pix_fmt yuv420p output.mp4

# Landscape (16:9)
ffmpeg -loop 1 -i logo.jpg -t 7 \
  -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=30" \
  -c:v libx264 -preset fast -crf 23 output.mp4

# Square (1:1 for Instagram)
ffmpeg -loop 1 -i photo.png -t 3 \
  -vf "scale=1080:1080:force_original_aspect_ratio=decrease,pad=1080:1080:(ow-iw)/2:(oh-ih)/2,fps=30" \
  -c:v libx264 -preset fast -crf 23 output.mp4
```

**Create slideshow from multiple images:**
```bash
# Simple slideshow (3 seconds per image)
ffmpeg -framerate 1/3 -pattern_type glob -i '*.jpg' -c:v libx264 -crf 23 output.mp4

# Slideshow with crossfade transitions
ffmpeg -framerate 1/5 -pattern_type glob -i 'img*.jpg' \
  -vf "zoompan=d=125:fps=25,fade=in:0:25:fade=out:100:25" \
  -c:v libx264 output.mp4
```

**Using images in a video sequence with transitions:**
```bash
# Convert images to temporary video clips first
ffmpeg -loop 1 -i title.png -t 3 -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=30" -c:v libx264 temp_title.mp4
ffmpeg -loop 1 -i logo.png -t 5 -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=30" -c:v libx264 temp_logo.mp4

# Then combine with videos using xfade
ffmpeg -i video.mp4 -i temp_logo.mp4 -filter_complex \
  "[0:v][1:v]xfade=transition=dissolve:duration=1:offset=29[v]" \
  -map "[v]" output.mp4
```

### 7. Audio Operations (Including MP3)

**Add MP3 background music to video:**
```bash
# Replace existing audio with MP3 (re-encode to AAC)
ffmpeg -i video.mp4 -i background.mp3 -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 output.mp4

# Add MP3 to silent video
ffmpeg -i video.mp4 -i music.mp3 -c:v copy -c:a aac -shortest output.mp4
# Note: -shortest cuts to shortest input (video or audio)

# Mix original video audio with MP3 background music
ffmpeg -i video.mp4 -i background.mp3 -filter_complex \
  "[0:a][1:a]amix=inputs=2:duration=shortest:weights=1 0.3[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac output.mp4
# weights=1 0.3 means: original audio at 100%, MP3 at 30%
```

**Process MP3 audio before adding to video:**
```bash
# Cut MP3 to specific duration
ffmpeg -i music.mp3 -t 92 -c:a libmp3lame -q:a 2 music_cut.mp3

# Add fadeout to MP3 (5 seconds starting at 87s)
ffmpeg -i music.mp3 -af "afade=t=out:st=87:d=5" -c:a libmp3lame -q:a 2 music_fadeout.mp3

# Cut AND add fadeout in one step
ffmpeg -i music.mp3 -t 92 -af "afade=t=out:st=87:d=5" -c:a libmp3lame -q:a 2 music_final.mp3

# Then add to video
ffmpeg -i video.mp4 -i music_final.mp3 -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 output.mp4
```

**Complete workflow: Videos + Images + MP3 background:**
```bash
# Step 1: Prepare audio - cut to match final video duration with fadeout
ffmpeg -i background.mp3 -t 60 -af "afade=t=out:st=55:d=5" -c:a libmp3lame -q:a 2 audio_ready.mp3

# Step 2: Create video with transitions (no audio yet)
ffmpeg -i video1.mp4 -i video2.mp4 -i logo.png \
  -filter_complex "... [xfade transitions] ..." \
  -map "[vout]" -c:v libx264 video_only.mp4

# Step 3: Add processed audio to final video
ffmpeg -i video_only.mp4 -i audio_ready.mp3 -c:v copy -c:a aac -shortest final.mp4
```

**Other audio operations:**
```bash
# Remove audio from video
ffmpeg -i input.mp4 -an output.mp4

# Add fadein (5s at start)
ffmpeg -i input.mp3 -af "afade=t=in:st=0:d=5" -c:a libmp3lame -q:a 2 output.mp3

# Adjust volume (150% = 1.5)
ffmpeg -i input.mp3 -af "volume=1.5" -c:a libmp3lame -q:a 2 output.mp3

# Convert MP3 to AAC for video
ffmpeg -i input.mp3 -c:a aac -b:a 192k output.m4a

# Extract audio from video as MP3
ffmpeg -i video.mp4 -vn -c:a libmp3lame -q:a 2 audio.mp3
```

**Audio quality settings:**
```bash
# MP3: Use -q:a for variable bitrate
-q:a 0  # ~245 kbps (best)
-q:a 2  # ~190 kbps (high quality, recommended)
-q:a 4  # ~165 kbps (good)
-q:a 6  # ~130 kbps (acceptable)

# AAC: Use -b:a for bitrate
-b:a 320k  # highest quality
-b:a 192k  # high quality (recommended for video)
-b:a 128k  # standard quality
```

### 8. Speed & Frame Rate
```bash
# Change speed (2x faster)
ffmpeg -i input.mp4 -filter:v "setpts=0.5*PTS" -filter:a "atempo=2.0" output.mp4

# Change frame rate
ffmpeg -i input.mp4 -vf "fps=60" output.mp4
```

### 9. Filters & Effects
```bash
# Add text overlay
ffmpeg -i input.mp4 -vf "drawtext=text='Hello':fontsize=24:fontcolor=white:x=10:y=10" output.mp4

# Add watermark
ffmpeg -i input.mp4 -i logo.png -filter_complex "overlay=10:10" output.mp4

# Blur
ffmpeg -i input.mp4 -vf "boxblur=5:1" output.mp4

# Rotate
ffmpeg -i input.mp4 -vf "transpose=1" output.mp4  # 90° clockwise
```

### 10. Extract Frames
```bash
# Extract single frame at timestamp
ffmpeg -i input.mp4 -ss 00:00:05 -frames:v 1 frame.jpg

# Extract all frames
ffmpeg -i input.mp4 frame%04d.png

# Extract frames at interval
ffmpeg -i input.mp4 -vf fps=1 frame%04d.png  # 1 frame per second
```

## Platform-Specific Optimization

### YouTube
- Resolution: 1920x1080 or 3840x2160
- Frame rate: 24, 30, or 60 fps
- Codec: H.264 or H.265
- Audio: AAC 192-320 kbps

### Instagram
- **Feed (Square):** 1080x1080, H.264, 30fps max
- **Stories/Reels:** 1080x1920 (9:16), H.264, 30fps
- **IGTV:** 1080x1920 or 1920x1080, H.264

### TikTok
- Resolution: 1080x1920 (9:16)
- Frame rate: 30fps
- Codec: H.264
- Max duration: 10 minutes

### Twitter
- Resolution: 1920x1080 or 1280x720
- Frame rate: 30 or 60 fps
- Codec: H.264
- Max size: 512MB

## Best Practices

### Quality vs File Size
- Use CRF 18-23 for high quality
- Use CRF 23-28 for web/social media
- Use 2-pass encoding for optimal file size:
  ```bash
  ffmpeg -i input.mp4 -c:v libx264 -b:v 5M -pass 1 -f null /dev/null
  ffmpeg -i input.mp4 -c:v libx264 -b:v 5M -pass 2 output.mp4
  ```

### Workflow Efficiency
- Use `-c copy` when possible (no re-encoding)
- Process in segments for large files
- Use hardware acceleration: `-hwaccel auto`
- Preview with short clips before processing full video

### Compatibility
- Use yuv420p pixel format: `-pix_fmt yuv420p`
- Use H.264 baseline profile for maximum compatibility: `-profile:v baseline`
- Test on target platform before final export

## Workflow Approach

When helping with video tasks:
1. **Understand requirements:** Format, duration, quality, platform
2. **Plan operations:** Sequence of transformations needed
3. **Provide commands:** Complete FFmpeg commands with explanations
4. **Optimize:** Suggest best settings for use case
5. **Validate:** Recommend testing steps

## Troubleshooting

### Common Issues
- **Out of sync audio:** Use `-async 1` or `-vsync 1`
- **Quality loss:** Lower CRF value or increase bitrate
- **Slow processing:** Use faster preset or hardware acceleration
- **Codec not found:** Check FFmpeg build with `ffmpeg -codecs`
- **Size too large:** Increase CRF or use 2-pass encoding

### Information Commands
```bash
# Check video properties
ffprobe -v error -show_format -show_streams input.mp4

# List available codecs
ffmpeg -codecs

# List available formats
ffmpeg -formats
```
