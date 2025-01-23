# transport-streamer

`transport-streamer` is designed to intercept, download, and combine `.ts` (transport stream) files while streaming from the network. It organizes the downloaded segments, merges them into a single video file, and logs essential details for future reference.

## Features

- Intercepts `.ts` files from streaming URLs.
- Downloads `.ts` segments into a folder named `segments/`.
- Combines all `.ts` segments into a single video file stored in `final_videos/`.
- Cleans up the `segments/` folder after the final video is created.
- Logs information such as:
  - URL of the stream.
  - Start and end time of the process.
  - Total time taken.
  - Final video size.
- Currently supported `regex` patterns in the `url`:
  - `seg-\d+`


## Requirements

- Python 3.10 or later
- Required Python libraries (install using `requirements.txt`)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/pradhanhitesh/transport-streamer.git
   cd transport-streamer
   ```

2. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Create the required folders:
   ```bash
   mkdir segments final_videos
   ```

2. Run the script:
   ```bash
   python transport_streamer.py
   ```

3. The script will:
   - Download the `.ts` files to the `segments/` folder.
   - Combine them into a single video file saved in the `final_videos/` folder.
   - Clean up the `segments/` folder after merging.
   - Log the process details in a log file.

## Logging

The script creates a log file (`ts_download.txt`) with details of each operation, including:

- URL of the stream.
- Start and end time of the process.
- Total time taken to download and combine the segments.
- Size of the final video file.

## Example

```bash
python transport_streamer.py 
Enter the URL template: <paste the url here>
```

Output:
- `.ts` files stored temporarily in `segments/`
- Final merged video saved in `final_videos/`
- Logs saved in `ts_download.txt`

## Directory Structure

```
transport-streamer/
|— segments/           # Temporary folder for .ts segments
|— final_videos/       # Folder for final merged videos
|— transport_streamer.py
|— requirements.txt
|— README.md
|— ts_download.txt
```

## Contributing

Contributions are welcome! If you have suggestions, improvements, or bug reports, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
