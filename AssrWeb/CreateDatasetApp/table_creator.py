from io import BytesIO
import numpy as np
from pandas import DataFrame, read_csv, concat
from PyPDF2 import PdfReader
from PyPDF2.errors import PdfReadError


class TableCreator:

    files: list[bytes]

    def __init__(self, files):
        self.files = files


    def to_dataframe(self) -> DataFrame:

        if not self.files:
            return DataFrame()

        # Read all files and determine file formats
        df_list = []
        single_column = True
        for i, file in enumerate(self.files):
            stream = BytesIO(file)
            csv = True
            pdf = True
            df = None

            try:
                reader = PdfReader(stream)
                page_test = [p.extract_text() for p in reader.pages]
                text = " \n ".join(page_test)
                
                df = DataFrame([text], columns=["documents"])
                df_list.append(df)
                single_column &= (df.shape[1] == 1)
                continue

            except PdfReadError:
                pdf = False

            stream.seek(0)

            try:
                df = read_csv(stream)
                df_list.append(df)
                single_column &= (df.shape[1] == 1)
                continue

            except UnicodeDecodeError:
                csv = False

            if not (csv or pdf):
                raise AttributeError(f"file formats for index {i} is not in (.csv, .pdf)")
            
        # Coerce to single column irrespective of column names (allows to combine CSV with PDF)
        if single_column:
            data = [df.iloc[0, 0] for df in df_list]
            return DataFrame(data, columns=["documents"])
         
        # Else, combine according to column names (maked lirrle sence for a blend of CSV and PDF)           
        return concat(df_list, ignore_index=True)


    def to_html(self) -> str:
        df = self.to_dataframe()
        class_np = np.full(df.shape, "frame-b")
        styled = df.style.set_td_classes(
            DataFrame(class_np, index=df.index, columns=df.columns)
        )
        return styled.to_html(
            table_attributes='class="w-100 main-text frame-b"',
            bold_headers=False,
            exclude_stylesbool=True
        )
    

    def to_csv(self) -> BytesIO:
        df = self.to_dataframe()
        buffer = BytesIO()
        df.to_csv(buffer)
        buffer.seek(0)

        return buffer