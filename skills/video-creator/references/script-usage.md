# Script Usage Guide

All FFmpeg operations in this skill follow the `run.sh` execution pattern.

## Basic Pattern

```bash
./run.sh script-name.sh [arguments]
```

## Available Scripts

### Video Editing

#### trim-video.sh
Trim video by start time and duration.
```bash
./run.sh trim-video.sh INPUT START DURATION OUTPUT
# Example: Extract 10 seconds starting at 1:30
./run.sh trim-video.sh input.mp4 00:01:30 00:00:10 output.mp4
```

#### trim-by-time.sh
Trim video by start and end time.
```bash
./run.sh trim-by-time.sh INPUT START END OUTPUT
# Example: Extract from 1:30 to 1:40
./run.sh trim-by-time.sh input.mp4 00:01:30 00:01:40 output.mp4
```

### Format Conversion

#### convert-format.sh
Convert video to different format with optimal settings.
```bash
./run.sh convert-format.sh INPUT OUTPUT [CRF] [PRESET]
# Example: Convert AVI to MP4
./run.sh convert-format.sh input.avi output.mp4
# Example: Convert with quality settings
./run.sh convert-format.sh input.avi output.mp4 23 medium
```

#### copy-streams.sh
Copy streams without re-encoding (fast, lossless).
```bash
./run.sh copy-streams.sh INPUT OUTPUT
# Example: Change container without re-encoding
./run.sh copy-streams.sh input.mp4 output.mkv
```

### Resolution & Scaling

#### resize-video.sh
Resize video to specific resolution.
```bash
./run.sh resize-video.sh INPUT WIDTH HEIGHT OUTPUT
# Example: Resize to 720p
./run.sh resize-video.sh input.mp4 1280 720 output.mp4
```

#### scale-maintain-aspect.sh
Scale video maintaining aspect ratio.
```bash
./run.sh scale-maintain-aspect.sh INPUT WIDTH OUTPUT
# Example: Scale to 1280 width, auto height
./run.sh scale-maintain-aspect.sh input.mp4 1280 output.mp4
```

#### crop-video.sh
Crop video to specific dimensions.
```bash
./run.sh crop-video.sh INPUT WIDTH HEIGHT X Y OUTPUT
# Example: Crop to 1920x1080 from top-left
./run.sh crop-video.sh input.mp4 1920 1080 0 0 output.mp4
```

#### add-padding.sh
Add letterbox/pillarbox padding to video.
```bash
./run.sh add-padding.sh INPUT WIDTH HEIGHT OUTPUT
# Example: Add padding to fit 16:9
./run.sh add-padding.sh input.mp4 1920 1080 output.mp4
```

### Concatenation

#### concat-simple.sh
Concatenate videos with same format (fast, no re-encoding).
```bash
./run.sh concat-simple.sh OUTPUT VIDEO1 VIDEO2 [VIDEO3...]
# Example: Join two videos
./run.sh concat-simple.sh output.mp4 video1.mp4 video2.mp4
```

#### concat-reencode.sh
Concatenate videos with re-encoding (different formats).
```bash
./run.sh concat-reencode.sh OUTPUT VIDEO1 VIDEO2 [VIDEO3...]
# Example: Join videos of different formats
./run.sh concat-reencode.sh output.mp4 video1.avi video2.mp4 video3.mov
```

### Transitions

#### create-transition.sh
Create transition between two videos.
```bash
./run.sh create-transition.sh VIDEO1 VIDEO2 TRANSITION DURATION OUTPUT
# Example: 2-second fade between videos
./run.sh create-transition.sh video1.mp4 video2.mp4 fade 2 output.mp4
```

Available transitions: fade, fadeblack, fadewhite, distance, wipeleft, wiperight, wipeup, wipedown, slideleft, slideright, slideup, slidedown, circlecrop, rectcrop, dissolve

#### chain-transitions.sh
Chain multiple videos with transitions.
```bash
./run.sh chain-transitions.sh OUTPUT TRANSITION DURATION VIDEO1 VIDEO2 [VIDEO3...]
# Example: Chain 3 videos with dissolve
./run.sh chain-transitions.sh output.mp4 dissolve 2 v1.mp4 v2.mp4 v3.mp4
```

### Image to Video

#### image-to-video.sh
Convert static image to video clip.
```bash
./run.sh image-to-video.sh IMAGE DURATION WIDTH HEIGHT OUTPUT
# Example: 5-second clip from image
./run.sh image-to-video.sh photo.jpg 5 1920 1080 output.mp4
```

#### create-slideshow.sh
Create slideshow from multiple images.
```bash
./run.sh create-slideshow.sh DURATION OUTPUT IMAGE1 IMAGE2 [IMAGE3...]
# Example: 3 seconds per image
./run.sh create-slideshow.sh 3 output.mp4 img1.jpg img2.jpg img3.jpg
```

### Audio Operations

#### add-audio.sh
Add audio track to video (replace existing).
```bash
./run.sh add-audio.sh VIDEO AUDIO OUTPUT
# Example: Add MP3 to video
./run.sh add-audio.sh video.mp4 music.mp3 output.mp4
```

#### mix-audio.sh
Mix video audio with background music.
```bash
./run.sh mix-audio.sh VIDEO MUSIC VIDEO_WEIGHT MUSIC_WEIGHT OUTPUT
# Example: Video 100%, music 30%
./run.sh mix-audio.sh video.mp4 music.mp3 1 0.3 output.mp4
```

