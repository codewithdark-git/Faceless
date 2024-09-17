import os
import tempfile
from moviepy.editor import (AudioFileClip, CompositeVideoClip, CompositeAudioClip,
                            TextClip, ImageClip, concatenate_videoclips)

def get_output_media(audio_file_path, timed_captions, image_files):
    OUTPUT_FILE_NAME = "rendered_video.mp4"

    visual_clips = []
    audio_clips = []
    audio_file_clip = AudioFileClip(audio_file_path)
    audio_clips.append(audio_file_clip)
    
    for idx, ((t1, t2), text) in enumerate(timed_captions):
        # Create an ImageClip for each generated image
        image_filename = image_files[idx] if idx < len(image_files) else image_files[-1]
        image_clip = ImageClip(image_filename).set_duration(t2 - t1).set_start(t1)
        image_clip = image_clip.resize(height=720)  # Resize to height 720 without method argument
        visual_clips.append(image_clip)
        
        # Add text overlay
        text_clip = TextClip(txt=text, fontsize=50, color="white", stroke_width=2, stroke_color="black", method="caption", size=(image_clip.w, None))
        text_clip = text_clip.set_start(t1).set_end(t2)
        text_clip = text_clip.set_position(("center", "bottom"))
        visual_clips.append(text_clip)
    
    final_clip = CompositeVideoClip(visual_clips)
    final_clip = final_clip.set_audio(CompositeAudioClip(audio_clips))
    final_clip.write_videofile(OUTPUT_FILE_NAME, codec="libx264", fps=24, audio_codec="aac")
    
    return OUTPUT_FILE_NAME