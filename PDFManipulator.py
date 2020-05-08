#import wx
import platform
import os
import datetime as dt
import pikepdf
from pikepdf import _cpphelpers

PROGRAM_DATE = 20200507


def version():
	return PROGRAM_DATE

def swap_item(alist,pos1,pos2):
	alist[pos1],alist[pos2] = alist[pos2],alist[pos1]
	return alist

def get_pages(PDF_FILE):
	pdf = pikepdf.Pdf.open(PDF_FILE)
	return len(pdf.pages)

def get_docinfo(PDF_FILE):
	# open the pdf file
	pdf = pikepdf.Pdf.open(PDF_FILE)
	
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
	
	return meta
	

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
	with DocObj.open_metadata() as meta:
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
	PIKEPDF_VER = pikepdf.__version__
	return f'pikepdf {PIKEPDF_VER}'

def pdf_timestamp():
	# generate PDF timestamp relative to utc time
	# timestamp format 2010-11-27T13:41:17+01:00
	NOW = dt.datetime.utcnow()
	#print(NOW)
	# NEEDS TO BE 4 DIGIT YEAR, 2 DIGIT MOND DAY HOUR MINUTE AND SECOND
	return f'{NOW.year:04}-{NOW.month:02}-{NOW.day:02}T{NOW.hour:02}:{NOW.minute:02}:{NOW.second:02}+00:00'


def split(PDF_FILE,OUT_DIR,PageRange,dismantle = False):
	# PDF_FILE must be a single PDF file
	# OUT_DIR must be a folder where the files will be created
	# PageRange must be a tuple containing start and end pages
	# dismantle denotes whether single files are required (True) or one file containing the range of pages (False)

	print(f'Opening {PDF_FILE}')
	pdf = pikepdf.Pdf.open(PDF_FILE)
	print(f'Getting Document Properties')
	meta = get_docinfo(PDF_FILE)
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
			doc.save(output,min_version=version)
			
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
		doc.save(output,min_version=version)
		

	

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
		PDF_FILES = files_in_folder(PDF_FILES)

	for PDF in PDF_FILES:
		print(f'Opening {PDF}')
		# Open source document
		pdf = pikepdf.Pdf.open(PDF)
		# keep track of versions so that we write a pdf of the highest version to support the most features in the output
		version = max(version,pdf.pdf_version)
		# pikepdf pages are list objects so extend into the source doc
		doc.pages.extend(pdf.pages)

	#remove unreferenced material as internal structure changed
	doc.remove_unreferenced_resources()
	print(f'Saving file as {OUT_FILENAME} (PDF Version {version})')
	# open meta as writeable for new pdf
	with doc.open_metadata() as docmeta:
		docmeta['xmp:ModifyDate'] = pdf_timestamp()
		docmeta['xmp:CreateDate'] = pdf_timestamp()	
		docmeta['xmp:CreatorTool'] = pdf_creator()
	doc.save(OUT_FILENAME,min_version=version)

def encrypt(PDF_FILE,OUT_FILENAME,Password,Strength):
	# open pdf file
	
	print(f'Opening {PDF_FILE}')
	pdf = pikepdf.Pdf.open(PDF_FILE)

	
	output = f'{OUT_FILENAME}.pdf'
	no_extracting = pikepdf.Permissions(extract=False)
	print(f'Writing file {output}')
	pdf.save(output,encryption = pikepdf.Encryption(user = Password, owner = Password[::-1], R=Strength, allow=no_extracting))

def emplace(PDF_FILE,OUT_FILENAME,SUBS,PAGE):
	# substitute pages in PDF_FILE for those in Subs.
	# Pages are zero indexed (i.e pdf page 1 is Page=0)
	
	print(f'Opening {PDF_FILE}')
	pdf = pikepdf.Pdf.open(PDF_FILE)
	print(f'Opening {SUBS}')
	subpdf = pikepdf.Pdf.open(SUBS)
	version = [pdf.pdf_version,subpdf.pdf_version]
	pages = [get_pages(PDF_FILE),get_pages(SUBS)]
	print(f'Pages: {pages} Version: {version}')
	
	# Check if the replacement pages exceeds the end of the document
	#if pages[1] + PAGE > pages[0]:
	#	print(f'Replacement pages exceeds the original document pages')
	
	# replace page
	# add substitue page to end of document (currently just the first page - plan to add extras) into original doc
	pdf.pages.append(subpdf.pages[0])
	# carry out the substitution
	pdf.pages[PAGE].emplace(pdf.pages[-1])
	# delete the added page
	del pdf.pages[-1]
	
	# create filename and save		
	output = f'{OUT_FILENAME}.pdf'
	print(f'Writing file {output}')
	# save the pdf with the greatest pdf version of both files	
	pdf.save(output,min_version=max(version))
	
def TestEncryption(PDF_FILE):
	try:
		pdf = pikepdf.Pdf.open(PDF_FILE)
	except pikepdf._qpdf.PasswordError:
		return True
	else:
		return False

# TESTS
#PDF = '/home/ashley/src/PDFManipulator/TestPDFs/file-example_PDF_500_kB.pdf'
#PDF = '/home/ashley/src/PDFManipulator/TestPDFs/c4611_sample_explain.pdf'
#PDF = '/home/ashley/src/PDFManipulator/TestPDFs/c4611_sample_explain.pdf'
#PDF = '/home/ashley/src/PDFManipulator/TestPDFs/pdf-test.pdf'
#PDF = '/home/ashley/src/PDFManipulator/TestPDFs/emplaced(enc).pdf'
#OutputFile = '/home/ashley/src/PDFManipulator/TestPDFs/TESTTEST.pdf'
print(TestEncryption(PDF))
#emplace(PDF,OutputFile,subpdf,1)

#print(get_pages(pdffile))

#split(PDF,OutputFile,(1,1),False)
#splittest(pdffile,outdir,(1,10))
#print(get_filename(PDF))
#join(folder,outfile,True)
#files_in_folder(folder)
#print(get_docinfo(outfile))
#print(pdf_datetime())
#passwd = wx.PasswordEntryDialog(None, "Whats the  password", 'Password','',style=wx.TextEntryDialogStyle)
#        	ans = passwd.ShowModal()
#        	if ans == wx.ID_OK:
#        		entered_password = passwd.GetValue()
#        	else:
#        		entered_password = False
#        	print("password ", entered_password)
#        	passwd.Destroy()	
