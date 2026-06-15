from flask import Flask


app = Flask(__name__)


@app.get("/")
def hello() -> str:
    return "Hello Work"


if __name__ == "__main__":
    app.run(debug=True, port=5000)