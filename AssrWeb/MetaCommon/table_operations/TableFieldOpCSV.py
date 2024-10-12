from .TableFieldOp import TableFieldOp
from .FileMismatchException import FileMismatchException
from pandas import DataFrame, read_csv, concat


class TableFieldOpCSV(TableFieldOp):

    def _coerce_to_table(self, file_list: list["DataFile"]) -> DataFrame:
        if len(file_list) == 0:
            return DataFrame()

        try:
            df_list = [read_csv(f.file) for f in file_list]
        except UnicodeDecodeError:
            raise FileMismatchException("Expected CSV file, found other")

        return concat(df_list, ignore_index=True)