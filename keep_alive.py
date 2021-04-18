# this file is needed to keep the bot running even when the replit tab is not open
from flask import Flask # using flask as the web server
from threading import Thread

app = Flask("")

@app.route("/")
def home():
    return "Hello. I am alive!"

def run():
    app.run(host = "0.0.0.0", port = 8080)

def keep_alive():
    t = Thread(target = run)
    t.start()