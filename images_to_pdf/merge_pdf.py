from PyPDF2 import PdfFileReader, PdfFileMerger

def merge_pdf_files(chapters_files, output_filename):
    merger = PdfFileMerger()
    pdf_files = get_pdf_file(chapters_files)
    output_file = list()
    number_of_pages = 0

    for file in pdf_files:
        bookmarks = file.getOutlines()
        if not bookmarks:
            merger.append(
                fileobj=file,
                bookmark=file.getDocumentInfo().title,
                import_bookmarks=False
            )

            continue

        merger.append(
            fileobj=file,
            import_bookmarks=False
        )

        parent = merger.addBookmark(file.getDocumentInfo().title, number_of_pages)
        add_childs_bookmarks(bookmarks, number_of_pages, parent, merger)
        number_of_pages += file.getNumPages()

    merger.addMetadata({
        u'/Title': u'{}'.format(output_filename.split('/')[-1].split('.')[0])
    })
    with open(output_filename, 'wb') as output_file:
        merger.write(output_file)

    merger.close()

def get_pdf_file(chapters_files):
    return map(PdfFileReader, chapters_files)

def add_childs_bookmarks(bookmarks, start_page, parent, merger):
    current_page = start_page

    for bookmark in bookmarks:
        merger.addBookmark(bookmark.title, current_page + bookmark.page, parent)
