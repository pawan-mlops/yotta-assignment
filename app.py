from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from Yotta user app"

@app.route("/health")
def health():
    return "OK"

@app.route("/cpu")
def cpu():
    x = 0
    for i in range(15_000_000):
        x += i
    return "CPU load generated"

app.run(host="0.0.0.0", port=8080)
