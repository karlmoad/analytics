import formatter
import re

class SampleFormatter(formatter.Formatter):
    # Notes: -----------------------------------------------------------------
    # * block size determined by self.lim value
    # * document id is derived from original document id multi by 100 + block id
    # * pages may be broken across blocks
    def prepare(self, document: dict) -> list:
        out = []
        baseDocid = document["id"]
        chunks = self._chunker(document["text"])
        id = 1
        for chunk in chunks:
            tmp = {"id": baseDocid * 100 + id, "language": "en", "text": chunk}
            id+=1
            out.append(tmp)
        return out

    def _chunker(self, chunk: str) -> list:
        out = []
        target = self.lim
        max = self.noexceed
        while len(chunk) > 0:
            buffer = chunk[:target]
            rem = chunk[target:]
            if len(rem) > 0:
                if len(buffer) + len(rem) <= max:
                    buffer += rem
                    rem = ""
                else:
                    m = re.search("[\?\.\!\:\;]", rem)
                    if m is not None:
                        size = m.start() + 1
                        if (len(buffer) + size) <= max:
                            buffer = buffer + rem[:size]
                            rem = rem[size:]
            out.append(buffer)
            chunk = rem
        return out


