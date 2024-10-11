from abc import ABC, abstractmethod
from pandas import DataFrame


class TableFieldOp(ABC):
    """This abstract class implements common table field
    manipilation operations. Subclasses must define specific 
    ways to populate table from files"""

    table: DataFrame

    def __init__(self, file_list: list["DataFile"]) -> None:
        super().__init__()
        self.table = TableFieldOp._coerce_to_table(file_list)

    @abstractmethod
    def _coerce_to_table(file_list: list["DataFile"]) -> DataFrame:
        """This method should be implemented in derived class to specify rules
        of file aggregation to tables. For example, table should be built 
        from PDFs in rows, while CSV can be simply imported"""

    def drop_columns(self, column_id_list: list[int]) -> None:
        self.table.drop(
            self.table.columns[column_id_list], axis=1, inplace=True
        )