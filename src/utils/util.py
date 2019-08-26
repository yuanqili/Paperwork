import hashlib
import re
import urllib.parse

from PyPDF2 import PdfFileReader, PdfFileWriter


def hash(path):
    m = hashlib.md5(open(str(path), 'rb').read())
    return m.digest()


def remove_links(pdf_path):
    pdf = PdfFileReader(open(str(pdf_path), 'rb'))
    out = PdfFileWriter()
    for page in range(pdf.numPages):
        out.addPage(pdf.getPage(page))
    out.removeLinks()
    out_path = pdf_path.parent / f'{pdf_path.stem}-pure.pdf'
    with open(out_path, 'wb') as o:
        out.write(o)


def build_url(base, path, params):
    url_parts = list(urllib.parse.urlparse(base))
    url_parts[2] = path
    url_parts[4] = urllib.parse.urlencode(params)
    return urllib.parse.urlunparse(url_parts)


def format_str(s):
    s = s.replace(' - ', '-')
    s = s.replace(' : ', ': ')
    s = s.replace(' . ', '. ')
    return s


def format_venue(s):

    # leading year
    leading_year = None
    me = re.match('\d{4}', s[:4])
    if me:
        leading_year = int(me.group())
        s = s[4:]
    # trailing year
    trailing_year = None
    me = re.match('\d{4}', s[-4:])
    if me:
        trailing_year = int(me.group())
        s = s[:-4]

    year = None
    if leading_year:
        year = leading_year
    if trailing_year:
        year = trailing_year
    if leading_year and trailing_year:
        if leading_year == trailing_year:
            year = leading_year
        else:
            year = None

    return {
        'venue': s.strip(),
        'year': year,
    }
