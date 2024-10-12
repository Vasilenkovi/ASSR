class FileMismatchException(Exception):
    """Exception rasied when files of different 
     types are pushed into the same table"""

    def __init__(self, *args):
        super().__init__(*args)