#### remove-audio.sh
Remove audio from video.
```bash
./run.sh remove-audio.sh INPUT OUTPUT
./run.sh remove-audio.sh input.mp4 silent.mp4
```

#### extract-audio.sh
Extract audio from video.
```bash
./run.sh extract-audio.sh VIDEO FORMAT OUTPUT
# Example: Extract as MP3
./run.sh extract-audio.sh video.mp4 mp3 audio.mp3
```

#### cut-audio.sh
Cut audio to specific duration.
```bash
./run.sh cut-audio.sh INPUT DURATION OUTPUT
# Example: Cut to 60 seconds
./run.sh cut-audio.sh music.mp3 60 music_cut.mp3
```

#### fade-audio.sh
Add fade in/out to audio.
```bash
./run.sh fade-audio.sh INPUT TYPE START DURATION OUTPUT
# Example: 5-second fadeout starting at 55s
./run.sh fade-audio.sh music.mp3 out 55 5 music_fade.mp3
```

### Speed & Frame Rate

#### change-speed.sh
Change video playback speed.
```bash
./run.sh change-speed.sh INPUT FACTOR OUTPUT
# Example: 2x speed
./run.sh change-speed.sh input.mp4 2.0 output.mp4
```

#### change-fps.sh
Change video frame rate.
```bash
./run.sh change-fps.sh INPUT FPS OUTPUT
# Example: Convert to 60fps
./run.sh change-fps.sh input.mp4 60 output.mp4
```

### Filters & Effects

#### add-text.sh
Add text overlay to video.
```bash
./run.sh add-text.sh INPUT TEXT X Y FONTSIZE COLOR OUTPUT
# Example: White text at top-left
./run.sh add-text.sh input.mp4 "Hello" 10 10 24 white output.mp4
```

#### add-watermark.sh
Add watermark image to video.
```bash
./run.sh add-watermark.sh VIDEO LOGO X Y OUTPUT
# Example: Logo at bottom-right
./run.sh add-watermark.sh video.mp4 logo.png 10 10 output.mp4
```

#### blur-video.sh
Apply blur effect.
```bash
./run.sh blur-video.sh INPUT STRENGTH OUTPUT
# Example: Medium blur
./run.sh blur-video.sh input.mp4 5 output.mp4
```

#### rotate-video.sh
Rotate video.
```bash
./run.sh rotate-video.sh INPUT DIRECTION OUTPUT
# Direction: 90cw, 90ccw, 180
./run.sh rotate-video.sh input.mp4 90cw output.mp4
```

### Frame Extraction

#### extract-frame.sh
Extract single frame at timestamp.
```bash
./run.sh extract-frame.sh VIDEO TIMESTAMP OUTPUT
# Example: Frame at 5 seconds
./run.sh extract-frame.sh video.mp4 00:00:05 frame.jpg
```

#### extract-frames.sh
Extract all frames from video.
```bash
./run.sh extract-frames.sh VIDEO PATTERN
# Example: Extract as PNG sequence
./run.sh extract-frames.sh video.mp4 frame%04d.png
```

#### extract-frames-interval.sh
Extract frames at intervals.
```bash
./run.sh extract-frames-interval.sh VIDEO FPS PATTERN
# Example: 1 frame per second
./run.sh extract-frames-interval.sh video.mp4 1 frame%04d.png
```

### Platform Optimization

#### optimize-youtube.sh
Optimize video for YouTube.
```bash
./run.sh optimize-youtube.sh INPUT OUTPUT [RESOLUTION]
# Example: Optimize for 1080p YouTube
./run.sh optimize-youtube.sh input.mp4 youtube.mp4 1080
```

#### optimize-instagram.sh
Optimize video for Instagram.
```bash
./run.sh optimize-instagram.sh INPUT TYPE OUTPUT
# Type: feed, story, reel
./run.sh optimize-instagram.sh input.mp4 feed output.mp4
```

#### optimize-tiktok.sh
Optimize video for TikTok.
```bash
./run.sh optimize-tiktok.sh INPUT OUTPUT
./run.sh optimize-tiktok.sh input.mp4 tiktok.mp4
```

#### optimize-twitter.sh
Optimize video for Twitter.
```bash
./run.sh optimize-twitter.sh INPUT OUTPUT [RESOLUTION]
./run.sh optimize-twitter.sh input.mp4 twitter.mp4 1080
```

### Utility

#### get-info.sh
Get detailed video information.
```bash
./run.sh get-info.sh VIDEO
./run.sh get-info.sh input.mp4
```

#### get-duration.sh
Get video duration.
```bash
./run.sh get-duration.sh VIDEO
./run.sh get-duration.sh input.mp4
```

#### list-codecs.sh
List available codecs.
```bash
./run.sh list-codecs.sh
```

## Script Chaining

Scripts can be chained together for complex operations:

```bash
# Example: Trim, add audio, optimize for YouTube
./run.sh trim-video.sh raw.mp4 00:00:10 00:01:00 trimmed.mp4
./run.sh add-audio.sh trimmed.mp4 music.mp3 with_audio.mp4
./run.sh optimize-youtube.sh with_audio.mp4 final.mp4 1080
```

## Error Handling

All scripts include:
- Input validation
- Clear error messages
- Exit codes (0 = success, non-zero = error)
- Usage instructions when called incorrectly
