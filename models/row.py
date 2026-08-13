class Row:
    def __init__(self,row_id,row_name):
        self.row_id = row_id
        self.row_name = row_name

    def display(self):
        print(f'Row ID : {self.row_id}')
        print(f'Row Name : {self.row_name}')
