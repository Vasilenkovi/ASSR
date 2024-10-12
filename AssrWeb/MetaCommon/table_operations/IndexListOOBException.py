class IndexListOOBException(Exception):
    """Exception rasied when index int columns of 
     a table is out of bounds"""

    def __init__(self, *args, id_list=[]):
        self.id_list = id_list
        super().__init__(*args)
