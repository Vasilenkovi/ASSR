from TableFieldOp import TableFieldOp
from pandas import DataFrame
from tika import parser


class TableFieldOpPDF(TableFieldOp):

    def _coerce_to_table(file_list: list["DataFile"]) -> DataFrame:
        df = DataFrame()

        for file_object in file_list:
            pdf = parser.from_file(file_object.file)
            df.append(pdf['content'])

        return df