# GoPro Archiver
## Summary
GoPro is terrible at filenames. This project tries to help with
that problem.

## Usage

`python gopro_archiver.py [ [-s,--source SOURCE_FOLDER] [-d,--destination] DESTINATION_FOLER]`

There are default values for source and destination folders.

Each file winds up in a specific directory structure in the output destination folder.

`{destination}/{file_create_year}/{file_create_month_digit}/{file_create_day}`

For example, a file you recorded on 17 January 1948 will be in the folder `{destination}/1948/01/17`.

## Notes
This was written on a Mac, but it should work everywhere. Look out
for the default folder locations.

## TODO
* Determine if a file is another chapter of an existing video and name it accordingly.
* Better input checking.
* Threading