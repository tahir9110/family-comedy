import subprocess
import os
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

def extract_last_frame(video_path, output_image_path):
    """Extracts the exact final frame of a clip for seamless continuation."""
    os.makedirs(os.path.dirname(output_image_path), exist_ok=True)
    cmd = [
        "ffmpeg", "-y", "-sseof", "-0.1", "-i", video_path,
        "-vsync", "0", "-vframes", "1", output_image_path
    ]
    subprocess.run(cmd, check=True)
    print(f"✅ Last frame successfully extracted to: {output_image_path}")

def stitch_and_polish(clip1_or_clips, clip2_or_output=None, output_final_path=None):
    """Stitches multiple clips (2, 3, 4, 5+ scenes) together with smooth audio normalization."""
    if isinstance(clip1_or_clips, list):
        clips = clip1_or_clips
        target_output = clip2_or_output
    else:
        clips = [clip1_or_clips, clip2_or_output]
        target_output = output_final_path

    os.makedirs(os.path.dirname(target_output), exist_ok=True)
    concat_file = "temp/concat_list.txt"
    os.makedirs(os.path.dirname(concat_file), exist_ok=True)

    with open(concat_file, "w", encoding="utf-8") as f:
        for c in clips:
            # Normalize path for ffmpeg concat
            norm_c = str(c).replace("\\", "/")
            f.write(f"file '{norm_c}'\n")

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", concat_file,
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        target_output
    ]
    subprocess.run(cmd, check=True)
    print(f"🎉 Final stitched episode ({len(clips)} scenes) produced at: {target_output}")
