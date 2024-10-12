class IndexListOOBException(Exception):

    def __init__(self, *args, id_list=[]):
        self.id_list = id_list
        super().__init__(*args)
