import os
import time
import sys
import select

class FolderSync:
    def __init__(self, source, destination, interval, log_file):
        self.source = source
        self.destination = destination
        self.interval = interval
        self.log_file = log_file
        self.source_folder_files = set()
        self.destination_folder_files = set()

    def copy_file(self, source_file, destination_file):
        """Copy a file from source to destination without using third party libraries."""
        try:
            with open(source_file, 'rb') as src:
                with open(destination_file, 'wb') as dst:
                    while True:
                        chunk = src.read(1024 * 1024)  # Read 1 MB at a time
                        if not chunk:
                            break
                        dst.write(chunk)
            self.log_action(f"Copied: {source_file} to {destination_file}")
        except Exception as e:
            self.log_action(f"Error copying {source_file} to {destination_file}: {e}")

    # Log every change to the log file and print to the terminal
    def log_action(self, message):
        try:
            with open(self.log_file, 'a') as f:
                f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
                print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
        except Exception as e:
            print(f"Error writing to log file {self.log_file}: {e}")

    # Core synchronizing function
    def sync_folders(self):
        # Ensure the destination directory exists
        try:
            if not os.path.exists(self.destination):
                os.makedirs(self.destination)
        except Exception as e:
            self.log_action(f"Error creating destination directory {self.destination}: {e}")
            return

        # Create the loop to check for file changes in each folder and keep the destination in sync with the source
        while True:
            # Update the files lists to the current files for the next iteration
            try:
                self.destination_folder_files = set(os.listdir(self.destination))
                self.source_folder_files = set(os.listdir(self.source))
            except Exception as e:
                self.log_action(f"Error accessing source directory {self.source}: {e}")
                time.sleep(self.interval)
                continue

            # Copy new or modified files to the destination, ignoring .DS_Store
            for file in self.source_folder_files:
                if file == '.DS_Store':
                    continue  # Skip .DS_Store files
                source_file = os.path.join(self.source, file)
                destination_file = os.path.join(self.destination, file)
                try:
                    # Check if the destination file exists and if so, if it's the newest version by checking its modification time
                    if file not in self.destination_folder_files or (os.path.exists(destination_file) and os.path.getmtime(source_file) > os.path.getmtime(destination_file)):
                        self.copy_file(source_file, destination_file)
                except Exception as e:
                    self.log_action(f"Error processing file {source_file}: {e}")

            # Remove files from the destination folder that are not in the source folder, ignoring .DS_Store
            for file in self.destination_folder_files:
                if file == '.DS_Store':
                    continue  # Skip .DS_Store files
                if file not in self.source_folder_files:
                    destination_file = os.path.join(self.destination, file)
                    try:
                        if os.path.exists(destination_file):
                            os.remove(destination_file)
                            self.log_action(f"Removed: {destination_file} (not in source)")
                    except Exception as e:
                        self.log_action(f"Error removing file {destination_file}: {e}")

            # If the user presses Enter the loop will break
            if select.select([sys.stdin], [], [], 1)[0]:
                input()  # Clear the input
                break

            # Sleep for the specified interval before the next iteration
            time.sleep(self.interval)
