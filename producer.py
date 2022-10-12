import random

class Producer:
    def __init__(self, producer_id, status, my_data):
        self.producer_id = producer_id
        self.status = status     # free, waiting to make, waiting for data
        self.my_data = my_data
        
    def create_data(self, menu_list):
        iteration = random.randint(1, 10)
        for item in range(iteration):
            index = random.randint(1, 3)
            item = random.choice(menu_list[index])
            self.my_data.append(item)
            
        self.status = "waiting for data"
        return self.my_data
