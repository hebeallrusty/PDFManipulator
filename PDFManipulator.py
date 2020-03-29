#import wx
import PyPDF4 as pypdf
import platform

pdffile = '/home/ashley/Astronomical Algorithms.pdf'
outdir = '/home/ashley/PDFManipulator/test/'

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
	

def split(PDF_FILE,OUT_DIR,PageRange,dismantle = False):
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
		
	
#print(get_docinfo(pdffile))
split(pdffile,outdir,(1,2),True)
#get_filename(pdffile)
