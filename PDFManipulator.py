#import wx
import PyPDF4 as pypdf

pdffile = '/home/ashley/Astronomical Algorithms.pdf'
outdir = '/home/ashley/PDFManipulator/test/'

def get_pages(PDF_FILE):
	pdf = pypdf.PdfFileReader(PDF_FILE)
	return pdf.getNumPages()

def get_docinfo(PDF_FILE):
	pdf = pypdf.PdfFileReader(PDF_FILE)
	return pdf.getDocumentInfo()

def update_meta(docinfo,PDFWriterObj):
	# updates the metadata of the PDF output so that it matches that of the input. Changes the "Producer" key to "PDFManipulator" to flag that the file hasn't been 
	meta = PDFWriterObj._info.getObject()
	# cycle through each document property and re-add it to the file
	for key in docinfo:
		meta.update({pypdf.generic.NameObject(key): pypdf.generic.createStringObject(docinfo[key])})
	# correct the Producer String otherwise it points to the original producer
	meta.update({pypdf.generic.NameObject('/Producer'): pypdf.generic.createStringObject(u'PyPDF4')})
	

def dismantle(PDF_FILE,OUT_DIR):
	pdf = pypdf.PdfFileReader(PDF_FILE)
	pages = get_pages(PDF_FILE)
	docinfo = get_docinfo(PDF_FILE)
	pdf_writer = pypdf.PdfFileWriter()
	# cycle through every page and add it to a writer object
	for i in range(pages):
		
		pdf_writer.addPage(pdf.getPage(i))
		
		#update the metadata of the output so it matches that of the original
		update_meta(docinfo,pdf_writer)
		# create filename. range is 0 based, so add in 1 so that page numbers match		
		output = f'{OUT_DIR}{i+1}.pdf'
		with open(output,'wb') as out:
			pdf_writer.write(out)
			out.close
		
	
#print(get_docinfo(pdffile))
dismantle(pdffile,outdir)
