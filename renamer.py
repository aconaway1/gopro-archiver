import os
import datetime
import shutil
import argparse
import sys
import re
import yaml

CONFIG_FILE = "config.yml"

def copy_the_file(source, destination) -> bool:
    print(f"Moving file to {destination}")
    try:
        # Copy the file
        shutil.copy2(source, destination)
        return True
    except PermissionError:
        print("Permissions problem with source or destination:")
        print(f"Source: {source}")
        print(f"Destination: {destination}")
        return False


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
        "-s", "--source", "--src", help="A file to be renamed.",
        action="append"
    )
    return parser

def main():
    # Parse the arguments
    parser = init_args()
    # Read in default values
    with open(CONFIG_FILE, encoding="UTF8") as file:
        defaults = yaml.safe_load(file)
    arguments = parser.parse_args()

    # # Get the source
    # if arguments.source:
    #     source_folder = arguments.source
    # else:
    #     source_folder = defaults['DEFAULT_SOURCE_FOLDER']

    # Get the destination
    if arguments.destination:
        destination_folder = arguments.destination
    else:
        destination_folder = defaults['DEFAULT_DESTINATION_FOLDER']

    # Make sure the destination folder ends in a trailing '/'
    if not destination_folder.endswith("/"):
        destination_folder = f"{destination_folder}/"

    try:
        # Make sure the destination exists
        dest_files = os.listdir(destination_folder)
    except FileNotFoundError:
        print(f"Couldn't open the destination at {destination_folder}.")
        sys.exit()

    # Summary table variables
    processed_file_count = 0
    moved_file_count = 0
    failed_files = []
    ignored_files = []

    for source_file in arguments.source:
        try:
            # Get the files from the source folder
            found_file = os.path.isfile(source_file)
        except FileNotFoundError:
            print(f"Couldn't open file {source_file}")
            sys.exit()

        if not found_file:
            print(f"The file {source_file} doesn't exist. Skipping.")
            ignored_files.append(source_file)
            continue

        processed_file_count += 1

        is_valid_extension = False
        for checked_extension in defaults['VALID_EXTENSIONS']:
            cased_extensions = [ checked_extension.upper(), checked_extension.lower()]
            for extension in cased_extensions:
                if source_file.endswith(extension):
                    is_valid_extension = True
                    continue

        if not is_valid_extension:
            print(f"File {source_file} does not have the right extension.")
            ignored_files.append(file)
            continue

        # Get the filename from the path
        base_name = os.path.basename(source_file)
        # Get the creation date and time
        create_epoch = os.path.getmtime(source_file)
        # Convert to a datetime object
        create_datetime = datetime.datetime.fromtimestamp(create_epoch)
        # Format the date
        create_date = create_datetime.strftime(defaults['DATE_FORMAT'])
        # Get the year, month, and day from the filename
        create_year = create_datetime.strftime('%Y')
        create_month = create_datetime.strftime('%m')
        create_day = create_datetime.strftime('%d')

        # Set up the directories if needed
        if not os.path.exists(f"{destination_folder}/{create_year}"):
            os.mkdir(f"{destination_folder}/{create_year}")

        if not os.path.exists(f"{destination_folder}/{create_year}/{create_month}"):
            os.mkdir(f"{destination_folder}/{create_year}/{create_month}")

        if not os.path.exists(f"{destination_folder}/{create_year}/{create_month}/{create_day}"):
            os.mkdir(f"{destination_folder}{create_year}/{create_month}/{create_day}")

        # Generate new filename
        new_filename = f"{destination_folder}{create_year}/{create_month}/{create_day}/{create_date}-{base_name}"
        # See if the destination file already exists.
        if os.path.isfile(new_filename):
            print(f"The file {new_filename} already exists.")
            failed_files.append(new_filename)
            continue

        copy_status = copy_the_file(source_file, new_filename)
        if copy_status:
            moved_file_count += 1


    # Print the summary
    print(f"{'=' * 20}")
    print(f"Number of processed files: {processed_file_count}")
    print(f"Copied {moved_file_count} files.")
    print(f"Ignored {len(ignored_files)} files:")
    for ignored_file in ignored_files:
        print(f"  {ignored_file}")
    print(f"Failed to copy {len(failed_files)} files:")
    for failed_file in failed_files:
        print(f"  {failed_file}")


if __name__ == "__main__":
    main()