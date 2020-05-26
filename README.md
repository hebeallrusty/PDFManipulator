# PDFManipulator

## Description

Program to do basic manipulation to PDF files such as split, join, encrypt, rotate pages and substitute pages

Written in Python and utilises the pikepdf library (1.13.0), and wxpython

## Releases

+ 20200507

```
	- Adding function to rotate PDFs
	- Better handling of meta data PDFs
	- Tweak the encrypting code so that a new document is not created - just encrypt the existing file
	- Fix the page ranges on the split code so that a start range is not greater than the end
	- Add emplacing function - to substitute pages whilst keeping the rest of the document intact
	- Add function to test if the pdf is encrypted (and if the password is correct)
	- Added function to allow "natural" page range inputs i.e 1-3,5,8,14-25 etc instead of strict boxes of start and end number
	- Reordered the menu items so that Quit is now at the bottom
	- Change UI to be more compact
	- Use page ranges in a natural way rather than boxes for start and end ranges
	- Add functionality for Rotate, Emplace (substitute pages) and to remove password (with the correct one) from a password protected PDF
	- Alert user of new version at the Status bar, and get user to the webpage for downloading
	- Changed icons to self drawn ones
```

+ 20200403

```
	- Initial Release
```


