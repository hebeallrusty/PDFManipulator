#import wx
import platform
import os
import datetime as dt
import pikepdf
from pikepdf import _cpphelpers
import requests

PROGRAM_DATE = 20200604
PIKEPDF_VER = '1.14.0'
URL_CHECK_UPDATE = 'https://raw.githubusercontent.com/hebeallrusty/PDFManipulator/master/VERSION'

def ERRORS(error,errobj,filename=None):
	if error == 'OpenFileNotFound':
		return f'Unable to open:{filename} - {errobj.strerror}'
	elif error == 'PasswordError':
		return f'Incorrect password given for {filename}'
	elif error == 'SaveFileNotFound':
		return f'Unable to save to:{filename} - {errobj.strerror}'
	elif error == 'Permission':
		return f'Access denied to {filename}'
	elif error == 'IO':
		return f'An Input / Output error occured when accessing {filename}'

def version():
	return PROGRAM_DATE
	
def pikepdfversion():
	return PIKEPDF_VER

def swap_item(alist,pos1,pos2):
	alist[pos1],alist[pos2] = alist[pos2],alist[pos1]
	return alist

def get_pages(PDF_FILE):
	# see if we can open the PDF file - return is a list
	pdf = TryOpenPDF(PDF_FILE)
	if pdf[0] == False:
		return (False,pdf[1])
	else:
		return (True,len(pdf[1].pages))
	
def CheckUpdate():
        print("CHECKING FOR UPDATE")
        # master branch has a version file which contains the latest version number
        # use "try" as network may not be available at all which will cause the program to not start
        try:
        	page = requests.get(URL_CHECK_UPDATE)
        	pagestatus = page.status_code
        	print(pagestatus)
        	# status codes are the http codes. Anything 400 and above is an error (4xx Client error; 5xx Server error). Let user know unable to check for error
        	if (pagestatus >= 400):
        		print(f'Unable to check for an update. Webpage is not available ({pagestatus} error)')
        		return False
        	else: # must have got a valid response
        		return(int(page.text))
        except Exception as e: # maybe not connected to the internet?
        	print(e)
        	return False
        		

def get_docinfo(PDF_FILE):
	# open the pdf file
	trypdf = TryOpenPDF(PDF_FILE)
	if trypdf[0] == False:
		return (False,trypdf[1])
	else:
		pdf = trypdf[1]
	#pdf = pikepdf.Pdf.open(PDF_FILE)
	
	# if there is an xmp metadata, get it, if the file is older then opening the meta with pikepdf will create a blank xmp metadata
	meta = pdf.open_metadata()

	# need to test if the meta is "blank". If it is then the meta is in docinfo. We don't want to copy the docinfo to xmp if the xmp is already there as it'll trash some of the metadata and the goal is to keep as much as possible.
	
	# set a test to see if there are any keys in the meta. They should only be present if there is prior xmp metadata and not just the blank xmp from pikepdf
	metakeys = 0
	#print(META)
	for key in meta:
		# only prior xmp metadata will achieve this execution, so flag that it is proper xmp meta
		metakeys = 1
		# lets not waste any cpu cycles
		#print(f'{key}:{meta[key]}')
		break
		
	# now check if we have flagged xmp or docinfo meta
	if metakeys == 0:
		# there was no xmp meta, so we want to copy the docinfo over to xmp so that we can keep that later on. Can only update meta with a WITH block
		with meta as META:
			META.load_from_docinfo(pdf.docinfo)		
	
	return (True,meta)
	

def get_filename(PDF_FILE):
	# check which system we are running as this governs the directory name delimiter
	if platform.system() == 'Windows':
		dir_char = '\\'
	else:
		dir_char = '/'
	print(f'Program running on {platform.system()} and directory character = {dir_char}')
	string = PDF_FILE.rpartition(dir_char)
	# filename is the 3rd item that is returned from rpartition but still contains .pdf so split the string again to remove this suffix
	return string[2].rpartition('.')[0]
	
def files_in_folder(FOLDER):
	# case sensitive so lowercase all ext and then test
	return [os.path.join(FOLDER,FILE) for FILE in os.listdir(FOLDER) if FILE.lower().endswith(".pdf")]
	

