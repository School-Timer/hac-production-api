from tokenize import triple_quoted
from flask import Flask, request
from flask_cors import CORS
from index import (getCurrentClasses)
from fakeData import *

import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

import random
import string

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET"])
def home():
    return "Hello World"

@app.route("/students/schedule", methods=["GET"])
def sendSchedule():
    username = request.args.get("username")
    password = request.args.get("password")

    encryptedUsername = request.args.get("username")
    encryptedPassword = request.args.get("password")

    key = 'AAAAAAAAAAAAAAAA'  # Must Be 16 char for AES128

    def decrypt(enc):
        enc = base64.b64decode(enc)
        cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
        return unpad(cipher.decrypt(enc), 16)
    # encryptedUsername = username
    username = decrypt(encryptedUsername)
    # encryptedPassword = password
    password = decrypt(encryptedPassword)

    username = username.decode("utf-8", "ignore")
    password = password.decode("utf-8", "ignore")

    if (username.lower() == "john" and password.lower() == "doe"):
        return schedule

    return {"schedule": getStudentSchedule(username, password)}


@app.route("/students/currentclasses", methods=["GET"])
def sendCurrentClasses():

    username = request.args.get("username")
    password = request.args.get("password")

    encryptedUsername = request.args.get("username")
    encryptedPassword = request.args.get("password")

    key = 'AAAAAAAAAAAAAAAA'  # Must Be 16 char for AES128

    def decrypt(enc):
        enc = base64.b64decode(enc)
        cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
        return unpad(cipher.decrypt(enc), 16)
    # encryptedUsername = username
    username = decrypt(encryptedUsername)
    # encryptedPassword = password
    password = decrypt(encryptedPassword)

    username = username.decode("utf-8", "ignore")
    password = password.decode("utf-8", "ignore")

    if (username.lower() == "john" and password.lower() == "doe"):
        return currentClasses

    courses = []

    classes = getCurrentClasses(username, password)

    for course in classes:
        courses.append(
            {
                "name": course.name,
                "grade": course.grade,
                "Last Updated": course.updateDate,
                "assignments": course.assignments
            }
        )

    return {"currentClasses": courses}


if __name__ == "__main__":
    app.run()