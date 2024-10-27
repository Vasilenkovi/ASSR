class StubDataFile:

    def __init__(self, filename: str) -> None:
        self.ancestorFile = open(filename, "rb").read()
