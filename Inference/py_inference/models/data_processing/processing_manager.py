from enum import Enum
from sqlalchemy.orm import Session
from .connection import Engine_Connected
from ..orm import Processing_Status


class Processing_Manager(Engine_Connected):

    class Status(Enum):
        Created = 0
        Running = 1
        Successful = 2
        Failed = 3

    processing_id: int
    processing_record: Processing_Status

    def __init__(self, in_id: int):
        super().__init__()

        self.processing_id = in_id
        self.get_processing_record() # Sets 'processing_record' field

    def get_processing_record(self) -> Processing_Status:
        with Session(self.engine) as session:
            processing = session.get(Processing_Status, self.processing_id)
            self.processing_record = processing

            return processing

    def update_status(self, new_state: Status) -> None:
        with Session(self.engine) as session:
            processing = session.get(Processing_Status, self.processing_id)
            processing.status = new_state
            session.commit()
