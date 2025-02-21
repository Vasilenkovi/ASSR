from sqlalchemy.orm import Mapped, mapped_column
from .config_base import Config_Base


class File(Config_Base):
    __tablename__ = "file"

    id: Mapped[int] = mapped_column(primary_key=True)
    binary_file: Mapped[bytes] = mapped_column()
