from PyPDF2 import PdfReader
from PyPDF2.errors import PdfReadError
from io import BytesIO
import base64
from pandas import read_csv
from CreateDatasetApp.table_creator import TableCreator


class ContentCreator():
    """Class for source file content geraton."""

    def __init__(self, files):
        self.files = files

    def to_html_embed(self, height="100%", width="100%") -> str:
        """
        Method will return html string with ether table\n
        in case of csv and in case of pdf embed tag.
        """
        style = """<embed
                src="data:application/pdf;base64,{0}"
                type="application/pdf"
                frameBorder="0"
                scrolling="auto"
                height={1}
                width={2}
            ></embed>
            """
        styled = """"""

        csv_list = []
        csv = False
        for i, file in enumerate(self.files):
            stream = BytesIO(file)
            try:
                PdfReader(stream)
                base = base64.b64encode(file).decode()
                styled += style.format(
                    base,
                    height,
                    width
                )
                continue
            except PdfReadError:
                try:
                    read_csv(stream)
                    csv_list.append(file)
                    csv = True
                except UnicodeDecodeError:
                    raise AttributeError(
                        f"file formats for index {i} is not in (.csv, .pdf)"
                    )
        if csv:
            styled += TableCreator(csv_list).to_html()
        return styled