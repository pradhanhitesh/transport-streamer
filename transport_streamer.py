import requests
import re
import os
import random
import string
import time
from datetime import datetime

def generate_random_folder_name(length=6):
    """Generate a random 6-alphanumeric string."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def download_video_segment(url, output_file):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(output_file, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
            return True  # Download successful
        else:
            return False  # Download failed
    except Exception as e:
        print(f"An error occurred while downloading {output_file}: {e}")
        return False  # Download failed due to an error

def combine_segments(segment_files, final_output_file):
    try:
        with open(final_output_file, 'wb') as final_file:
            for segment in segment_files:
                with open(segment, 'rb') as seg_file:
                    final_file.write(seg_file.read())
        return os.path.getsize(final_output_file)  # Return the final file size
    except Exception as e:
        print(f"An error occurred while combining files: {e}")
        return 0

def process_url(url):
    url = re.sub(r"seg-\d+", "seg-{}", url)
    return url

def log_download_details(url, start_time_str, end_time_str, total_time, video_size, log_file="download_log.txt"):
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

# Main script
url_template = process_url(input("Enter the URL template: "))

# Generate a random folder name
random_folder = generate_random_folder_name()
os.makedirs(os.path.join("segments", random_folder), exist_ok=True)

# Start timing
start_time = time.time()
start_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Log timestamp

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
log_download_details(url_template, start_time_str, end_time_str, total_time, final_video_size)

# Cleanup the segment files and folder
cleanup_segments(os.path.join("segments", random_folder))
move_final_video(final_video_file, "final_videos")
remove_segment_folder(os.path.join("segments", random_folder))

print(f"Total time taken: {total_time:.2f} seconds")