from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .config_base import Config_Base
from .dataset_model import Dataset


class Processing_Status(Config_Base):
    __tablename__ = "processing"

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str] = mapped_column()
    model_name: Mapped[str] = mapped_column()
    extra_parameters: Mapped[str] = mapped_column()
    dataset_id: Mapped["Dataset"] = mapped_column(ForeignKey("dataset.id"))
    task: Mapped[int] = mapped_column()
