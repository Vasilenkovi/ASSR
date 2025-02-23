from io import BytesIO
import html
import re
import numpy as np
import pandas as pd
from pandas import DataFrame, read_csv, concat
from PyPDF2 import PdfReader
from PyPDF2.errors import PdfReadError
from bs4 import BeautifulSoup

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
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        df = df.reset_index(drop=True)
        df.insert(0, '', df.index)
        
        def format_cell(x):
            if pd.isna(x):
                return f'<input class="table-cell" value="" />'
            return f'<input class="table-cell" value="{html.escape(str(x))}" />'
        
        cell_formatter = {
            '': lambda x: f'<input type="checkbox" class="row-checkbox" data-rowid="{x}">',
            **{
                col: lambda x, row_idx=row_idx, col_idx=col_idx: format_cell(x)
                for col_idx, col in enumerate(df.columns[1:], start=1)
                for row_idx in range(len(df))
            }
        }
        
        styled = df.style.format(cell_formatter, escape=False)
        

        class_np = np.full(df.shape, "frame-b")
        styled.set_td_classes(
            DataFrame(class_np, index=df.index, columns=df.columns)
        )
        
        html_str = styled.to_html(
            table_attributes='class="w-100 main-text frame-b"',
            bold_headers=False,
            exclude_styles=True,
            escape=False
        )
        html_str = re.sub(
            r'<th>(.*?)</th>',
            lambda m: f'<th><label><input type="checkbox" class="column-checkbox"> {m.group(1)}</label></th>' 
                    if m.group(1).strip() != '' else '<th></th>',
            html_str
        )
        # Добавляем атрибуты данных к ячейкам
        soup = BeautifulSoup(html_str, 'html.parser')
        for row_idx, tr in enumerate(soup.find_all('tr')[1:]):  # Пропускаем заголовок
            for col_idx, td in enumerate(tr.find_all('td')):
                td['data-row'] = str(row_idx)
                td['data-col'] = str(col_idx)
        
        return str(soup)


    def to_csv(self) -> BytesIO:
        df = self.to_dataframe()
        buffer = BytesIO()
        df.to_csv(buffer)
        buffer.seek(0)

        return buffer