import time
import json
import random
import threading


class Table:
    def __init__(self, table_id, status, my_order):
        self.table_id = table_id
        self.status = status     # free, waiting to make, waiting for order
        self.my_order = my_order

    def description(self):
        print(f"Table {self.table_id} is {self.status} and it's order is {self.my_order}")
        return f"{self.table_id} is {self.status} and it's order is {self.my_order}"

    def create_order(self, menu_list):
        iteration = random.randint(1, 10)
        for item in range(iteration):
            index = random.randint(1, 3)
            item = random.choice(menu_list[index])
            self.my_order.append(item)
        # print(self.my_order)
        self.status = "waiting for order"
        print("Debug my_order (Table class)", self.my_order)


class Waiter:

    def __init__(self, waiter_id, thread_id):
        self.waiter_id = waiter_id
        self.thread_id = thread_id
        # self.thread_id = threading.Thread(target=self.send_order, args=(self, ))

    def send_order(self, table, menu_list):
        global order_id
        order_id += 1

        items = []
        max_wait = 0
        for item in table.my_order:
            items.append(menu_list[item]["id"])
            max_wait_comp = menu_list[item]["preparation-time"]
            if max_wait_comp > max_wait:
                max_wait = max_wait_comp

        payload = {
            "order_id": order_id,
            "table_id": table.table_id,
            "waiter_id": self.waiter_id,
            "items": items,
            "priority": random.randint(1, 5),
            "max_wait": max_wait * 1.3,
            "pick_up_time": int(time.time())  # UNIX timestamp
        }
        print(table.my_order)
        print(payload)
        print("DEBUG")
        return payload


def food_pool():
    f = open('food.json')
    food = json.load(f)
    menu_list = {1: [], 2: [], 3: []}
    for line in food:
        complexity = food[line]["complexity"]
        menu_list[complexity].append(food[line]["name"])

    f.close()
    print(menu_list)
    return menu_list


def initial_food_list():
    f = open('food.json')
    food = json.load(f)
    f.close()
    return food


order_id = 0
order = []
menu = food_pool()
food_list = initial_food_list()
# make_order(menu, order)

order1 = []
T1 = Table(1, "free", order1)

order2 = []
T2 = Table(2, "free", order2)

W1 = Waiter(1, "t1")
# W2 = Waiter(2, "t2")

# W1.thread_id = threading.Thread(target=W1.send_order, args=(T1, food_list))
# W2.thread_id = threading.Thread(target=W2.send_order, args=(T2, food_list))

T1.create_order(menu)
# T2.create_order(menu)
# T1.description()

# W1.thread_id.start()
# W2.thread_id.start()

# W1.thread_id.join()
# W2.thread_id.join()


W1.send_order(T1, food_list)
# W2.send_order(T1, food_list)

# sending to the kitchen
