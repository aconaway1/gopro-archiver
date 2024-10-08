# GoPro Archiver
## Summary
GoPro is terrible at filenames. This project tries to help with
that problem.

## Usage

### GoPro Archiver

This script takes the terribly-named files that a GoPro puts on your SD card and copies them to
a destination folder with a dated folder structure and dated files.

> python gopro_archiver.py [ [ -s,--source ] SOURCE_FOLDER ] [ [ -d,--destination ] DESTINATION_FOLER ]

There are default values for source and destination folders, which are declared in the `config.yml` file.

The format for the date in the filename is declared in the `config.yml` file.

Each file winds up in a specific directory structure in the output destination folder.

`{destination}/{file_create_year}/{file_create_month_digit}/{file_create_day}`

For example, a file you recorded on 17 January 1948 will be in the folder `{destination}/1948/01/17`. If that
file is called "GX010101.MP4", then the filename will be `19480117-GX010101.MP4`.

When you record a long video with your GoPro, it may break up your recording into more than one file. This is
called file chaptering and is very annoying. If chaptered files are detected, it will rename subsequent files 
as `FILENAME-02` with the proper extension.

### Renamer

This script takes individual files and copies them to an archive folder in the same manner as the
GoPro Archiver. The intended purpose is really to take finalized videos (finished videos to publish)
and copy them individually to archive.

> python renamer.py [ [-s,--source] ] [ [-d,--destination] ]

More than one source file may be indicated with multiple `-s` flags. For example, to copy the files `final1.mp4` and
`final2.mp4` to folder, you would run the following.

> python renamer.py -s final1.mp4 -s final2.mp4 -d archiver_folder

The folder structure and filenames are handled the same way as the GoPro Archiver, so make sure to
read that section as well.

There is no chapter detection, and file names are simple prefixed with the familiar date
string.

## Config File

The file `config.yml` has some directives and default values in it. Most of them can be left alone, but some
may be used to make your life easier. There is a sample in the repo.

```
DEFAULT_SOURCE_FOLDER: "./sample"
DEFAULT_DESTINATION_FOLDER: "./sample/output"
DATE_FORMAT: "%Y%m%d"
MAX_THREADS: 10
VALID_EXTENSIONS: [ "MP4", "AVI", "MOV" ]
HASHCHECK: True
```
The two default folder locations can be used to avoid having to use big, long arguments each time you run it.
The rest should probably be left as-is unless you know what you're doing.

`DATE_FORMAT` is the how the date is represented in the destination filename prefix.

`MAX_THREADS` does nothing. I never go around to putting threading in.

`VALID_EXTENSIONS` are all the file extensions that the scripts will process. Everything else is ignored.

`HASHCHECK` is whether or not an MD5 checksum should be compared when the files are copied. 

## Notes
This was all written on a Mac, but it should work everywhere. Look out
for the default folder locations.

## TODO
* Better input checking.
* Threading