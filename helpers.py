import os

def is_valid_directory(path):
    """Check if the given path is a valid directory."""
    return os.path.isdir(path)

def is_positive_integer(value):
    """Check if the given value is a positive integer."""
    try:
        ivalue = int(value)
        return ivalue > 0
    except ValueError:
        return False

def input_sync_details():
    """Gather and validate input for folder synchronization."""
    while True:
        source_directory = input("Enter the source directory: ")
        if not is_valid_directory(source_directory):
            print("Invalid source directory. Please enter a valid path.")
            continue

        destination_directory = input("Enter the destination directory: ")
        if not os.path.exists(destination_directory):
            print("Destination directory does not exist. It will be created.")
        
        interval = input("Enter the synchronization interval in seconds: ")
        if not is_positive_integer(interval):
            print("Invalid interval. Please enter a positive integer.")
            continue
        interval = int(interval)

        log_file = input("Enter the log file path: ")
        if not os.path.isdir(os.path.dirname(log_file)):
            print("Invalid log file path. Please enter a valid directory for the log file.")
            continue

        return source_directory, destination_directory, interval, log_file
