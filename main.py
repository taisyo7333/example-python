from flask import Flask


app = Flask(__name__)


@app.get("/")
def hello() -> str:
    return "Hello OpenShift DevSpaces"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)