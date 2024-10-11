from TableFieldOp import TableFieldOp
from pandas import DataFrame, read_csv


class TableFieldOpCSV(TableFieldOp):

    def _coerce_to_table(file_list: list["DataFile"]) -> DataFrame:
        df = DataFrame()

        for file_object in file_list:
            file_df = read_csv(file_object.file)
            df.append(file_df)

        return df