# Facebook Messenger Exif

Facebook Messenger Exif is a small python program used to add metadata, specifically the date, back into the Facebook Messenger media found in a Facebook archive.

This is useful because, by default, when you download an archive of your Facebook data the media within it doesn't contain any metadata. You are actually given the metadata in the archive, but it is stored separately from the media files.

This means that if you try and import media into another service, such as Google Photos or Apple Photos, it will be missing that metadata. Crucially this includes the date, making importing a very time consuming process as you have to manually add the date each piece of media. Facebook Messenger Exif automates that, letting you simply drag and drop media into other services.

This tool only adds metadata back into Facebook Messenger media, not media found elsewhere in a Facebook archive. You can use facebook-data-image-exif to handle that other media: https://github.com/addshore/facebook-data-image-exif

Photos, videos and gifs are all supported. For most media Facebook stores a creation date, and this will be used if possible. In limited cases this data is missing, in which case the sent date will be used instead.

Note that this tool will be writing directly to the media, overwriting any existing metadata. If you have just downloaded your Facebook archive this shouldn't be a concern (as there won't be any metadata) but please keep this in mind.

## Usage

1. Request and download a copy of your Facebook data. It must be in JSON format. 'High' media quality is strongly recommended
2. Make sure you have python installed
3. Download `messengerexif.py` from this repo
4. Download ExifTool: https://exiftool.org/
5. Place `messengerexif.py` and the ExifTool .exe file inside the same folder as the `messages` folder from your Facebook archive
6. Open `messengerexif.py` with a text editor of your choice and edit line 8 to point to the ExifTool .exe
7. Run `messengerexif.py`

Assuming everything has gone well, you should see text appearing showing Facebook Messenger Exif going from media file to media file adding dates. It should only take a few moments per file.

If you have an especially large archive you can speed up the process by first going through your Facebook archive and deleting the media you don't want, and then running the tool. It will skip all missing media files and thereby speed up the process.

## Contributing
Pull requests and issues reports alike are welcome. Additionally, if you know any Java, there is an issue report to implement this functionally directly into facebook-data-image-exif: https://github.com/addshore/facebook-data-image-exif/issues/15

# Credits
Created by Yard1

Readme and testing by Zankoas

Inspired by addshore's facebook-data-image-exif

## License
...?
