import os
import datetime
import shutil
import argparse
import sys

import yaml

CONFIG_FILE = "config.yml"

# DEFAULT_SOURCE_FOLDER = "/Volumes/Untitled/DCIM/100GOPRO/"
# DEFAULT_DESTINATION_FOLDER = "/Users/aconaway/Desktop/"
#
# DATE_FORMAT = "%Y%m%d"
#
# MAX_THREADS = 10

def copy_the_file(source, destination):
    print(f"Moving file to {destination}")
    # Copy the file
    shutil.copyfile(source, destination)


def init_args() -> argparse.ArgumentParser:
    """
    Initializes the CLI arguments

    Returns:
        argparse.ArgumentParser - The argparse parser to use later
    """
    parser = argparse.ArgumentParser(
        description="Post a message to Mastodon during a streaming event",
    )
    # parser.add_argument(
    #     "-v", "--version", action="version",
    #     version=f"{parser.prog} {VERSION}"
    # )
    parser.add_argument(
        "-d", "--destination", "--dst", help="The folder where we're sending the files."
    )
    parser.add_argument(
        "-s", "--source", "--src", help="The folder where the GoPro files live."
    )
    return parser

def main():
    # Parse the arguments
    parser = init_args()
    # Read in default values
    with open(CONFIG_FILE, encoding="UTF8") as file:
        defaults = yaml.safe_load(file)
    arguments = parser.parse_args()


    # Get the source
    if arguments.source:
        source_folder = arguments.source
    else:
        source_folder = defaults['DEFAULT_SOURCE_FOLDER']

    # Get the destination
    if arguments.destination:
        destination_folder = arguments.destination
    else:
        destination_folder = defaults['DEFAULT_DESTINATION_FOLDER']

    # Make sure the destination folders all end in a trailing '/'
    if not source_folder.endswith("/"):
        source_folder = f"{source_folder}/"
    if not destination_folder.endswith("/"):
        destination_folder = f"{destination_folder}/"

    try:
        # Get the files from the source folder
        found_files = os.listdir(source_folder)
    except FileNotFoundError:
        print(f"Couldn't open files in {source_folder}")
        sys.exit()

    try:
        # Make sure the destination exists
        dest_files = os.listdir(destination_folder)
    except FileNotFoundError:
        print(f"Couldn't open the destination at {destination_folder}.")
        sys.exit()
    for file in found_files:
        if not file.endswith("MP4"):
            #print(f"{file} is not an MP4 file.")
            continue

        # Generate full path
        full_source_file_path = f"{source_folder}/{file}"
        # Make sure the file exits
        if not os.path.isfile(full_source_file_path):
            #print(f"{file} does not exists. Skipping.")
            continue


        # Get the filename from the path
        # base_name = os.path.basename(full_source_file_path)
        # Get the creation date and time
        create_epoch = os.path.getctime(full_source_file_path)
        # Convert to a datetime object
        create_datetime = datetime.datetime.fromtimestamp(create_epoch)
        # Format the date
        create_date = create_datetime.strftime(defaults['DATE_FORMAT'])
        # Generate new filename
        new_filename = f"{destination_folder}{create_date}-{file}"
        # See if the destination file already exists.
        if os.path.isfile(new_filename):
            print(f"The file {new_filename} already exists.")
            continue

        copy_the_file(full_source_file_path, new_filename)


if __name__ == "__main__":
    main()