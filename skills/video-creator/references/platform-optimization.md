# Platform Optimization Guide

## YouTube

### Recommended Specifications

**Resolution options:**
- 3840x2160 (4K, 16:9)
- 2560x1440 (2K, 16:9)
- 1920x1080 (1080p, 16:9) - Most common
- 1280x720 (720p, 16:9) - Minimum HD

**Frame rates:**
- 24 fps (cinematic)
- 30 fps (standard, recommended)
- 60 fps (smooth motion, gaming)

**Codec & Format:**
- Video: H.264 (most compatible) or H.265/HEVC
- Audio: AAC-LC, 192-320 kbps, stereo or 5.1
- Container: MP4

**Bitrate recommendations:**
- 4K (60fps): 53-68 Mbps
- 4K (30fps): 35-45 Mbps
- 1080p (60fps): 12-15 Mbps
- 1080p (30fps): 8-12 Mbps
- 720p (60fps): 7.5-10 Mbps
- 720p (30fps): 5-7.5 Mbps

### YouTube Optimization Commands

```bash
# 1080p 30fps (standard, recommended)
ffmpeg -i input.mp4 \
  -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=30" \
  -c:v libx264 -preset slow -crf 18 \
  -c:a aac -b:a 192k -ar 48000 \
  -pix_fmt yuv420p -movflags +faststart \
  youtube_1080p.mp4

# 4K 30fps (high quality)
ffmpeg -i input.mp4 \
  -vf "scale=3840:2160:force_original_aspect_ratio=decrease,pad=3840:2160:(ow-iw)/2:(oh-ih)/2,fps=30" \
  -c:v libx264 -preset slow -crf 18 \
  -c:a aac -b:a 192k -ar 48000 \
  -pix_fmt yuv420p -movflags +faststart \
  youtube_4k.mp4

# 1080p 60fps (smooth motion)
ffmpeg -i input.mp4 \
  -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=60" \
  -c:v libx264 -preset slow -crf 18 \
  -c:a aac -b:a 192k -ar 48000 \
  -pix_fmt yuv420p -movflags +faststart \
  youtube_1080p60.mp4
```

**Key parameters:**
- `-preset slow`: Better compression (use `medium` for faster encoding)
- `-crf 18`: High quality (lower = better, 18-23 recommended)
- `-movflags +faststart`: Enable streaming before full download
- `-ar 48000`: 48kHz audio sample rate (YouTube standard)

## Instagram

### Feed Posts (Square)

**Specifications:**
- Resolution: 1080x1080 (1:1)
- Max duration: 60 seconds
- Frame rate: 30 fps max
- Codec: H.264
- Audio: AAC, 128 kbps

```bash
# Instagram Feed (square)
ffmpeg -i input.mp4 \
  -vf "scale=1080:1080:force_original_aspect_ratio=decrease,pad=1080:1080:(ow-iw)/2:(oh-ih)/2,fps=30" \
  -c:v libx264 -preset medium -crf 23 \
  -c:a aac -b:a 128k -ar 44100 \
  -t 60 -pix_fmt yuv420p -movflags +faststart \
  instagram_feed.mp4
```

### Stories & Reels (Portrait)

**Specifications:**
- Resolution: 1080x1920 (9:16)
- Stories max: 15 seconds per clip
- Reels max: 90 seconds
- Frame rate: 30 fps
- Codec: H.264
- Audio: AAC, 128 kbps

```bash
# Instagram Stories/Reels (portrait 9:16)
ffmpeg -i input.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,fps=30" \
  -c:v libx264 -preset medium -crf 23 \
  -c:a aac -b:a 128k -ar 44100 \
  -pix_fmt yuv420p -movflags +faststart \
  instagram_story.mp4

# For Reels, add max duration
ffmpeg -i input.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,fps=30" \
  -c:v libx264 -preset medium -crf 23 \
  -c:a aac -b:a 128k -ar 44100 \
  -t 90 -pix_fmt yuv420p -movflags +faststart \
  instagram_reel.mp4
```

### IGTV (Landscape or Portrait)

**Specifications:**
- Resolution: 1080x1920 (portrait) or 1920x1080 (landscape)
- Duration: 1-60 minutes
- Frame rate: 30 fps
- Codec: H.264

```bash
# IGTV Portrait
ffmpeg -i input.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,fps=30" \
  -c:v libx264 -preset medium -crf 23 \
  -c:a aac -b:a 128k \
  -pix_fmt yuv420p -movflags +faststart \
  igtv_portrait.mp4

# IGTV Landscape
ffmpeg -i input.mp4 \
  -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=30" \
  -c:v libx264 -preset medium -crf 23 \
  -c:a aac -b:a 128k \
  -pix_fmt yuv420p -movflags +faststart \
  igtv_landscape.mp4
```

## TikTok

### Recommended Specifications

**Resolution:**
- 1080x1920 (9:16 portrait) - Recommended
- Also supports: 1080x1080 (square), 1920x1080 (landscape)

**Duration:**
- Regular: Up to 10 minutes
- TikTok Series: Up to 30 minutes

