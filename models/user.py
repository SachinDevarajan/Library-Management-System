class User:
    def __init__(self,user_id,name,phone,email,role,doj):
        self.user_id = user_id
        self.name = name
        self.phone = phone
        self.email = email
        self.role = role
        self.doj = doj
        self.borrowed_books = []

    def display(self):
        print(f"User ID         : {self.user_id}")
        print(f'User Name       : {self.name}')
        print(f"Phone Number    : {self.phone}")
        print(f"Email           : {self.email}")
        print(f"Role            : {self.role}")
        print(f"Date Of Joining : {self.doj}")
        print(f"Borrowed Books  : {self.borrowed_books}")
    