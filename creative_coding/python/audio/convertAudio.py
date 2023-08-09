import os
import ffmpeg
from pydub import AudioSegment

def process_audio(input_path, output_path, output_format, new_bitrate):
    input_audio = AudioSegment.from_file(input_path)

    # Change format and bitrate
    input_audio.export(output_path, format=output_format, bitrate=f"{new_bitrate}k")

def main():
    input_file = "/Users/matthewheaton/Documents/GitHub/cdp_colloquium_i/site_refactor/assets/audio/WFH_DJ.aif"
    output_format = "mp3"
    new_bitrate = 128  # in kbps

    output_file_processed = os.path.splitext(input_file)[0] + "_processed." + output_format

    process_audio(input_file, output_file_processed, output_format, new_bitrate)

if __name__ == "__main__":
    main()
