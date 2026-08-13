class Master:
    def __init__(self,row_id,rack_id,shelf_id):
        self.master_id = str(row_id)+str(rack_id)+str(shelf_id)
        self.row_id = row_id
        self.rack_id = rack_id
        self.shelf_id = shelf_id

    def display(self):
        print(f"Master ID  : {self.master_id}")
        print(f"Row ID  : {self.row_id}")
        print(f"Rack ID  : {self.rack_id}")
        print(f"Shelf ID  : {self.shelf_id}")

