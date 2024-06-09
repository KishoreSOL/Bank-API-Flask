from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)

# Connect to MongoDB
client = MongoClient("mongodb://db:27017")
db = client.MoneyManagementDB
users = db["Users"]

def UserExist(username):
    # Use count_documents for checking existence
    if users.count_documents({"Username": username}) == 0:
        return False
    else:
        return True

class Register(Resource):
    def post(self):
        # Step 1: Get posted data by the user
        postedData = request.get_json()

        # Extract username and password
        username = postedData["username"]
        password = postedData["password"]

        # Check if the user already exists
        if UserExist(username):
            retJson = {
                'status': 301,
                'msg': 'Invalid Username'
            }
            return jsonify(retJson)

        # Hash the password
        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        # Store the user information in the database
        users.insert_one({
            "Username": username,
            "Password": hashed_pw,
            "Own": 0,
            "Debt": 0
        })

        retJson = {
            "status": 200,
            "msg": "You successfully signed up for the API"
        }
        return jsonify(retJson)

def verifyPw(username, password):
    if not UserExist(username):
        return False

    # Find user and check password
    user = users.find_one({"Username": username})
    if bcrypt.checkpw(password.encode('utf8'), user["Password"]):
        return True
    else:
        return False

def cashWithUser(username):
    # Retrieve user's cash balance
    return users.find_one({"Username": username})["Own"]

def debtWithUser(username):
    # Retrieve user's debt balance
    return users.find_one({"Username": username})["Debt"]

def generateReturnDictionary(status, msg):
    return {
        "status": status,
        "msg": msg
    }

def verifyCredentials(username, password):
    if not UserExist(username):
        return generateReturnDictionary(301, "Invalid Username"), True

    if not verifyPw(username, password):
        return generateReturnDictionary(302, "Incorrect Password"), True

    return None, False

def updateAccount(username, balance):
    users.update_one(
        {"Username": username},
        {"$set": {"Own": balance}}
    )

def updateDebt(username, balance):
    users.update_one(
        {"Username": username},
        {"$set": {"Debt": balance}}
    )

class Add(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]
        money = postedData["amount"]

        retJson, error = verifyCredentials(username, password)
        if error:
            return jsonify(retJson)

        if money <= 0:
            return jsonify(generateReturnDictionary(304, "The money amount entered must be greater than 0"))

        cash = cashWithUser(username)
        money -= 1  # Transaction fee
        bank_cash = cashWithUser("BANK")
        updateAccount("BANK", bank_cash + 1)

        updateAccount(username, cash + money)

        return jsonify(generateReturnDictionary(200, "Amount Added Successfully to account"))

class Transfer(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]
        to = postedData["to"]
        money = postedData["amount"]

        retJson, error = verifyCredentials(username, password)
        if error:
            return jsonify(retJson)

        cash = cashWithUser(username)
        if cash <= 0:
            return jsonify(generateReturnDictionary(303, "You are out of money, please Add Cash or take a loan"))

        if money <= 0:
            return jsonify(generateReturnDictionary(304, "The money amount entered must be greater than 0"))

        if not UserExist(to):
            return jsonify(generateReturnDictionary(301, "Recipient username is invalid"))

        cash_from = cashWithUser(username)
        cash_to = cashWithUser(to)
        bank_cash = cashWithUser("BANK")

        updateAccount("BANK", bank_cash + 1)
        updateAccount(to, cash_to + money - 1)
        updateAccount(username, cash_from - money)

        return jsonify(generateReturnDictionary(200, "Amount transferred successfully"))

class Balance(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]

        retJson, error = verifyCredentials(username, password)
        if error:
            return jsonify(retJson)

        user_data = users.find_one(
            {"Username": username},
            {"Password": 0, "_id": 0}  # Exclude password and ID from the response
        )

        return jsonify(user_data)

class TakeLoan(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]
        money = postedData["amount"]

        retJson, error = verifyCredentials(username, password)
        if error:
            return jsonify(retJson)

        cash = cashWithUser(username)
        debt = debtWithUser(username)
        updateAccount(username, cash + money)
        updateDebt(username, debt + money)

        return jsonify(generateReturnDictionary(200, "Loan added to your account"))

class PayLoan(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]
        money = postedData["amount"]

        retJson, error = verifyCredentials(username, password)
        if error:
            return jsonify(retJson)

        cash = cashWithUser(username)

        if cash < money:
            return jsonify(generateReturnDictionary(303, "Not enough cash in your account"))

        debt = debtWithUser(username)
        updateAccount(username, cash - money)
        updateDebt(username, debt - money)

        return jsonify(generateReturnDictionary(200, "Loan paid"))

# Add resource routes
api.add_resource(Register, '/register')
api.add_resource(Add, '/add')
api.add_resource(Transfer, '/transfer')
api.add_resource(Balance, '/balance')
api.add_resource(TakeLoan, '/takeloan')
api.add_resource(PayLoan, '/payloan')

if __name__=="__main__":
    app.run(host='0.0.0.0')
