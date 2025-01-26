import re
import os
import random
import string
from utils.patterns import patterns

def create_session(length=6):
    """Generate a random 6-alphanumeric string."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def process_url(input_string, replacement_values):
    for _, pattern_data in patterns.items():
        # Compile the regex pattern
        regex = re.compile(pattern_data["to_match"])
        
        # Search for matches in the input string
        match = regex.search(input_string)
        if match:            
            # Replace the match with the formatted replacement string
            input_string = regex.sub(pattern_data["to_replace"], input_string)

    return input_string

def create_log(url, start_time_str, end_time_str, total_time, video_size, log_file="download_log.txt"):
    """Log the details of the download to a common file."""
    with open(log_file, 'a') as log:
        log.write(f"URL: {url}\n")
        log.write(f"Start Time: {start_time_str}\n")
        log.write(f"End Time: {end_time_str}\n")
        log.write(f"Time Taken: {total_time:.2f} seconds\n")
        log.write(f"Final Video Size: {video_size / (1024 * 1024):.2f} MB\n")
        log.write("="*50 + "\n")

def cleanup_segments(folder):
    """Delete all segment files in the folder."""
    for file in os.listdir(folder):
        if file.startswith("segment_") and file.endswith(".ts"):
            os.remove(os.path.join(folder, file))

def move_final_video(final_video_file, destination_folder):
    """Move the final video file to a specified folder."""
    os.makedirs(destination_folder, exist_ok=True)
    os.rename(final_video_file, os.path.join(destination_folder, os.path.basename(final_video_file)))

def remove_segment_folder(folder):
    """Remove the segment folder."""
    os.rmdir(folder)