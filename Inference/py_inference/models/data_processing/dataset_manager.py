from typing import Generator
from sqlalchemy.orm import Session
from ..orm import File, Dataset
from .connection import Engine_Connected


class Dataset_Manager(Engine_Connected):

    file_list: list[File]

    def __init__(self, dataset_id: int):
        super().__init__()

        with Session(self.engine) as session:
            dataset = session.get(Dataset, dataset_id)
            self.file_list = dataset.file_list

    def get_file(self) -> Generator[File]:
        for f in self.file_list:
            yield f
        