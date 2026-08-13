class Transaction:
    def __init__(self,trasaction_id,user_id,book_id,issue_date,due_date,return_date= None,status = 'Issued'):
        self.trasaction_id = trasaction_id
        self.user_id = user_id
        self.book_id = book_id
        self.issue_date = issue_date
        self.due_date = due_date
        self.return_date = return_date
        self.status = status

    def display(self):
        print(f'Trasaction ID  :  {self.trasaction_id}')
        print(f'User ID        :  {self.user_id}')
        print(f'Book ID        :  {self.book_id}')
        print(f'Issue Date     :  {self.issue_date}')
        print(f'Due Date       :  {self.due_date}')
        print(f'Return Date    :  {self.return_date}')
        print(f"Status         :  {self.status}")


        