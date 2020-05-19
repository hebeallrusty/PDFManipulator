# PDFManipulator

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
```

+ 20200403

```
	- Initial Release
```

## Description

Program to do basic manipulation to PDF files such as split, join, encrypt. 

Written in Python and utilises the pikepdf library, and wxpython