def copy_meta(SrcMeta,DocObj):
	# DocObj is the new pdf with blank meta
	# SrcMeta is the meta object from the source pdf
	#print(SrcMeta)
	
	# open meta as writeable for new pdf
	with DocObj.open_metadata(set_pikepdf_as_editor=False) as meta:
		#meta.load_from_docinfo()
		#cycle through each key in the Source meta, and write that into the new blank file
		for key in SrcMeta:
			#print(f'key: {key} ; meta:{SrcMeta[key]}')
			meta[key] = SrcMeta[key]
		# alter the Modified Date
		meta['xmp:ModifyDate'] = pdf_timestamp()
		meta['xmp:CreatorTool'] = pdf_creator()
		meta['pdf:Producer'] = pdf_producer()
	
def pdf_creator():
	return f'PDFManipulator {PROGRAM_DATE}'
	
def pdf_producer():
	#PIKEPDF_VER = '1.14.0' # not ideal but internal method fails on compiled windows binary
	return f'pikepdf {PIKEPDF_VER}'

def pdf_timestamp():
	# generate PDF timestamp relative to utc time
	# timestamp format 2010-11-27T13:41:17+01:00
	NOW = dt.datetime.utcnow()
	#print(NOW)
	# NEEDS TO BE 4 DIGIT YEAR, 2 DIGIT MOND DAY HOUR MINUTE AND SECOND
	return f'{NOW.year:04}-{NOW.month:02}-{NOW.day:02}T{NOW.hour:02}:{NOW.minute:02}:{NOW.second:02}+00:00'

def ConvertMixedRanges(INPUT):
	# Function to convert a page range or list into a proper list i.e. 1-3,5,7 = [1,2,3,5,7]. Similar to print range dialog boxes
	
	# spilt the list using the comma as a delimeter. We will be able to iterate over these items to build a proper list containing all the elements
	InputList = INPUT.split(",")
	
	# prime a list for the output
	OutputList = []
		
	# iterate over all the parts
	for i in InputList:
	
		# check if there is a dash - in this context include all items e.g 1-3 = 1,2,3
		if "-" in i:
		
			# check if there is only one range within the item, and if there are more, raise an error / Return False
			if i.count("-") > 1:
					#raise IndexError(f'Only one "-" allowed within a single range, however received {i.count("-")} in item {i}')
					return False
			# now split this string to find out the start and end points
			iRange = i.split("-")
			
			# convert to integers as split will output strings - check that it is convertable and if not return False
			try:
				iRange = list(map(int,iRange))
			except:
				return False
			
			# check if starting number is greater than the ending number - range is reversed
			if iRange[1] < iRange [0]:
				# forgive the user's mistake and fix what they most likely meant
				swap_item(iRange,0,1)
			
			# create a range to then append each number to the Output
			for j in range(iRange[0],iRange[1]+1):
			
				OutputList.append(j)
			# we now need to discard this i as it has been parsed and dealt with, so move on to the next iteration
			continue
		
		# add i to the list but convert to an integer
		try:
			OutputList.append(int(i))
		except:
			return False
			
		
		# potential to sort the list here into numerical order - however this behaviour is to be checked as functions are altered in frontend. With Rotation, multiple versions of the same page are ignored
	return OutputList

def ConvertSimpleRange(INPUT):
	# check if INPUT is delimetered with a "-" and returns a list of two items with the start and end ranges
	
	if "-" in INPUT:
	
		#check there is only one "-". If there are more then return False which means it's failed to work
		if INPUT.count("-") > 1:
			return False
		
		# split the range
		InputList = INPUT.split("-")
		
		# convert items to integers - but check if they are convertable. If not then return false, else return th
		try:
			InputList = list(map(int,InputList))
		except:
			return False
		else:
			# items must be two integers. Now forgive if the range is the wrong way around
			if InputList[0] > InputList[1]:
				# swap them around
				swap_item(InputList,0,1)
			return InputList
	
	else:
		try:
			Input = int(INPUT)
		except:
			return False
		else:
			# single item must be an integer - return the two items repeated
			return [Input, Input]		
	
			

