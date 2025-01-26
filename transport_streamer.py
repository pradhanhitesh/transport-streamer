import requests
import re
import os
import random
import string
import time
from datetime import datetime
from utils.patterns import patterns
from utils.download import download_video_segment, combine_segments
from utils.processing import process_url, create_session, create_log, cleanup_segments, move_final_video, remove_segment_folder

# Main script
url_template = process_url(input("Enter the URL template: "), patterns)

# Generate session
random_folder = create_session()
os.makedirs(os.path.join("segments", random_folder), exist_ok=True)

# Start timing
start_time = time.time()
start_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Download multiple segments into the random folder
segment_files = []
max_failures = 3
consecutive_failures = 0

for i in range(1, 10000):  # Loop through an arbitrary range
    segment_url = url_template.format(i)
    segment_file = os.path.join("segments", random_folder, f"segment_{i}.ts")
    time_start = time.time()
    success = download_video_segment(segment_url, segment_file)
    time_end = time.time()
    elapsed_time = time_end - time_start
    print(f"Downloaded: {segment_file} | Time Taken: {elapsed_time:.4f} seconds")
    
    if success:
        segment_files.append(segment_file)
        consecutive_failures = 0
    else:
        consecutive_failures += 1
        if consecutive_failures >= max_failures:
            break

# Combine all successfully downloaded segments into a single file
final_video_file = os.path.join("segments", random_folder, f"{random_folder}.ts")
combine_segments(segment_files, final_video_file)
final_video_size = os.path.getsize(final_video_file)

# End timing
end_time = time.time()
end_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Calculate total time taken
total_time = end_time - start_time

# Log the details in a common file
create_log(url_template, start_time_str, end_time_str, total_time, 
           final_video_size, log_file=os.path.join('utils','ts_download.txt'))

# Cleanup the segment files and folder
cleanup_segments(os.path.join("segments", random_folder))
move_final_video(final_video_file, "final_videos")
remove_segment_folder(os.path.join("segments", random_folder))

print(f"Total time taken: {total_time:.2f} seconds")