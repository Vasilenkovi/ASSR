from pandas import read_csv
import base64
from PyPDF2 import PdfReader
from PyPDF2.errors import PdfReadError
from io import BytesIO

from CreateDatasetApp.table_creator import TableCreator


class ContentCreator():
    """Create a html storing object\n
    get html rows using getNRows method\n"""
    def __init__(self, files: list):
        self.files = files

        if len(files) == 1:
            stream = BytesIO(files[0])
            try:
                PdfReader(stream)
                base = base64.b64encode(files[0]).decode()
                style = """<embed
                        src="data:application/pdf;base64,{0}"
                        type="application/pdf"
                        frameBorder="0"
                        scrolling="auto"
                        height={1}
                        width={2}
                    ></embed>
                """
                self.styled = style.format(
                    base,
                    "100%",
                    "100%"
                )
                self.type = "pdf"
            except PdfReadError:
                try:
                    self.df = read_csv(stream)
                    self.type = "csv"
                except UnicodeDecodeError:
                    raise AttributeError(
                        "CSVTableCutter will not be " +
                        "created file format is not (.csv)"
                    )
            stream.close()
        else:
            self.type = "csv"
            TC = TableCreator(files)
            self.df = TC.to_dataframe()

    def getHeader(self) -> list[str]:
        """
        Returns head of table in case of csv,
        in case of pdf will return embed.
        """
        if self.type != "pdf":
            html_header = "<thead>\n<tr>\n<th></th>\n"
            html_header += (
                '<th><input class="column-header-checkbox" ' +
                'data-col="0" type="checkbox"></th>\n'
            )
            for header in self.df.columns.to_list():
                html_header += f"<th>{header}</th>"
            html_header += "</tr>\n</thead>"
            return html_header
        return self.styled

    def getNRows(self, begin_from: int, step: int) -> str:
        if self.type != "pdf":
            return self.df[begin_from:begin_from+step].to_json()
        return ""

    def getEnd(self) -> int:
        """
        Returns end index if file was csv.
        """
        return self.df.shape[0] - 1 if self.type != "pdf" else "" 
