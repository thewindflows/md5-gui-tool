# This script requires the 'customtkinter' library for a modern dark UI.
# Install it via: pip install customtkinter
# Also requires tkinter, which is standard.
import os
import hashlib
import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import customtkinter as ctk
import csv
import pyperclip
from threading import Thread
import threading
from concurrent.futures import ThreadPoolExecutor
import multiprocessing

ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class MD5HasherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MD5 Hash Calculator")
        self.root.geometry("600x500")
        self.root.resizable(True, True)

        # Variables
        self.selected_paths = []  # List of files or folders
        self.is_folder_mode = False
        self.recurse_subfolders = tk.BooleanVar(value=False)
        self.granular = tk.BooleanVar(value=False)
        self.extensions = tk.StringVar(value="")
        self.output_report_txt = tk.BooleanVar(value=False)
        self.output_report_csv = tk.BooleanVar(value=False)
        self.report_txt_path = tk.StringVar(value="")
        self.report_csv_path = tk.StringVar(value="")
        self.progress = tk.DoubleVar(value=0)
        self.time_est = tk.StringVar(value="Estimated time: N/A")
        self.results_text = ""
        self.results_csv = []
        self.bytes_processed = tk.DoubleVar(value=0)
        self.total_size = 0
        self.lock = threading.Lock()
        self.is_hashing = False  # Flag to control the monitor

        # UI Elements
        self.create_ui()

    def create_ui(self):
        # Frame for selection
        select_frame = ctk.CTkFrame(self.root)
        select_frame.pack(pady=10, padx=10, fill="x")

        self.select_button = ctk.CTkButton(select_frame, text="Select File or Folder", command=self.select_paths)
        self.select_button.pack(side="left", padx=5)

        # Folder options (hidden initially)
        self.folder_options_frame = ctk.CTkFrame(self.root)
        self.recurse_check = ctk.CTkCheckBox(self.folder_options_frame, text="Recurse Subfolders", variable=self.recurse_subfolders)
        self.recurse_check.pack(side="left", padx=5)
        self.granular_check = ctk.CTkCheckBox(self.folder_options_frame, text="Granular (by extension)", variable=self.granular, command=self.toggle_granular)
        self.granular_check.pack(side="left", padx=5)
        self.extensions_entry = ctk.CTkEntry(self.folder_options_frame, textvariable=self.extensions, placeholder_text="e.g., .txt,.py", state="disabled")
        self.extensions_entry.pack(side="left", padx=5)

        # Report options
        report_frame = ctk.CTkFrame(self.root)
        report_frame.pack(pady=10, padx=10, fill="x")
        self.report_txt_check = ctk.CTkCheckBox(report_frame, text="Output to TXT Report", variable=self.output_report_txt, command=self.select_txt_report_path)
        self.report_txt_check.pack(side="left", padx=5)
        self.report_txt_label = ctk.CTkLabel(report_frame, textvariable=self.report_txt_path)
        self.report_txt_label.pack(side="left", padx=5)

        report_csv_frame = ctk.CTkFrame(self.root)
        report_csv_frame.pack(pady=5, padx=10, fill="x")
        self.report_csv_check = ctk.CTkCheckBox(report_csv_frame, text="Output to CSV Report", variable=self.output_report_csv, command=self.select_csv_report_path)
        self.report_csv_check.pack(side="left", padx=5)
        self.report_csv_label = ctk.CTkLabel(report_csv_frame, textvariable=self.report_csv_path)
        self.report_csv_label.pack(side="left", padx=5)

        # Calculate and Copy buttons
        button_frame = ctk.CTkFrame(self.root)
        button_frame.pack(pady=10)
        self.calc_button = ctk.CTkButton(button_frame, text="Calculate MD5 Hashes", command=self.start_calculation)
        self.calc_button.pack(side="left", padx=5)
        self.copy_button = ctk.CTkButton(button_frame, text="Copy Results", command=self.copy_results)
        self.copy_button.pack(side="left", padx=5)

        # Progress bar
        self.progress_bar = ttk.Progressbar(self.root, orient="horizontal", length=400, mode="determinate", variable=self.progress)
        self.progress_bar.pack(pady=10)

        # Time estimation label
        self.time_label = ctk.CTkLabel(self.root, textvariable=self.time_est)
        self.time_label.pack(pady=5)

        # Results text area
        self.results_area = ctk.CTkTextbox(self.root, height=200)
        self.results_area.pack(pady=10, padx=10, fill="both", expand=True)

    def toggle_granular(self):
        if self.granular.get():
            self.extensions_entry.configure(state="normal")
        else:
            self.extensions_entry.configure(state="disabled")

    def select_paths(self):
        choice = messagebox.askyesno("Selection Mode", "Do you want to select folders? (No for files)")
        self.is_folder_mode = choice
        self.selected_paths = []

        if self.is_folder_mode:
            # Show folder options frame
            self.folder_options_frame.pack(pady=10, padx=10, fill="x", before=self.report_txt_check.master)
            while True:
                folder = filedialog.askdirectory(title="Select Folder")
                if folder:
                    self.selected_paths.append(folder)
                else:
                    break
                if not messagebox.askyesno("Multiple Folders", "Select another folder?"):
                    break
        else:
            # Hide folder options frame
            self.folder_options_frame.pack_forget()
            files = filedialog.askopenfilenames(title="Select File(s)")
            self.selected_paths = list(files)

        if self.selected_paths:
            self.results_area.delete("1.0", "end")
            self.results_area.insert("end", f"Selected: {len(self.selected_paths)} item(s)\n")

    def select_txt_report_path(self):
        if self.output_report_txt.get():
            messagebox.showinfo("Select TXT Output", "Please select where to save the TXT report.")
            report_file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            if report_file:
                self.report_txt_path.set(report_file)
            else:
                self.output_report_txt.set(False)
                self.report_txt_path.set("")
        else:
            self.report_txt_path.set("")

    def select_csv_report_path(self):
        if self.output_report_csv.get():
            messagebox.showinfo("Select CSV Output", "Please select where to save the CSV report.")
            report_file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if report_file:
                self.report_csv_path.set(report_file)
            else:
                self.output_report_csv.set(False)
                self.report_csv_path.set("")
        else:
            self.report_csv_path.set("")

    def copy_results(self):
        if self.results_text:
            pyperclip.copy(self.results_text)
            messagebox.showinfo("Copied", "Results copied to clipboard.")
        else:
            messagebox.showwarning("No Results", "No results to copy.")

    def start_calculation(self):
        if not self.selected_paths:
            messagebox.showwarning("No Selection", "Please select files or folders first.")
            return

        self.results_area.delete("1.0", "end")
        self.progress.set(0)
        self.time_est.set("Estimated time: N/A")
        self.results_text = ""
        self.results_csv = []

        thread = Thread(target=self.calculate_hashes)
        thread.start()

    def hash_file(self, file_path):
        """Hash a single file and return its result, updating bytes processed."""
        hash_md5 = hashlib.md5()
        file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(131072), b""):
                    hash_md5.update(chunk)
                    with self.lock:
                        self.bytes_processed.set(self.bytes_processed.get() + len(chunk))
            md5_hash = hash_md5.hexdigest()
            filename = os.path.basename(file_path)
            return {"Filename": filename, "Path": file_path, "MD5 Hash": md5_hash, "Error": None}
        except Exception as e:
            # On error, still "process" the full file size to avoid stalling progress
            with self.lock:
                self.bytes_processed.set(self.bytes_processed.get() + file_size)
            return {"Filename": os.path.basename(file_path), "Path": file_path, "MD5 Hash": None, "Error": str(e)}

    def monitor_progress(self, start_time):
        while self.is_hashing:
            if self.total_size > 0:
                current_progress = min(self.bytes_processed.get() / self.total_size * 100, 100)
                self.progress.set(current_progress)
                elapsed = time.time() - start_time
                if current_progress > 0:
                    est_total = elapsed / (current_progress / 100)
                    est_remaining = max(est_total - elapsed, 0)
                    self.time_est.set(f"Estimated time remaining: {int(est_remaining)} seconds")
            time.sleep(0.5)  # Update every 0.5 seconds
        # Final update when done
        self.progress.set(100)
        self.time_est.set("Completed.")

    def calculate_hashes(self):
        all_files = self.get_all_files()
        if not all_files:
            self.results_area.insert("end", "No files found to hash.\n")
            return

        self.total_size = sum(os.path.getsize(f) for f in all_files if os.path.exists(f))
        if self.total_size == 0:
            self.results_area.insert("end", "All files are empty or inaccessible.\n")
            return

        self.results_area.delete("1.0", "end")
        self.progress.set(0)
        self.bytes_processed.set(0)
        self.time_est.set("Estimated time: Calculating...")
        self.results_text = ""
        self.results_csv = []
        self.is_hashing = True

        start_time = time.time()
        monitor_thread = Thread(target=self.monitor_progress, args=(start_time,))
        monitor_thread.start()

        from concurrent.futures import as_completed

        with ThreadPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
            futures = [executor.submit(self.hash_file, f) for f in all_files]
            for fut in as_completed(futures):
                result = fut.result()
                if result["Error"]:
                    error = f"Error hashing {result['Path']}: {result['Error']}\n"
                    self.results_text += error
                    self.results_area.insert("end", error)
                else:
                    result_text = f"{result['Path']}: {result['MD5 Hash']}\n"
                    self.results_text += result_text
                    self.results_area.insert("end", result_text)
                    self.results_csv.append(result)
                self.results_area.see("end")

        self.is_hashing = False
        monitor_thread.join()  # Wait for monitor to finish

        # Write to TXT report if selected
        if self.output_report_txt.get() and self.report_txt_path.get():
            with open(self.report_txt_path.get(), "w") as report:
                report.write(self.results_text)

        # Write to CSV report if selected
        if self.output_report_csv.get() and self.report_csv_path.get():
            with open(self.report_csv_path.get(), "w", newline="") as csvfile:
                fieldnames = ["Filename", "Path", "MD5 Hash"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for row in self.results_csv:
                    if row["MD5 Hash"]:  # Only write successful hashes
                        filtered_row = {key: row[key] for key in fieldnames}
                        writer.writerow(filtered_row)

    def get_all_files(self):
        all_files = []
        extensions_set = set(ext.strip().lower() for ext in self.extensions.get().split(",") if ext.strip()) if self.granular.get() else None

        for path in self.selected_paths:
            if self.is_folder_mode:
                if self.recurse_subfolders.get():
                    for root, _, files in os.walk(path):
                        for file in files:
                            if extensions_set is None or os.path.splitext(file)[1].lower() in extensions_set:
                                all_files.append(os.path.join(root, file))
                else:
                    for file in os.listdir(path):
                        full_path = os.path.join(path, file)
                        if os.path.isfile(full_path) and (extensions_set is None or os.path.splitext(file)[1].lower() in extensions_set):
                            all_files.append(full_path)
            else:
                all_files.append(path)  # It's a file

        return all_files

if __name__ == "__main__":
    root = ctk.CTk()
    app = MD5HasherApp(root)
    root.mainloop()