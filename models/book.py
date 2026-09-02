class Book:
    def __init__(self,book_id,title,author,publisher,category,quantity,available,master_id):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.category = category
        self.quantity = quantity
        self.publisher = publisher
        self.master_id = master_id
        self.available = quantity if available is None else available


    def display(self):
        print(f'Book ID     :  {self.book_id}')
        print(f'Title       :  {self.title}')
        print(f'Author      :  {self.author}')
        print(f'Category    :  {self.category}')
        print(f'Quantity    :  {self.quantity}')
        print(f"Publisher   :  {self.publisher}")
        print(f"Master ID    :  {self.master_id}")
        print(f"Available   :  {self.available}")