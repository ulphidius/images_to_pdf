from PyPDF2 import PdfFileReader, PdfFileMerger

def merge_pdf_files(chapters_files, output_filename):
    merger = PdfFileMerger()
    pdf_files = get_pdf_file(chapters_files)
    output_file = list()

    for file in pdf_files:
        merger.append(
            fileobj=file,
            bookmark=file.getDocumentInfo().title,
            import_bookmarks=True
        )

    with open(output_filename, 'wb') as output_file:
        merger.write(output_file)

    merger.close()

def get_pdf_file(chapters_files):
    return map(PdfFileReader, chapters_files)
