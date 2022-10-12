import time
import random
import json
import threading

class Sender:
    
    data_id = 0
    
    def __init__(self, sender_id):
        self.sender_id = sender_id
        
    def send_data(self, producer, menu_list):
        sleep = random.randint(2, 5)
        time.sleep(sleep)
        print(threading.current_thread().name)
        Sender.data_id += 1
        items = []
        for item in producer.my_data:
            items.append(menu_list[item]["id"])

        payload = {
            "data_id": Sender.data_id,
            "producer_id": producer.producer_id,
            "sender_id": self.sender_id,
            "items": items,
        }

        return payload
    
    