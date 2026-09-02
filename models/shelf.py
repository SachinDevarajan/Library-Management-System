class Shelf:
    def __init__(self, shelf_id, rack_id, capacity):
        self.shelf_id = shelf_id
        self.rack_id = rack_id
        self.capacity = capacity

    def display(self):
        print(f"Shelf ID   : {self.shelf_id}")
        print(f"Rack ID    : {self.rack_id}")
        print(f"Capacity   : {self.capacity}")
