from sqlalchemy.orm import Mapped, mapped_column
from .config_base import Config_Base


class Processing_Status(Config_Base):
    __tablename__ = "processing"

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str] = mapped_column()
