from this import d
from flask import Flask, request
import threading
import producer
import sender
import json
import random
import time
import requests

app = Flask(__name__)
producers = [producer.Producer(i, "free", []) for i in range(1, 11)]
senders = [sender.Sender(i) for i in range(1, 5)]

def food_pool():
    f = open('food.json')
    food = json.load(f)
    menu_list = {1: [], 2: [], 3: []}
    for line in food:
        eating_difficulty = food[line]["eating-difficulty"]
        menu_list[eating_difficulty].append(food[line]["name"])
    f.close()
    return menu_list


def new_producers(producers_list):
    number_of_new_producers = random.randint(1, 10)
    counter = 0
    for i in range(number_of_new_producers):
        if counter != 10:
            for producer in producers_list:
                if producer.status == "free":
                    producer.status = "waiting_to_make"
                    counter = 0
                    break
                else:
                    counter += 1
    return producers_list


def take_data(sender, producer_list, _menu, _food_list):
    # find free table 
    # get order 
    # send order 
    for table in producer_list:
        if table.status == "waiting_to_make":
            table.create_data(_menu)
            take_time = random.randint(2, 4)
            time.sleep(take_time)
            table.status = "waiting_for_data"
            return sender.send_data(table, _food_list)


def initial_food_list():
    f = open('food.json')
    food = json.load(f)
    f.close()
    return food

def sendData():
    while True:
        menu = food_pool()
        food_list = initial_food_list()
        
        new_producers(producers)
        current_sender = random.choice(senders) 

        payload = take_data(current_sender, producers, menu, food_list)
        if payload == None:
            continue
        else:
            print(payload, "PAYLOAD")
            post = requests.post("http://192.168.1.128:6000/order", json = payload)
            print("data has been sended to ComponentK")
            time.sleep(10)
        
        time.sleep(10)

@app.route('/distribution', methods=['POST'])
def send():    
    data = request.get_json()
    print(data, "DATA POST")
    
    producer_id = data["producer_id"]
    producer_id = int(producer_id)
    producers[producer_id-1].status = "free"
    print("data has been received from ComponentK")
    return "data has been received from ComponentK"

    
if __name__ == '__main__':
    # app.run(debug=False, host="0.0.0.0", port=5000, use_reloader=False)
    flask_thread = threading.Thread(target=lambda: app.run(debug=False, host="0.0.0.0", port=5000, use_reloader=False))

    threads = list()
    threads.append(flask_thread)
    for index in range(6):
        print("Main    : create and start thread.", index)
        x = threading.Thread(target=sendData, args=())
        threads.append(x)

    for index, thread in enumerate(threads):
        print("Main    : before joining thread.", index)
        thread.start()
        print("Main    : thread done", index)