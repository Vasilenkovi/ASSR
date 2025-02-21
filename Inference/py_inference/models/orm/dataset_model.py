from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .config_base import Config_Base
from .file_model import File


class Dataset(Config_Base):
    __tablename__ = "dataset"

    id: Mapped[int] = mapped_column(primary_key=True)
    file_list: Mapped[List["File"]] = relationship("File", secondary="dataset_files")


class Dataset_Files(Config_Base):
    __tablename__ = "dataset_files"

    id: Mapped[int] = mapped_column(primary_key=True)
    dataset_id: Mapped[int] = mapped_column(ForeignKey("dataset.id"))
    file_id: Mapped[int] = mapped_column(ForeignKey("file.id"))
