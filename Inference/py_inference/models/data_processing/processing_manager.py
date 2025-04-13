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

    class Task(Enum):
        Other = 0
        Text_class = 1
        Token_class = 2

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
            processing.status = new_state.value
            session.commit()

    def set_task(self, current_task: str) -> None:
        with Session(self.engine) as session:
            processing = session.get(Processing_Status, self.processing_id)

            if current_task.lower() in (
                "text-classification", "text classification"
            ):
                processing.task = self.Task.Text_class.value
            elif current_task.lower() in (
                "token-classification", "token classification"
            ):
                processing.task = self.Task.Token_class.value
            else:
                processing.task = self.Task.Other.value

            session.commit()
