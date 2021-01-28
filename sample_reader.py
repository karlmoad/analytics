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
            doc = {"id": id, "name": file, "text": ""}
            pdfInputFile = open(file, 'rb')
            pdfReader = PyPDF2.PdfFileReader(pdfInputFile)
            for i in range(pdfReader.numPages):
                pageObj = pdfReader.getPage(i)
                doc["text"] = doc["text"] + " " + pageObj.extractText()
            pdfInputFile.close()
            out.append(doc)
            id+=1
        return out