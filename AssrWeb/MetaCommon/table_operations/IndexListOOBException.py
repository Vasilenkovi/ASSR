class IndexListOOBException(Exception):
    
    def __init__(self, msg = "", id_list = [], *args):
        self.msg = msg
        self.id_list = id_list
        super().__init__(*args)