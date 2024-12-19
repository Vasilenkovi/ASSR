from pandas import read_csv, DataFrame
import numpy as np
from io import BytesIO


class CSVTableAsHTML():
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
        # styled = self.df.style.set_td_classes(
        #     DataFrame(
        #         np.full(df.shape, "frame-b"),
        #         index=df.index,
        #         columns=df.columns
        #     )
        # )
        # styled = styled.to_html(
        #     table_attributes='class="w-100 main-text frame-b"',
        #     bold_headers=False,
        #     exclude_stylesbool=True
        # )
        # self.head_html = styled[  # get colomns
        #     styled.find('<thead>'):
        #     styled.find('</thead>')+8
        # ]
        # self.body_list_tr = styled[
        #     styled.find('<tbody>')+7:
        #     styled.find('</tbody>')-2
        # ].split('</tr>')
        # self.body_list_tr.pop()

    def getHeader(self) -> list[str]:
        html_header = "<thead>\n<tr>\n<th></th>\n"
        for header in self.df.columns.to_list():
            html_header += f"<th>{header}</th>"
        html_header += "</tr>\n</thead>"
        return html_header

    def getNRows(self, begin_from: int, step: int) -> str:
        # if begin_from + step > len(self.body_list_tr):
        #     return '</tr>'.join(self.body_list_tr[begin_from::])
        # return '</tr>'.join(self.body_list_tr[begin_from:begin_from+step])
        look = self.df[begin_from:begin_from+step].to_json()
        return look