**Other specs:**
- Frame rate: 30 fps
- Codec: H.264
- Audio: AAC, 128 kbps
- Max file size: 287.6 MB (iOS), 72 MB (Android)

### TikTok Optimization Commands

```bash
# TikTok (portrait 9:16, recommended)
ffmpeg -i input.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,fps=30" \
  -c:v libx264 -preset medium -crf 23 \
  -c:a aac -b:a 128k -ar 44100 \
  -pix_fmt yuv420p -movflags +faststart \
  tiktok.mp4

# TikTok with file size limit (for Android)
ffmpeg -i input.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,fps=30" \
  -c:v libx264 -preset medium -b:v 5M \
  -c:a aac -b:a 128k \
  -pix_fmt yuv420p -movflags +faststart \
  -fs 72M \
  tiktok_optimized.mp4
```

## Twitter (X)

### Recommended Specifications

**Resolution:**
- 1920x1080 or 1280x720 (landscape)
- 1080x1920 (portrait)
- 1080x1080 (square)

**Limitations:**
- Max duration: 2 minutes 20 seconds (140 seconds)
- Max file size: 512 MB
- Frame rate: 30 or 60 fps
- Codec: H.264
- Audio: AAC

**Bitrate recommendations:**
- 1080p: 5-10 Mbps
- 720p: 3-5 Mbps

### Twitter Optimization Commands

```bash
# Twitter 1080p landscape
ffmpeg -i input.mp4 \
  -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=30" \
  -c:v libx264 -preset medium -crf 23 -maxrate 5M -bufsize 10M \
  -c:a aac -b:a 128k -ar 44100 \
  -t 140 -pix_fmt yuv420p -movflags +faststart \
  twitter.mp4

# Twitter 720p (smaller file size)
ffmpeg -i input.mp4 \
  -vf "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,fps=30" \
  -c:v libx264 -preset medium -crf 25 \
  -c:a aac -b:a 128k \
  -t 140 -pix_fmt yuv420p -movflags +faststart \
  twitter_720p.mp4
```

## Facebook

### Recommended Specifications

**Resolution:**
- 1080p: 1080x1080 (square), 1920x1080 (landscape), 1080x1920 (portrait)
- 720p minimum

**Specifications:**
- Frame rate: 30 fps
- Codec: H.264
- Audio: AAC, stereo, 128 kbps
- Max file size: 4 GB
- Max duration: 240 minutes

### Facebook Optimization Commands

```bash
# Facebook 1080p landscape
ffmpeg -i input.mp4 \
  -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=30" \
  -c:v libx264 -preset medium -crf 23 \
  -c:a aac -b:a 128k -ar 44100 \
  -pix_fmt yuv420p -movflags +faststart \
  facebook.mp4

# Facebook square (for feed)
ffmpeg -i input.mp4 \
  -vf "scale=1080:1080:force_original_aspect_ratio=decrease,pad=1080:1080:(ow-iw)/2:(oh-ih)/2,fps=30" \
  -c:v libx264 -preset medium -crf 23 \
  -c:a aac -b:a 128k \
  -pix_fmt yuv420p -movflags +faststart \
  facebook_square.mp4
```

## LinkedIn

### Recommended Specifications

**Resolution:**
- Minimum: 256x144
- Maximum: 4096x2304
- Recommended: 1920x1080

**Specifications:**
- Frame rate: 30 fps or less
- Codec: H.264
- Audio: AAC
- Max file size: 5 GB
- Max duration: 10 minutes
- Aspect ratio: 1:2.4 to 2.4:1

### LinkedIn Optimization Commands

```bash
# LinkedIn 1080p
ffmpeg -i input.mp4 \
  -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=30" \
  -c:v libx264 -preset medium -crf 23 \
  -c:a aac -b:a 128k \
  -pix_fmt yuv420p -movflags +faststart \
  linkedin.mp4
```

## Quick Reference Table

| Platform | Aspect Ratio | Resolution | FPS | Duration | CRF |
|----------|--------------|------------|-----|----------|-----|
| YouTube | 16:9 | 1920x1080 | 30/60 | Unlimited | 18 |
| Instagram Feed | 1:1 | 1080x1080 | 30 | 60s | 23 |
| Instagram Story | 9:16 | 1080x1920 | 30 | 15s | 23 |
| Instagram Reel | 9:16 | 1080x1920 | 30 | 90s | 23 |
| TikTok | 9:16 | 1080x1920 | 30 | 10min | 23 |
| Twitter | 16:9 | 1920x1080 | 30/60 | 140s | 23 |
| Facebook | 16:9/1:1 | 1920x1080 | 30 | 240min | 23 |
| LinkedIn | 16:9 | 1920x1080 | 30 | 10min | 23 |

## Best Practices

1. **Always use `-movflags +faststart`** for web/social media (enables progressive streaming)
2. **Use `-pix_fmt yuv420p`** for maximum compatibility
3. **Test on target platform** before bulk processing
4. **Keep file sizes reasonable** - higher quality doesn't always mean better user experience
5. **Match platform requirements** exactly for best results
6. **Use appropriate CRF values**: 18-20 for YouTube, 23-25 for social media
7. **Consider mobile users** - most social media views are on mobile devices
