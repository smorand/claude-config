# Advanced Techniques Guide

## Advanced Filters

### Text Overlays

```bash
# Basic text overlay
ffmpeg -i input.mp4 \
  -vf "drawtext=text='Hello World':fontsize=24:fontcolor=white:x=10:y=10" \
  output.mp4

# Text with background box
ffmpeg -i input.mp4 \
  -vf "drawtext=text='Title':fontsize=48:fontcolor=white:x=10:y=10:box=1:boxcolor=black@0.5:boxborderw=5" \
  output.mp4

# Centered text
ffmpeg -i input.mp4 \
  -vf "drawtext=text='Centered':fontsize=36:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2" \
  output.mp4

# Dynamic timestamp
ffmpeg -i input.mp4 \
  -vf "drawtext=text='%{pts\:hms}':fontsize=20:fontcolor=yellow:x=10:y=10" \
  output.mp4

# Text from file
ffmpeg -i input.mp4 \
  -vf "drawtext=textfile=subtitle.txt:fontsize=24:fontcolor=white:x=10:y=h-50" \
  output.mp4
```

### Watermarks and Logos

```bash
# Simple watermark (top-left)
ffmpeg -i video.mp4 -i logo.png \
  -filter_complex "overlay=10:10" \
  output.mp4

# Watermark (bottom-right with margin)
ffmpeg -i video.mp4 -i logo.png \
  -filter_complex "overlay=main_w-overlay_w-10:main_h-overlay_h-10" \
  output.mp4

# Semi-transparent watermark
ffmpeg -i video.mp4 -i logo.png \
  -filter_complex "[1:v]format=rgba,colorchannelmixer=aa=0.5[logo];[0:v][logo]overlay=10:10" \
  output.mp4

# Watermark with scaling
ffmpeg -i video.mp4 -i logo.png \
  -filter_complex "[1:v]scale=200:-1[logo];[0:v][logo]overlay=10:10" \
  output.mp4
```

### Visual Effects

#### Blur Effects

```bash
# Box blur
ffmpeg -i input.mp4 -vf "boxblur=5:1" output.mp4

# Gaussian blur
ffmpeg -i input.mp4 -vf "gblur=sigma=5" output.mp4

# Blur specific region
ffmpeg -i input.mp4 \
  -vf "boxblur=enable='between(t,5,10)':5:1" \
  output.mp4
```

#### Color Adjustments

```bash
# Brightness/Contrast
ffmpeg -i input.mp4 \
  -vf "eq=brightness=0.1:contrast=1.2" \
  output.mp4

# Saturation
ffmpeg -i input.mp4 \
  -vf "eq=saturation=1.5" \
  output.mp4

# Black & white
ffmpeg -i input.mp4 \
  -vf "hue=s=0" \
  output.mp4

# Sepia tone
ffmpeg -i input.mp4 \
  -vf "colorchannelmixer=.393:.769:.189:0:.349:.686:.168:0:.272:.534:.131" \
  output.mp4

# Color temperature adjustment
ffmpeg -i input.mp4 \
  -vf "colortemperature=temperature=6500" \
  output.mp4
```

#### Rotation and Flipping

```bash
# Rotate 90° clockwise
ffmpeg -i input.mp4 -vf "transpose=1" output.mp4

# Rotate 90° counter-clockwise
ffmpeg -i input.mp4 -vf "transpose=2" output.mp4

# Rotate 180°
ffmpeg -i input.mp4 -vf "transpose=2,transpose=2" output.mp4

# Horizontal flip
ffmpeg -i input.mp4 -vf "hflip" output.mp4

# Vertical flip
ffmpeg -i input.mp4 -vf "vflip" output.mp4

# Arbitrary rotation (45 degrees)
ffmpeg -i input.mp4 -vf "rotate=45*PI/180" output.mp4
```

### Advanced Cropping

```bash
# Center crop to 16:9
ffmpeg -i input.mp4 \
  -vf "crop=ih*16/9:ih" \
  output.mp4

# Auto-detect crop (remove black bars)
ffmpeg -i input.mp4 \
  -vf "cropdetect=24:16:0" \
  -f null -
# Then use detected values:
ffmpeg -i input.mp4 -vf "crop=1920:800:0:140" output.mp4

# Dynamic crop (tracking)
ffmpeg -i input.mp4 \
  -vf "crop=640:480:x='if(gte(t,5),(w-640)/2,0)':y=0" \
  output.mp4
```

## Multi-track Processing

### Picture-in-Picture

