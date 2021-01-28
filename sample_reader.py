import input_reader
import glob
import os
import PyPDF2

class SampleReader(input_reader.InputReader):

    def __init__(self, directory):
        self.directory = directory

    def process(self) -> list:
        out = []
        os.chdir(self.directory)
        id = 1
        for file in glob.glob("*.pdf"):
            doc = {"id": id, "language": "en"}
            pdfInputFile = open(file, 'rb')
            pdfReader = PyPDF2.PdfFileReader(pdfInputFile)
            for i in range(pdfReader.numPages):
                pageObj = pdfReader.getPage(i)
                doc['text'] = doc.get('text', '') + pageObj.extractText()
            pdfInputFile.close()
            out.append(doc)
            id+=1
        return out


