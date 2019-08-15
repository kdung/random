from flask import Flask, request, jsonify
import uuid
import random


class Error(Exception):
    def __init__(self, code, msg):
        self.msg = msg
        self.code = code

    def msg(self):
        return self.msg()


class Account(object):
    def __init__(self, balance):
        self.id = uuid.uuid1()
        self.balance = balance

    def update_balance(self, amount):
        try:
            float(amount)
            # check balance is enough
            self.balance += amount
        except ValueError:
            print("Amount is not number")
            return Error(401, "Amount should be number")


app = Flask(__name__)


@app.route('/')
def welcome():
    return 'Hello World!'


def initialize():
    random_db = {}
    for i in range(1, 5):
        acc = Account(random.randint(1, 1000))
        random_db[acc.id] = acc
    return random_db


@app.route("/insync/account/transfer", methods=["POST"])
def transfer():
    result = {"status": "Submitted"}
    to_acc_id = request.json['to_acc_id']
    from_acc_id = request.json['from_acc_id']
    amount = request.json['amount']
    print("Action Type: Transfer")
    print("To Acc: " + request.json['to_acc_id'])
    print("From Acc: " + request.json['from_acc_id'])
    print("Amount: " + str(amount))

    try:
        to_acc = get_account(to_acc_id)
        from_acc = get_account(from_acc_id)
        to_acc.update_balance(amount)
        from_acc.update_balance(0 - amount)

        print("to acc balance: " + str(to_acc.balance))
        print("from acc balance: " + str(from_acc.balance))
        result["status"] = "Success"
    except Error as e:
        print(e.msg())
        # roll-back handle
        result["status"] = "Success"
        result["error"] = e.msg()

    return jsonify(result)


@app.route("/insync/account/deposit", methods=["POST"])
def deposit():
    result = {"status": "Submitted"}
    to_acc_id = request.json['to_acc_id']
    from_acc_id = request.json['from_acc_id']
    amount = request.json['amount']
    print("Action Type: Deposit")
    print("To Acc: " + request.json['to_acc_id'])
    print("From Acc: " + from_acc_id)
    print("Amount: " + str(amount))

    try:
        to_acc = get_account(to_acc_id)
        print(to_acc.id)
        to_acc.update_balance(amount)

        print("to acc balance: " + str(to_acc.balance))
        result["status"] = "Success"
    except Error as e:
        print(e.msg())
        result["status"] = "Success"
        result["error"] = e.msg()

    return jsonify(result)


@app.route("/insync/account/withdrawal", methods=["POST"])
def withdrawal():
    result = {"status": "Submitted"}
    acc_id = request.json['acc_id']
    amount = request.json['amount']
    print("Action Type: Deposit")
    print("From Acc: " + acc_id)
    print("Amount: " + str(amount))

    try:
        to_acc = get_account(acc_id)
        # check if balance is enough
        to_acc.update_balance(0-amount)

        print("acc balance: " + str(to_acc.balance))
        result["status"] = "Success"
    except Error as e:
        print(e.msg())
        result["status"] = "Success"
        result["error"] = e.msg()

    return jsonify(result)


def get_account(id):
    print(id)
    if id and id in db:
        print(id)
        return db[id]
    else:
        print("Account not found")
        return Error(404, "Account not found")


db = initialize()
for item, obj in db.items():
    print(str(item) + ": " + str(obj.balance))

if __name__ == '__main__':
    print("starting server")

    app.run(port=5003)


"""

https://send.firefox.com/download/ef7827eeabe959a1/#ELPC3xTo0MOeS36jZPqP-Q

deposit

 curl -i -H "Content-Type: application/json" -X POST -d 
 "{\"to_acc_id\":\"1c0dec1c-be92-11e9-90ca-dca9047bb50b\",
  \"from_acc_id\": \"c184448a-be91-11e9-b07a-dca9047bb50b\", 
  \"amount\":10 }" 
  http://localhost:5003/insync/account/deposit
  
  
"""