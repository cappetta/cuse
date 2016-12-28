from cStringIO import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import re

def convert(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = file(fname, 'rb')
    for pageNumber, page in enumerate(PDFPage.get_pages(infile, pagenums)):
        print "parsing through pages... %s " % pageNumber
        interpreter.process_page(page)

    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    reg = 'Number of Positions'
    positions = re.findall(reg, text)                 # Our data are contained in matches[0]
    if positions:
        # print(positions)
        extract_personal(text)

    # return text

def extract_personal(text):
    # print "Text::::: +> " + text
    # next((i for i, c in enumerate(text.split()) if c != ' '), len(text))
    for word in text.split("\n"):
        print "-" + word.strip() + "-"
        # for Grade, rate, position, # of positions (last yr/ this year)



def toc(fname):
    from pdfminer.pdfparser import PDFParser
    from pdfminer.pdfdocument import PDFDocument

    # Open a PDF document.
    fp = open(fname, 'rb')
    parser = PDFParser(fp)
    document = PDFDocument(parser)

    # Get the outlines of the document.
    outlines = document.get_outlines()
    for (level,title,dest,a,se) in outlines:
        print (level, title)


def pdf_to_csv(filename, separator, threshold):
    from cStringIO import StringIO
    from pdfminer.converter import LTChar, TextConverter
    from pdfminer.layout import LAParams
    from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
    from pdfminer.pdfpage import PDFPage

    class CsvConverter(TextConverter):
        def __init__(self, *args, **kwargs):
            TextConverter.__init__(self, *args, **kwargs)
            self.separator = separator
            self.threshold = threshold

        def end_page(self, i):
            from collections import defaultdict
            lines = defaultdict(lambda: {})
            for child in self.cur_item._objs:  # <-- changed
                if isinstance(child, LTChar):
                    (_, _, x, y) = child.bbox
                    line = lines[int(-y)]
                    line[x] = child._text.encode(self.codec)  # <-- changed
            for y in sorted(lines.keys()):
                line = lines[y]
                self.line_creator(line)
                self.outfp.write(self.line_creator(line))
                self.outfp.write("\n")

        def line_creator(self, line):
            keys = sorted(line.keys())
            # calculate the average distange between each character on this row
            average_distance = sum([keys[i] - keys[i - 1] for i in range(1, len(keys))]) / len(keys)
            # append the first character to the result
            result = [line[keys[0]]]
            for i in range(1, len(keys)):
                # if the distance between this character and the last character is greater than the average*threshold
                if (keys[i] - keys[i - 1]) > average_distance * self.threshold:
                    # append the separator into that position
                    result.append(self.separator)
                # append the character
                result.append(line[keys[i]])
            printable_line = ''.join(result)
            return printable_line

    # ... the following part of the code is a remix of the
    # convert() function in the pdfminer/tools/pdf2text module
    rsrc = PDFResourceManager()
    outfp = StringIO()
    device = CsvConverter(rsrc, outfp, codec="utf-8", laparams=LAParams())
    # becuase my test documents are utf-8 (note: utf-8 is the default codec)

    fp = open(filename, 'rb')

    interpreter = PDFPageInterpreter(rsrc, device)
    for i, page in enumerate(PDFPage.get_pages(fp)):
        outfp.write("START PAGE %d\n" % i)
        if page is not None:
            interpreter.process_page(page)
            # reg = 'Number of Positions'
            # text = page.getvalue()
            # positions = re.findall(reg, text)                 # Our data are contained in matches[0]
            # if positions:
            #     print(positions)
            #     extract_personal(text)
    outfp.write("END PAGE %d\n" % i)




    device.close()
    fp.close()
    return outfp.getvalue()



def main():
    src = "./budgets/2016-2017_BUDGET.pdf"
    # pdftxt = convert(src, [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17])
    # pdftxt = convert(src, [125,126,127,128])
    pdftxt = convert(src, [128])
    # print(pdftxt)
    # toc(src)

    # the separator to use with the CSV
    separator = ' '
    # the distance multiplier after which a character is considered part of a new word/column/block. Usually 1.5 works quite well
    threshold = 1.5
    # print pdf_to_csv(src, separator, threshold)

if __name__ == '__main__':
    main()


