#import wx
import PyPDF4 as pypdf
import platform
import os
import datetime as dt

pdffile = '/home/ashley/Astronomical Algorithms.pdf'
outdir = '/home/ashley/PDFManipulator/test/'
pdffiles = []
for i in range (1,10):
	pdffiles.append(f'/home/ashley/PDFManipulator/test/Astronomical Algorithms({i}).pdf')
pdffiles.append('/home/ashley/PDFManipulator/test/OUTPUT.pdf')
outfile = '/home/ashley/PDFManipulator/test/OUTPUT.pdf'

folder = '/home/ashley/PDFManipulator/test'


def get_pages(PDF_FILE):
	pdf = pypdf.PdfFileReader(PDF_FILE)
	return pdf.getNumPages()

def get_docinfo(PDF_FILE):
	pdf = pypdf.PdfFileReader(PDF_FILE)
	return pdf.getDocumentInfo()

def get_filename(PDF_FILE):
	# check which system we are running as this governs the directory name delimiter
	if platform.system() == 'Windows':
		dir_char = '/'
	else:
		dir_char = '/'
	print(f'Program running on {platform.system()} and directory character = {dir_char}')
	string = PDF_FILE.rpartition(dir_char)
	# filename is the 3rd item that is returned from rpartition but still contains .pdf so split the string again to remove this suffix
	#print(string[2].rpartition('.')[0])
	return string[2].rpartition('.')[0]
	
	

def update_meta(docinfo,PDFWriterObj):
	# updates the metadata of the PDF output so that it matches that of the input. Changes the "Producer" key to "PDFManipulator" to flag that the file hasn't been 
	meta = PDFWriterObj._info.getObject()
	# cycle through each document property and re-add it to the file
	for key in docinfo:
		meta.update({pypdf.generic.NameObject(key): pypdf.generic.createStringObject(docinfo[key])})
	# correct the Producer String otherwise it points to the original producer
	meta.update({pypdf.generic.NameObject('/Producer'): pypdf.generic.createStringObject(u'PyPDF4')})
	# TODO - make this work - or at least match the pdf version	
	#PDFWriterObj._header.replace(b_("%PDF-1.3"),b_("%PDF-1.6"))
	
def pdf_timestamp():
	# generate PDF timestamp relative to utc time
	NOW = dt.datetime.utcnow()
	return f'D:{NOW.year}{NOW.month}{NOW.day}{NOW.hour}{NOW.minute}{NOW.second}+01\'00\''


def split(PDF_FILE,OUT_DIR,PageRange,dismantle = False):
	# PDF_FILE must be a single PDF file
	# OUT_DIR must be a folder where the files will be created
	# PageRange must be a tuple containing start and end pages
	# dismantle denotes whether single files are required (True) or one file containing the range of pages (False)

	print(f'Opening {PDF_FILE}')
	pdf = pypdf.PdfFileReader(PDF_FILE)
	print(f'Getting Document Properties')
	docinfo = get_docinfo(PDF_FILE)
	
	filename = get_filename(PDF_FILE) # for the output	
	
	pdf_writer = pypdf.PdfFileWriter() # initiate pdf_writer object - needed for ranges
	# cycle through every page and add it to a writer object
	print(f'Entering Page loop for pages {PageRange[0]} to {PageRange[1]}')
	for i in range(PageRange[0]-1,PageRange[1]): # pypdf is zero indexed, pdf files are one indexed
		print(f'Dealing with page {i+1}')
		if dismantle == True: 
			
			if i != PageRange[0] - i: #we already have a pdf_writer object
				pdf_writer = pypdf.PdfFileWriter() # writer needs to be in loop so a new instance is used each run, otherwise file sizes grow large
			# add page to pdf that is to be written		
			pdf_writer.addPage(pdf.getPage(i))
		
			#update the metadata of the output so it matches that of the original
			update_meta(docinfo,pdf_writer)
			# create filename. range is 0 based, so add in 1 so that page numbers match		
			output = f'{OUT_DIR}{filename}({i+1}).pdf'
			print(f'Writing file {output}')
			with open(output,'wb') as out:
				pdf_writer.write(out)
				out.close
		else:
			pdf_writer.addPage(pdf.getPage(i))
			if i == PageRange[1] - 1: # we have done all the pages in the range, need to write
				#update the metadata of the output so it matches that of the original
				update_meta(docinfo,pdf_writer)				
				output = f'{OUT_DIR}{filename}({PageRange[0]}-{PageRange[1]}).pdf'
				print(f'Writing file {output}')
				with open(output,'wb') as out:
					pdf_writer.write(out)
					out.close
def files_in_folder(FOLDER):
	# case sensitive so lowercase all ext and then test
	return [os.path.join(FOLDER,FILE) for FILE in os.listdir(FOLDER) if FILE.lower().endswith(".pdf")]
	

def join(PDF_FILES,OUT_FILENAME,folder=False):
	# PDF_FILES must be a list of files or a folder of pdf files (must use folder=True to denote Folder)
	# OUT_FILENAME is the file that will be created
	# folder is the switch to denote tha PDF_FILES is actually a folder
	
	# initiate the writer object
	pdf_writer = pypdf.PdfFileWriter()
	# if we are dealing with a folder - get all the pdf's in that folder and convert that into the PDF_FILES
	if folder == True:
		print(f'getting all PDF files in {PDF_FILES}')
		PDF_FILES = files_in_folder(PDF_FILES)

	for PDF in PDF_FILES:
		print(f'Opening {PDF}')
		# get a writer object
		pdf = pypdf.PdfFileReader(PDF)
		# we need all the pages to add to the writer object in the page writer loop
		pages = get_pages(PDF)
		print(f'{PDF} has {pages} pages')
		
		for PAGE in range(pages):
			print(f'Dealing with page {PAGE+1} in {PDF}')
			# add each page to the writer
			pdf_writer.addPage(pdf.getPage(PAGE))

	# TODO make this work properly - put in the creation date and modified date as today
	print(f'{pdf_timestamp()}')
	meta = pdf_writer._info.getObject()
	meta.update({pypdf.generic.NameObject('/CreationDate'): pypdf.generic.createStringObject(pdf_timestamp())})
	meta.update({pypdf.generic.NameObject('/ModDate'): pypdf.generic.createStringObject(pdf_timestamp())})
	
	print(f'Writing {OUT_FILENAME}')
	with open(OUT_FILENAME,'wb') as out:
		pdf_writer.write(out)


print(get_docinfo(pdffile))
#split(pdffile,outdir,(1,get_pages(pdffile)),True)
#get_filename(pdffile)
join(folder,outfile,True)
#files_in_folder(folder)
print(get_docinfo(outfile))
#print(pdf_datetime())
