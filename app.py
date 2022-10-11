from this import d
from flask import Flask, request
import threading
import table
import waiter
import json
import random
import time
import requests

app = Flask(__name__)
tables = [table.Table(i, "free", []) for i in range(1, 11)]
waiters = [waiter.Waiter(i) for i in range(1, 5)]

def food_pool():
    f = open('food.json')
    food = json.load(f)
    menu_list = {1: [], 2: [], 3: []}
    for line in food:
        complexity = food[line]["complexity"]
        menu_list[complexity].append(food[line]["name"])

    f.close()
    return menu_list


def new_tables(tables_list):
    number_of_guests = random.randint(1, 10)
    # print(number_of_guests, "nr guests FLAG")
    counter = 0
    for i in range(number_of_guests):
        if counter != 10:
            for table in tables_list:
                # print(table.status, table.table_id, " - table status NEW_TABLES (free)")
                if table.status == "free":
                    table.status = "waiting_to_make"
                    # print(table.status,  table.table_id, " - table status NEW_TABLES (waiting to make)")
                    counter = 0
                    break
                else:
                    counter += 1

        
    return tables_list


def take_data(waiter, table_list, _menu, _food_list):
    # find free table 
    # get order 
    # send order 
    for table in table_list:
        # print(table.status, table.table_id, " - DEBUG status TAKE_ORDER")
        if table.status == "waiting_to_make":
            table.create_data(_menu)
            take_time = random.randint(2, 4)
            time.sleep(take_time)
            table.status = "waiting_for_data"
            # print(table.status, table.table_id, " - DEBUG status TAKE_ORDER (waiting for order)")
            # print(waiter.send_data(table, _food_list), "DEBUG take_order")
            return waiter.send_data(table, _food_list)


def initial_food_list():
    f = open('food.json')
    food = json.load(f)
    f.close()
    return food

def sendData():
    while True:
        menu = food_pool()
        food_list = initial_food_list()
        new_tables(tables)
        current_waiter = random.choice(waiters) 

        payload = take_data(current_waiter, tables, menu, food_list)
        if payload == None:
            continue
        else:
            print(payload, "PAYLOAD")
            post = requests.post("http://26.249.68.98:6000/order", json = payload)
            # print(post, 'POST') 
            print("data has been sended to ComponentK")
            time.sleep(10)
        
        time.sleep(10)
    return "data has been sended to ComponentK"

@app.route('/distribution', methods=['POST'])
def send():    
    data = request.get_json()
    print(data, "DATA POST")
    
    table_id = data["table_id"]
    table_id = int(table_id)
    tables[table_id-1].status = "free"
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