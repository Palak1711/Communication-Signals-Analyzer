from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():
    return "Communication Signal Analyzer — Web Version Coming Soon"


if __name__ == '__main__':
    app.run(debug=True)