def split(PDF_FILE,OUT_DIR,PageRange,dismantle = False):
	# PDF_FILE must be a single PDF file
	# OUT_DIR must be a folder where the files will be created
	# PageRange must be a tuple containing start and end pages
	# dismantle denotes whether single files are required (True) or one file containing the range of pages (False)

	# error handling if file cannot be opened
	print(f'Opening {PDF_FILE}')
	
	# check if we can open the file - main errors are file is missing, or is the password is wrong. Current implementation doesn't allow for unlock password in this module. Anything that isn't caught returns the generic error

	trypdf = TryOpenPDF(PDF_FILE)
	if trypdf[0] == False:
		return (False,trypdf[1])
	else:
		pdf = trypdf[1]
	
	# document is openable so next command will succeed so just receive the object
	print(f'Getting Document Properties')
	meta = get_docinfo(PDF_FILE)[1]
	version = pdf.pdf_version
	print(f'PDF Version {version}')
	
	#filename = get_filename(PDF_FILE) # for the output	
	filename=""
	
	# initiate pdf_writer object - needed for ranges
	# cycle through every page and add it to a writer object

	if dismantle == True:
		print(f'Entering Page loop for pages {PageRange[0]} to {PageRange[1]}')
		for i in range(PageRange[0]-1,PageRange[1]): # pikepdf is zero indexed, pdf files are one indexed
			print(f'Dealing with page {i+1}')
			# initialise output document
			doc = pikepdf.Pdf.new()

			# add page to pdf that is to be written		
			doc.pages.append(pdf.pages[i])
			
		
			#update the metadata of the output so it matches that of the original
			copy_meta(meta,doc)

			# create filename. range is 0 based, so add in 1 so that page numbers match		
			output = f'{OUT_DIR}{filename}({i+1}).pdf'
			print(f'Writing file {output}')
			
			try:
				doc.save(output,min_version=version)
			except FileNotFoundError as e:
				print(f'Output File not Found')
				return ERRORS('SaveFileNotFound',e,filename = output)
			except PermissionError as e:
				print(f'Permission Error')
				return ERRORS('Permission',e,filename = output)
			except IOError as e:
				print(f'Input / Output Error')
				return ERRORS('IO',e,filename = output)
			except Exception as e:
				print(e.__class__)
				return e
			
	else:
		# create new output object
		doc = pikepdf.Pdf.new()
		# pikepdf produces pages as lists, so use a slicer to extend into empty document
		print(f'Getting pages {PageRange[0]} to {PageRange[1]}')
		doc.pages.extend(pdf.pages[PageRange[0]-1 :PageRange[1]])

		#update the metadata of the output so it matches that of the original
		copy_meta(meta,doc)
	
		output = f'{OUT_DIR}{filename}.pdf'
		print(f'Writing file {output}')
		try:
			doc.save(output,min_version=version)
		except FileNotFoundError as e:
			print(f'Output File not Found')
			return ERRORS('SaveFileNotFound',e,filename = output)
		except PermissionError as e:
			print(f'Permission Error')
			return ERRORS('Permission',e,filename = output)
		except IOError as e:
			print(f'Input / Output Error')
			return ERRORS('IO',e,filename=output)
		except Exception as e:
			print(e.__class__)
			return e
	
	# if we got here, then we must have run successfully - return True to let caller know we were successful	
	return True
	

def join(PDF_FILES,OUT_FILENAME,folder=False):
	# PDF_FILES must be a list of files or a folder of pdf files (must use folder=True to denote Folder)
	# OUT_FILENAME is the file that will be created
	# folder is the switch to denote tha PDF_FILES is actually a folder
	
	# initiate the new pdf object which will be the output
	doc = pikepdf.Pdf.new()
	version = doc.pdf_version
	# if we are dealing with a folder - get all the pdf's in that folder and convert that into the PDF_FILES
	if folder == True:
		print(f'getting all PDF files in {PDF_FILES}')
		# TODO check for problems here!!
		PDF_FILES = files_in_folder(PDF_FILES)

	for PDF in PDF_FILES:
		print(f'Opening {PDF}')
		# Open source document
		#pdf = pikepdf.Pdf.open(PDF)
		trypdf = TryOpenPDF(PDF)
		if trypdf[0] == False:
			return (False,trypdf[1])
		else:
			pdf = trypdf[1]
		
		# keep track of versions so that we write a pdf of the highest version to support the most features in the output
		version = max(version,pdf.pdf_version)
		# pikepdf pages are list objects so extend into the source doc
		doc.pages.extend(pdf.pages)

	#remove unreferenced material as internal structure changed
	doc.remove_unreferenced_resources()
	print(f'Saving file as {OUT_FILENAME} (PDF Version {version})')
	# open meta as writeable for new pdf
	with doc.open_metadata(set_pikepdf_as_editor=False) as docmeta:
		docmeta['xmp:ModifyDate'] = pdf_timestamp()
		docmeta['xmp:CreateDate'] = pdf_timestamp()	
		docmeta['xmp:CreatorTool'] = pdf_creator()
		docmeta['pdf:Producer'] = pdf_producer()
	doc.save(OUT_FILENAME,min_version=version)
	
	return True

