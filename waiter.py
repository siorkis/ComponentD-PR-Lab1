import time
import random
import json
import threading

class Waiter:
    
    order_id = 0
    
    def __init__(self, waiter_id):
        self.waiter_id = waiter_id
        # self.thread_id = thread_id
        # self.thread_id = threading.Thread(target=self.send_order, args=(self, ))
    
    def send_data(self, table, menu_list):
        sleep = random.randint(2, 5)
        time.sleep(sleep)
        print(threading.current_thread().name)
        Waiter.order_id += 1
        items = []
        max_wait = 0
        for item in table.my_order:
            items.append(menu_list[item]["id"])
            max_wait_comp = menu_list[item]["preparation-time"]
            if max_wait_comp > max_wait:
                max_wait = max_wait_comp

        payload = {
            "order_id": Waiter.order_id,
            "table_id": table.table_id,
            "waiter_id": self.waiter_id,
            "items": items,
            "priority": random.randint(1, 5),
            "max_wait": max_wait * 1.3,
            "pick_up_time": int(time.time())  # UNIX timestamp
        }
       
        # print(table.my_order)
        # print(payload)
        # print("DEBUG")
        print(payload, "PAYLOAD SEND DATA")
        # message = json.dumps(payload)
        return payload
    
    