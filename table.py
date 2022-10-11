import random

class Table:
    def __init__(self, table_id, status, my_order):
        self.table_id = table_id
        self.status = status     # free, waiting to make, waiting for order
        self.my_order = my_order

    def description(self):
        # print(f"Table {self.table_id} is {self.status} and it's order is {self.my_order}")
        return f"{self.table_id} is {self.status} and it's order is {self.my_order}"

    def create_data(self, menu_list):
        iteration = random.randint(1, 10)
        for item in range(iteration):
            index = random.randint(1, 3)
            item = random.choice(menu_list[index])
            self.my_order.append(item)
        # print(self.my_order)
        self.status = "waiting for order"
        # print("Debug my_order (Table class)", self.my_order)
        return self.my_order
