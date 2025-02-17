from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .config_base import Config_Base
from .file_model import File


class Dataset(Config_Base):
    __tablename__ = "dataset"

    id: Mapped[int] = mapped_column(primary_key=True)
    binary_file: Mapped[List["File"]] = relationship("File", secondary="Dataset_Files")


class Dataset_Files(Config_Base):
    __tablename__ = "dataset_files"

    id: Mapped[int] = mapped_column(primary_key=True)
    dataset_id: Mapped[int] = relationship("Dataset", back_populates="id")
    file_id: Mapped[int] = relationship("File", back_populates="id")
