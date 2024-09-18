import os
import tempfile
from moviepy.editor import (AudioFileClip, CompositeVideoClip, CompositeAudioClip,
                            TextClip, ImageClip, VideoFileClip)

def get_output_media(audio_file_path, timed_captions, image_files, video_files):
    OUTPUT_FILE_NAME = "rendered_video.mp4"

    visual_clips = []
    audio_clips = []
    audio_file_clip = AudioFileClip(audio_file_path)
    audio_clips.append(audio_file_clip)
    
    for idx, ((t1, t2), text) in enumerate(timed_captions):
        image_clip = None  # Initialize image_clip to None

        # Check if there are images available
        if idx < len(image_files):
            image_filename = image_files[idx]
            image_clip = ImageClip(image_filename).set_duration(t2 - t1).set_start(t1)
            image_clip = image_clip.resize(height=720)
            visual_clips.append(image_clip)
        elif image_files:  # If there are images but not enough for the index
            image_filename = image_files[-1]  # Use the last image
            image_clip = ImageClip(image_filename).set_duration(t2 - t1).set_start(t1)
            image_clip = image_clip.resize(height=720)
            visual_clips.append(image_clip)

        # Create video clip if available
        if idx < len(video_files):
            video_clip = VideoFileClip(video_files[idx]).set_duration(t2 - t1).set_start(t1)
            video_clip = video_clip.resize(height=720)
            visual_clips.append(video_clip)

        # Add text overlay only if image_clip is created
        if image_clip is not None:
            text_clip = TextClip(txt=text, fontsize=50, color="white", stroke_width=2, stroke_color="black", method="caption", size=(image_clip.w, None))
            text_clip = text_clip.set_start(t1).set_end(t2)
            text_clip = text_clip.set_position(("center", "bottom"))
            visual_clips.append(text_clip)

    # Check if visual_clips is empty before creating the CompositeVideoClip
    if not visual_clips:
        print("No visual clips to create a video. Exiting.")
        return None  # Or handle this case as needed

    final_clip = CompositeVideoClip(visual_clips)
    final_clip = final_clip.set_audio(CompositeAudioClip(audio_clips))
    final_clip.write_videofile(OUTPUT_FILE_NAME, codec="libx264", fps=24, audio_codec="aac")
    
    return OUTPUT_FILE_NAME