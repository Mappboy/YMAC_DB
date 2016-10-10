"""
Extract title from PDF file.
Depends on: pyPDF, PDFMiner.
Usage:
    find . -name "*.pdf" |  xargs -I{} pdftitle -d tmp --rename {}
"""

import getopt
import os
import re
import string
import sys
from io import StringIO

from PyPDF2 import PdfFileReader
from PyPDF2.utils import PdfReadError
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter#process_pdf
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFSyntaxError

__all__ = ['pdf_title']

def sanitize(filename):
    """
    Turn string to valid file name.
    """
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    return ''.join([c for c in filename if c in valid_chars])

def meta_title(filename):
    """
    Title from pdf metadata.
    """
    try:
        docinfo = PdfFileReader(open(filename, 'rb')).getDocumentInfo()
        return docinfo.title if docinfo.title else ""
    except PdfReadError:
        return ""

def copyright_line(line):
    """
    Judge if a line is copyright info.
    """
    return re.search(r'technical\s+report|proceedings|preprint|to\s+appear|submission', line.lower())

def empty_str(s):
    return len(s.strip()) == 0

def pdf_text(filename):
    try:

        # PDFMiner boilerplate
        rsrcmgr = PDFResourceManager()
        sio = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, sio, codec=codec, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        # Extract text
        fp = open(filename, 'rb')
        for page in PDFPage.get_pages(fp):
            interpreter.process_page(page)
        fp.close()

        # Get text from StringIO
        text = sio.getvalue()

        # Cleanup
        device.close()
        sio.close()

        return text
    except (PDFSyntaxError):
        return ""

def title_start(lines):
    for i, line in enumerate(lines):
        if not empty_str(line) and not copyright_line(line):
            return i;
    return 0

def title_end(lines, start, max_lines=2):
    for i, line in enumerate(lines[start+1:start+max_lines+1], start+1):
        if empty_str(line):
            return i
    return start + 1

def text_title(filename):
    """
    Extract title from PDF's text.
    """
    lines = pdf_text(filename).strip().split('\n')

    i = title_start(lines)
    j = title_end(lines, i)

    return ' '.join(line.strip() for line in lines[i:j])

def valid_title(title):
    return not empty_str(title) and empty_str(os.path.splitext(title)[1])

def pdf_title(filename):
    title = meta_title(filename)
    if valid_title(title):
        return title

    title = text_title(filename)
    if valid_title(title):
        return title

    return os.path.basename(os.path.splitext(filename)[0])

if __name__ == "__main__":
    opts, args = getopt.getopt(sys.argv[1:], 'nd:', ['dry-run', 'rename'])

    dry_run = False
    rename = False
    dir = "."

    for opt, arg in opts:
        if opt in ['-n', '--dry-run']:
            dry_run = True
        elif opt in ['--rename']:
            rename = True
        elif opt in ['-d']:
            dir = arg

    if len(args) == 0:
        print("Usage: %s [-d output] [--dry-run] [--rename] filenames" % sys.argv[0])
        sys.exit(1)

    for filename in args:
        title = pdf_title(filename)
        if rename:
            new_name = os.path.join(dir, sanitize(' '.join(title.split())) + ".pdf")
            print("%s => %s" % (filename, new_name))
            if not dry_run:
                if os.path.exists(new_name):
                    print("*** Target %s already exists! ***" % new_name)
                else:
                    os.rename(filename, new_name)
        else:
            print(title)