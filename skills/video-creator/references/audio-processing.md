# Audio Processing Guide

## Audio Extraction

### Extract Audio from Video

```bash
# Extract as MP3 (variable bitrate)
ffmpeg -i video.mp4 -vn -c:a libmp3lame -q:a 2 audio.mp3

# Extract as AAC
ffmpeg -i video.mp4 -vn -c:a aac -b:a 192k audio.m4a

# Extract as WAV (uncompressed)
ffmpeg -i video.mp4 -vn -c:a pcm_s16le audio.wav

# Extract as Opus (efficient for web)
ffmpeg -i video.mp4 -vn -c:a libopus -b:a 128k audio.opus
```

**Audio quality parameters:**

**MP3 (variable bitrate with `-q:a`):**
- `-q:a 0`: ~245 kbps (best quality)
- `-q:a 2`: ~190 kbps (high quality, recommended)
- `-q:a 4`: ~165 kbps (good quality)
- `-q:a 6`: ~130 kbps (acceptable)
- `-q:a 9`: ~65 kbps (low quality)

**AAC (constant bitrate with `-b:a`):**
- `-b:a 320k`: Highest quality
- `-b:a 192k`: High quality (recommended for video)
- `-b:a 128k`: Standard quality
- `-b:a 96k`: Lower quality

## Adding Audio to Video

### Replace Video Audio with MP3

```bash
# Replace existing audio (re-encode to AAC)
ffmpeg -i video.mp4 -i background.mp3 \
  -c:v copy -c:a aac -b:a 192k \
  -map 0:v:0 -map 1:a:0 output.mp4

# Add audio to silent video
ffmpeg -i video.mp4 -i music.mp3 \
  -c:v copy -c:a aac -b:a 192k \
  -shortest output.mp4
# -shortest: Cut to shortest input (video or audio)
```

### Mix Video Audio with Background Music

```bash
# Mix original audio with background music
# Original at 100%, background at 30%
ffmpeg -i video.mp4 -i background.mp3 -filter_complex \
  "[0:a][1:a]amix=inputs=2:duration=shortest:weights=1 0.3[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k output.mp4

# Mix at equal volumes (50% each)
ffmpeg -i video.mp4 -i music.mp3 -filter_complex \
  "[0:a][1:a]amix=inputs=2:duration=shortest:weights=0.5 0.5[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac output.mp4
```

**Weight values:**
- `weights=1 0.3`: Original 100%, background 30%
- `weights=1 0.5`: Original 100%, background 50%
- `weights=0.7 0.3`: Original 70%, background 30%
- `weights=0.5 0.5`: Both at 50%

## Processing MP3 Files

### Cutting Audio

```bash
# Cut to specific duration
ffmpeg -i music.mp3 -t 60 -c:a libmp3lame -q:a 2 music_cut.mp3

# Cut by start time and duration
ffmpeg -i music.mp3 -ss 00:00:30 -t 00:01:00 \
  -c:a libmp3lame -q:a 2 music_segment.mp3

# Cut by start and end time
ffmpeg -i music.mp3 -ss 00:00:30 -to 00:01:30 \
  -c:a libmp3lame -q:a 2 music_segment.mp3
```

### Audio Fade Effects

```bash
# Fade in (5 seconds at start)
ffmpeg -i music.mp3 -af "afade=t=in:st=0:d=5" \
  -c:a libmp3lame -q:a 2 music_fadein.mp3

# Fade out (5 seconds ending at 60s)
ffmpeg -i music.mp3 -af "afade=t=out:st=55:d=5" \
  -c:a libmp3lame -q:a 2 music_fadeout.mp3

# Both fade in and fade out
ffmpeg -i music.mp3 -af "afade=t=in:st=0:d=5,afade=t=out:st=55:d=5" \
  -c:a libmp3lame -q:a 2 music_fades.mp3

# Cut to duration WITH fadeout
ffmpeg -i music.mp3 -t 60 -af "afade=t=out:st=55:d=5" \
  -c:a libmp3lame -q:a 2 music_ready.mp3
```

**Fade parameters:**
- `t=in`: Fade in
- `t=out`: Fade out
- `st=START`: Start time in seconds
- `d=DURATION`: Fade duration in seconds

### Volume Adjustment

```bash
# Increase volume (150%)
ffmpeg -i music.mp3 -af "volume=1.5" \
  -c:a libmp3lame -q:a 2 music_louder.mp3

# Decrease volume (50%)
ffmpeg -i music.mp3 -af "volume=0.5" \
  -c:a libmp3lame -q:a 2 music_quieter.mp3

# Normalize audio (auto-adjust to optimal level)
ffmpeg -i music.mp3 -af "loudnorm" \
  -c:a libmp3lame -q:a 2 music_normalized.mp3
```

### Audio Format Conversion

```bash
# MP3 to AAC
ffmpeg -i input.mp3 -c:a aac -b:a 192k output.m4a

# AAC to MP3
ffmpeg -i input.m4a -c:a libmp3lame -q:a 2 output.mp3

# WAV to MP3
ffmpeg -i input.wav -c:a libmp3lame -q:a 2 output.mp3

# Any format to MP3 (high quality)
ffmpeg -i input.* -c:a libmp3lame -q:a 2 output.mp3
```

## Complete Audio + Video Workflows

### Workflow 1: Videos with Background Music

Process audio separately, then add to video:

