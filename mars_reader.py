import input_reader
import re

class MarsReader(input_reader.InputReader):
    def __init__(self, path):
        self.path = path
        self.sor = re.compile("S_O_H")
        self.eoh = re.compile("E_O_H")
        self.eor = re.compile("E_O_R")

    def process(self) -> list:
        out = []
        doc = {}
        inRecord = False
        inHeader = False
        id = 1

        file = open(self.path, "r")
        while True:
            line = file.readline()
            if self.sor.match(line) and not inRecord:
                doc = {"id": id}
                id += 1
                inRecord = True
                inHeader = True
                continue
            if self.eoh.match(line):
                inHeader = False
                continue
            if self.eor.match(line):
                inRecord = False
                out.append(doc)
                continue

            if inRecord and inHeader:
                doc["header"] = doc.get("header", "") + line

            if inRecord and not inHeader:
                doc["text"] = doc.get("text", "") + line

            if not line:
                break

        file.close()
        return out