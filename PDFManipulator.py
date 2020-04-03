#import wx
import platform
import os
import datetime as dt
import pikepdf

PROGRAM_DATE = '20200403'


def get_pages(PDF_FILE):
	pdf = pikepdf.Pdf.open(PDF_FILE)
	return len(pdf.pages)

def get_docinfo(PDF_FILE):
	pdf = pikepdf.Pdf.open(PDF_FILE)
	meta = pdf.open_metadata()

	#for key in meta:
		
	#	print(f'{key}:{meta[key]}')
	return meta

def get_filename(PDF_FILE):
	# check which system we are running as this governs the directory name delimiter
	if platform.system() == 'Windows':
		dir_char = '/'
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
	
	# open meta as writeable for new pdf
	with DocObj.open_metadata() as meta:
		#cycle through each key in the Source meta, and write that into the new blank file
		for key in SrcMeta:
			meta[key] = SrcMeta[key]
		# alter the Modified Date
		meta['xmp:ModifyDate'] = pdf_timestamp()
		meta['xmp:CreatorTool'] = pdf_creator()
	
def pdf_creator():
	return f'PDFManipulator {PROGRAM_DATE}'
	
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
	
	filename = get_filename(PDF_FILE) # for the output	
	
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
	
		output = f'{OUT_DIR}{filename}({PageRange[0]}-{PageRange[1]}).pdf'
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

##### Testing ######

pdffile = '/home/ashley/Astronomical Algorithms.pdf'
outdir = '/home/ashley/PDFManipulator/test/'
pdffiles = []
for i in range (1,10):
	pdffiles.append(f'/home/ashley/PDFManipulator/test/Astronomical Algorithms({i}).pdf')
pdffiles.append('/home/ashley/PDFManipulator/test/OUTPUT.pdf')
outfile = '/home/ashley/PDFManipulator/test/OUTPUT.pdf'

folder = '/home/ashley/PDFManipulator/test'

#print(get_pages(pdffile))
#print(get_docinfo('/home/ashley/PDFManipulator/test/Astronomical Algorithms(1).pdf'))
#split(pdffile,outdir,(1,10),True)
#splittest(pdffile,outdir,(1,10))
#get_filename(pdffile)
join(folder,outfile,True)
#files_in_folder(folder)
#print(get_docinfo(outfile))
#print(pdf_datetime())
