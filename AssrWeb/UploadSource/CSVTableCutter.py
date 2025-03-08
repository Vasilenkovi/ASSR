from pandas import read_csv, DataFrame
import numpy as np
import json
from io import BytesIO


class CSVTableCutter():
    """Create a html storing object\n
    get html rows using getNRows method\n"""
    def __init__(self, file):
        self.files = file

        stream = BytesIO(file)
        try:
            self.df = read_csv(stream)
        except UnicodeDecodeError:
            raise AttributeError(
                "file format is not (.csv)"
            )
        stream.close()

    def getHeader(self) -> list[str]:
        html_header = "<thead>\n<tr>\n<th></th>\n"
        for header in self.df.columns.to_list():
            html_header += f"<th>{header}</th>"
        html_header += "</tr>\n</thead>"
        return html_header

    def getNRows(self, begin_from: int, step: int) -> str:
        look = self.df[begin_from:begin_from+step].to_json()
        return look

    def getEnd(self) -> int:
        """
        Returns end index.
        """
        return self.df.shape[0] - 1
