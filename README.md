# GoPro Archiver
## Summary
GoPro is terrible at filenames. This project tries to help with
that problem.

## Usage

`python gopro_archiver.py [ [-s,--source SOURCE_FOLDER] [-d,--destination] DESTINATION_FOLER]`

There are default values for source and destination folders.

## Notes
This was written on a Mac, but it should work everywhere. Look out
for the default folder locations.

## TODO
* Move defaults to config file
* Determine if a file is another chapter of an existing video and name it accordingly.
* Better input checking.
* Threading