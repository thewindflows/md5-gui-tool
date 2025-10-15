MD5 Hash Calculator
A modern, user-friendly Python application for calculating MD5 hashes of files and folders. The application features a dark-themed GUI inspired by the Discord app, built using customtkinter. It supports single/multiple file and folder selection, granular file extension filtering, progress tracking, and output to TXT or CSV reports.
Features

File and Folder Selection:

Select single or multiple files.
Select single or multiple folders with optional recursive subfolder processing.
Granular mode to filter files by extensions (e.g., .txt,.py).


MD5 Hash Calculation:

Computes MD5 hashes for selected files efficiently using a 128KB buffer.
Parallel processing with ThreadPoolExecutor for improved performance on multiple files.


Output Options:

Display results in the GUI with a scrollable text area.
Copy results to clipboard with a "Copy Results" button.
Export results to a TXT file (file path and hash, including errors).
Export successful hashes to a CSV file (columns: Filename, Path, MD5 Hash).


Progress and Time Estimation:

Progress bar showing completion percentage.
Estimated time remaining based on processing speed.


Modern UI:

Dark theme with a sleek, Discord-like design using customtkinter.
Responsive layout with intuitive controls.



Requirements

Python 3.6 or higher
Required Python packages:
customtkinter (for the GUI)
pyperclip (for copying results to clipboard)


Standard library modules (included with Python):
hashlib, tkinter, csv, threading, concurrent.futures, multiprocessing



Installation

Install Python:Ensure Python 3.6+ is installed on your system. Download from python.org if needed.

Install Dependencies:Install the required packages using pip:
pip install customtkinter pyperclip


Download the Script:Save the script as md5_hasher.py (or download from this repository).


Usage

Run the Application:Execute the script using Python:
python md5_hasher.py


Select Files or Folders:

Click "Select File or Folder" and choose whether to select files or folders.
For files, select one or multiple files via the file dialog.
For folders, select one or multiple folders. You can enable:
Recurse Subfolders: Process all files in subdirectories.
Granular (by extension): Specify file extensions (e.g., .txt,.py) to process only matching files.




Configure Output:

Check "Output to TXT Report" to save results (file paths, hashes, and errors) to a TXT file. Select the save location when prompted.
Check "Output to CSV Report" to save successful hashes to a CSV file (columns: Filename, Path, MD5 Hash). Select the save location when prompted.


Calculate Hashes:

Click "Calculate MD5 Hashes" to start processing.
Monitor progress via the progress bar and estimated time remaining.


View and Copy Results:

Results appear in the GUI text area.
Click "Copy Results" to copy the text output to the clipboard.



Example Output
TXT Report (output.txt):
/path/to/file1.txt: d41d8cd98f00b204e9800998ecf8427e
/path/to/file2.py: 5f4dcc3b5aa765d61d8327deb882cf99
Error hashing /path/to/file3.txt: Permission denied

CSV Report (output.csv):
Filename,Path,MD5 Hash
file1.txt,/path/to/file1.txt,d41d8cd98f00b204e9800998ecf8427e
file2.py,/path/to/file2.py,5f4dcc3b5aa765d61d8327deb882cf99

Performance Notes

Optimized for Speed:

Uses a 128KB buffer for file reading to reduce I/O overhead.
Employs parallel processing with ThreadPoolExecutor to hash multiple files concurrently.
Minimizes UI updates to improve performance for large file sets.


Limitations:

Performance depends on disk speed (SSD vs. HDD) and file sizes.
Threading helps with I/O-bound tasks, but MD5 hashing is CPU-bound and limited by Python’s GIL.
For very large datasets, consider testing on your system to evaluate performance.



Troubleshooting

Error: "No files found to hash":

Ensure you’ve selected files or folders.
If using granular mode, verify that the specified extensions match files in the selected folders.


Error: Permission Denied:

Check that you have read access to the selected files/folders.
Run the script with appropriate permissions (e.g., as administrator on Windows).


CSV Export Fails:

Ensure the CSV file path is valid and writable.
Verify that the CSV checkbox is checked and a file location is selected.


Slow Performance:

For many small files, parallel processing should help. For large files, disk speed is the primary bottleneck.
Test with a smaller dataset to confirm functionality.



License
This project is licensed under the MIT License. Feel free to use, modify, and distribute as needed.
Contributing
Contributions are welcome! Please submit issues or pull requests to the repository for bug fixes, performance improvements, or new features.
Acknowledgments

Built with customtkinter for the modern GUI.
Uses Python’s standard library for hashing and file operations.
