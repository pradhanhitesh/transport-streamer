import requests
import os

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