def encrypt(PDF_FILE,OUT_FILENAME,Password,Strength):
	# open pdf file
	
	print(f'Opening {PDF_FILE}')
	#pdf = pikepdf.Pdf.open(PDF_FILE)
	trypdf = TryOpenPDF(PDF_FILE)
	if trypdf[0] == False:
		return (False,trypdf[1])
	else:
		pdf = trypdf[1]
	
	output = f'{OUT_FILENAME}.pdf'
	no_extracting = pikepdf.Permissions(extract=False)
	print(f'Writing file {output}')
	pdf.save(output,encryption = pikepdf.Encryption(user = Password, owner = Password[::-1], R=Strength, allow=no_extracting))

def emplace(PDF_FILE,OUT_FILENAME,SUBS,PAGE):
	# substitute pages in PDF_FILE for those in Subs.
	# Pages are zero indexed (i.e pdf page 1 is Page=0)
	# currently only does one page but plan for whole sub document
	
	print(f'Opening {PDF_FILE}')
	#pdf = pikepdf.Pdf.open(PDF_FILE)
	
	trypdf = TryOpenPDF(PDF_FILE)
	
	if trypdf[0] == False:
		return (False,trypdf[1])
	else
		pdf = trypdf[1]
	
	print(f'Opening {SUBS}')
	subpdf = pikepdf.Pdf.open(SUBS)
	
	trypdf = TryOpenPDF(SUBS)
	
	if trypdf[0] == False:
		return (False,trypdf[1])
	else
		subpdf = trypdf[1]	
	
	
	version = [pdf.pdf_version,subpdf.pdf_version]
	pages = [get_pages(PDF_FILE),get_pages(SUBS)]
	print(f'Pages: {pages} Version: {version}')
	
	# Check if the replacement pages exceeds the end of the document
	#if pages[1] + PAGE > pages[0]:
	#	print(f'Replacement pages exceeds the original document pages')
	
	# replace page
	# PAGE is desired page, but index is 1 less i.e PAGE = 1 is actual page 0 in pdf
	
	# add substitue page to end of document into original doc
	for i in range(0,pages[1]):
		print(f'Substituting page {PAGE+i} in {PDF_FILE} with page {i+1} in {SUBS}')
		pdf.pages.append(subpdf.pages[i])
		# carry out the substitution
		pdf.pages[PAGE - 1 + i].emplace(pdf.pages[-1])
		# delete the added page
		del pdf.pages[-1]
	
	# create filename and save		
	output = f'{OUT_FILENAME}.pdf'
	print(f'Writing file {output}')
	# save the pdf with the greatest pdf version of both files	
	pdf.save(output,min_version=max(version))
	
def TestEncryption(PDF_FILE,PASSWORD=""):
	# check if the file has a password and cannot be opened. Return is True (is encrypted) or False (isn't encrypted or correct password)
	# default is blank password
	
	# An error is raised if the file cannot be opened, so on a Password error return True, otherwise it's false. Any other error should be raised
	try:
		pdf = pikepdf.Pdf.open(PDF_FILE,password = PASSWORD)
	except pikepdf._qpdf.PasswordError:
		return True
	else:
		return False
		
