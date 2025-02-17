from enum import Enum
from sqlalchemy import Engine, select
from sqlalchemy.orm import Session
from .connection import get_engine
from ..orm import Processing_Status


class Status_Manager:

    class Status(Enum):
        Created = 0
        Running = 1
        Successful = 2
        Failed = 3

    processing_id: int
    state: Status

    engine: None | Engine

    def __init__(self, in_id: int):
        self.processing_id = in_id
        self.engine = get_engine()
        self.get_status() # Sets 'state' field

    def get_status(self) -> Status:
        with Session(self.engine) as session:
            processing = session.get(Processing_Status, self.processing_id)
            self.state = processing.status

            return processing.status

    def update_status(self, new_state: Status) -> None:
        with Session(self.engine) as session:
            processing = session.get(Processing_Status, self.processing_id)
            processing.status = new_state
            session.commit()
