class Rack:
    def __init__(self,rack_id, rack_name, row_id):
        self.rack_id = rack_id
        self.rack_name = rack_name
        self.row_id = row_id

    def display(self):
        print(f'Rack ID     : {self.rack_id}')
        print(f'Rack Name   : {self.rack_name}')
        print(f'Row ID      : {self.row_id}')