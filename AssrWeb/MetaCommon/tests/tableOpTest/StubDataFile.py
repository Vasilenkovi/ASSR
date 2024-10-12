class StubDataFile:

    def __init__(self, filename: str) -> None:
        self.file = open(filename, "rb")
