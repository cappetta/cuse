#############################################################
# Edouard TALLENT @ TaGoMa.Tech, March, 2014                #
# Parse a series of online PDF documents to  build          #
# historical time series                                    #
# QuantCorner @ https://quantcorner.wordpress.com            #
#############################################################

# Some sources
# http://www.unixuser.org/~euske/python/pdfminer/programming.html
# http://denis.papathanasiou.org/2010/08/04/extracting-text-images-from-pdf-files/
# http://stackoverflow.com/questions/25665/python-module-for-converting-pdf-to-text

# Required headers
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import  TextConverter # , XMLConverter, HTMLConverter
import urllib2
from urllib2 import Request
import datetime
import re

# Define a PDF parser function
def parsePDF(url):

    # Open the url provided as an argument to the function and read the content
    open = urllib2.urlopen(Request(url)).read()

    # Cast to StringIO object
    from StringIO import StringIO
    memory_file = StringIO(open)

    # Create a PDF parser object associated with the StringIO object
    parser = PDFParser(memory_file)

    # Create a PDF document object that stores the document structure
    document = PDFDocument(parser)

    # Define parameters to the PDF device objet
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    codec = 'utf-8'

    # Create a PDF device object
    device = TextConverter(rsrcmgr, retstr, codec = codec, laparams = laparams)

    # Create a PDF interpreter object
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    # Process each page contained in the document
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        data =  retstr.getvalue()

    # Perform Regex
    # Get values for Iowa B100 prices
    reg = '(?<=\n---\n\n)\d.\d{2}-\d.\d{2}'
    matches = re.findall(reg, data)                 # Our data are contained in matches[0]

    # Compute the average
    # Extract value from previous regex
    low = re.search('\d.\d{2}(?=-)', matches[0])
    high = re.search('(?<=-)\d.\d{2}', matches[0])

    # Cast string variables to float type
    low_val = float(low.group(0))
    high_val = float (high.group(0))

    # Calculate the average
    #import numpy
    #value = [high_val, low_val]
    #print value.mean
    ave = (high_val + low_val) /2

    # Search the date of the report
    reg = '\w{3},\s\w{3}\s\d{2},\s\d{4}'
    match = re.search(reg, data)        # Result is contained in matches[0]
    dat = match.group(0)

    # Cast to date format
    #import datetime
    #form = datetime.datetime.strptime(match.group(0), '%a, %b %d, %Y')
    #print form

    # http://stackoverflow.com/questions/9752958/how-can-i-return-two-values-from-a-function-in-python
    return (dat, ave)

# The date of the latest weekly price bulletin
start_date = raw_input("Enter the date of the latest weekly price bulletin (dd/mm/yyyy): ")

# Convert start_date string to Python date format
dat = datetime.datetime.strptime(start_date,  '%d/%m/%Y')

# Time series length
back_weeks = raw_input("How many weeks back in time: ")

# A bit of order onto the screen
print '\n'
print 'Date as read in PDF' + '\t' + 'Formatted date' + '\t' + 'Value'

# Loop through the dates
for weeks in xrange(0, int(back_weeks)):

    # Basic exception handling mechamism
    try:
        wk = datetime.timedelta(weeks = weeks)
        date_back = dat - wk

        # Construct the url
        url = 'http://search.ams.usda.gov/mndms/' + str(date_back.year) + \
              '/' + str(date_back.month).zfill(2) + '/LS' + str(date_back.year) + \
              str(date_back.month).zfill(2) + str(date_back.day).zfill(2) + \
              'WAGENERGY.PDF'

        # Call to function
        fun =  parsePDF(url)

        # Information we are after
        res = str(fun[0]) + '\t' +  str(date_back.day).zfill(2) + '/' + \
              str(date_back.month).zfill(2) +  '/' + str(date_back.year) + \
              '\t' + str(fun[1])

    except Exception:
        print 'NA\t\t\t' +  str(date_back.day).zfill(2) + '/' + \
              str(date_back.month).zfill(2) +  '/' + str(date_back.year) + \
              '\t' + 'NA'

    # Output onto the screen
    print res

'''
Result example:

>>>

Date as read in PDF Formatted date  Value
Fri, Mar 07, 2014   07/03/2014  3.67
Fri, Feb 28, 2014   28/02/2014  3.57
Fri, Feb 21, 2014   21/02/2014  3.475
Fri, Feb 14, 2014   14/02/2014  3.225
Fri, Feb 07, 2014   07/02/2014  3.175
Fri, Jan 31, 2014   31/01/2014  3.15
Fri, Jan 24, 2014   24/01/2014  3.295
Fri, Jan 17, 2014   17/01/2014  3.24
Fri, Jan 10, 2014   10/01/2014  3.2
Fri, Jan 03, 2014   03/01/2014  3.825
Fri, Dec 27, 2013   27/12/2013  3.845
Fri, Dec 20, 2013   20/12/2013  3.855
Fri, Dec 13, 2013   13/12/2013  3.885
Fri, Dec 06, 2013   06/12/2013  4.025
Fri, Nov 29, 2013   29/11/2013  4.05
Fri, Nov 22, 2013   22/11/2013  4.025
Fri, Nov 15, 2013   15/11/2013  4.075
Fri, Nov 08, 2013   08/11/2013  4.325
Fri, Nov 01, 2013   01/11/2013  4.365
Fri, Oct 25, 2013   25/10/2013  4.54

'''