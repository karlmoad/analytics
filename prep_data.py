import PyPDF2
import json

files = list()

files.append('docs/Family_Medicine_HP.pdf')
files.append('docs/sample_written_H_and_P.pdf')
files.append('docs/SampleWriteUp.pdf')

print(files)

# creating a pdf file object
pdfFileObj = open('docs/Family_Medicine_HP.pdf', 'rb')

# creating a pdf reader object
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

# printing number of pages in pdf file
print(pdfReader.numPages)

for i in range(pdfReader.numPages):
# creating a page object
    pageObj = pdfReader.getPage(i)
# extracting text from page
    print(pageObj.extractText())

# closing the pdf file object
pdfFileObj.close()