```bash
# Basic PiP (small video in corner)
ffmpeg -i main.mp4 -i pip.mp4 \
  -filter_complex "[1:v]scale=320:180[pip];[0:v][pip]overlay=main_w-overlay_w-10:main_h-overlay_h-10" \
  output.mp4

# PiP with border
ffmpeg -i main.mp4 -i pip.mp4 \
  -filter_complex "[1:v]scale=320:180,pad=330:190:5:5:white[pip];[0:v][pip]overlay=10:10" \
  output.mp4

# Animated PiP (moving)
ffmpeg -i main.mp4 -i pip.mp4 \
  -filter_complex "[1:v]scale=320:180[pip];[0:v][pip]overlay='x=if(gte(t,2),10+100*(t-2)/5,10):y=10'" \
  output.mp4
```

### Split Screen

```bash
# Horizontal split (2 videos side-by-side)
ffmpeg -i left.mp4 -i right.mp4 \
  -filter_complex "[0:v]scale=960:1080[left];[1:v]scale=960:1080[right];[left][right]hstack" \
  output.mp4

# Vertical split (2 videos stacked)
ffmpeg -i top.mp4 -i bottom.mp4 \
  -filter_complex "[0:v]scale=1920:540[top];[1:v]scale=1920:540[bottom];[top][bottom]vstack" \
  output.mp4

# 4-way split
ffmpeg -i v1.mp4 -i v2.mp4 -i v3.mp4 -i v4.mp4 \
  -filter_complex "\
    [0:v]scale=960:540[v1];\
    [1:v]scale=960:540[v2];\
    [2:v]scale=960:540[v3];\
    [3:v]scale=960:540[v4];\
    [v1][v2]hstack[top];\
    [v3][v4]hstack[bottom];\
    [top][bottom]vstack" \
  output.mp4
```

## Time Manipulation

### Speed Changes

```bash
# 2x speed (video and audio)
ffmpeg -i input.mp4 \
  -filter:v "setpts=0.5*PTS" \
  -filter:a "atempo=2.0" \
  output.mp4

# 0.5x speed (slow motion)
ffmpeg -i input.mp4 \
  -filter:v "setpts=2.0*PTS" \
  -filter:a "atempo=0.5" \
  output.mp4

# Variable speed (speed up specific section)
ffmpeg -i input.mp4 \
  -filter_complex "\
    [0:v]trim=0:5,setpts=PTS-STARTPTS[v1];\
    [0:v]trim=5:15,setpts=0.5*(PTS-STARTPTS)[v2];\
    [0:v]trim=15,setpts=PTS-STARTPTS[v3];\
    [v1][v2][v3]concat=n=3:v=1[v]" \
  -map "[v]" output.mp4
```

### Reverse Video

```bash
# Reverse video (with audio)
ffmpeg -i input.mp4 \
  -vf reverse -af areverse \
  output.mp4

# Reverse only video
ffmpeg -i input.mp4 \
  -vf reverse \
  output.mp4
```

### Looping

```bash
# Loop video 3 times
ffmpeg -stream_loop 3 -i input.mp4 -c copy output.mp4

# Loop with filter (smoother)
ffmpeg -i input.mp4 \
  -filter_complex "loop=loop=3:size=1:start=0" \
  output.mp4
```

## Advanced Audio

### Audio Visualization

```bash
# Waveform visualization
ffmpeg -i audio.mp3 \
  -filter_complex "showwaves=s=1920x1080:mode=line:rate=30" \
  -c:v libx264 -crf 23 waveform.mp4

# Spectrum analyzer
ffmpeg -i audio.mp3 \
  -filter_complex "showspectrum=s=1920x1080:mode=combined:color=rainbow" \
  -c:v libx264 -crf 23 spectrum.mp4

# Frequency bars
ffmpeg -i audio.mp3 \
  -filter_complex "showfreqs=s=1920x1080:mode=bar:cmode=combined" \
  -c:v libx264 -crf 23 freqs.mp4
```

### Audio Filters

```bash
# Bass boost
ffmpeg -i input.mp3 \
  -af "equalizer=f=100:width_type=h:width=50:g=3" \
  output.mp3

# Treble boost
ffmpeg -i input.mp3 \
  -af "equalizer=f=10000:width_type=h:width=2000:g=3" \
  output.mp3

# Noise reduction
ffmpeg -i input.mp3 \
  -af "highpass=f=200,lowpass=f=3000" \
  output.mp3

# Normalize audio levels
ffmpeg -i input.mp3 \
  -af "loudnorm=I=-16:TP=-1.5:LRA=11" \
  output.mp3
```

## Batch Processing

### Process Multiple Files

