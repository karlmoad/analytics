import formatter
import sample_formatter
import re

class MarsFormatter(sample_formatter.SampleFormatter):
    def prepare(self, document: dict) -> list:
        return super().prepare(document)

    def _chunker(self, chunk: str) -> list:
        return super()._chunker(chunk)