```bash
# Step 1: Process audio - cut to video duration and add fadeout
ffmpeg -i background.mp3 -t 92 -af "afade=t=out:st=87:d=5" \
  -c:a libmp3lame -q:a 2 audio_ready.mp3

# Step 2: Create video with transitions (no audio)
ffmpeg -i video1.mp4 -i video2.mp4 -filter_complex \
  "[0:v][1:v]xfade=transition=dissolve:duration=2:offset=30[vout]" \
  -map "[vout]" -c:v libx264 -crf 23 video_only.mp4

# Step 3: Add processed audio to final video
ffmpeg -i video_only.mp4 -i audio_ready.mp3 \
  -c:v copy -c:a aac -b:a 192k -shortest final.mp4
```

### Workflow 2: Images + Videos + Background Music

```bash
# Step 1: Prepare audio to match total video duration
ffmpeg -i music.mp3 -t 60 -af "afade=t=in:st=0:d=3,afade=t=out:st=55:d=5" \
  -c:a libmp3lame -q:a 2 audio_ready.mp3

# Step 2: Convert images to video clips
ffmpeg -loop 1 -i title.png -t 5 \
  -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=30" \
  -c:v libx264 -preset fast -crf 23 title.mp4

ffmpeg -loop 1 -i logo.png -t 5 \
  -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=30" \
  -c:v libx264 -preset fast -crf 23 logo.mp4

# Step 3: Create video with transitions (no audio yet)
ffmpeg -i title.mp4 -i video.mp4 -i logo.mp4 -filter_complex "\
  [0:v][1:v]xfade=transition=dissolve:duration=2:offset=3[vout1]; \
  [vout1][2:v]xfade=transition=dissolve:duration=2:offset=51[vout]" \
  -map "[vout]" -c:v libx264 -crf 23 video_only.mp4

# Step 4: Add processed audio to final video
ffmpeg -i video_only.mp4 -i audio_ready.mp3 \
  -c:v copy -c:a aac -b:a 192k -shortest final.mp4
```

### Workflow 3: Mix Original Video Audio with Background Music

```bash
# Step 1: Prepare background music
ffmpeg -i music.mp3 -t 45 -af "afade=t=out:st=40:d=5" \
  -c:a libmp3lame -q:a 2 music_ready.mp3

# Step 2: Mix video audio (100%) with background music (30%)
ffmpeg -i video.mp4 -i music_ready.mp3 -filter_complex \
  "[0:a][1:a]amix=inputs=2:duration=shortest:weights=1 0.3[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k output.mp4
```

## Audio Synchronization

### Remove Audio from Video

```bash
# Remove all audio streams
ffmpeg -i input.mp4 -an output.mp4

# Copy video, no audio
ffmpeg -i input.mp4 -c:v copy -an output.mp4
```

### Fix Audio Sync Issues

```bash
# Delay audio by 0.5 seconds
ffmpeg -i video.mp4 -itsoffset 0.5 -i video.mp4 \
  -map 0:v -map 1:a -c:v copy -c:a aac output.mp4

# Advance audio by 0.5 seconds (video delay)
ffmpeg -itsoffset 0.5 -i video.mp4 -i video.mp4 \
  -map 0:v -map 1:a -c:v copy -c:a aac output.mp4

# Force sync
ffmpeg -i video.mp4 -async 1 -c:v copy -c:a aac output.mp4
```

## Advanced Audio Processing

### Multi-track Audio

```bash
# Extract specific audio track
ffmpeg -i video.mp4 -map 0:a:0 -c:a libmp3lame -q:a 2 audio_track1.mp3
ffmpeg -i video.mp4 -map 0:a:1 -c:a libmp3lame -q:a 2 audio_track2.mp3

# Add multiple audio tracks to video
ffmpeg -i video.mp4 -i audio1.mp3 -i audio2.mp3 \
  -map 0:v -map 1:a -map 2:a \
  -c:v copy -c:a aac output.mp4
```

### Audio Filters Chain

```bash
# Combine multiple filters: volume, fade, normalize
ffmpeg -i music.mp3 \
  -af "volume=1.2,afade=t=in:st=0:d=3,afade=t=out:st=55:d=5,loudnorm" \
  -c:a libmp3lame -q:a 2 output.mp3

# EQ adjustments (bass boost)
ffmpeg -i music.mp3 \
  -af "equalizer=f=100:width_type=h:width=50:g=3" \
  -c:a libmp3lame -q:a 2 output.mp3
```

### Audio Concatenation

```bash
# Concatenate audio files
# Create list.txt:
# file 'audio1.mp3'
# file 'audio2.mp3'
ffmpeg -f concat -safe 0 -i list.txt -c copy output.mp3

# Concatenate with crossfade
ffmpeg -i audio1.mp3 -i audio2.mp3 -filter_complex \
  "[0][1]acrossfade=d=2[a]" \
  -map "[a]" -c:a libmp3lame -q:a 2 output.mp3
```

## Best Practices

1. **Process audio separately** before adding to video for better control
2. **Always add fadeout** to background music for professional finish
3. **Use `-shortest`** when adding background music to match video duration
4. **Use AAC for video**, MP3 for standalone audio
5. **Use `-q:a 2` for MP3** (high quality) or `-b:a 192k` for AAC
6. **Test volume levels** before final render - adjust weights if needed
7. **Use `-c:v copy`** when only processing audio to avoid re-encoding video