```bash
# Convert all videos in directory
for file in *.mp4; do
  ffmpeg -i "$file" -c:v libx264 -crf 23 "converted_${file}"
done

# Batch resize
for file in *.mp4; do
  ffmpeg -i "$file" -vf scale=1280:720 "720p_${file}"
done

# Process with different outputs
for file in *.mp4; do
  base="${file%.*}"
  # YouTube version
  ffmpeg -i "$file" -vf scale=1920:1080 -crf 18 "${base}_youtube.mp4"
  # Instagram version
  ffmpeg -i "$file" -vf scale=1080:1080 -crf 23 "${base}_instagram.mp4"
  # TikTok version
  ffmpeg -i "$file" -vf scale=1080:1920 -crf 23 "${base}_tiktok.mp4"
done
```

### Parallel Processing

```bash
# Process files in parallel (using GNU parallel)
parallel -j 4 ffmpeg -i {} -c:v libx264 -crf 23 converted_{} ::: *.mp4

# Or with xargs
find . -name "*.mp4" | xargs -P 4 -I {} ffmpeg -i {} -c:v libx264 -crf 23 converted_{}
```

## Hardware Acceleration

### NVIDIA NVENC

```bash
# H.264 with NVENC
ffmpeg -hwaccel cuda -i input.mp4 \
  -c:v h264_nvenc -preset fast -crf 23 \
  -c:a copy output.mp4

# H.265 with NVENC
ffmpeg -hwaccel cuda -i input.mp4 \
  -c:v hevc_nvenc -preset fast -crf 23 \
  -c:a copy output.mp4
```

### Intel Quick Sync

```bash
# H.264 with QSV
ffmpeg -hwaccel qsv -i input.mp4 \
  -c:v h264_qsv -preset fast -global_quality 23 \
  -c:a copy output.mp4
```

### Apple VideoToolbox (macOS)

```bash
# H.264 with VideoToolbox
ffmpeg -hwaccel videotoolbox -i input.mp4 \
  -c:v h264_videotoolbox -b:v 5M \
  -c:a copy output.mp4
```

## Quality Optimization

### Two-Pass Encoding

For best quality at target file size:

```bash
# Pass 1
ffmpeg -i input.mp4 -c:v libx264 -b:v 5M -pass 1 -f null /dev/null

# Pass 2
ffmpeg -i input.mp4 -c:v libx264 -b:v 5M -pass 2 -c:a aac output.mp4
```

### Constant Quality with Max Bitrate

```bash
ffmpeg -i input.mp4 \
  -c:v libx264 -crf 23 -maxrate 5M -bufsize 10M \
  -c:a aac output.mp4
```

## Advanced Workflows

### Multi-format Export Script

```bash
#!/bin/bash
INPUT="$1"
BASE="${INPUT%.*}"

# YouTube 1080p
ffmpeg -i "$INPUT" \
  -vf scale=1920:1080 -c:v libx264 -preset slow -crf 18 \
  -c:a aac -b:a 192k "${BASE}_youtube.mp4"

# Instagram Feed
ffmpeg -i "$INPUT" \
  -vf scale=1080:1080 -c:v libx264 -crf 23 \
  -c:a aac -b:a 128k -t 60 "${BASE}_instagram.mp4"

# TikTok
ffmpeg -i "$INPUT" \
  -vf scale=1080:1920 -c:v libx264 -crf 23 \
  -c:a aac -b:a 128k "${BASE}_tiktok.mp4"

# Twitter
ffmpeg -i "$INPUT" \
  -vf scale=1920:1080 -c:v libx264 -crf 23 \
  -c:a aac -b:a 128k -t 140 "${BASE}_twitter.mp4"
```

### Complex Filter Graph

Example combining multiple effects:

```bash
ffmpeg -i input.mp4 -i logo.png \
  -filter_complex "\
    [0:v]scale=1920:1080,eq=brightness=0.1:contrast=1.1[scaled];\
    [1:v]scale=100:-1,format=rgba,colorchannelmixer=aa=0.7[logo];\
    [scaled][logo]overlay=main_w-overlay_w-10:10[watermarked];\
    [watermarked]drawtext=text='Title':fontsize=48:fontcolor=white:x=(w-text_w)/2:y=20[v]" \
  -map "[v]" -map 0:a \
  -c:v libx264 -preset medium -crf 23 \
  -c:a copy output.mp4
```

## Best Practices

1. **Test filters on short clips** before processing full videos
2. **Use hardware acceleration** when available for faster processing
3. **Monitor CPU/GPU usage** during batch processing
4. **Save filter chains** in separate files for reuse
5. **Document complex filter graphs** with comments
6. **Use two-pass encoding** for target file sizes
7. **Check output quality** before deleting source files
8. **Keep source files** until final output is verified
