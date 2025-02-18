from sqlalchemy.orm import Mapped, mapped_column, relationship
from .config_base import Config_Base
from .dataset_model import Dataset


class Processing_Status(Config_Base):
    __tablename__ = "processing"

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str] = mapped_column()
    model_name: Mapped[str] = mapped_column()
    parameters: Mapped[str] = mapped_column()
    dataset: Mapped["Dataset"] = relationship("Dataset")
