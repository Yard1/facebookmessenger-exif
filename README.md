# Facebook Messenger Exif

Facebook Messenger Exif is a small python program used to add date and time metadata back into the Facebook Messenger media found in a Facebook archive.

This is useful because, at least currently, when you download an archive of your Facebook data the media within it doesn't contain any metadata. You are given the metadata in the archive, but it is stored separately from the media files.

As a result if you try to import media into another service, such as Google Photos or Apple Photos, it will be missing that metadata. Crucially this includes the date, making importing a very time-consuming process as you will need to manually add the date to each piece of media in order for it to show in the right place in your timeline. Facebook Messenger Exif automates that, letting you simply drag and drop media into other services.

This tool only adds metadata back into Facebook Messenger media, not media found elsewhere in a Facebook archive. You can use [facebook-data-image-exif](https://github.com/addshore/facebook-data-image-exif) to handle that other media.

Photos, videos and gifs are all supported. For most media Facebook stores a creation date, and this will be used if possible. If, for whatever reason, this data is missing the sent date will be used instead. No other metadata is added.

Note that this tool will be writing directly to the media, overwriting any existing attached metadata. If you have just downloaded your Facebook archive this shouldn't be a concern (as there won't be any attached metadata) but please keep this in mind.

## Usage

1. Request and download a copy of your Facebook data. It must be in JSON format. 'High' media quality is strongly recommended
2. Install Python 3.7 or newer: https://www.python.org/downloads/
3. Download `messengerexif.py` from this repo
4. Download ExifTool: https://exiftool.org/
5. Run `python messengerexif.py [path_to_messages] [path_to_exiftool_executable]`

Assuming everything has gone well you should see text appearing showing Facebook Messenger Exif going from media file to media file adding dates. It should only take a few moments per file.

If you have an especially large archive you can speed up the process by first going through your Facebook archive and deleting the media you don't want, and then running the tool. It will skip all missing media files and thereby speed up the process.

Documentation is provided when running with the `--help` argument:
`python messengerexif.py --help`

## Contributing

Pull requests and issue reports alike are very welcome.

Additionally, if you know any Java, there is an [open issue report](https://github.com/addshore/facebook-data-image-exif/issues/15) for facebook-data-image-exif for implementing this functionality directly into that tool. This would be great in saving people from having to run two different tools, as well as giving the tool a UI to aid in usability. If you are interested in helping, consider contacting the creator of that tool.

## Credits

Created by Yard1

Readme and testing by Zankoas

Inspired by addshore's [facebook-data-image-exif](https://github.com/addshore/facebook-data-image-exif)

## License

MIT
