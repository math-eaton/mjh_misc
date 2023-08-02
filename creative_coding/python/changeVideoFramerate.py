from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.fx.all import speedx

def speed_up_video(input_video_path, output_video_path, speedup_factor):
    # Load the video
    video = VideoFileClip(input_video_path)
    
    # Speed up the video
    video = video.fx(speedx, speedup_factor)

    # Write the result to a file
    video.write_videofile(output_video_path, codec='libx264')


input_video_path = "/Users/matthewheaton/Documents/DOCENTS/Screen Recording 2023-08-02 at 5.03.21 PM.mov"
output_video_path = "/Users/matthewheaton/Documents/DOCENTS/Screen Recording 2023-08-02 at 5.03.21 PM RETIME.mov"
speedup_factor = 6.0

speed_up_video(input_video_path, output_video_path, speedup_factor)
print("done.")