def RotatePages(PDF_FILE,OUT_FILENAME,Pages,Rotation):
	# Rotates a Page in the PDF
	# Pages is a list containing the pages to rotate
	# Rotation is an angle clockwise at [90,180,270]
	
	if Rotation not in [90,180,270]:
		raise ValueError(f'Rotation must be either 90, 180 or 270, but received {Rotation}')
	
	print(f'Opening {PDF_FILE}')
	#pdf = pikepdf.Pdf.open(PDF_FILE)
	
	trypdf = TryOpenPDF(PDF_FILE)
	
	if trypdf[0] == False:
		return (False,trypdf[1])
	else:
		pdf = trypdf[1]
	
	for i in Pages:
		# pdf counting numbers start at 1, references begin at 0. User will have given actual page numbers
		i = i - 1
		print(f'Rotating Page {i+1}')
		pdf.pages[i].Rotate = Rotation
	
	# create filename and save		
	output = f'{OUT_FILENAME}.pdf'
	print(f'Writing file {output}')
	# save the pdf with the greatest pdf version of both files	
	pdf.save(output)
	
def RemoveEncryption(PDF_FILE,OUT_FILENAME,PASSWORD):
	# open pdf file
	
	print(f'Opening {PDF_FILE}')
	#pdf = pikepdf.Pdf.open(PDF_FILE,PASSWORD)
	trypdf = TryOpenPDF(PDF_FILE,PASSWORD)
	
	if trypdf[0] == False:
		return (False, trypdf[1])
	else:
		pdf = trypdf[1]
	
	output = f'{OUT_FILENAME}.pdf'
	#no_extracting = pikepdf.Permissions(extract=False)
	print(f'Writing file {output}')
	pdf.save(output)
	
def TryOpenPDF(PDF_FILE,PASSWORD = ""):
	# we want to wrap the opening of the PDF into a try/except statement as the file may not actually be openable
	
	try: 
		print(f'Trying to open {PDF_FILE}')
		ret = pikepdf.Pdf.open(PDF_FILE,password=PASSWORD)
		#print(get_pages(ret))
		# success - we can return the object back to the caller, and let them know it came back true
		return (True,ret)#print("success")
		
		# otherwise check for errors and do something sane to allow error messages to be displayed
	except FileNotFoundError as e:
		print(f'File Not Found')
		return (False,ERRORS('OpenFileNotFound',e, filename=PDF_FILE))
	except pikepdf._qpdf.PasswordError as e:
		print(f'Wrong Password')
		return (False,ERRORS('PasswordError',e,filename=PDF_FILE))
	except PermissionError as e:
		print(f'Permission Error')
		return (False,ERRORS('Permission',e,filename=PDF_FILE))
	except IOError as e:
		print(f'Input / Output Error')
		return (False,ERRORS('IO',e,filename=PDF_FILE))
	except Exception as e:
		print(f'Unhandled Error')
		print(e.__class__)
		return (False,e)
		
#def TrySavePDF(PDF_FILE)


# TESTS
PDF = '/home/ashley/src/PDFManipulator/TestPDFs/file-example_PDF_500_kB.pdf#'
#SUBPDF = '/home/ashley/src/PDFManipulator/TestPDFs/c4611_sample_explain.pdf'
#PDF = '/home/ashley/src/PDFManipulator/TestPDFs/c4611_sample_explain.pdf'
#PDF = '/home/ashley/src/PDFManipulator/TestPDFs/test.pdf'
#PDF = '/home/ashley/src/PDFManipulator/TestPDFs/emplaced(enc).pdf'
#PDF = '/home/ashley/src/PDFManipulator/TestPDFs/c4611_sample_explain(ENC).pdf'
#OutputFile = '/home/ashley/src/PDFManipulator/TestPDFs/test'
#OutputFile = '/'
#print(TestEncryption(PDF,"blah"))
#emplace(PDF,OutputFile,SUBPDF,2)
#RemoveEncryption(PDF,OutputFile,"blah")
#print(ConvertSimpleRange("1,3"))
#pdf = TryOpenPDF(PDF)
#if pdf[0] == True:
#	print("SUCCESS")
#	print(len(pdf[1].pages))
#else:
#	print("ERROR")
#RotatePages(PDF,OutputFile,ConvertRanges("1-3,5"),90)
#print(ConvertMixedRanges("1-3,5,9,12-18"))
#print(get_pages(PDF))
#a=split(PDF,OutputFile,(1,1),False)
#print(a)
#splittest(pdffile,outdir,(1,10))
#print(get_filename(PDF))
#join(folder,outfile,True)
#files_in_folder(folder)
#print(get_docinfo(PDF))
#print(pdf_datetime())

