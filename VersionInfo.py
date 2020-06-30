# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
# filevers and prodvers should be always a tuple with four items: (1, 2, 3, 4)
# Set not needed items to zero 0.
filevers=(20, 6, 4, 0000),
prodvers=(20, 6, 4, 0000),
# Contains a bitmask that specifies the valid bits 'flags'r
mask=0x3f,
# Contains a bitmask that specifies the Boolean attributes of the file.
flags=0x0,
# The operating system for which this file was designed.
# 0x4 - NT and there is no need to change it.
OS=0x4,
# The general type of file.
# 0x1 - the file is an application.
fileType=0x1,
# The function of the file.
# 0x0 - the function is not defined for this fileType
subtype=0x0,
# Creation date and time stamp.
date=(0, 0)
),
  kids=[
StringFileInfo(
  [
  StringTable(
    u'040904B0',
    [StringStruct(u'CompanyName', u'Ashley Butler'),
    StringStruct(u'FileDescription', u'Manipulator for PDF Files'),
    StringStruct(u'FileVersion', u'20200604 '),
    StringStruct(u'InternalName', u'PDFManipulator'),
    StringStruct(u'LegalCopyright', u'Copyright (C) 2020 Ashley Butler'),
    StringStruct(u'OriginalFilename', u'PDFManipulator.exe'),
    StringStruct(u'ProductName', u'PDFManipulator'),
    StringStruct(u'ProductVersion', u'20200604 ()')])
  ]), 
VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
