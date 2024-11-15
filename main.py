# Please implement a program that synchronizes two folders: source and replica.
# The program should maintain a full, identical copy of source folder at replica folder.

# Synchronization must be one-way: after the synchronization content of the replica folder should be modified to exactly match content of the source folder;
# Synchronization should be performed periodically;
# File creation/copying/removal operations should be logged to a file and to the console output;
# Folder paths, synchronization interval and log file path should be provided using the command line arguments;
# It is undesirable to use third-party libraries that implement folder synchronization;
# It is allowed (and recommended) to use external libraries implementing other well-known algorithms.
# For example, there is no point in implementing yet another function that calculates MD5 if you need it for the task – it is perfectly acceptable to use a third-party (or built-in) library;
# The solution should be presented in the form of a link to the public GitHub repository.

from foldersync import FolderSync
from helpers import input_sync_details

def main():

    sync_details = input_sync_details() # Get and validate user inputs
    source_directory, destination_directory, interval, log_file = sync_details

    print(f"Starting synchronization from {source_directory} to {destination_directory} every {interval} seconds.")
    print("Press Enter to stop the synchronization.")

    # Create a FolderSync object and start synchronization
    folder_sync = FolderSync(source_directory, destination_directory, interval, log_file)
    folder_sync.sync_folders()

    print("All synchronizations stopped.")

if __name__ == "__main__":
    main()